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

    def test_join_models_metrics(self):
        """join between 'Models' and 'Metrics'"""
        db["Models"].insert_many(
            [
                {
                    "name": "model1",
                    "version": "LLaMA",
                    "numberOfParameters [B]": 3,
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
        db["Metrics"].insert_many(
            [
                {"name": "m1", "description": "desc1"},
                {"name": "m2", "description": "desc2"},
            ]
        )
        db["Evaluate"].insert_many(
            [
                {
                    "model": {
                        "name": "model1",
                        "version": "LLaMA",
                        "numberOfParameters [B]": 3,
                    },
                    "metric": "m1",
                },
                {
                    "model": {
                        "name": "model1",
                        "version": "LLaMA",
                        "numberOfParameters [B]": 3,
                    },
                    "metric": "m2",
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


if __name__ == "__main__":
    unittest.main()
