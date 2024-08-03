"""unit tests for the dao module"""

import unittest
from dao import Dao

dao = Dao("Test")


class SingleCollection(unittest.TestCase):
    """single collection test case"""

    def setUp(self):
        dao.drop("Models")
        dao.drop("Datasets")
        dao.drop("Downstream Tasks")
        dao.drop("Metrics")

    def test_models(self):
        """query from the 'Models' collection"""
        dao.insert_many(
            "Models",
            [
                {"name": "model1", "version": "LLaMA", "numberOfParameters [B]": 3},
                {"name": "model2", "version": "GPT", "numberOfParameters [B]": 5},
            ],
        )

        res = dao.query([{"collection": "Models"}])
        self.assertEqual(len(res), 2)

    def test_datasets(self):
        """query from the 'Datasets' collection"""
        dao.insert_many(
            "Datasets",
            [
                {
                    "name": "dataset1",
                },
                {
                    "name": "dataset2",
                },
            ],
        )
        res = dao.query([{"collection": "Datasets"}])
        self.assertEqual(len(res), 2)

    def test_metrics(self):
        """query from the 'Metrics' collection"""
        dao.insert_many(
            "Metrics",
            [
                {
                    "name": "m1",
                },
                {
                    "name": "m2",
                },
            ],
        )

        res = dao.query([{"collection": "Metrics"}])
        self.assertEqual(len(res), 2)

    def test_downstream(self):
        """query from the 'Downstream Tasks' collection"""
        dao.insert_many(
            "Downstream Tasks",
            [
                {
                    "name": "ds1",
                },
                {
                    "name": "ds2",
                },
            ],
        )

        res = dao.query([{"collection": "Downstream Tasks"}])
        self.assertEqual(len(res), 2)

    def test_no_spec(self):
        """tests wrong function calls"""
        dao.insert_many(
            "Downstream Tasks",
            [
                {
                    "name": "ds1",
                },
                {
                    "name": "ds2",
                },
            ],
        )

        res = dao.query([])
        self.assertEqual(len(res), 0)
        res = dao.query(None)
        self.assertEqual(len(res), 0)
        res = dao.query({})
        self.assertEqual(len(res), 0)

    def test_project(self):
        """projection feature"""
        dao.insert_many(
            "Models",
            [
                {"name": "model1", "version": "LLaMA", "numberOfParameters [B]": 3},
                {"name": "model2", "version": "GPT", "numberOfParameters [B]": 5},
            ],
        )

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
        dao.insert_many(
            "Models",
            [
                {"name": "model1", "version": "LLaMA", "numberOfParameters [B]": 3},
                {"name": "model2", "version": "GPT", "numberOfParameters [B]": 5},
            ],
        )

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
        dao.insert_many(
            "Models",
            [
                {"name": "model1", "version": "LLaMA", "numberOfParameters [B]": 3},
                {"name": "model2", "version": "GPT", "numberOfParameters [B]": 5},
            ],
        )

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
        dao.insert_many(
            "Models",
            [
                {"name": "model1", "version": "LLaMA", "numberOfParameters [B]": 3},
                {"name": "model2", "version": "GPT", "numberOfParameters [B]": 5},
            ],
        )

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
        dao.insert_many(
            "Models",
            [
                {"name": "model1", "version": "LLaMA", "numberOfParameters [B]": 3},
                {"name": "model2", "version": "GPT", "numberOfParameters [B]": 5},
            ],
        )

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
        dao.drop("Models")
        dao.drop("Datasets")
        dao.drop("Downstream Tasks")
        dao.drop("Metrics")
        dao.drop("Evaluate")
        dao.drop("Suited For")
        dao.drop("Train")
        dao.drop("Enable")
        dao.drop("Assess")

    def test_join_models_metrics(self):  # Evaluate
        """join between 'Models' and 'Metrics'"""
        models = dao.insert_many(
            "Models",
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
            ],
        )
        metrics = dao.insert_many(
            "Metrics",
            [
                {"name": "m1", "description": "desc1"},
                {"name": "m2", "description": "desc2"},
            ],
        )
        dao.insert_many(
            "Evaluate",
            [
                {
                    "Models": models.inserted_ids[0],
                    "Metrics": metrics.inserted_ids[0],
                },
                {
                    "Models": models.inserted_ids[0],
                    "Metrics": metrics.inserted_ids[1],
                },
            ],
        )

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
        models = dao.insert_many(
            "Models",
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
            ],
        )
        downstreams = dao.insert_many(
            "Downstream Tasks",
            [
                {"name": "ds1", "description": "desc1", "subTask": "st1"},
                {"name": "ds2", "description": "desc2", "subTask": "st2"},
                {"name": "ds3", "description": "desc3", "subTask": "st3"},
            ],
        )
        dao.insert_many(
            "Suited For",
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
            ],
        )

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
        models = dao.insert_many(
            "Models",
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
            ],
        )
        datasets = dao.insert_many(
            "Datasets",
            [
                {
                    "name": "d1",
                    "description": "desc1",
                    "languages": ["English", "Italian"],
                },
                {"name": "d2", "description": "desc2", "languages": ["Python"]},
                {"name": "d3", "description": "desc3", "languages": ["Rust"]},
            ],
        )
        dao.insert_many(
            "Train",
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
            ],
        )

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
        datasets = dao.insert_many(
            "Datasets",
            [
                {
                    "name": "d1",
                    "description": "desc1",
                    "languages": ["English", "Italian"],
                },
                {"name": "d2", "description": "desc2", "languages": ["Python"]},
                {"name": "d3", "description": "desc3", "languages": ["Rust"]},
            ],
        )
        downstreams = dao.insert_many(
            "Downstream Tasks",
            [
                {"name": "ds1", "description": "desc1", "subTask": "st1"},
                {"name": "ds2", "description": "equal description", "subTask": "st2"},
                {"name": "ds3", "description": "equal description", "subTask": "st3"},
            ],
        )
        dao.insert_many(
            "Enable",
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
            ],
        )

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
        metrics = dao.insert_many(
            "Metrics",
            [
                {"name": "m1", "description": "desc1"},
                {"name": "m2", "description": "desc2"},
            ],
        )
        downstreams = dao.insert_many(
            "Downstream Tasks",
            [
                {"name": "ds1", "description": "desc1", "subTask": "st1"},
                {"name": "ds2", "description": "equal description", "subTask": "st2"},
                {"name": "ds3", "description": "equal description", "subTask": "st3"},
            ],
        )
        dao.insert_many(
            "Assess",
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
            ],
        )

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
        models = dao.insert_many(
            "Models",
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
            ],
        )
        metrics = dao.insert_many(
            "Metrics",
            [
                {"name": "m1", "description": "desc1"},
                {"name": "m2", "description": "desc2"},
            ],
        )
        dao.insert_many(
            "Evaluate",
            [
                {
                    "Models": models.inserted_ids[0],
                    "Metrics": metrics.inserted_ids[0],
                },
                {
                    "Models": models.inserted_ids[0],
                    "Metrics": metrics.inserted_ids[1],
                },
            ],
        )

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
        models = dao.insert_many(
            "Models",
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
            ],
        )
        metrics = dao.insert_many(
            "Metrics",
            [
                {"name": "m1", "description": "desc1"},
                {"name": "m2", "description": "desc2"},
            ],
        )
        dao.insert_many(
            "Evaluate",
            [
                {
                    "Models": models.inserted_ids[0],
                    "Metrics": metrics.inserted_ids[0],
                },
                {
                    "Models": models.inserted_ids[0],
                    "Metrics": metrics.inserted_ids[1],
                },
            ],
        )

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
        models = dao.insert_many(
            "Models",
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
            ],
        )
        metrics = dao.insert_many(
            "Metrics",
            [
                {"name": "m1", "description": "desc1"},
                {"name": "m2", "description": "desc2"},
            ],
        )
        dao.insert_many(
            "Evaluate",
            [
                {
                    "Models": models.inserted_ids[0],
                    "Metrics": metrics.inserted_ids[0],
                },
                {
                    "Models": models.inserted_ids[0],
                    "Metrics": metrics.inserted_ids[1],
                },
            ],
        )

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

    def test_join_mixed(self):
        """join with some filters and some projections"""
        models = dao.insert_many(
            "Models",
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
            ],
        )
        metrics = dao.insert_many(
            "Metrics",
            [
                {"name": "m1", "description": "desc1"},
                {"name": "m2", "description": "desc2"},
            ],
        )
        dao.insert_many(
            "Evaluate",
            [
                {
                    "Models": models.inserted_ids[0],
                    "Metrics": metrics.inserted_ids[0],
                },
                {
                    "Models": models.inserted_ids[0],
                    "Metrics": metrics.inserted_ids[1],
                },
            ],
        )

        res = dao.query(
            [
                {"collection": "Models", "project": ["name"]},
                {
                    "collection": "Metrics",
                    "filters": {"description": "desc"},
                },
            ]
        )
        self.assertEqual(len(res), 0)


class GetAll(unittest.TestCase):
    """get the domain of a certain attribute"""

    def setUp(self) -> None:
        dao.drop("Metrics")
        dao.drop("Models")
        dao.drop("Downstream Tasks")
        dao.drop("Datasets")

    def test_array_attribute(self):
        """the type of the attribute is an array"""
        dao.insert_many(
            "Datasets",
            [
                {
                    "name": "MT-Bench",
                    "size [GB]": None,
                    "size [rows]": 80,
                    "languages": ["English"],
                    "licenseToUse": "Apache-2.0",
                    "domain": [
                        "Mathematics",
                        "Coding",
                        "STEM",
                        "Humanities",
                        "Social Sciences",
                        "Miscellaneous",
                    ],
                    "uri": "https://arxiv.org/pdf/2306.05685",
                    "trainingDataset": False,
                    "fineTuning": False,
                    "evaluationDataset": True,
                    "downstreamTask": [],
                    "largeLanguageModel": ["LLaMA", "Vicuna"],
                    "evaluationTechnique": [],
                },
                {
                    "name": "C4",
                    "size [GB]": 7000,
                    "size [rows]": None,
                    "languages": ["English"],
                    "licenseToUse": "Apache-2.0",
                    "domain": [
                        "Miscellaneous",
                        "STEM",
                        "Medical",
                        "Juridic",
                        "Other",
                        "Hiring",
                    ],
                    "uri": "https://arxiv.org/pdf/1910.10683",
                    "trainingDataset": True,
                    "fineTuning": False,
                    "evaluationDataset": False,
                    "downstreamTask": [],
                    "largeLanguageModel": [],
                    "evaluationTechnique": [],
                },
            ],
        )
        result = dao.get_all("Datasets", "domain")
        self.assertCountEqual(
            result,
            [
                "Mathematics",
                "Coding",
                "STEM",
                "Humanities",
                "Social Sciences",
                "Miscellaneous",
                "Medical",
                "Juridic",
                "Other",
                "Hiring",
            ],
        )

    def test_string_attribute(self):
        """the type of the attribute is a string"""
        dao.insert_many(
            "Metrics",
            [
                {
                    "name": "BLEU",
                    "description": "Measures overlap between generated text and reference translations.",
                    "context": "Context-free",
                    "trained": False,
                    "featureBased/endToEnd": None,
                    "granularity": "N-gram level",
                    "uri": "https://www.aclweb.org/anthology/P02-1040.pdf",
                    "extra": None,
                    "type": "metric",
                },
                {
                    "name": "BERTScore",
                    "description": "Uses BERT embeddings to compare generated text to reference text.",
                    "context": "Context-dependent",
                    "trained": True,
                    "featureBased/endToEnd": "Feature-based",
                    "granularity": None,
                    "uri": "https://arxiv.org/abs/1904.09675",
                    "extra": None,
                    "type": "metric",
                },
            ],
        )
        result = dao.get_all("Metrics", "context")
        self.assertCountEqual(
            result,
            [
                "Context-free",
                "Context-dependent",
            ],
        )


if __name__ == "__main__":
    unittest.main()
