import json

from django.contrib.auth.models import Group, User

from budgets.models import MoneyFlow

def load_json_file(json_path: str) -> list[dict]:
    ret = None
    with open(json_path, 'r', encoding='utf-8') as file:
        ret = json.load(file)
    return ret


def create_users_from_json(json_path: str):
    json_users = load_json_file(json_path)

    for dict_user in json_users:
        group = dict_user["groups"]
        del dict_user["groups"]
        
        obj, _ = User.objects.using('primary').get_or_create(**dict_user)
        group, _ = Group.objects.using('primary').get_or_create(name=group)
        obj.groups.add(group)
        obj, _ = User.objects.using('replica').get_or_create(**dict_user)
        group, _ = Group.objects.using('replica').get_or_create(name=group.name)
        obj.groups.add(group)


def add_family_to_superuser():
    super_user = User.objects.get(is_staff=True)
    family, _ = Group.objects.get_or_create(name='Family A')
    super_user.groups.add(family)


def create_money_flow_from_json(json_path: str) -> None:
    json_income = load_json_file(json_path)

    for dict_income in json_income:
        owner = dict_income["owner"]
        family = dict_income['family']
        del dict_income["owner"]
        del dict_income["family"]

        owner = User.objects.using('primary').get(pk=owner)
        family = Group.objects.using('primary').get(pk=family)
        obj, _ = MoneyFlow.objects.using('primary').get_or_create(owner=owner, family=family, **dict_income)
        obj, _ = MoneyFlow.objects.using('replica').get_or_create(owner=owner, family=family, **dict_income)
