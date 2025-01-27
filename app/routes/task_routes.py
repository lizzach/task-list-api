from flask import Blueprint, jsonify, request, make_response, abort
from app.models.task import Task
from .routes_helpers import validate_model
from sqlalchemy import asc, desc
from app import db
from datetime import datetime
import requests
import json
import os

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

# get all endpoint
@tasks_bp.route("", methods=["GET"])
def get_all_tasks():
    
    sort_param = request.args.get("sort")
    task_query = Task.query

    if sort_param == "asc":
        task_query = task_query.order_by(asc(Task.title))
    if sort_param == "desc":
        task_query = task_query.order_by(desc(Task.title))

    task_list = [task.to_dict() for task in task_query]

    return jsonify(task_list), 200

# get one task endpoint
@tasks_bp.route("/<id>", methods=["GET"])
def get_one_task(id):
    task = validate_model(Task, id)

    response_body = task.to_dict()

    return jsonify({"task": response_body}), 200

# create task endpoint
@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    
    new_task = Task.from_dict(request_body)

    db.session.add(new_task)
    db.session.commit()

    return jsonify({f"task": new_task.to_dict()}), 201

# update task endpoint
@tasks_bp.route("/<id>", methods=["PUT"])
def update_task(id):
    task = validate_model(Task, id)

    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()

    return jsonify({"task": task.to_dict()}), 200

# delete task endpoint
@tasks_bp.route("/<id>", methods=["DELETE"])
def delete_task(id):
    task = validate_model(Task, id)

    db.session.delete(task)
    db.session.commit()

    return jsonify({"details": f'Task {task.id} "{task.title}" successfully deleted'}), 200

# mark a task complete endpoint
@tasks_bp.route("/<id>/mark_complete", methods=["PATCH"])
def complete_task(id):
    task = validate_model(Task, id)

    task.completed_at = datetime.utcnow()

    db.session.commit()

    post_message_to_slack(task)

    return jsonify({"task": task.to_dict()}), 200

# mark a task incomplete endpoint
@tasks_bp.route("/<id>/mark_incomplete", methods=["PATCH"])
def incomplete_task(id):
    task = validate_model(Task, id)

    task.completed_at = None

    db.session.commit()

    return jsonify({"task": task.to_dict()}), 200

# helper function to post completion message to slack
def post_message_to_slack(task):
    url = "https://slack.com/api/chat.postMessage"
    message = f"Someone just completed the task {task.title}"

    payload = json.dumps(
        {
        "channel": "U0574FB59PS",
        "text": message
        }
    )

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {os.environ.get("BOT_TOKEN")}'
        }

    response = requests.post(url, headers=headers, data=payload)
    print(response.text)

