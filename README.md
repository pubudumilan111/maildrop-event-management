# maildrop-event-management

Tiny learning project for understanding the first layers of the CalendarSnack deployment model.

## What phase 2 covers
- AWS SAM template structure
- API Gateway to Lambda routing
- DynamoDB reads
- Asynchronous writes with SNS + SQS + Lambda
- Cloud deployment with `sam deploy`

## Architecture

```text
GET  /notes        -> API Gateway -> Lambda -> DynamoDB
GET  /notes/{id}   -> API Gateway -> Lambda -> DynamoDB
POST /notes        -> API Gateway -> Lambda -> SNS -> SQS -> Lambda -> DynamoDB
```

## Project structure

```text
maildrop-event-management/
  template.yaml
  events/
    create-note-api.json
    create-note-record-sqs.json
    get-note.json
    list-notes.json
  src/
    create_note_request_api/
      app.py
    create_note_record/
      app.py
    get_notes_api/
      app.py
    get_note_api/
      app.py
  requirements.txt
```

## Build

```bash
sam build
```

## Local API run

```bash
sam local start-api
```

## Local read tests

```bash
curl http://127.0.0.1:3000/notes
curl http://127.0.0.1:3000/notes/1
```

## POST note after deploy

```bash
curl -X POST \
  -H 'Content-Type: application/json' \
  -d '{"title":"My async note","body":"Created through SNS and SQS"}' \
  <API_URL>/notes
```

Expected response:
- `202 Accepted`
- note payload with generated `id`

## Deploy

```bash
sam build
sam deploy \
  --stack-name maildrop-event-management \
  --resolve-s3 \
  --capabilities CAPABILITY_IAM
```

## Seed read-path test data

```bash
aws dynamodb put-item \
  --table-name notes \
  --item '{
    "pk": {"S": "note#1"},
    "sk": {"S": "note#1"},
    "id": {"S": "1"},
    "title": {"S": "First note"},
    "body": {"S": "Hello from DynamoDB"},
    "source": {"S": "seed"},
    "status": {"S": "created"},
    "created": {"N": "1777500000"}
  }'

aws dynamodb put-item \
  --table-name notes \
  --item '{
    "pk": {"S": "note#2"},
    "sk": {"S": "note#2"},
    "id": {"S": "2"},
    "title": {"S": "Second note"},
    "body": {"S": "Another note"},
    "source": {"S": "seed"},
    "status": {"S": "created"},
    "created": {"N": "1777500100"}
  }'
```

## What to observe in phase 2
- `POST /notes` does not write directly to DynamoDB
- the API Lambda publishes to SNS
- SNS fans out into SQS
- the worker Lambda consumes the SQS message and writes the note
- this mirrors the async style used in CalendarSnack

## Next step ideas
- add SES inbound email and S3-based processing
- add a second repo for deployment orchestration
- publish the app through SAR
- wrap the full stack with Sceptre + Jinja + CloudFormation
