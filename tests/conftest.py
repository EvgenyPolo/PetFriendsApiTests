import requests, pytest, datetime, sys
from settings import valid_email, valid_password


# from requests_toolbelt.multipart.encoder import MultipartEncoder


@pytest.fixture()
def time_delta():
    start_time = datetime.datetime.now()
    print(f"\nВремя старта: {start_time}")
    yield
    end_time = datetime.datetime.now()
    print(f"\nВремя финиша: {end_time}")
    print(f"\nТест шел: {end_time - start_time}")


# @pytest.fixture(scope="class", autouse=True)
@pytest.fixture()
def get_key(time_delta):
    # переменные email и password нужно заменить своими учетными данными
    response = requests.post(url='https://petfriends1.herokuapp.com/login',
                             data={"email": valid_email, "pass": valid_password})
    assert response.status_code == 200, 'Запрос выполнен неуспешно'
    assert 'Cookie' in response.request.headers, 'В запросе не передан ключ авторизации'
    print("\nreturn auth_key")
    return response.request.headers.get('Cookie')


# @pytest.fixture(scope="function", autouse=True)
@pytest.fixture()
def request_fixture(request):
    print(request.fixturename)
    print(request.scope)
    print(request.function.__name__)
    print(request.cls)
    print(request.module.__name__)
    print(request.fspath)
    if request.cls:
        return f"\n У теста {request.function.__name__} класс есть\n"
    else:
        return f"\n У теста {request.function.__name__} класса нет\n"


@pytest.fixture(autouse=True)
def request_fixture_1(request):
    if 'Pets' in request.function.__name__:
        print(f"\nЗапущен тест из сьюта Дом Питомца: {request.function.__name__}")


minversion = pytest.mark.skipif(sys.version_info < (3, 6), reason="at least mymodule-1.1 required")


@pytest.fixture(scope="function", params=[
    ("Короткая строка", "Короткая строка"),
    ('Длинная строка, не то чтобы прям очень длинная, но достаточно для нашего теста, и в ней нет названия языка',
     "Длинная строка, не то чтобы прям очень длинная, но"),
    ("Короткая строка со словом python", "Короткая строка со словом python"),
    ("Длинная строка, нам достаточно будет для проверки, и в ней есть слово python",
     "Длинная строка, нам достаточно будет для проверки, и в ней есть слово python"),
], ids=["len < 50", "len > 50", "len < 50 contains python", "len > 50 contains python"])
def param_fun(request):
    return request.param


def generate_id(val):
    ids = "params: " + str(val[1])
    print("!!!*****!!!", ids)
    return "Params: "
    # return "params: {0}".format(str(val))


@pytest.fixture(scope="function", params=[
    ("Short line", "Short line"),
    ("Длинная строка, не то чтобы прям очень длинная, но достаточно для нашего теста, и в ней нет названия языка",
     "Длинная строка, не то чтобы прям очень длинная, но"),
    ("Короткая строка со словом python", "Короткая строка со словом python"),
    ("Длинная строка, нам достаточно будет для проверки, и в ней есть слово python",
     "Длинная строка, нам достаточно будет для проверки, и в ней есть слово python"),
], ids=generate_id)
def param_fun_generated(request):
    print(f"\n{request.param[1]}")
    return request.param


@minversion
def test_python36_and_greater():
    print("Версия Python меньше 3,7")


@pytest.mark.api
@pytest.mark.auth
def test_auth_api():
    pass


@pytest.mark.ui
@pytest.mark.auth
def test_auth_ui():
    pass


@pytest.mark.api
@pytest.mark.event
def test_event_api():
    pass


@pytest.mark.ui
@pytest.mark.event
def test_event_ui():
    pass
