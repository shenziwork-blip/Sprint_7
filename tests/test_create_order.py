import allure
import pytest
import requests

import data
import urls


@allure.epic("API Яндекс Самокат")
@allure.feature("Создание заказа")
class TestCreateOrder:

    @allure.title("Можно создать заказ с разным набором цветов, в ответе есть track")
    @pytest.mark.parametrize("color", data.ORDER_COLORS)
    def test_create_order_with_different_colors_returns_track(self, color):
        payload = data.ORDER_BODY.copy()
        payload["color"] = color

        response = requests.post(urls.CREATE_ORDER_URL, json=payload)

        assert response.status_code == 201
        assert "track" in response.json()
        assert isinstance(response.json()["track"], int)
         