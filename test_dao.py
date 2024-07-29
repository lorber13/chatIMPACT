from dao import query
import unittest

from database import getDatabase

db = getDatabase("Test")

class SingleCollection(unittest.TestCase):
    def setUp(self):
        db["Models"].drop()
        db["Datasets"].drop()
        db["Downstream Tasks"].drop()
        db["Metrics"].drop()

    def test_models(self):
        db["Models"].insert_many([
            {
                "name": "model1",
                "version": "LLaMA",
                "numberOfParameters [B]": 3
            },
            {
                "name": "model2",
                "version": "GPT",
                "numberOfParameters [B]": 5
            }
        ])

        res = query(db, [
            {
                "collection": "Models"
            }
        ])
        self.assertEqual(len(res), 2)

    def test_datasets(self):
        db["Datasets"].insert_many([
            {
                "name": "dataset1",
            },
            {
                "name": "dataset2",
            }
        ])

        res = query(db, [
            {
                "collection": "Datasets"
            }
        ])
        self.assertEqual(len(res), 2)

    def test_metrics(self):
        db["Metrics"].insert_many([
            {
                "name": "m1",
            },
            {
                "name": "m2",
            }
        ])

        res = query(db, [
            {
                "collection": "Metrics"
            }
        ])
        self.assertEqual(len(res), 2)

    def test_downstream(self):
        db["Downstream Tasks"].insert_many([
            {
                "name": "ds1",
            },
            {
                "name": "ds2",
            }
        ])

        res = query(db, [
            {
                "collection": "Downstream Tasks"
            }
        ])
        self.assertEqual(len(res), 2)

    def test_no_spec(self):
        db["Downstream Tasks"].insert_many([
            {
                "name": "ds1",
            },
            {
                "name": "ds2",
            }
        ])

        res = query(db, [])
        self.assertEqual(len(res), 0)
        res = query(db, None)
        self.assertEqual(len(res), 0)
        res = query(db, {})
        self.assertEqual(len(res), 0)

    def test_project(self):
        db["Models"].insert_many([
            {
                "name": "model1",
                "version": "LLaMA",
                "numberOfParameters [B]": 3
            },
            {
                "name": "model2",
                "version": "GPT",
                "numberOfParameters [B]": 5
            }
        ])

        res = query(db, [
            {
                "collection": "Models",
                "project": ["name"],
            },
        ])
        self.assertEqual(len(res), 2)
        for item in res:
            self.assertIn("name", item)
            self.assertNotIn("version", item)
            self.assertNotIn("numberOfParameters [B]", item)

    def test_filter(self):
        db["Models"].insert_many([
            {
                "name": "model1",
                "version": "LLaMA",
                "numberOfParameters [B]": 3
            },
            {
                "name": "model2",
                "version": "GPT",
                "numberOfParameters [B]": 5
            }
        ])

        res = query(db, [
            {
                "collection": "Models",
                "filters": {"name": "model1"},
            },
        ])
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0]["name"], "model1")
        self.assertEqual(res[0]["version"], "LLaMA")
        self.assertEqual(res[0]["numberOfParameters [B]"], 3)

    def test_filter_project(self):
        db["Models"].insert_many([
            {
                "name": "model1",
                "version": "LLaMA",
                "numberOfParameters [B]": 3
            },
            {
                "name": "model2",
                "version": "GPT",
                "numberOfParameters [B]": 5
            }
        ])

        res = query(db, [
            {
                "collection": "Models",
                "project": ["name"],
                "filters": {"name": "model1"},
            },
        ])
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0]["name"], "model1")
        self.assertNotIn("version", res[0])
        self.assertNotIn("numberOfParameters [B]", res[0])

if __name__ == '__main__':
    unittest.main()
