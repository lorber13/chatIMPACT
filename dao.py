"""
Local JSON based Data Access Object (DAO).

This module provides a simple in‑memory data access layer over a set of
predefined JSON files.  It was designed to mirror the structure of the
original MongoDB backed DAO used in the Chat IMPACT prototype, but without
requiring a running database.  All data for the entities (Models,
Datasets, Downstream Tasks, Metrics) as well as the relationships between
them are stored under the ``local_data`` directory in JSON format.  Upon
instantiation the DAO loads this data into memory and subsequent queries
operate purely on these Python objects.

The primary entrypoints are:

* ``get_all(collection, attribute)``: return a list of unique values for
  the given attribute across the specified collection.  Arrays are
  flattened and all values deduplicated.

* ``get_attributes(collection)``: return a list of top–level attribute
  names present in the documents of the specified collection.  This is
  useful for populating selection widgets in the UI.

* ``query(specs)``: execute a single collection query or a two–way join
  across collections.  Filters support equality, range comparisons
  (``$gte``/``$lte``), logical AND (``$and``) and containment for array
  fields (``$all``).  Projections allow selecting a subset of fields.

The join behaviour is governed by the ``Edges.json`` file.  Each entry
describes a binary relationship between two entity instances.  When a
query spans two collections the DAO consults this list to find matching
edges and produces a Cartesian join between the filtered rows of the two
collections wherever an edge exists.  Only a single join level is
supported (i.e. queries with exactly two collections).  If no join
relationship is defined between the requested collections an empty list
is returned.

This implementation intentionally omits any persistence logic (e.g.
writing back to the JSON files) since the purpose of this module is to
provide a static snapshot of the conceptual map described in the
reference paper.  Should you need to modify or extend the data, edit
the files under ``local_data`` and reinstantiate the DAO.

"""

from __future__ import annotations

import json
import os
from typing import Any, Dict, Iterable, List, Optional, Tuple


class Dao:
    """A simple data access object reading from local JSON files."""

    def __init__(self, db_name: str = "") -> None:
        # Determine the path to the ``local_data`` folder relative to this
        # module.  We avoid hardcoding absolute paths to keep the code
        # portable.
        base_dir = os.path.dirname(os.path.abspath(__file__))
        data_dir = os.path.join(base_dir, "local_data")

        # Load collections.  Each file contains a list of dictionaries.
        # Documents must have an ``id`` key which is used for joins.
        self.data: Dict[str, List[Dict[str, Any]]] = {}
        for filename, collection_name in [
            ("Models.json", "Models"),
            ("Datasets.json", "Datasets"),
            ("Downstream Tasks.json", "Downstream Tasks"),
            ("Metrics.json", "Metrics"),
        ]:
            file_path = os.path.join(data_dir, filename)
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    self.data[collection_name] = json.load(f)
            except FileNotFoundError:
                # If the file is missing, default to an empty list.
                print(f"Warning: {file_path} not found. Using empty collection.")
                self.data[collection_name] = []

        # Load edges.  ``Edges.json`` holds relationship records.  Each
        # record indicates which two entity instances are connected and by
        # which relation type.  See the documentation at the top of this
        # file for more details.
        edges_path = os.path.join(data_dir, "Edges.json")
        try:
            with open(edges_path, "r", encoding="utf-8") as f:
                self.edges: List[Dict[str, Any]] = json.load(f)
        except FileNotFoundError:
            print(f"Warning: {edges_path} not found. No relationships will be available.")
            self.edges = []

        # Maintain a monotonically increasing counter for synthetic IDs when
        # inserting new records via ``insert_many``.  Each collection has
        # its own counter to avoid collisions.  The counters are only
        # relevant when using the in‑memory insertion methods; they are
        # ignored when reading from the predefined JSON files.
        self._id_counters: Dict[str, int] = {
            name: len(self.data.get(name, [])) for name in self.data
        }

    # ------------------------------------------------------------------
    # Mutation helpers
    # ------------------------------------------------------------------
    def drop(self, collection: str) -> None:
        """Reset the specified collection to an empty list.

        This method clears the in‑memory list for the collection and
        resets the synthetic ID counter.  It does not modify any JSON
        files on disk.
        """
        if collection in self.data:
            self.data[collection] = []
            self._id_counters[collection] = 0

    def insert_many(self, collection: str, docs: Iterable[Dict[str, Any]]):
        """Insert multiple documents into a collection.

        Documents inserted via this method are assigned synthetic IDs if
        they do not already define an ``id`` field.  The IDs are
        sequential integers represented as strings.  The return value is
        an object exposing an ``inserted_ids`` attribute containing the
        list of assigned IDs.  This behaviour loosely mimics the
        ``pymongo`` insert API used in the original prototype.  Only
        in‑memory state is updated; data is not persisted to disk.
        """
        if collection not in self.data:
            self.data[collection] = []
            self._id_counters[collection] = 0
        inserted_ids: List[Any] = []
        for doc in docs:
            # assign id if absent
            if "id" not in doc:
                next_id = self._id_counters[collection]
                self._id_counters[collection] += 1
                doc["id"] = next_id
            inserted_ids.append(doc["id"])
            # Append a shallow copy to avoid side effects
            self.data[collection].append(dict(doc))
        # Also update id counter if some docs came with explicit ids
        max_id = self._id_counters.get(collection, 0)
        for doc in self.data[collection]:
            try:
                # Attempt to coerce to int if possible
                numeric_id = int(doc["id"])
                if numeric_id >= max_id:
                    max_id = numeric_id + 1
            except (ValueError, TypeError, KeyError):
                continue
        self._id_counters[collection] = max_id
        # Return a simple object to mimic pymongo's InsertManyResult
        class _Result:
            def __init__(self, ids):
                self.inserted_ids = ids
        return _Result(inserted_ids)

    # ------------------------------------------------------------------
    # Utility methods
    # ------------------------------------------------------------------
    def get_all(self, collection: str, attribute: str) -> List[Any]:
        """Return a list of unique values for the given attribute.

        If the attribute holds arrays, all elements are flattened and
        deduplicated.  None values are ignored.  The order of results
        follows insertion order (first seen first).  If the collection
        does not exist or no values are found, an empty list is returned.
        """
        results: List[Any] = []
        seen = set()
        docs = self.data.get(collection, [])
        for doc in docs:
            value = doc.get(attribute)
            if value is None:
                continue
            if isinstance(value, list):
                for item in value:
                    if item not in seen:
                        seen.add(item)
                        results.append(item)
            else:
                if value not in seen:
                    seen.add(value)
                    results.append(value)
        return results

    def get_attributes(self, collection: str) -> List[str]:
        """Return the list of attribute names for the given collection.

        The result is the union of keys across all documents.  The
        ordering is alphabetical for determinism.  If the collection is
        empty or not known, an empty list is returned.
        """
        docs = self.data.get(collection, [])
        keys = set()
        for doc in docs:
            keys.update(doc.keys())
        # remove the internal identifier if present since the user should
        # not query on it directly
        keys.discard("id")
        return sorted(keys)

    # ------------------------------------------------------------------
    # Query methods
    # ------------------------------------------------------------------
    def _matches_filters(self, doc: Dict[str, Any], filters: Dict[str, Any], prefix: str) -> bool:
        """Check whether a document matches the provided filter specification.

        ``doc``: the document to test.
        ``filters``: the filter dictionary.  Keys may include the
          collection prefix (e.g. "Models.name").  Supported operators:
            * Equality: {"field": value}
            * Logical AND: {"$and": [filter1, filter2, ...]}
            * Range: {"field": {"$gte": val}} and {"field": {"$lte": val}}
            * Array contains all: {"field": {"$all": [values...]}}
        ``prefix``: the prefix to strip from filter keys (e.g. "Models.").
        """
        if not filters:
            return True
        for key, value in filters.items():
            # Handle logical AND separately
            if key == "$and":
                if not isinstance(value, list):
                    return False
                # All subfilters must match
                for subf in value:
                    if not self._matches_filters(doc, subf, prefix):
                        return False
                continue
            # Handle logical OR separately
            if key == "$or":
                if not isinstance(value, list):
                    return False
                # At least one subfilter must match
                or_matched = False
                for subf in value:
                    if self._matches_filters(doc, subf, prefix):
                        or_matched = True
                        break
                if not or_matched:
                    return False
                continue
            # Determine the attribute name by stripping the prefix if present
            attr = key
            if prefix and key.startswith(prefix + "."):
                attr = key[len(prefix) + 1 :]
            # If the filter value is a dict, treat as operator
            if isinstance(value, dict):
                for op, op_val in value.items():
                    if op == "$gte":
                        # Non comparable types (None) fail the test
                        val = doc.get(attr)
                        if val is None or val < op_val:
                            return False
                    elif op == "$lte":
                        val = doc.get(attr)
                        if val is None or val > op_val:
                            return False
                    elif op == "$all":
                        # Require doc[attr] to be an iterable containing all op_val items
                        val = doc.get(attr)
                        if not isinstance(val, list) or not set(op_val).issubset(set(val)):
                            return False
                    else:
                        # Unknown operator – treat as mismatch
                        return False
            else:
                # Equality check
                if doc.get(attr) != value:
                    return False
        return True

    def _apply_projection(self, doc: Dict[str, Any], project: Optional[List[str]], prefix: str) -> Dict[str, Any]:
        """Apply projection to a document.

        ``doc``: the original document.
        ``project``: list of fields to keep.  Field names may include
          the collection prefix.  If None or empty, the entire document is
          returned (except for the internal ``id``).
        ``prefix``: the prefix to strip from project entries.
        """
        if not project:
            # Return a copy without the id field
            return {k: v for k, v in doc.items() if k != "id"}
        result = {}
        for field in project:
            # strip prefix if present
            attr = field
            if prefix and field.startswith(prefix + "."):
                attr = field[len(prefix) + 1 :]
            if attr in doc:
                result[attr] = doc[attr]
        return result

    def query(self, specs: Optional[List[Dict[str, Any]]]) -> List[Dict[str, Any]]:
        """Execute a query across one or two collections.

        ``specs``: A list containing one or two dictionaries.  Each
        dictionary must include a ``collection`` key and may include
        ``filters`` and ``project`` keys.  If ``specs`` is empty or not
        provided, an empty list is returned.

        For a single collection the DAO filters and projects the rows as
        specified and returns a list of dictionaries of the form
        ``{collection: document}``.

        For two collections the DAO performs a join via the edges.  The
        join is performed on the ``id`` fields of the documents as
        determined by the entries in ``Edges.json``.  Only edges whose
        relation type connects the two requested collections contribute
        to the result.  Filters and projections are applied separately
        to each side of the join.  If no edges connect the two
        collections, an empty list is returned.
        """
        # Validate input
        if not specs or not isinstance(specs, list):
            return []
        # Only one spec – simple selection
        if len(specs) == 1:
            spec = specs[0]
            collection = spec.get("collection")
            
            # Special case for Edges collection
            if collection == "Edges":
                filters = spec.get("filters") or {}
                project = spec.get("project") or []
                result = []
                for doc in self.edges:
                    if self._matches_filters(doc, filters, collection):
                        projected = self._apply_projection(doc, project, collection)
                        result.append({collection: projected})
                return result
            
            if not collection or collection not in self.data:
                return []
            filters = spec.get("filters") or {}
            project = spec.get("project") or []
            result = []
            for doc in self.data[collection]:
                if self._matches_filters(doc, filters, collection):
                    projected = self._apply_projection(doc, project, collection)
                    result.append({collection: projected})
            return result
        # For multi collection queries we currently support exactly two
        if len(specs) != 2:
            return []
        # Extract specs for each side
        spec_a, spec_b = specs
        col_a = spec_a.get("collection")
        col_b = spec_b.get("collection")
        # Validate collections
        if not col_a or not col_b or col_a not in self.data or col_b not in self.data:
            return []
        # Prepare filters and projections
        filters_a = spec_a.get("filters") or {}
        filters_b = spec_b.get("filters") or {}
        proj_a = spec_a.get("project") or []
        proj_b = spec_b.get("project") or []
        # Filter rows for each collection first
        rows_a: List[Tuple[Dict[str, Any], Dict[str, Any]]] = []
        for doc in self.data[col_a]:
            if self._matches_filters(doc, filters_a, col_a):
                rows_a.append((doc, self._apply_projection(doc, proj_a, col_a)))
        rows_b: List[Tuple[Dict[str, Any], Dict[str, Any]]] = []
        for doc in self.data[col_b]:
            if self._matches_filters(doc, filters_b, col_b):
                rows_b.append((doc, self._apply_projection(doc, proj_b, col_b)))
        # If either side has no matches, short circuit
        if not rows_a or not rows_b:
            return []
        # Determine which edge properties to use based on the pair of collections
        # Each edge entry may have keys model_id, dataset_id, task_id, metric_id.
        # We'll map from collection names to the corresponding id key.
        collection_to_key = {
            "Models": "model_id",
            "Datasets": "dataset_id",
            "Downstream Tasks": "task_id",
            "Metrics": "metric_id",
        }
        key_a = collection_to_key.get(col_a)
        key_b = collection_to_key.get(col_b)
        # If we cannot identify the key for either collection, return no result
        if not key_a or not key_b:
            return []
        # Build a mapping from id to projected doc for quick lookup
        # rows_a and rows_b hold tuples (full_doc, projected_doc)
        # We'll keep the full doc to access its id
        id_to_proj_a = {doc["id"]: proj for doc, proj in rows_a if "id" in doc}
        id_to_proj_b = {doc["id"]: proj for doc, proj in rows_b if "id" in doc}
        # Perform the join by scanning edges
        results: List[Dict[str, Dict[str, Any]]] = []
        for edge in self.edges:
            # Skip if relation doesn't connect our collections (an edge must
            # have both keys present)
            if key_a not in edge or key_b not in edge:
                continue
            id_a = edge.get(key_a)
            id_b = edge.get(key_b)
            if id_a is None or id_b is None:
                continue
            # Check if both ids are in the filtered sets
            if id_a in id_to_proj_a and id_b in id_to_proj_b:
                # Append the pair
                results.append({col_a: id_to_proj_a[id_a], col_b: id_to_proj_b[id_b]})
        return results
