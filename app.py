# -----------------------------------------------------------#
# imports.
# -----------------------------------------------------------#

import os
import sys
from urllib.error import HTTPError
from flask import Flask, request, jsonify, abort, flash, url_for
from flask_migrate import Migrate
from sqlalchemy import exc
import json
import config
from flask_cors import CORS
from auth.auth import AuthError, requires_auth
from werkzeug.utils import redirect
from database.models import db, Drug, Pharmacy, Drug_Availability, setup_db
from flask_moment import Moment


# -----------------------------------------------------------#
# App and db set up.
# -----------------------------------------------------------#
def create_app():
    app = Flask(__name__)
    app.config.from_object(os.environ['APP_SETTINGS'])
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    setup_db(app)
    CORS(app)

    # -----------------------------------------------------------#
    # Routes.
    # -----------------------------------------------------------#

    @app.route('/')
    def index():
        return jsonify({'Welcome To DrugsApp!': 'App is Running'},
                       {'Endpoints': ['/login', '/drugs',
                                      '/drugs/<int:drug_id>', '/drug/create',
                                      '/pharmacies',
                                      '/pharmacies/<int:pharmacy_id>',
                                      '/pharmacy/create',
                                      '/pharmacy/<int:pharmacy_id>/edit',
                                      '/pharmacy/<int:pharmacy_id>/delete']})

    # Endpoint to login
    @app.route('/login')
    def login():
        return jsonify({
            'LoginURL': 'https://dev-faisal.us.auth0.com/authorize?audience'
                        '=drugs&response_type=token&client_id '
                        '=ISIDDGjOprw72TuzTcLp9bACvnbo7dDX&redirect_uri'
                        '=https://capstone-drugs-app.herokuapp.com/'})

    # Endpoint to retrieve drugs list
    @app.route('/drugs')
    @requires_auth('get:drugs')
    def drugs(payload):
        try:
            drugs = Drug.query.order_by(Drug.id).all()
            data = []
            for drug in drugs:
                data.append({
                    "id": drug.id,
                    "name": drug.name,
                    "price": drug.price,
                })
        except (HTTPError, Exception):
            abort(422)
        return jsonify({
            "success": True,
            "data": data
        })

    # Endpoint to retrieve a specific drug
    @app.route('/drugs/<int:drug_id>', methods=['GET'])
    @requires_auth('get:drugs')
    def show_drug(payload, drug_id):
        drug = Drug.query.get(drug_id)
        if drug is None:
            abort(404)
        else:
            available_at = db.session.query(Drug_Availability).filter(
                Drug_Availability.drug_id == drug.id).all()
            pharmacies_names = []
            for item in available_at:
                pharmacy = db.session.query(Pharmacy).filter(
                    Pharmacy.id == item.id).first()
                pharmacies_names.append(pharmacy.name)
            data = {
                "id": drug.id,
                "name": drug.name,
                "description": drug.description,
                "side_effects": drug.side_effects,
                "price": drug.price,
                "image_link": drug.image_link,
                "available_at": [name for name in pharmacies_names]
            }
            return jsonify({
                "success": True,
                "data": data
            })

    # Endpoint to insert a drug to db
    @app.route('/drug/create', methods=['POST'])
    @requires_auth('post:drugs')
    def create_drug_submission(payload):
        body = request.get_json()
        if body is None:
            abort(404)
        try:
            name = body['name']
            price = body['price']
            description = body['description']
            side_effects = body['side_effects']
            image_link = body['image_link']
            drug = Drug(name=name, price=price, description=description,
                        side_effects=side_effects,
                        image_link=image_link)
            drug.insert()
            all_drugs = Drug.query.order_by(Drug.id).all()
            return jsonify({
                "success": True,
                "data": [drug.long() for drug in all_drugs]
            })
        except (HTTPError, Exception):
            db.session.rollback()
            print(sys.exc_info())
            abort(422)
        finally:
            db.session.close()

    # Endpoint to retrieve pharmacies list
    @app.route('/pharmacies')
    @requires_auth('get:pharmacies')
    def pharmacies(payload):
        try:
            all_pharmacies = Pharmacy.query.order_by(Pharmacy.id).all()
            data = []
            for pharmacy in all_pharmacies:
                data.append({
                    "id": pharmacy.id,
                    "name": pharmacy.name,
                })
        except (HTTPError, Exception):
            abort(422)
        return jsonify({
            "success": True,
            "data": data})

    # Endpoint to retrieve a specific pharmacy
    @app.route('/pharmacies/<int:pharmacy_id>', methods=['GET'])
    @requires_auth('get:pharmacies')
    def show_pharmacy(payload, pharmacy_id):
        pharmacy = Pharmacy.query.get(pharmacy_id)
        if pharmacy is None:
            abort(404)
        else:
            data = {
                "id": pharmacy.id,
                "name": pharmacy.name,
                "city": pharmacy.city,
                "phone": pharmacy.phone,
                "location_link": pharmacy.location_link,
                "image_link": pharmacy.image_link,
            }
            return jsonify({
                "success": True,
                "data": data
            })

    # Endpoint to insert a pharmacy to db
    @app.route('/pharmacy/create', methods=['POST'])
    @requires_auth('post:pharmacies')
    def create_pharmacy_submission(payload):
        body = request.get_json()
        if body is None:
            abort(404)
        try:
            name = body['name']
            city = body['city']
            phone = body['phone']
            location_link = body['location_link']
            image_link = body['image_link']
            pharmacy = Pharmacy(name=name, city=city, phone=phone,
                                location_link=location_link,
                                image_link=image_link)
            pharmacy.insert()
            all_pharmacies = Pharmacy.query.order_by(Pharmacy.id).all()
            return jsonify({
                "success": True,
                "data": [pharmacy.long() for pharmacy in all_pharmacies]
            })
        except (HTTPError, Exception):
            db.session.rollback()
            print(sys.exc_info())
            abort(422)
        finally:
            db.session.close()

    # Endpoint to edit a specific pharmacy
    @app.route('/pharmacy/<int:pharmacy_id>/edit', methods=['PATCH'])
    @requires_auth('edit:pharmacies')
    def edit_pharmacy_submission(payload, pharmacy_id):
        body = request.get_json()
        # check if no body
        updated_attributes = 0
        if body is None:
            abort(404)
        try:
            pharmacy_to_edit = Pharmacy.query.get(pharmacy_id)
            # check if invalid id
            if pharmacy_to_edit is None:
                abort(404)
            if 'name' in body and body['name']:
                pharmacy_to_edit.name = body['name']
                updated_attributes += 1
            if 'city' in body and body['city']:
                pharmacy_to_edit.city = body['city']
                updated_attributes += 1
            if 'phone' in body and body['phone']:
                pharmacy_to_edit.phone = body['phone']
                updated_attributes += 1
            if 'location_link' in body and body['location_link']:
                pharmacy_to_edit.location_link = body['location_link']
                updated_attributes += 1
            if 'image_link' in body and body['image_link']:
                pharmacy_to_edit.image_link = body['image_link']
                updated_attributes += 1
            # check if no attributes has updated (empty request or
            # invalid attributes)
            if updated_attributes == 0:
                abort(422)
            pharmacy_to_edit.update()
            all_pharmacies = Pharmacy.query.order_by(Pharmacy.id).all()
            return jsonify({
                "success": True,
                "pharmacies": [pharmacy.long() for pharmacy in all_pharmacies]
            })
        except (HTTPError, Exception):
            db.session.rollback()
            print(sys.exc_info())
            abort(422)
        finally:
            db.session.close()

    # Endpoint to delete a specific pharmacy
    @app.route('/pharmacy/<int:pharmacy_id>/delete', methods=['DELETE'])
    @requires_auth('delete:pharmacies')
    def delete_pharmacy(payload, pharmacy_id):
        try:
            pharmacy_to_delete = Pharmacy.query.get(pharmacy_id)
            if pharmacy_to_delete is None:
                abort(404)
            print(pharmacy_to_delete.name)
            # check and remove pharmacy from other tables
            # to avoid integrity error
            dependent_record = Drug_Availability.query.get(pharmacy_id)
            if dependent_record:
                db.session.delete(dependent_record)
            # then remove from main table
            pharmacy_to_delete.delete()
            all_pharmacies = Pharmacy.query.order_by(Pharmacy.id).all()
            return jsonify({
                "success": True,
                "data": [pharmacy.long() for pharmacy in all_pharmacies]
            })
        except (HTTPError, Exception):
            db.session.rollback()
            print(sys.exc_info())
            abort(422)
        finally:
            db.session.close()

    # -----------------------------------------------------------#
    # Error Handling.
    # -----------------------------------------------------------#

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad request "
        }), 400

    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({
            "success": False,
            "error": 401,
            "message": "Unauthorized"
        }), 401

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "Method not allowed"
        }), 405

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "Internal server error"
        }), 500

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Resource not found"
        }), 404

    @app.errorhandler(AuthError)
    def auth_error(AuthError):
        return jsonify({
            "success": False,
            "error": AuthError.status_code,
            "message": AuthError.error['description']
        }), AuthError.status_code

    return app


app = create_app()

if __name__ == '__main__':
    app.run()
