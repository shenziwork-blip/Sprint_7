import allure
import pytest
import requests

import data
import urls


@allure.epic("API Яндекс Самокат")
@allure.feature("Логин курьера")
class TestLoginCourier:

    @allure.title("Курьер может авторизоваться. В ответе есть id")
    def test_courier_can_login_and_response_contains_id(self, new_courier):
        login, password, _ = new_courier
        response = requests.post(
            urls.LOGIN_COURIER_URL,
            data={"login": login, "password": password}
        )

        assert response.status_code == 200
        assert "id" in response.json()
        assert isinstance(response.json()["id"], int)

    @allure.title("Для авторизации нужны все обязательные поля")
    @pytest.mark.parametrize("missing_field", ["login", "password"])
    def test_login_missing_required_field(self, new_courier, missing_field):
        login, password, _ = new_courier
        payload = {"login": login, "password": password}
        payload[missing_field] = ""

        response = requests.post(urls.LOGIN_COURIER_URL, data=payload)

        assert response.status_code == 400
        assert response.json().get("message") == data.COURIER_LOGIN_MISSING_FIELDS

    @allure.title("Ошибка, если логин или пароль неверные")
    @pytest.mark.parametrize(
        "wrong_login, wrong_password",
        [
            (True, False),
            (False, True),
        ]
    )
    def test_login_wrong_login_or_password(self, new_courier, wrong_login, wrong_password):
        login, password, _ = new_courier
        payload = {
            "login": "wrong_login_value" if wrong_login else login,
            "password": "wrong_password_value" if wrong_password else password
        }

        response = requests.post(urls.LOGIN_COURIER_URL, data=payload)

        assert response.status_code == 404
        assert response.json().get("message") == data.COURIER_ACCOUNT_NOT_FOUND

    @allure.title("Ошибка при авторизации под несуществующим пользователем")
    def test_login_nonexistent_user(self):
        response = requests.post(
            urls.LOGIN_COURIER_URL,
            data={"login": "no_such_courier_zzz", "password": "no_such_password_zzz"}
        )

        assert response.status_code == 404
        assert response.json().get("message") == data.COURIER_ACCOUNT_NOT_FOUND
