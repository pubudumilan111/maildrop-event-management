# maildrop-event-management

## Overview
`maildrop-event-management` is a small AWS serverless learning project built to understand the architecture patterns used in larger event-driven systems. It uses a simple notes application as the business use case so the focus stays on infrastructure, messaging, and deployment flow rather than domain complexity.

The project demonstrates how to:
- expose REST APIs with Amazon API Gateway and AWS Lambda
- store and retrieve data with Amazon DynamoDB
- process asynchronous writes using Amazon SNS and Amazon SQS
- define and deploy infrastructure with AWS SAM and CloudFormation

This project is designed as a step-by-step learning path toward more advanced serverless platform patterns.

## Current Features
- `GET /notes`
- `GET /notes/{id}`
- `POST /notes`

The `POST /notes` flow is asynchronous:
1. API Gateway receives the request
2. Lambda validates and publishes the payload to SNS
3. SNS delivers the message to SQS
4. A worker Lambda consumes the queue message
5. The note is written to DynamoDB

This mirrors the decoupled processing style used in production-grade serverless systems.

## Architecture
```text
GET  /notes        -> API Gateway -> Lambda -> DynamoDB
GET  /notes/{id}   -> API Gateway -> Lambda -> DynamoDB
POST /notes        -> API Gateway -> Lambda -> SNS -> SQS -> Lambda -> DynamoDB
