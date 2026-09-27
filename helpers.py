import random
import string
import requests

import urls


def generate_random_string(length):
    letters = string.ascii_lowercase
    return "".join(random.choice(letters) for _ in range(length))


def register_new_courier_and_return_login_password():
    """Регистрирует нового курьера. Возвращает [login, password, firstName] или []."""
    login_pass = []

    login = generate_random_string(10)
    password = generate_random_string(10)
    first_name = generate_random_string(10)

    payload = {
        "login": login,
        "password": password,
        "firstName": first_name
    }

    response = requests.post(urls.CREATE_COURIER_URL, data=payload)

    if response.status_code == 201:
        login_pass.append(login)
        login_pass.append(password)
        login_pass.append(first_name)

    return login_pass


def login_courier(login, password):
    """Логинит курьера и возвращает его id. Если не вышло — None."""
    response = requests.post(
        urls.LOGIN_COURIER_URL,
        data={"login": login, "password": password}
    )
    if response.status_code == 200:
        return response.json().get("id")
    return None


def delete_courier(courier_id):
    """Удаляет курьера по id. Нужно, чтобы тесты не оставляли мусор."""
    if not courier_id:
        return None
    return requests.delete(f"{urls.DELETE_COURIER_URL}/{courier_id}")
 