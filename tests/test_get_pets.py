# import os, sys
import json
import pytest
# from requests_toolbelt.multipart.encoder import MultipartEncoder
from api import PetFriends
from settings import valid_email, valid_password

pf = PetFriends()
invalid_key = {"key": "invalid"}
_, valid_key = pf.get_api_key(valid_email, valid_password)


def generate_string(num):
    return "x" * num


def russian_chars():
    return 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'


def chinese_chars():
    return '的一是不了人我在有他这为之大来以个中上们'


def special_chars():
    return '|\\/!@#$%^&*()-_=+`~?"№;:[]{}'


def processing(res):
    try:
        result = res.json()
    except json.decoder.JSONDecodeError:
        result = res.text
    return res.status_code, res.headers.get('Content-Type'), result


def test_get_api_key_for_valid_user():
    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а ключ в pytest.key
    status, pytest.key = pf.get_api_key(valid_email, valid_password)

    # """ Проверяем, что запрос api-ключа возвращает статус 200 и в результате содержится слово key"""
    assert status == 200
    assert 'key' in pytest.key


@pytest.mark.parametrize("email", ["xxx@yyy.zz",
                                   generate_string(255), generate_string(1001), russian_chars(),
                                   russian_chars().upper(), chinese_chars(), special_chars(), 123],
                         ids=["xxx@yyy.zz", '255 symbols', 'more than 1000 symbols', 'russian',
                              'RUSSIAN', 'chinese', 'specials', 'digit'])
@pytest.mark.parametrize("password",
                         [generate_string(255), generate_string(1001), russian_chars(),
                          russian_chars().upper(), chinese_chars(), special_chars(), 123],
                         ids=['255 symbols', 'more than 1000 symbols', 'russian',
                              'RUSSIAN', 'chinese', 'specials', 'digit'])
def test_get_api_key_negative_user(email, password):
    try:
        # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status
        status, _ = pf.get_api_key(email, password)
    except Exception as e:
        print("\nError:" + str(e))
        status = 403

    # """ Проверяем, что запрос api-ключа возвращает статус 403 """
    assert status == 403


@pytest.mark.parametrize("pet_filter", ['', 'my_pets'], ids=['empty string', 'only my pets'])
@pytest.mark.parametrize("accept_content_type", ["application/json; indent=4", 'application/xml'], ids=['json', 'xml'])
def test_get_pets_with_positive_filter(pet_filter, accept_content_type, time_delta):
    # Отправляем запрос и обрабатываем полученный ответ
    status, content_type, result = processing(pf.get_list_of_pets(valid_key, pet_filter, accept_content_type))

    # Проверяем полученные результаты
    assert status == 200
    assert content_type == accept_content_type[0:16]
    if pet_filter == 'my_pets':
        assert len(result['pets']) >= 0
    else:
        assert len(result['pets']) > 0


@pytest.mark.parametrize("pet_filter",
                         [generate_string(255), generate_string(1001), russian_chars(),
                          russian_chars().upper(), chinese_chars(), special_chars(), 123],
                         ids=['255 symbols', 'more than 1000 symbols', 'russian',
                              'RUSSIAN', 'chinese', 'specials', 'digit'])
def test_get_pets_with_negative_filter(pet_filter):
    res = pf.get_list_of_pets(valid_key, pet_filter, "application/json; indent=4")

    # Проверяем статус ответа
    assert res.status_code == 403


@pytest.mark.parametrize("pet_filter", ['', 'my_pets'], ids=['empty string', 'only my pets'])
@pytest.mark.parametrize("key",
                         [invalid_key, {"key": generate_string(255)}, {"key": generate_string(1001)},
                          {"key": russian_chars()},
                          {"key": russian_chars().upper()}, {"key": chinese_chars()}, {"key": special_chars()},
                          {"key": 123}],
                         ids=['invalid key', '255 symbols', 'more than 1000 symbols', 'russian',
                              'RUSSIAN', 'chinese', 'specials', 'digit'])
def test_get_pets_with_negative_API_key(pet_filter, key):
    try:
        # Отправляем запрос и сохраняем полученный ответ в res
        res = pf.get_list_of_pets(key, pet_filter, "application/json; indent=4")
        status = res.status_code
    except Exception as e:
        print("\nError:" + str(e))
        status = 403

    # Проверяем статус ответа
    assert status == 403
