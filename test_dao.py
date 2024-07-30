"""unit tests for the dao module"""

import unittest
from dao import Dao

from database import get_database

db = get_database("Test")


class SingleCollection(unittest.TestCase):
    """single collection test case"""

    def setUp(self):
        db["Models"].drop()
        db["Datasets"].drop()
        db["Downstream Tasks"].drop()
        db["Metrics"].drop()

    def test_models(self):
        """query from the 'Models' collection"""
        db["Models"].insert_many(
            [
                {"name": "model1", "version": "LLaMA", "numberOfParameters [B]": 3},
                {"name": "model2", "version": "GPT", "numberOfParameters [B]": 5},
            ]
        )

        dao = Dao(db)
        res = dao.query([{"collection": "Models"}])
        self.assertEqual(len(res), 2)

    def test_datasets(self):
        """query from the 'Datasets' collection"""
        db["Datasets"].insert_many(
            [
                {
                    "name": "dataset1",
                },
                {
                    "name": "dataset2",
                },
            ]
        )

        dao = Dao(db)
        res = dao.query([{"collection": "Datasets"}])
        self.assertEqual(len(res), 2)

    def test_metrics(self):
        """query from the 'Metrics' collection"""
        db["Metrics"].insert_many(
            [
                {
                    "name": "m1",
                },
                {
                    "name": "m2",
                },
            ]
        )

        dao = Dao(db)
        res = dao.query([{"collection": "Metrics"}])
        self.assertEqual(len(res), 2)

    def test_downstream(self):
        """query from the 'Downstream Tasks' collection"""
        db["Downstream Tasks"].insert_many(
            [
                {
                    "name": "ds1",
                },
                {
                    "name": "ds2",
                },
            ]
        )

        dao = Dao(db)
        res = dao.query([{"collection": "Downstream Tasks"}])
        self.assertEqual(len(res), 2)

    def test_no_spec(self):
        """tests wrong function calls"""
        db["Downstream Tasks"].insert_many(
            [
                {
                    "name": "ds1",
                },
                {
                    "name": "ds2",
                },
            ]
        )

        dao = Dao(db)
        res = dao.query([])
        self.assertEqual(len(res), 0)
        res = dao.query(None)
        self.assertEqual(len(res), 0)
        res = dao.query({})
        self.assertEqual(len(res), 0)

    def test_project(self):
        """projection feature"""
        db["Models"].insert_many(
            [
                {"name": "model1", "version": "LLaMA", "numberOfParameters [B]": 3},
                {"name": "model2", "version": "GPT", "numberOfParameters [B]": 5},
            ]
        )

        dao = Dao(db)
        res = dao.query(
            [
                {
                    "collection": "Models",
                    "project": ["name"],
                },
            ]
        )
        self.assertEqual(len(res), 2)
        for item in res:
            self.assertIn("Models", item)
            self.assertIn("name", item["Models"])
            self.assertNotIn("version", item["Models"])
            self.assertNotIn("numberOfParameters [B]", item["Models"])

    def test_filter(self):
        """filtering feature (A.K.A. 'where' clause)"""
        db["Models"].insert_many(
            [
                {"name": "model1", "version": "LLaMA", "numberOfParameters [B]": 3},
                {"name": "model2", "version": "GPT", "numberOfParameters [B]": 5},
            ]
        )

        dao = Dao(db)
        res = dao.query(
            [
                {
                    "collection": "Models",
                    "filters": {"name": "model1"},
                },
            ]
        )
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0]["Models"]["name"], "model1")
        self.assertEqual(res[0]["Models"]["version"], "LLaMA")
        self.assertEqual(res[0]["Models"]["numberOfParameters [B]"], 3)

    def test_filter_project(self):
        """filtering + projection together"""
        db["Models"].insert_many(
            [
                {"name": "model1", "version": "LLaMA", "numberOfParameters [B]": 3},
                {"name": "model2", "version": "GPT", "numberOfParameters [B]": 5},
            ]
        )

        dao = Dao(db)
        res = dao.query(
            [
                {
                    "collection": "Models",
                    "project": ["name"],
                    "filters": {"name": "model1"},
                },
            ]
        )
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0]["Models"]["name"], "model1")
        self.assertNotIn("version", res[0]["Models"])
        self.assertNotIn("numberOfParameters [B]", res[0]["Models"])

    def test_wrong_filter(self):
        """wrong filter (attribute not present)"""
        db["Models"].insert_many(
            [
                {"name": "model1", "version": "LLaMA", "numberOfParameters [B]": 3},
                {"name": "model2", "version": "GPT", "numberOfParameters [B]": 5},
            ]
        )

        dao = Dao(db)
        res = dao.query(
            [
                {
                    "collection": "Models",
                    "filters": {"nam": "model1"},
                },
            ]
        )
        self.assertEqual(len(res), 0)

    def test_wrong_project(self):
        """wrong projection (attribute not present)"""
        db["Models"].insert_many(
            [
                {"name": "model1", "version": "LLaMA", "numberOfParameters [B]": 3},
                {"name": "model2", "version": "GPT", "numberOfParameters [B]": 5},
            ]
        )

        dao = Dao(db)
        res = dao.query(
            [
                {
                    "collection": "Models",
                    "project": ["nam"],
                },
            ]
        )
        self.assertEqual(len(res), 2)
        for item in res:
            self.assertEqual(item, {"Models": {}})


class CrossEntity(unittest.TestCase):
    """single join test case (2 collections involved)"""

    def setUp(self):
        db["Models"].drop()
        db["Datasets"].drop()
        db["Downstream Tasks"].drop()
        db["Metrics"].drop()
        db["Evaluate"].drop()
        db["Suited For"].drop()
        db["Train"].drop()
        db["Enable"].drop()
        db["Assess"].drop()

    def test_join_models_metrics(self):  # Evaluate
        """join between 'Models' and 'Metrics'"""
        models = db["Models"].insert_many(
            [
                {
                    "name": "model1",
                    "version": "LLaMA",
                    "numberOfParameters [B]": 3,
                    "architecture": "LLaMA",
                },
                {
                    "name": "model1",
                    "version": "LLaMA",
                    "numberOfParameters [B]": 5,
                    "architecture": "LLaMA",
                },
                {
                    "name": "model2",
                    "version": "GPT",
                    "numberOfParameters [B]": 5,
                    "architecture": "LLaMA",
                },
            ]
        )
        metrics = db["Metrics"].insert_many(
            [
                {"name": "m1", "description": "desc1"},
                {"name": "m2", "description": "desc2"},
            ]
        )
        db["Evaluate"].insert_many(
            [
                {
                    "Models": models.inserted_ids[0],
                    "Metrics": metrics.inserted_ids[0],
                },
                {
                    "Models": models.inserted_ids[0],
                    "Metrics": metrics.inserted_ids[1],
                },
            ]
        )

        dao = Dao(db)
        res = dao.query(
            [
                {"collection": "Models", "filters": {"name": "model1"}},
                {"collection": "Metrics", "filters": {"description": "desc2"}},
            ]
        )
        self.assertEqual(len(res), 1)
        self.assertDictEqual(
            res[0],
            {
                "Models": {
                    "name": "model1",
                    "version": "LLaMA",
                    "numberOfParameters [B]": 3,
                    "architecture": "LLaMA",
                },
                "Metrics": {"name": "m2", "description": "desc2"},
            },
        )

    def test_join_models_downstream(self):  # Suited For
        """join between 'Models' and 'Downstream Tasks'"""
        models = db["Models"].insert_many(
            [
                {
                    "name": "model1",
                    "version": "LLaMA",
                    "numberOfParameters [B]": 3,
                    "architecture": "LLaMA",
                },
                {
                    "name": "model1",
                    "version": "LLaMA",
                    "numberOfParameters [B]": 5,
                    "architecture": "LLaMA",
                },
                {
                    "name": "model2",
                    "version": "GPT",
                    "numberOfParameters [B]": 5,
                    "architecture": "LLaMA",
                },
            ]
        )
        downstreams = db["Downstream Tasks"].insert_many(
            [
                {"name": "ds1", "description": "desc1", "subTask": "st1"},
                {"name": "ds2", "description": "desc2", "subTask": "st2"},
                {"name": "ds3", "description": "desc3", "subTask": "st3"},
            ]
        )
        db["Suited For"].insert_many(
            [
                {
                    "Models": models.inserted_ids[0],
                    "Downstream Tasks": downstreams.inserted_ids[0],
                },
                {
                    "Models": models.inserted_ids[0],
                    "Downstream Tasks": downstreams.inserted_ids[1],
                },
                {
                    "Models": models.inserted_ids[1],
                    "Downstream Tasks": downstreams.inserted_ids[2],
                },
                {
                    "Models": models.inserted_ids[2],
                    "Downstream Tasks": downstreams.inserted_ids[0],
                },
            ]
        )

        dao = Dao(db)
        res = dao.query(
            [
                {
                    "collection": "Models",
                    "filters": {"name": "model1", "version": "LLaMA"},
                },
                {"collection": "Downstream Tasks", "filters": {"description": "desc2"}},
            ]
        )
        self.assertEqual(len(res), 1)
        self.assertDictEqual(
            res[0],
            {
                "Models": {
                    "name": "model1",
                    "version": "LLaMA",
                    "numberOfParameters [B]": 3,
                    "architecture": "LLaMA",
                },
                "Downstream Tasks": {
                    "name": "ds2",
                    "description": "desc2",
                    "subTask": "st2",
                },
            },
        )

    def test_join_models_datasets(self):  # Train
        """join between 'Models' and 'Datasets'"""
        models = db["Models"].insert_many(
            [
                {
                    "name": "model1",
                    "version": "LLaMA",
                    "numberOfParameters [B]": 3,
                    "architecture": "LLaMA",
                },
                {
                    "name": "model1",
                    "version": "LLaMA",
                    "numberOfParameters [B]": 5,
                    "architecture": "LLaMA",
                },
                {
                    "name": "model2",
                    "version": "GPT",
                    "numberOfParameters [B]": 5,
                    "architecture": "LLaMA",
                },
            ]
        )
        datasets = db["Datasets"].insert_many(
            [
                {
                    "name": "d1",
                    "description": "desc1",
                    "languages": ["English", "Italian"],
                },
                {"name": "d2", "description": "desc2", "languages": ["Python"]},
                {"name": "d3", "description": "desc3", "languages": ["Rust"]},
            ]
        )
        db["Train"].insert_many(
            [
                {
                    "Models": models.inserted_ids[0],
                    "Datasets": datasets.inserted_ids[2],
                },
                {
                    "Models": models.inserted_ids[1],
                    "Datasets": datasets.inserted_ids[1],
                },
                {
                    "Models": models.inserted_ids[1],
                    "Datasets": datasets.inserted_ids[2],
                },
                {
                    "Models": models.inserted_ids[2],
                    "Datasets": datasets.inserted_ids[1],
                },
                {
                    "Models": models.inserted_ids[2],
                    "Datasets": datasets.inserted_ids[2],
                },
            ]
        )

        dao = Dao(db)
        res = dao.query(
            [
                {
                    "collection": "Models",
                    "filters": {"name": "model2", "numberOfParameters [B]": 5},
                },
                {"collection": "Datasets", "filters": {"description": "desc2"}},
            ]
        )
        self.assertEqual(len(res), 1)
        self.assertDictEqual(
            res[0],
            {
                "Models": {
                    "name": "model2",
                    "version": "GPT",
                    "numberOfParameters [B]": 5,
                    "architecture": "LLaMA",
                },
                "Datasets": {
                    "name": "d2",
                    "description": "desc2",
                    "languages": ["Python"],
                },
            },
        )

    def test_join_datasets_downstreams(self):  # Enable
        """join between 'Datasets' and 'Downstream Tasks'"""
        datasets = db["Datasets"].insert_many(
            [
                {
                    "name": "d1",
                    "description": "desc1",
                    "languages": ["English", "Italian"],
                },
                {"name": "d2", "description": "desc2", "languages": ["Python"]},
                {"name": "d3", "description": "desc3", "languages": ["Rust"]},
            ]
        )
        downstreams = db["Downstream Tasks"].insert_many(
            [
                {"name": "ds1", "description": "desc1", "subTask": "st1"},
                {"name": "ds2", "description": "equal description", "subTask": "st2"},
                {"name": "ds3", "description": "equal description", "subTask": "st3"},
            ]
        )
        db["Enable"].insert_many(
            [
                {
                    "Downstream Tasks": downstreams.inserted_ids[0],
                    "Datasets": datasets.inserted_ids[2],
                },
                {
                    "Downstream Tasks": downstreams.inserted_ids[1],
                    "Datasets": datasets.inserted_ids[1],
                },
                {
                    "Downstream Tasks": downstreams.inserted_ids[1],
                    "Datasets": datasets.inserted_ids[2],
                },
                {
                    "Downstream Tasks": downstreams.inserted_ids[2],
                    "Datasets": datasets.inserted_ids[1],
                },
                {
                    "Downstream Tasks": downstreams.inserted_ids[2],
                    "Datasets": datasets.inserted_ids[2],
                },
            ]
        )

        dao = Dao(db)
        res = dao.query(
            [
                {"collection": "Datasets", "filters": {"description": "desc2"}},  # id 1
                {
                    "collection": "Downstream Tasks",
                    "filters": {"description": "equal description"},  # id 1 and 2
                },
            ]
        )
        self.assertEqual(len(res), 2)
        self.assertDictEqual(
            res[0],
            {
                "Datasets": {
                    "name": "d2",
                    "description": "desc2",
                    "languages": ["Python"],
                },
                "Downstream Tasks": {
                    "name": "ds2",
                    "description": "equal description",
                    "subTask": "st2",
                },
            },
        )
        self.assertDictEqual(
            res[1],
            {
                "Datasets": {
                    "name": "d2",
                    "description": "desc2",
                    "languages": ["Python"],
                },
                "Downstream Tasks": {
                    "name": "ds3",
                    "description": "equal description",
                    "subTask": "st3",
                },
            },
        )

    def test_join_metric_downstream(self):  # Assess
        """join between 'Metrics' and 'Downstream Tasks'"""
        metrics = db["Metrics"].insert_many(
            [
                {"name": "m1", "description": "desc1"},
                {"name": "m2", "description": "desc2"},
            ]
        )
        downstreams = db["Downstream Tasks"].insert_many(
            [
                {"name": "ds1", "description": "desc1", "subTask": "st1"},
                {"name": "ds2", "description": "equal description", "subTask": "st2"},
                {"name": "ds3", "description": "equal description", "subTask": "st3"},
            ]
        )
        db["Assess"].insert_many(
            [
                {
                    "Downstream Tasks": downstreams.inserted_ids[0],
                    "Metrics": metrics.inserted_ids[0],
                },
                {
                    "Downstream Tasks": downstreams.inserted_ids[0],
                    "Metrics": metrics.inserted_ids[1],
                },
                {
                    "Downstream Tasks": downstreams.inserted_ids[1],
                    "Metrics": metrics.inserted_ids[0],
                },
                {
                    "Downstream Tasks": downstreams.inserted_ids[1],
                    "Metrics": metrics.inserted_ids[1],
                },
            ]
        )

        dao = Dao(db)
        res = dao.query(
            [
                {"collection": "Metrics", "filters": {"name": "m1"}},  # id 0
                {
                    "collection": "Downstream Tasks",
                    "filters": {"description": "equal description"},  # id 1 and 2
                },
            ]
        )
        self.assertEqual(len(res), 1)
        self.assertDictEqual(
            res[0],
            {
                "Metrics": {
                    "name": "m1",
                    "description": "desc1",
                },
                "Downstream Tasks": {
                    "name": "ds2",
                    "description": "equal description",
                    "subTask": "st2",
                },
            },
        )

    def test_join_with_projection(self):
        """join with projection of some fields + filters"""
        models = db["Models"].insert_many(
            [
                {
                    "name": "model1",
                    "version": "LLaMA",
                    "numberOfParameters [B]": 3,
                    "architecture": "LLaMA",
                },
                {
                    "name": "model1",
                    "version": "LLaMA",
                    "numberOfParameters [B]": 5,
                    "architecture": "LLaMA",
                },
                {
                    "name": "model2",
                    "version": "GPT",
                    "numberOfParameters [B]": 5,
                    "architecture": "LLaMA",
                },
            ]
        )
        metrics = db["Metrics"].insert_many(
            [
                {"name": "m1", "description": "desc1"},
                {"name": "m2", "description": "desc2"},
            ]
        )
        db["Evaluate"].insert_many(
            [
                {
                    "Models": models.inserted_ids[0],
                    "Metrics": metrics.inserted_ids[0],
                },
                {
                    "Models": models.inserted_ids[0],
                    "Metrics": metrics.inserted_ids[1],
                },
            ]
        )

        dao = Dao(db)
        res = dao.query(
            [
                {
                    "collection": "Models",
                    "filters": {"name": "model1"},
                    "project": ["name"],
                },
                {
                    "collection": "Metrics",
                    "filters": {"description": "desc2"},
                    "project": ["name"],
                },
            ]
        )
        self.assertEqual(len(res), 1)
        self.assertDictEqual(
            res[0],
            {
                "Models": {
                    "name": "model1",
                },
                "Metrics": {"name": "m2"},
            },
        )

    def test_join_no_filters_no_projection(self):
        """join without projection nor fields"""
        models = db["Models"].insert_many(
            [
                {
                    "name": "model1",
                    "version": "LLaMA",
                    "numberOfParameters [B]": 3,
                    "architecture": "LLaMA",
                },
                {
                    "name": "model1",
                    "version": "LLaMA",
                    "numberOfParameters [B]": 5,
                    "architecture": "LLaMA",
                },
                {
                    "name": "model2",
                    "version": "GPT",
                    "numberOfParameters [B]": 5,
                    "architecture": "LLaMA",
                },
            ]
        )
        metrics = db["Metrics"].insert_many(
            [
                {"name": "m1", "description": "desc1"},
                {"name": "m2", "description": "desc2"},
            ]
        )
        db["Evaluate"].insert_many(
            [
                {
                    "Models": models.inserted_ids[0],
                    "Metrics": metrics.inserted_ids[0],
                },
                {
                    "Models": models.inserted_ids[0],
                    "Metrics": metrics.inserted_ids[1],
                },
            ]
        )

        dao = Dao(db)
        res = dao.query(
            [
                {
                    "collection": "Models",
                },
                {
                    "collection": "Metrics",
                },
            ]
        )
        self.assertEqual(len(res), 2)
        self.assertDictEqual(
            res[0],
            {
                "Models": {
                    "name": "model1",
                    "version": "LLaMA",
                    "numberOfParameters [B]": 3,
                    "architecture": "LLaMA",
                },
                "Metrics": {"name": "m1", "description": "desc1"},
            },
        )
        self.assertDictEqual(
            res[1],
            {
                "Models": {
                    "name": "model1",
                    "version": "LLaMA",
                    "numberOfParameters [B]": 3,
                    "architecture": "LLaMA",
                },
                "Metrics": {"name": "m2", "description": "desc2"},
            },
        )

    def test_join_no_filters(self):
        """join with only projection (no filters)"""
        models = db["Models"].insert_many(
            [
                {
                    "name": "model1",
                    "version": "LLaMA",
                    "numberOfParameters [B]": 3,
                    "architecture": "LLaMA",
                },
                {
                    "name": "model1",
                    "version": "LLaMA",
                    "numberOfParameters [B]": 5,
                    "architecture": "LLaMA",
                },
                {
                    "name": "model2",
                    "version": "GPT",
                    "numberOfParameters [B]": 5,
                    "architecture": "LLaMA",
                },
            ]
        )
        metrics = db["Metrics"].insert_many(
            [
                {"name": "m1", "description": "desc1"},
                {"name": "m2", "description": "desc2"},
            ]
        )
        db["Evaluate"].insert_many(
            [
                {
                    "Models": models.inserted_ids[0],
                    "Metrics": metrics.inserted_ids[0],
                },
                {
                    "Models": models.inserted_ids[0],
                    "Metrics": metrics.inserted_ids[1],
                },
            ]
        )

        dao = Dao(db)
        res = dao.query(
            [
                {"collection": "Models", "project": ["name"]},
                {
                    "collection": "Metrics",
                },
            ]
        )
        self.assertEqual(len(res), 2)
        self.assertDictEqual(
            res[0],
            {
                "Models": {
                    "name": "model1",
                },
            },
        )
        self.assertDictEqual(
            res[1],
            {
                "Models": {
                    "name": "model1",
                }
            },
        )


if __name__ == "__main__":
    unittest.main()
