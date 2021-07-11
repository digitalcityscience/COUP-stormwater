from http import HTTPStatus

from celery.result import AsyncResult, GroupResult
from flask import Flask, request, abort, make_response, jsonify

import services
from models import ComplexTask
from mycelery import app as celery_app

app = Flask(__name__)


@app.errorhandler(404)
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


@app.route("/grouptasks", methods=['POST'])
def process_grouptask():
    # Validate request
    if not request.json and not 'tasks' in request.json:
        abort(400)

    # Parse requests
    try:
        complex_tasks = [ComplexTask.from_json(json=ct) for ct in request.json['tasks']]
        group_result = services.compute(complex_tasks=complex_tasks)
        result_ids = [result.id for result in group_result.results]
        response = {'groupTaskId': group_result.id, 'resultIds': result_ids}

        # return jsonify(response), HTTPStatus.OK
        return make_response(
            jsonify(response),
            HTTPStatus.OK,
        )
    except KeyError:
        return bad_request("Payload not correctly structured.")


@app.route("/grouptasks/<grouptask_id>", methods=['GET'])
def get_grouptask(grouptask_id: str):
    group_result = GroupResult.restore(grouptask_id, app=celery_app)

    # Fields available
    # https://docs.celeryproject.org/en/stable/reference/celery.result.html#celery.result.ResultSet
    response = {
        'grouptaskId': group_result.id,
        'tasksCompleted': group_result.completed_count(),
        'tasksTotal': len(group_result.results),
        'grouptaskReady': group_result.ready(),
        'grouptaskSucceeded': group_result.successful(),
        'results': [result.get() for result in group_result.results if result.ready()]
    }
    if group_result.ready():
        response['result'] = group_result.get()

    return make_response(
        response,
        HTTPStatus.OK,
    )


@app.route("/tasks/<task_id>", methods=['GET'])
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
