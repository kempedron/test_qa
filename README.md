# Тестовый фреймворк для API студентов

Автотесты на API со студентами (http://194.87.126.16/apidocs). Покрыты операции
создания, чтения, обновления и удаления студентов (GET / POST / PUT / DELETE).

## Что внутри

- `src/api_client.py` — HTTP-клиент на `requests` с логированием запросов и ответов.
- `tests/test_students.py` — автотесты со шагами Allure и прикреплённым логом к каждому тесту.
- `conftest.py` — фикстура клиента и автоматическое прикрепление лога как вложения в Allure-отчёт.

## Как запустить

```bash
pip install -r requirements.txt
pytest
allure serve allure-results
```

`pytest.ini` уже настроен на генерацию результатов в `allure-results` для Allure-отчёта.