import json
import os
import time
import uuid

import boto3

sns = boto3.client("sns")
TOPIC_ARN = os.environ["NEW_NOTE_TOPIC_ARN"]


def lambda_handler(event, context):
    try:
        body = json.loads(event.get("body") or "{}")
    except json.JSONDecodeError:
        return response(400, {"error": "Request body must be valid JSON"})

    title = (body.get("title") or "").strip()
    note_body = (body.get("body") or "").strip()

    if not title or not note_body:
        return response(400, {"error": "Both 'title' and 'body' are required"})

    note = {
        "id": uuid.uuid4().hex[:12],
        "title": title,
        "body": note_body,
        "created": int(time.time()),
        "source": "api",
        "status": "queued",
    }

    sns.publish(
        TargetArn=TOPIC_ARN,
        MessageStructure="json",
        Message=json.dumps({"default": json.dumps(note)}),
    )

    return response(202, {"message": "Note queued", "note": note})


def response(status_code, body):
    return {
        "statusCode": status_code,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(body),
    }
