""" Change or rename roles and permission for different purposes """
from enum import Enum


class Roles(Enum):
    """All available roles"""
    SUPERUSER = "SUPERUSER"
    TEACHER = "TEACHER"
    USER = "USER"


class Permissions(Enum):
    """All available permissions"""
    CREATE_TEACHER = "CREATE_TEACHER"
    GET_ROLES = "GET_ROLES"
    GET_USERS_LIST = "GET_USERS_LIST"
    CHANGE_ANOTHER_USERS_PROFILE = "CHANGE_ANOTHER_USERS_PROFILE"
    CHANGE_ANOTHER_USERS_PASSWORD = "CHANGE_ANOTHER_USERS_PASSWORD"
    BLOCK_USERS = "BLOCK_USERS"
    CREATE_OBJECT = "CREATE_OBJECT"
    BLOCK_OBJECT = "BLOCK_OBJECT"
    GET_OBJECT = "GET_OBJECT"
    EDIT_OBJECT = "EDIT_OBJECT"
    GET_OBJECT_LIST = "GET_OBJECT_LIST"


# note: could be refactored with encapsulation principal but need to be reworked init_db


AVAILABLE_ROLES = {
    Roles.SUPERUSER.value: {
        'access_level': 1,
        'description': 'Администратор, доступны все возможности'
    },
    Roles.TEACHER.value: {
        'access_level': 2,
        'description': 'Учитель, может добавлять учебные материалы, но не влияет на систему в целом'
    },
    Roles.USER.value: {
        'access_level': 3,
        'description': 'Ученик, обычный пользователь, только просмотр'
    },
}

AVAILABLE_PERMISSIONS = {
    Permissions.CREATE_TEACHER.value: 'Создавать других админов',

    Permissions.GET_ROLES.value: 'Получать список доступных ролей',
    Permissions.GET_USERS_LIST.value: 'Получить список всех пользователей',
    Permissions.CHANGE_ANOTHER_USERS_PROFILE.value: 'Изменить информацию профиля других пользователей уровнем ниже',
    Permissions.CHANGE_ANOTHER_USERS_PASSWORD.value: 'Изменить пароль других пользователей уровнем ниже',

    Permissions.BLOCK_USERS.value: 'Блокировать пользователей уровнем доступа ниже',

    Permissions.CREATE_OBJECT.value: 'Создать любой объект',
    Permissions.BLOCK_OBJECT.value: 'Блокировать(Удалить) любой объект',
    Permissions.GET_OBJECT.value: 'Получать информацию об объекте',
    Permissions.EDIT_OBJECT.value: 'Изменять любой объект. Полный доступ',

    Permissions.GET_OBJECT_LIST.value: 'Получать список объектов',
}

PERMISSION_X_ROLE = {
    Roles.SUPERUSER.value: (
        Permissions.CREATE_TEACHER.value, Permissions.CHANGE_ANOTHER_USERS_PASSWORD.value,
        Permissions.BLOCK_USERS.value, Permissions.CREATE_OBJECT.value, Permissions.EDIT_OBJECT.value,
        Permissions.BLOCK_OBJECT.value, Permissions.GET_OBJECT.value, Permissions.GET_OBJECT_LIST.value,
    ),

    Roles.TEACHER.value: (
        Permissions.CREATE_OBJECT.value, Permissions.EDIT_OBJECT.value, Permissions.BLOCK_OBJECT.value,
        Permissions.GET_OBJECT.value, Permissions.GET_OBJECT_LIST.value,
    ),
    Roles.USER.value: (Permissions.GET_OBJECT_LIST.value, Permissions.GET_OBJECT.value,)
}
