# Python boto3 basics

## Что такое boto3

boto3 - это Python SDK для работы с AWS-сервесами.

## Зачем это нужно в Cloud Security

Cloud Security Engineer часто автоматизирует проверки:

- получить спиоск ресурсов
- проверить настройки
- найти misconfiguration
- сформировать fingings
- создать отчёт

## LocalStack endpooint

В этом lab boto3  подключается не к реальному AWS, а к LocalStack:

```text
http://localhost.localstack.cloud:4566
```

### First automated security check

I wrote a Python script that checks S3 bucket policies and detects public read access.

The script checks the following policy fields:

- `Effect: Allow`
- `Principal: "*"`
- `Action: "s3:GetObject"`

If all three conditions are true, the bucket is reported as a HIGH severity finding.

## Handling different Action formats

Aws polic `Action` can be represented as a string:

```json
"Action": "s3:GetObject"
```

or as list:

```json
"Action": ["s3:GetObject", "s3:ListBucket"]
```

The function `has_get_object()` handles both cases and return `True` when `s3:GetObject` is allowed.

