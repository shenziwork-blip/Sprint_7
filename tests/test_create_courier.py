import allure
import pytest
import requests

import data
import helpers
import urls


@allure.epic("API Яндекс Самокат")
@allure.feature("Создание курьера")
class TestCreateCourier:

    @allure.title("Курьера можно создать. Код 201 и тело ok: true")
    def test_create_courier_success(self):
        login = helpers.generate_random_string(10)
        password = helpers.generate_random_string(10)
        first_name = helpers.generate_random_string(10)
        payload = {
            "login": login,
            "password": password,
            "firstName": first_name
        }

        response = requests.post(urls.CREATE_COURIER_URL, data=payload)

        try:
            assert response.status_code == 201
            assert response.json() == {"ok": True}
        finally:
            courier_id = helpers.login_courier(login, password)
            helpers.delete_courier(courier_id)

    @allure.title("Нельзя создать двух одинаковых курьеров")
    def test_cannot_create_two_identical_couriers(self):
        login_pass = helpers.register_new_courier_and_return_login_password()
        assert login_pass, "Не удалось создать первого курьера"

        payload = {
            "login": login_pass[0],
            "password": login_pass[1],
            "firstName": login_pass[2]
        }
        response = requests.post(urls.CREATE_COURIER_URL, data=payload)

        try:
            assert response.status_code == 409
            assert data.COURIER_LOGIN_ALREADY_EXISTS in response.json().get("message", "")
        finally:
            courier_id = helpers.login_courier(login_pass[0], login_pass[1])
            helpers.delete_courier(courier_id)

    @allure.title("Если нет обязательного поля, возвращается ошибка 400")
    @pytest.mark.parametrize(
        "missing_field",
        ["login", "password"]
    )
    def test_create_courier_missing_required_field(self, missing_field):
        payload = {
            "login": helpers.generate_random_string(10),
            "password": helpers.generate_random_string(10),
            "firstName": helpers.generate_random_string(10)
        }
        payload.pop(missing_field)

        response = requests.post(urls.CREATE_COURIER_URL, data=payload)

        assert response.status_code == 400
        assert response.json().get("message") == data.COURIER_CREATE_MISSING_FIELDS
