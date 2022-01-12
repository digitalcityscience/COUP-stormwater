import os
from http import HTTPStatus

from celery.result import AsyncResult
from flask import Flask, request, abort, make_response, jsonify
from flask_compress import Compress
from flask_cors import CORS
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash

import services
import tasks
from mycelery import app as celery_app

app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
Compress(app)

auth = HTTPBasicAuth()

CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_PASSWORD = os.getenv('CLIENT_PASSWORD')

pw_hashes = {
    CLIENT_ID: generate_password_hash(CLIENT_PASSWORD)
}


@auth.verify_password
def verify_password(client_id, password):
    if client_id in pw_hashes and \
            check_password_hash(pw_hashes.get(client_id), password):
        return client_id


@auth.error_handler
def auth_error(status):
    return make_response(
        jsonify({'error': 'Access denied.'}),
        status
    )


@app.route('/')
@app.errorhandler(404)
def not_found(message: str):
    return make_response(
        jsonify({'error': message}),
        404
    )


@app.errorhandler(401)
def not_found(message: str):
    return make_response(
        jsonify({'error': message}),
        404
    )


@app.errorhandler(400)
def bad_request(message: str):
    return make_response(
        jsonify({'error': message}),
        400
    )


# process calculation requests 
@app.route("/task", methods=['POST'])
@auth.login_required
def process_swimdocktask():
    # Validate request
    if not request.json:
        abort(400)

    # Handle requests
    try:
        single_result = tasks.compute_task.delay(*services.get_calculation_input(request.json))
        response = {'taskId': single_result.id}

        # return jsonify(response), HTTPStatus.OK
        return make_response(
            jsonify(response),
            HTTPStatus.OK,
        )
    except KeyError as e:
        print("THIS IS THE ERROR %s " % e)
        print("THIS IS THE request %s " % request)

        return make_response(
            jsonify(e),
            HTTPStatus.OK,
        )
        return bad_request("Payload not correctly structured.")



@app.route("/tasks/<task_id>", methods=['GET'])
@auth.login_required
def get_task(task_id: str):
    async_result = AsyncResult(task_id, app=celery_app)

    # Fields available
    # https://docs.celeryproject.org/en/stable/reference/celery.result.html#celery.result.Result
    response = {
        'taskId': async_result.id,
        'taskState': async_result.state,
        'taskSucceeded': async_result.successful(),
        'resultReady': async_result.ready(),
    }
    if async_result.ready():
        response['result'] = async_result.get()

    return make_response(
        response,
        HTTPStatus.OK,
    )
