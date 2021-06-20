import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from database.models import setup_db, Pharmacy, Drug


class DrugsAppTestCase(unittest.TestCase):
    """This class represents the Drugs App test case"""

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        self.admin_token = os.environ['admin_token']
        self.visitor_token = os.environ['visitor_token']
        self.database_name = "drugsApp"
        self.database_path = "postgresql://postgres:viktor@localhost:5432/" + \
                             self.database_name
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        self.VALID_NEW_PHARMACY = {
            "name": "pharmacy5",
            "city": "Riyadh",
            "phone": "0555546135",
            "location_link": "https://location.com",
            "image_link": "https://image.com"
        }

        self.INVALID_NEW_PHARMACY = {
            "name": "pharmacy5"
        }

        self.VALID_UPDATE_PHARMACY = {
            "name": "pharmacy22"
        }

        self.INVALID_UPDATE_PHARMACY = {
            "side effect": "side effect"
        }

        self.VALID_NEW_DRUG = {
            "name": "Panadol",
            "description": "drug_description",
            "side_effects": "Headache",
            "price": "13",
            "image_link": "https://image.com"
        }

        self.INVALID_NEW_DRUG = {
            "name": "Panadol",
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_running(self):
        """Test for GET / (default endpoint)"""
        res = self.client().get('/')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['Welcome To DrugsApp!'], 'App is Running')

    def test_api_call_without_token(self):
        """Failing Test trying to make a call without token"""
        res = self.client().get('/drugs')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data["success"])
        self.assertEqual(data["message"], "Authorization Header is required.")

    def test_get_pharmacies(self):
        """Passing Test for GET /pharmacies"""
        res = self.client().get('/pharmacies', headers={
            'Authorization': "Bearer {}".format(self.visitor_token)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data))
        self.assertTrue(data["success"])
        self.assertIn('data', data)
        self.assertTrue(len(data["data"]))

    def test_get_pharmacies_by_id(self):
        """Passing Test for GET /pharmacies/<pharmacy_id>"""
        res = self.client().get('/pharmacies/7', headers={
            'Authorization': "Bearer {}".format(self.user_token)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertIn('data', data)
        self.assertIn('name', data['data'])
        self.assertTrue(len(data["data"]))

    def test_404_get_pharmacy_by_id(self):
        """Failing Test for GET /pharmacies/<pharmacy_id>"""
        res = self.client().get('/pharmacies/999', headers={
            'Authorization': "Bearer {}".format(self.user_token)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertIn('message', data)

    def test_create_pharmacy_with_visitor_token(self):
        """Failing Test for POST /pharmacy/create"""
        res = self.client().post('/pharmacies', headers={
            'Authorization': "Bearer {}".format(self.visitor_token)
        }, json=self.VALID_NEW_PHARMACY)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data["success"])
        self.assertIn('message', data)

    def test_create_pharmacy(self):
        """Passing Test for POST /pharmacy/create"""
        res = self.client().post('/pharmacy/create', headers={
            'Authorization': "Bearer {}".format(self.admin_token)
        }, json=self.VALID_NEW_PHARMACY)
        data = json.loads(res.data)

        self.assertTrue(data["success"])

    def test_422_create_pharmacy(self):
        """Failing Test for POST /pharmacy/create"""
        res = self.client().post('/pharmacy/create', headers={
            'Authorization': "Bearer {}".format(self.admin_token)
        }, json=self.INVALID_NEW_PHARMACY)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])
        self.assertIn('message', data)

    def test_update_pharmacy_info(self):
        """Passing Test for PATCH /pharmacy/<pharmacy_id>/edit"""
        res = self.client().patch('/pharmacy/6/edit', headers={
            'Authorization': "Bearer {}".format(self.manager_token)
        }, json=self.VALID_UPDATE_PHARMACY)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertIn('data', data)
        self.assertEqual(data["data"]["name"],
                         self.VALID_UPDATE_PHARMACY["name"])

    def test_422_update_pharmacy_info(self):
        """Failing Test for PATCH /pharmacy/<pharmacy_id>/edit"""
        res = self.client().patch('/pharmacy/6/edit', headers={
            'Authorization': "Bearer {}".format(self.manager_token)
        }, json=self.INVALID_UPDATE_PHARMACY)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])
        self.assertIn('message', data)

    def test_delete_pharmacy_with_visitor_token(self):
        """Failing Test for DELETE /pharmacy/<int:pharmacy_id>/delete"""
        res = self.client().delete('/pharmacy/8/delete', headers={
            'Authorization': "Bearer {}".format(self.visitor_token)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data["success"])
        self.assertIn('message', data)

    def test_delete_pharmacy(self):
        """Passing Test for DELETE /pharmacy/<int:pharmacy_id>/delete"""
        res = self.client().delete('/pharmacy/8/delete', headers={
            'Authorization': "Bearer {}".format(self.admin_token)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertIn('data', data)

    def test_404_delete_pharmacy(self):
        """Failing Test for DELETE /pharmacy/<int:pharmacy_id>/delete"""
        res = self.client().delete('/pharmacy/999/delete', headers={
            'Authorization': "Bearer {}".format(self.admin_token)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertIn('message', data)

    def test_get_drugs(self):
        """Passing Test for GET /drugs"""
        res = self.client().get('/drugs', headers={
            'Authorization': "Bearer {}".format(self.visitor_token)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data))
        self.assertTrue(data["success"])
        self.assertIn('data', data)
        self.assertTrue(len(data["data"]))

    def test_get_drug_by_id(self):
        """Passing Test for GET /drugs/<drug_id>"""
        res = self.client().get('/drugs/1', headers={
            'Authorization': "Bearer {}".format(self.visitor_token)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertIn('data', data)
        self.assertIn('name', data['data'])
        self.assertIn('price', data['data'])

    def test_404_get_drug_by_id(self):
        """Failing Test for GET /drugs/<drug_id>"""
        res = self.client().get('/drugs/999', headers={
            'Authorization': "Bearer {}".format(self.visitor_token)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertIn('message', data)

    def test_create_drug_with_visitor_token(self):
        """Failing Test for POST /drug/create"""
        res = self.client().post('/drug/create', headers={
            'Authorization': "Bearer {}".format(self.visitor_token)
        }, json=self.VALID_NEW_DRUG)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data["success"])
        self.assertIn('message', data)

    def test_create_drug(self):
        """Passing Test for POST /drug/create"""
        res = self.client().post('/drug/create', headers={
            'Authorization': "Bearer {}".format(self.admin_token)
        }, json=self.VALID_NEW_DRUG)
        data = json.loads(res.data)

        self.assertTrue(data["success"])
        self.assertIn('data', data)

    def test_422_create_drug(self):
        """Failing Test for POST /drug/create"""
        res = self.client().post('/drug/create', headers={
            'Authorization': "Bearer {}".format(self.admin_token)
        }, json=self.INVALID_NEW_DRUG)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])
        self.assertIn('message', data)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
