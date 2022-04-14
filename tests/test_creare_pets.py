import os, sys
import json
import requests, pytest
from requests_toolbelt.multipart.encoder import MultipartEncoder
from api import PetFriends
from settings import valid_email, valid_password

global list_value
pf = PetFriends()
invalid_key = {"key": "invalid"}
_, valid_key = pf.get_api_key(valid_email, valid_password)


def fool_path(file):
    # Получаем полный путь изображения питомца сохраняем в переменную file и возвращаем
    file = os.path.join(os.path.dirname(__file__), file)
    return file


def generate_string(num):
    return "x" * num


def russian_chars():
    return 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'


def chinese_chars():
    return '的一是不了人我在有他这为之大来以个中上们'


def special_chars():
    return '|\\/!@#$%^&*()-_=+`~?"№;:[]{}'


@pytest.mark.parametrize("name",
        [generate_string(255), generate_string(1001), russian_chars(),
         russian_chars().upper(), chinese_chars(), special_chars(), '123'],
        ids=['255 symbols', 'more than 1000 symbols', 'russian', 'RUSSIAN',
             'chinese', 'specials', 'digit'])
@pytest.mark.parametrize("animal_type",
        [generate_string(255), generate_string(1001), russian_chars(),
         russian_chars().upper(), chinese_chars(), special_chars(), '123'],
        ids=['255 symbols', 'more than 1000 symbols', 'russian', 'RUSSIAN',
             'chinese', 'specials', 'digit'])
@pytest.mark.parametrize("age", ['1'], ids=['min'])
def test_add_new_pet_simple_positive(name, animal_type, age):
# def test_add_new_pet_simple_positive(name="name", animal_type="u-u-u-x", age="1"):
    """Проверяем, что можно добавить питомца с различными данными"""

    # Добавляем питомца
    pytest.status, result = pf.add_new_pet_simple(valid_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert pytest.status == 200
    assert result['name'] == name
    assert result['age'] == age
    assert result['animal_type'] == animal_type


@pytest.mark.parametrize("name", [''], ids=['empty'])
@pytest.mark.parametrize("animal_type", [''], ids=['empty'])
@pytest.mark.parametrize("age",
                         ['', '-1', '0', '100', '1.5', '2147483647', '2147483648', special_chars(),
                          russian_chars(), russian_chars().upper(), chinese_chars()],
                         ids=['empty', 'negative', 'zero', 'greater than max', 'float', 'int_max',
                              'int_max + 1', 'specials', 'russian', 'RUSSIAN', 'chinese'])
def test_add_new_pet_simple_negative(name, animal_type, age):
    # Добавляем питомца
    pytest.status, result = pf.add_new_pet_simple(valid_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert pytest.status == 400


# *****************************************************************************************************
# ************************************ "+" and "-" ****************************************************
def is_age_valid(age):
    # Проверяем, что возраст - это число от 1 до 49 и целое
    return age.isdigit() \
           and 0 < int(age) < 50 \
           and float(age) == int(age)


@pytest.mark.parametrize("name"
    , ['', generate_string(255), generate_string(1001), russian_chars(), russian_chars().upper(), chinese_chars(),
       special_chars(), '123']
    , ids=['empty', '255 symbols', 'more than 1000 symbols', 'russian', 'RUSSIAN', 'chinese', 'specials', 'digit'])
@pytest.mark.parametrize("animal_type"
    , ['', generate_string(255), generate_string(1001), russian_chars(), russian_chars().upper(), chinese_chars(),
       special_chars(), '123']
    , ids=['empty', '255 symbols', 'more than 1000 symbols', 'russian', 'RUSSIAN', 'chinese', 'specials', 'digit'])
@pytest.mark.parametrize("age"
    , ['', '-1', '0', '1', '100', '1.5', '2147483647', '2147483648', special_chars(), russian_chars(),
       russian_chars().upper(), chinese_chars()]
    , ids=['empty', 'negative', 'zero', 'min', 'greater than max', 'float', 'int_max', 'int_max + 1', 'specials',
           'russian', 'RUSSIAN', 'chinese'])
def test_add_new_pet_simple(name, animal_type, age):
    """Проверяем, что можно добавить питомца с различными данными"""

    # Добавляем питомца
    pytest.status, result = pf.add_new_pet_simple(valid_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    if name == '' or animal_type == '' or is_age_valid():
        assert pytest.status == 400
    else:
        assert pytest.status == 200
        assert result['name'] == name
        assert result['age'] == age
        assert result['animal_type'] == animal_type


def test_key(): # контроль валидного ключа
    print("\nkey->", valid_key)
    assert True

