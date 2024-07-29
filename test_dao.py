from dao import Dao
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

        dao = Dao(db)
        res = dao.query([
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

        dao = Dao(db)
        res = dao.query([
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

        dao = Dao(db)
        res = dao.query([
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

        dao = Dao(db)
        res = dao.query([
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

        dao = Dao(db)
        res = dao.query([])
        self.assertEqual(len(res), 0)
        res = dao.query(None)
        self.assertEqual(len(res), 0)
        res = dao.query({})
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

        dao = Dao(db)
        res = dao.query([
            {
                "collection": "Models",
                "project": ["name"],
            },
        ])
        self.assertEqual(len(res), 2)
        for item in res:
            self.assertIn("Models", item)
            self.assertIn("name", item["Models"])
            self.assertNotIn("version", item["Models"])
            self.assertNotIn("numberOfParameters [B]", item["Models"])

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

        dao = Dao(db)
        res = dao.query([
            {
                "collection": "Models",
                "filters": {"name": "model1"},
            },
        ])
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0]["Models"]["name"], "model1")
        self.assertEqual(res[0]["Models"]["version"], "LLaMA")
        self.assertEqual(res[0]["Models"]["numberOfParameters [B]"], 3)

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

        dao = Dao(db)
        res = dao.query([
            {
                "collection": "Models",
                "project": ["name"],
                "filters": {"name": "model1"},
            },
        ])
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0]["Models"]["name"], "model1")
        self.assertNotIn("version", res[0]["Models"])
        self.assertNotIn("numberOfParameters [B]", res[0]["Models"])

    def test_wrong_filter(self):
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

        dao = Dao(db)
        res = dao.query([
            {
                "collection": "Models",
                "filters": {"nam": "model1"},
            },
        ])
        self.assertEqual(len(res), 0)

    def test_wrong_project(self):
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

        dao = Dao(db)
        res = dao.query([
            {
                "collection": "Models",
                "project": ["nam"],
            },
        ])
        self.assertEqual(len(res), 2)
        for item in res:
            self.assertEqual(item, {"Models": {}})


if __name__ == '__main__':
    unittest.main()
