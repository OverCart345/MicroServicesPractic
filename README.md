# Проект: Микросервисное финансовое приложение

## Описание

Это пример микросервисного приложения для управления пользователями, учёта транзакций и формирования отчётов.

Компоненты:
- **User Service** – регистрация, авторизация, профиль.
- **Transaction Service** – добавление и получение транзакций.
- **Report Service** – генерация и экспорт отчётов.
- **CLI** – клиентское приложение для взаимодействия с сервисами.
- **Интеграционные тесты** – проверка всего потока и замеры производительности.

Коммуникация между сервисами:
- Основной протокол: gRPC + Protocol Buffers.
- Альтернативный: HTTP/1.1 + MessagePack (в Transaction Service доступен HTTP+MessagePack интерфейс).

## Структура репозитория

```
second/
├── user_service/
│   ├── proto/                # .proto + сгенерированные *_pb2.py
│   └── user_service.py       # реализация gRPC-сервера
├── transaction_service/
│   ├── proto/
│   └── transaction_service.py# gRPC + HTTP/MessagePack
├── report_service/
│   ├── proto/
│   └── report_service.py     # gRPC-сервер, собирает данные из Transaction Service
├── client/
│   └── cli.py                # CLI на Click для всех операций
├── tests/
│   └── integration_test.py   # интеграционные тесты и бенчмарки
├── requirements.txt          # список зависимостей
├── .gitignore                # игнорируем .venv, *.db, *.pyc и т.п.
└── README.md                 # этот файл
```

## Быстрый старт

### 1. Клонировать репозиторий
```bash
git clone <repo-url>
cd second
```

### 2. Создать и активировать виртуальное окружение
```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux/macOS:
source .venv/bin/activate
```

### 3. Установить зависимости
```bash
pip install -r requirements.txt
```

### 4. Сгенерировать Python-код из .proto (при необходимости)
```bash
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. user_service/proto/user.proto
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. transaction_service/proto/transaction.proto
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. report_service/proto/report.proto
```

### 5. Запустить сервисы в отдельных терминалах
```bash
# User Service
dd user_service && python -m user_service.user_service
# Transaction Service
dd transaction_service && python transaction_service.py
# Report Service
dd report_service && python -m report_service.report_service
```

### 6. Использовать CLI
```bash
cd client
python cli.py register   # регистрация
python cli.py login      # авторизация
python cli.py profile    # получить профиль
python cli.py add-tx     # добавить транзакцию
python cli.py list-tx    # список транзакций
python cli.py gen-report # сформировать отчёт
python cli.py get-report # получить отчёт
```

### 7. Интеграционные тесты
```bash
cd tests
python integration_test.py
```

## Конфигурация

Переменные окружения (по умолчанию):
- `SECRET_KEY` – ключ для подписи JWT (`secret`).
- `USER_GRPC_URL`, `TRANSACTION_GRPC_URL`, `REPORT_GRPC_URL` – адреса gRPC-сервисов.
- `TRANSACTION_HTTP_URL` – базовый URL для HTTP+MessagePack Transaction Service.

## Результаты тестирования

- **Корректность**: регистрация, транзакции и отчёты работают без ошибок.
- **Производительность**: gRPC~14.9 s vs HTTP+MessagePack~18.4 s (100 транзакций)