# Project Status

## Project Path
`/Users/pubudumilan/Documents/practice/calendarsnack/maildrop-event-management`

## Purpose
Small learning project to understand the core platform concepts used in CalendarSnack, starting from a much simpler use case.

This project is intended to teach:
- AWS SAM
- CloudFormation-style resource modeling through SAM
- API Gateway
- Lambda
- DynamoDB
- SNS
- SQS
- later: SES inbound email, SAR, Sceptre, and Jinja

## Current Phase
Phase 2

## What Exists Now
### API read path
- `GET /notes`
- `GET /notes/{id}`

### Async write path
- `POST /notes`
- API Lambda publishes to SNS
- SNS delivers to SQS
- worker Lambda consumes SQS and writes to DynamoDB

## Current Files
- `template.yaml`
- `README.md`
- `requirements.txt`
- `events/get-note.json`
- `events/list-notes.json`
- `events/create-note-api.json`
- `events/create-note-record-sqs.json`
- `src/get_notes_api/app.py`
- `src/get_note_api/app.py`
- `src/create_note_request_api/app.py`
- `src/create_note_record/app.py`

## Architecture
```text
GET  /notes        -> API Gateway -> Lambda -> DynamoDB
GET  /notes/{id}   -> API Gateway -> Lambda -> DynamoDB
POST /notes        -> API Gateway -> Lambda -> SNS -> SQS -> Lambda -> DynamoDB
```

## Next Goal
Deploy and test phase 2 end-to-end.

### Expected next steps
1. Run `sam build`
2. Run `sam deploy`
3. Get deployed API URL from CloudFormation outputs
4. Seed a couple of notes for GET testing
5. Test `GET /notes`
6. Test `GET /notes/{id}`
7. Test `POST /notes`
8. Verify the async note reaches DynamoDB

## Suggested Commands
### Build
```bash
cd /Users/pubudumilan/Documents/practice/calendarsnack/maildrop-event-management
sam build
```

### Deploy
```bash
sam deploy \
  --stack-name maildrop-event-management \
  --resolve-s3 \
  --capabilities CAPABILITY_IAM
```

### Get API URL
```bash
aws cloudformation describe-stacks \
  --stack-name maildrop-event-management \
  --query "Stacks[0].Outputs[?OutputKey=='ApiUrl'].OutputValue" \
  --output text
```

### Seed notes
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
```

```bash
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

### Test GET
```bash
curl "$API_URL/notes"
curl "$API_URL/notes/1"
```

### Test POST
```bash
curl -X POST \
  -H 'Content-Type: application/json' \
  -d '{"title":"My async note","body":"Created through SNS and SQS"}' \
  "$API_URL/notes"
```

## Learning Intent
The next chat should continue from the existing generated code, not recreate the project from scratch.

The focus should be:
- understanding the architecture while deploying it
- learning how SNS + SQS + Lambda fit together
- preparing for phase 3, which will introduce SES inbound email
