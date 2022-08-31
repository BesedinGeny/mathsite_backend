""" Change or rename roles and permission for different purposes """

AVAILABLE_ROLES = {
	'SUPERUSER': {'access_level': 1,
	              'description': 'Администратор, доступны все возможности'},
	'TEACHER': {'access_level': 2,
	            'description': 'Учитель, может добавлять учебные материалы, но не влияет на '
	                           'систему в целом'},
	'USER': {'access_level': 3, 'description': 'Ученик, обычный пользователь, '
	                                           'только просмотр'},
}

AVAILABLE_PERMISSIONS = {
	'CREATE_TEACHER': 'Создавать других админов',
	
	'GET_ROLES': 'Получать список доступных ролей',
	'GET_USERS_LIST': 'Получить список всех пользователей',
	'CHANGE_ANOTHER_USERS_PROFILE': 'Изменить информацию профиля других пользователей уровнем ниже',
	'CHANGE_ANOTHER_USERS_PASSWORD': 'Изменить пароль других пользователей уровнем ниже',
	
	'BLOCK_USERS': 'Блокировать пользователей уровнем доступа ниже',
	
	'CREATE_OBJECT': 'Создать любой объект',
	'BLOCK_OBJECT': 'Блокировать(Удалить) любой объект',
	'GET_OBJECT': 'Получать информацию об объекте',
	'EDIT_OBJECT': 'Изменять любой объект. Полный доступ',
	
	'GET_OBJECT_LIST': 'Получать список объектов',
}

PERMISSION_X_ROLE = {
	'SUPERUSER': ['CREATE_TEACHER', 'CHANGE_ANOTHER_USERS_PASSWORD',
	              'BLOCK_USERS', 'CREATE_OBJECT', 'EDIT_OBJECT',
	              'BLOCK_OBJECT', 'GET_OBJECT', 'GET_OBJECT_LIST'],
	
	'TEACHER': ['CREATE_OBJECT', 'EDIT_OBJECT',
	            'BLOCK_OBJECT', 'GET_OBJECT', 'GET_OBJECT_LIST'],
	'USER': ['GET_OBJECT_LIST', 'GET_OBJECT']
}
