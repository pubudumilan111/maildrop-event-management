import json
import os

import boto3
from botocore.exceptions import ClientError


dynamodb = boto3.client("dynamodb")
TABLE_NAME = os.environ["DYNAMODB_TABLE"]


def lambda_handler(event, context):
    for record in event.get("Records", []):
        note = extract_note_from_sqs_record(record)
        create_note_record(note)

    return {"status": "complete"}


def extract_note_from_sqs_record(record):
    envelope = json.loads(record["body"])
    return json.loads(envelope["Message"])


def create_note_record(note):
    item = {
        "pk": {"S": f"note#{note['id']}"},
        "sk": {"S": f"note#{note['id']}"},
        "id": {"S": note["id"]},
        "title": {"S": note["title"]},
        "body": {"S": note["body"]},
        "source": {"S": note.get("source", "api")},
        "status": {"S": "created"},
        "created": {"N": str(note["created"])},
    }

    dynamodb.put_item(
        TableName=TABLE_NAME,
        Item=item,
        ConditionExpression="attribute_not_exists(pk) AND attribute_not_exists(sk)",
    )
