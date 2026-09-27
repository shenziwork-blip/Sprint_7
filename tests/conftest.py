import pytest
import requests

import helpers
import urls


@pytest.fixture
def new_courier():
    """Создаёт курьера до теста и удаляет после теста."""
    login_pass = helpers.register_new_courier_and_return_login_password()
    yield login_pass

    if login_pass:
        courier_id = helpers.login_courier(login_pass[0], login_pass[1])
        helpers.delete_courier(courier_id)
         