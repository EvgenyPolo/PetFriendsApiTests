import os

from api import PetFriends
from settings import valid_email, valid_password

global list_value


def fp(file):
    # Получаем полный путь изображения питомца сохраняем в переменную file и возвращаем
    file = os.path.join(os.path.dirname(__file__), file)
    return file


class TestPetFriends:
    def setup(self):
        self.pf = PetFriends()
        # Назначаем невалидный ключ api
        self.invalid_key = {"key": "invalid"}
        # Запрашиваем валидный ключ
        try:
            status, auth_key = self.pf.get_api_key(valid_email, valid_password)
            if status == 200:
                self.valid_key = auth_key
            else:
                raise Exception(f"Ошибка получения API ключа. Статус: {status}")
        except Exception as e:
            print("Error:", e)
        global list_value
        list_value = []

    def l_values(self):
        # Функция возвращает объединенный список значений всех своих питомцев
        try:
            # Запрашиваем список своих питомцев
            res = self.pf.get_list_of_pets(self.valid_key, "my_pets")
            if res.status_code == 200:
                if len(res.json()['pets']) > 0:
                    # Если они есть, возвращаем ответ сервера и объединенный список значений
                    # так как в my_pets.values() id питомца не находится при сравнении
                    for item in res.json()['pets']:
                        # Соберем все значения списка словарей в один список list_value
                        list_value.extend(list(item.values()))
                    return list_value
                else:
                    return ["пусто"]
            else:
                raise Exception(f"Ошибка получения списка своих питомцев. Статус: {res.status_code}")
        except Exception as e:
            print("\nError:", e)

    def pet_id_0(self):
        # Запрашиваем список своих питомцев
        try:
            res = self.pf.get_list_of_pets(self.valid_key, "my_pets")
            # status, my_pets = self.pf.get_list_of_pets(self.valid_key, "my_pets")
            if res.status_code == 200:
                if len(res.json()['pets']) > 0:
                    # Если они есть, возвращаем id первого питомца
                    return res.json()['pets'][0]['id']
                else:
                    # Если список пуст, добавляем питомца и возвращаем его id.
                    status, result = self.pf.add_new_pet_simple(self.valid_key, "Первенец", "зверь", "1")
                    if status == 200:
                        print(" : Пришлось создать питомца!")
                        return result['id']
                    # Поднимаем ошибку, если не удалось создать питомца
                    raise Exception("Не удалось создать питомца. Список своих питомцев пуст")
            else:
                raise Exception(f"Ошибка получения списка своих питомцев. Статус: {res.status_code}")
        except Exception as e:
            print("\nError:", e)
            return ""

    def test_successful_get_api_key_for_valid_user(self, email=valid_email, password=valid_password):
        """ Проверяем что запрос api ключа возвращает статус 200 и в результате содержится слово key"""

        # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
        status, result = self.pf.get_api_key(email, password)

        # Сверяем полученные данные с нашими ожиданиями
        assert status == 200
        assert 'key' in result

    def test_failed_get_api_key_for_not_valid_email(self, email="invalid_email", password="invalid_password"):
        """ Проверяем что запрос api ключа возвращает статус не 200
                            и в результате не содержится слово key"""

        # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
        status, result = self.pf.get_api_key(email, password)

        # Сверяем полученные данные с нашими ожиданиями
        assert status != 200
        assert 'key' not in result

    def test_failed_get_api_key_for_valid_user_not_valid_pass(self, email=valid_email, password="off"):
        """ Проверяем что запрос api ключа не возвращает статус 200 и в результате не содержится слово key"""

        # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
        status, result = self.pf.get_api_key(email, password)

        # Сверяем полученные данные с нашими ожиданиями
        assert status != 200
        assert 'key' not in result

    def test_successful_get_all_pets_with_valid_key(self, pet_filter=''):
        """ Проверяем что запрос всех питомцев возвращает не пустой список.
        Для этого получаем валидный api ключ self.api_key(True), запрашиваем список
        всех питомцев filter='' и проверяем что status = 200 и список не пустой."""

        res = self.pf.get_list_of_pets(self.valid_key, pet_filter)

        assert res.status_code == 200
        assert len(res.json()['pets']) > 0

    def test_failed_get_all_pets_with_not_valid_key(self, pet_filter=''):
        """ Проверяем что запрос всех питомцев с невалидным ключом не возвращает код 200.
        Используя этот ключ, запрашиваем список всех питомцев и проверяем что result не
        содержит 'pets' """

        # res = self.pf.get_list_of_pets(self.valid_key, pet_filter)
        res = self.pf.get_list_of_pets(self.invalid_key, pet_filter)

        assert res.status_code == 403
        assert 'pets' not in res.text

    def test_successful_add_new_pet_with_valid_data(self, name='Котейка', animal_type='котяра',
                                                    age='5', pet_photo='images/cat1.jpg'):
        """Проверяем что можно добавить питомца с корректными данными"""

        # Добавляем питомца
        status, result = self.pf.add_new_pet(self.valid_key, name, animal_type, age, fp(pet_photo))

        # Сверяем полученный ответ с ожидаемым результатом
        assert status == 200
        assert result['name'] == name and result['animal_type'] == animal_type

    def test_add_new_pet_with_null_data(self, name='', animal_type='',
                                        age='', pet_photo='images/cat1.jpg'):
        """Проверяем что можно добавить питомца с пустыми данными и существующем фото"""

        # Добавляем питомца
        status, result = self.pf.add_new_pet(self.valid_key, name, animal_type, age, fp(pet_photo))

        # Сверяем полученный ответ с ожидаемым результатом
        assert status == 200
        assert result['name'] == name and result['animal_type'] == animal_type

    def test_add_new_pet_with_spec_data(self, pet_photo='images/cat1.jpg'):
        """Проверяем что можно добавить питомца с длинными данными из цифр и спецсимволов"""
        name = """7867697)&*&(*^&*^098-078*^97097*(709809&987097)79079*&897987*(&897987(*7987987(*798789&8979879*&987 
        98789&987987*(&987987*(&98789798&987987(*&987987*(7987987(*7987897Котейка"""
        animal_type = '''54^&674764&^576467$&^%4765^&%&^%&^576576576%^&%76%&^5876(*^&(*&08)(*_)(-098_)(_)9-09_)(-09-08) 
        (&*(^&*%76465$&^568769876&5563$@54476*(0-9_)(*097896&*%764576897*(687576$^котяра'''
        age = '''&^&^76786&68768^&(*7896^%654567656767867*(7987*(&687576534$%243254#654766578^897986&^%654653543^%476587 
        6(*^87576$653543543^%%$8768976(*'''
        # Добавляем питомца
        status, result = self.pf.add_new_pet(self.valid_key, name, animal_type, age, fp(pet_photo))

        # Сверяем полученный ответ с ожидаемым результатом
        assert status == 200
        assert result['name'] == name and result['animal_type'] == animal_type

    def test_failed_add_new_pet_with_valid_data_and_invalid_key(self, name='Котейка', animal_type='котяра',
                                                                age='5', pet_photo='images/cat1.jpg'):
        """Проверяем что невозможно добавить питомца с корректными данными и невалидным ключом"""

        # Добавляем питомца
        status, result = self.pf.add_new_pet(self.invalid_key, name, animal_type, age, fp(pet_photo))

        # Сверяем полученный ответ с ожидаемым результатом
        assert status != 200

    def test_failed_add_new_pet_without_name(self, animal_type='котяра',
                                             age='5', pet_photo='images/cat1.jpg'):
        """Проверяем что невозможно добавить питомца без параметра name и валидным ключом"""

        # Добавляем питомца
        try:
            status, result = self.pf.add_new_pet(self.valid_key, animal_type, age, fp(pet_photo))
        except TypeError as e:
            print("\n" + str(e))
            status = 400

        # Сверяем полученный ответ с ожидаемым результатом
        assert status != 200

    def test_failed_add_new_pet_without_animal_type(self, name='Котейка',
                                                    age='5', pet_photo='images/cat1.jpg'):
        """Проверяем что невозможно добавить питомца без параметра animal_type и валидным ключом"""

        # Добавляем питомца
        try:
            status, result = self.pf.add_new_pet(self.valid_key, name, age, fp(pet_photo))
        except TypeError as e:
            print("\n" + str(e))
            status = 400

        # Сверяем полученный ответ с ожидаемым результатом
        assert status != 200

    def test_failed_add_new_pet_without_age(self, name='Котейка', animal_type='котяра',
                                            pet_photo='images/cat1.jpg'):
        """Проверяем что невозможно добавить питомца без параметра age и валидным ключом"""

        # Добавляем питомца
        try:
            status, result = self.pf.add_new_pet(self.valid_key, name, animal_type, fp(pet_photo))
        except TypeError as e:
            print("\n" + str(e))
            status = 400

        # Сверяем полученный ответ с ожидаемым результатом
        assert status != 200

    def test_successful_add_new_pet_simple_with_valid_data(self, name='Барбос', animal_type='двор', age='5'):
        """Проверяем что можно добавить питомца с корректными данными без фото"""

        # Добавляем питомца
        status, result = self.pf.add_new_pet_simple(self.valid_key, name, animal_type, age)

        # Сверяем полученный ответ с ожидаемым результатом
        assert status == 200
        assert result['name'] == name and result['animal_type'] == animal_type

    def test_failed_add_new_pet_simple_with_valid_data_and_invalid_key(self, name='Барбоскин',
                                                                       animal_type='двортерьер', age='5'):
        """Проверяем что невозможно добавить питомца с корректными данными без фото и невалидным ключом"""

        # Добавляем питомца
        status, result = self.pf.add_new_pet_simple(self.invalid_key, name, animal_type, age)

        # Сверяем полученный ответ с ожидаемым результатом
        assert status != 200

    def test_successful_update_self_pet_info(self, name='Мурзик', animal_type='Котяра', age=7):
        """Проверяем возможность обновления информации о питомце"""

        status, result = self.pf.update_pet_info(self.valid_key, self.pet_id_0(), name, animal_type, age)

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name and result['animal_type'] == animal_type

    def test_successful_add_photo_pet(self, pet_photo='images/cat1.jpg'):
        """Проверяем возможность обновления фото питомца"""

        status, result = self.pf.add_pet_photo(self.valid_key, self.pet_id_0(), fp(pet_photo))

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert "image" in result['pet_photo']

    def test_failed_add_photo_pet_with_invalid_key(self, pet_photo='images/cat1.jpg'):
        """Проверяем невозможность обновления фото питомца с невалидным ключом"""

        status, result = self.pf.add_pet_photo(self.invalid_key, self.pet_id_0(), fp(pet_photo))

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status != 200

    def test_failed_add_photo_pet_with_valid_key_with_without_file(self, pet_photo='images/cat2.jpg'):
        """Проверяем невозможность обновления фото питомца с отсутствующим файлом фото"""

        try:
            status, result = self.pf.add_pet_photo(self.valid_key, self.pet_id_0(), pet_photo)
        except FileNotFoundError as e:
            print("\n" + str(e))
            status = 2

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status != 200

    def test_failed_add_photo_pet_with_valid_key_without_file(self):
        """Проверяем невозможность обновления фото питомца не передавая в параметрах сам файл"""

        try:
            status, result = self.pf.add_pet_photo(self.valid_key, self.pet_id_0())
        except TypeError as e:
            print("\nError: " + str(e))
            status = 2

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status != 200

    def test_successful_delete_self_pet(self):
        """Проверяем возможность удаления питомца"""

        # Получаем id первого питомца
        pet_id = self.pet_id_0()
        # Удаляем его
        status, _ = self.pf.delete_pet(self.valid_key, pet_id)

        # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
        assert status == 200
        # Запрашиваем объединенный список значений self.l_values() для своих питомцев и убеждаемся,
        # что в списке нет id питомца, которого удалили
        assert pet_id not in self.l_values()

    def test_failed_delete_self_pet_with_invalid_key(self):
        """Проверяем возможность удаления питомца с невалидным API ключом"""

        # Получаем id своего первого питомца
        pet_id = self.pet_id_0()

        # Пробуем удалить его, используя невалидный ключ
        status, _ = self.pf.delete_pet(self.invalid_key, pet_id)

        # Проверяем что статус ответа не равен 200
        assert status != 200
        # Запрашиваем объединенный список значений self.l_values() для своих питомцев и убеждаемся,
        # что в списке есть id питомца, которого пытались удалить
        assert pet_id in self.l_values()

    def test_cleaner_test_pets(self):
        """Зачищаем после тестирования"""
        try:
            # Запрашиваем список своих питомцев
            res = self.pf.get_list_of_pets(self.valid_key, "my_pets")
            if res.status_code == 200:
                if len(res.json()['pets']) > 0:
                    # Если они есть, то удаляем
                    for item in res.json()['pets']:
                        status, _ = self.pf.delete_pet(self.valid_key, item.get('id'))
                        assert status == 200
                    return ["пусто"]
                else:
                    return ["пусто"]
            else:
                raise Exception(f"Ошибка получения списка своих питомцев. Статус: {res.status_code}")
        except Exception as e:
            print("\nError:", e)

         # Проверяем что статус ответа равен 200
        assert status == 200

