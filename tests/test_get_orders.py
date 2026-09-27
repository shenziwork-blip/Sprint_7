import allure
import requests

import urls


@allure.epic("API Яндекс Самокат")
@allure.feature("Список заказов")
class TestGetOrders:

    @allure.title("В теле ответа возвращается список заказов")
    def test_get_orders_returns_orders_list(self):
        response = requests.get(urls.GET_ORDERS_URL)

        assert response.status_code == 200
        body = response.json()
        assert "orders" in body
        assert isinstance(body["orders"], list)
         