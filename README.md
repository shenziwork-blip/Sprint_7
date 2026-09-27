# Sprint_7. Тестирование API Яндекс Самокат

Автотесты REST API учебного сервиса:
https://qa-scooter.education-services.ru/

Документация:
https://qa-scooter.education-services.ru/docs/

## Что покрыто
- создание курьера
- логин курьера
- создание заказа с разным набором цветов
- получение списка заказов

## Стек
- Python
- pytest
- requests
- allure-pytest

## Запуск
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest tests -v
