# S3 Basics

## Что я сделал

- Создал S3 bucket `company-public-files`
- Загрузил файл `test-file.txt`
- Посмотрел содержимое bucket
- Скачал файл обратно

## Что такое bucket

Bucket - это контейнер для хранения объектов в S3

## Что такое object

Object - это файл или данные, хранящиеся внутри bucket

## Почему S3 важен для Cloud Security

S3 часто используют для хранения логов, документов, бэкапов и других данных. Если bucket настроен неправильно эти данные могут стать доступными злоумышленнику.

## Разделение bucket по назаначению

Я создал два bucket:

- `company-public-files` - для условных файлов компании 
- `internal-security-logs` - для внутренних security logs

С точки зрения Cloud Security важно понимать назнаени bucket, потому что разные данные требуют разного уровня защиты.

Security logs должны быть приватными, потому что они могут содержать информацию о пользователях, IP-адресах, действиях администраторов и событиях безопастности.

## Bucket policy

Bucket policy - это JSON-документ, который управляет доступ к bucket и объектам внутри него.

С помощью bucket policy можно разрешить или запретить действия:

- чтение объектов
- загрузку объектов 
- удаление объектов
- доступ для конкретных пользователей
- доступ для всех пользователей

Если bucket policy разрешает доступ Principal `"*"`, это может означать публичный доступ.


## Public bucket policy

Я настроил bucket policy для `company-public-files`, которая разрешает публичное чтение объектов.

Ключевые элементы policy:

- `Effect: Allow` - разрешить действие
- `Principal: "*"` - разрешить всем
- `Action: s3:GetObject` - разрешить чтение оьъектов
- `Resource: arn:aws:s3:::company-public-files/*` - применить ко всем объектам внутри bucket

С точки зрения Cloud Security `Principal: "*"` вместе с `s3:GetObject` может означать публичный доступ к данным.

Для bucket `internal-security-logs` публичная policy не настроенна, потому что security logs должны быть приватными


```markdown
## Security finding

`company-public-files` has public read access because its bucket policy allows:

- `Principal: "*"`
- `Action: "s3:GetObject"`
- `Resource: "arn:aws:s3:::company-public-files/*"`

Severity: HIGH

Recommendation: remove public access unless it is explicitly required.
```