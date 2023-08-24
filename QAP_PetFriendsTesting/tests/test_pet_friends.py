from api import PetFriends
from settings import valid_email, valid_password, unvalid_email, unvalid_password, invalid_auth_key
import os

pf = PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """Получить уникальный ключ по валидным данным пользователя """
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result
    print(result)


def test_get_api_key_for_unvalid_email(email=unvalid_email, password=valid_password):
    """Получить уникальный ключ c невалидной почтой"""
    status, result = pf.get_api_key(email, password)
    assert status == 403


def test_get_api_key_for_unvalid_pass(email=valid_email, password=unvalid_password):
    """Получить уникальный ключ с невалидным паролем"""
    status, result = pf.get_api_key(email, password)
    assert status == 403


def test_get_all_pets_with_valid_key(filter=''):
    """ Получить не пустой список всех питомцев. Для этого получить ключ."""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0
    print(auth_key)


def test_get_all_pets_with_invalid_key(filter=''):
    """ Получить не пустой список всех питомцев. Для этого получить ключ."""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets_incorrect_auth_key(auth_key, filter)
    assert status == 403


def test_add_new_pet_simple(name='Murzik', animal_type='iork', age='7'):
    """Добавить питомца с корректными данными"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_simple(auth_key, name, animal_type, age)
    assert status == 200
    assert result['name'] == name


def test_add_new_pet_simple_incorrect_auth_key(name='Murzik', animal_type='iork', age='7'):
    """Добавить питомца с некорректным ключем."""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_simple_unsuccessfully(auth_key, name, animal_type, age)
    assert status == 403


def test_add_new_pet_simple_long_name(name='ЗLСOFjpYШоWЭrмAЯKВmWBцMJцzGтшPqшnDЙDзФГгиМCeпСghGёcTЕЪYHяёдУжЩЙжМdиЛGbГQfшIUГjWлMnЯCЗлЫЬcuюSЯкrхJЖSfsjХЦXЛКIТЗъGLЯУdFХрОЖШоИVвТvBtШvУАKЫюЛWOeЖzЮГзRnyТВжcЫзеQiEpoтwUVхвГaиABдиCУULйrюЖoгСзЫZlgтVёIrHлкIITctHzШЖоМqмЫCЧяGтбсхBБЭёwkфVoKЙkщЮsУdЁэvмеHЖЬTTXбJvЭCLD5', animal_type='iork', age='7'):
    """Добавить питомца. Name - 256 символов. Сейчас баг - имя принимается!"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_simple(auth_key, name, animal_type, age)
    assert status == 400


def test_add_new_pet_simple_long_animal_type(name='Murzik', animal_type='ЗLСOFjpYШоWЭrмAЯKВmWBцMJцzGтшPqшnDЙDзФГгиМCeпСghGёcTЕЪYHяёдУжЩЙжМdиЛGbГQfшIUГjWлMnЯCЗлЫЬcuюSЯкrхJЖSfsjХЦXЛКIТЗъGLЯУdFХрОЖШоИVвТvBtШvУАKЫюЛWOeЖzЮГзRnyТВжcЫзеQiEpoтwUVхвГaиABдиCУULйrюЖoгСзЫZlgтVёIrHлкIITctHzШЖоМqмЫCЧяGтбсхBБЭёwkфVoKЙkщЮsУdЁэvмеHЖЬTTXбJvЭCLD', age='7'):
    """Добавить питомца. animal_type - 256 символов. Сейчас баг - количество символов принимается!"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_simple(auth_key, name, animal_type, age)
    assert status == 400


def test_add_photo(pet_photo='images/71.jpg'):
    """Добавить фото к имеющемуся питомцу."""
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        status, result = pf.add_photo(auth_key, my_pets['pets'][0]['id'], pet_photo)
        assert status == 200
        assert result['pet_photo'] != ''

    else:
        raise Exception


def test_add_photo_invalid_format(pet_photo='images/png-york.png'):
    """Добавить фото в невалидном формате(не jpg). По документации ожидается код 400, сейчас приходит код 500"""
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        status, result = pf.add_photo_png(auth_key, my_pets['pets'][0]['id'], pet_photo)
        assert status == 400
    else:
        raise Exception


def test_successful_update_self_pet_info(name='Мурзик', animal_type='Кот', age=5):
    """Добавить информацию о питомце"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
        assert status == 200
        assert result['name'] == name
    else:
        raise Exception("There is no my pets")


def test_update_self_pet_info_age_symbols(name='', animal_type='', age='cTЕЪYHяёдУжЩЙжМdиЛGbГQfшIU'):
    """Поле "возраст" - ввести символы. Ожидается 400, сейчас баг - поле принимает значения."""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info_incorrect(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
        assert status == 400
    else:
        raise Exception("There is no my pets")


def test_update_self_pet_negative_age(name='', animal_type='', age=-5):
    """Добавить отрицательное значение возраста у питомца. Сейчас баг, значение добавляется!"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
        assert status == 400
    else:
        raise Exception("There is no my pets")


def test_update_self_pet_long_age(name='', animal_type='', age=3453453487876507839854678546789347968719353148958463487671309437468578674985678497272722987645346589435673465413781675731569563476762182889213450475634781657806187346817363774675630430478813674657647568474444444444413680745613780456183746504387563874379065):
    """Добавить 256 цифр для строки возраст. Сейчас баг, количество принимается!"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
        assert status == 400
    else:
        raise Exception("There is no my pets")


def test_successful_delete_self_pet():
    """Удалить питомца"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    if len(my_pets['pets']) == 0:
        pf.add_new_pet_simple(auth_key, "Murzik", "iork", "7")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    assert status == 200
    assert pet_id not in my_pets.values()
