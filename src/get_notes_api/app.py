import json
import os
from decimal import Decimal

import boto3


dynamodb = boto3.client("dynamodb")
TABLE_NAME = os.environ["DYNAMODB_TABLE"]


def lambda_handler(event, context):
    response = dynamodb.scan(
        TableName=TABLE_NAME,
        FilterExpression="begins_with(pk, :prefix) AND pk = sk",
        ExpressionAttributeValues={":prefix": {"S": "note#"}},
    )

    notes = [deserialize_item(item) for item in response.get("Items", [])]
    notes.sort(key=lambda x: x.get("created", 0), reverse=True)

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(notes),
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
