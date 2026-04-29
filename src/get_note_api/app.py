import json
import os

import boto3


dynamodb = boto3.client("dynamodb")
TABLE_NAME = os.environ["DYNAMODB_TABLE"]


def lambda_handler(event, context):
    note_id = event.get("pathParameters", {}).get("id")

    if not note_id:
        return {
            "statusCode": 400,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"error": "Missing note id"}),
        }

    key = f"note#{note_id}"

    response = dynamodb.get_item(
        TableName=TABLE_NAME,
        Key={
            "pk": {"S": key},
            "sk": {"S": key},
        },
    )

    item = response.get("Item")
    if not item:
        return {
            "statusCode": 404,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"error": "Note not found"}),
        }

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(deserialize_item(item)),
    }


def deserialize_item(item):
    result = {}
    for key, value in item.items():
        if "S" in value:
            result[key] = value["S"]
        elif "N" in value:
            number = value["N"]
            result[key] = int(number) if number.isdigit() else float(number)
        elif "BOOL" in value:
            result[key] = value["BOOL"]
        elif "NULL" in value:
            result[key] = None
    return result
