from app.models import *
# добавляем в target_metadata <tablename>.metadata


target_metadata = [
	User.metadata, UserXRole.metadata, Role.metadata, Permission.metadata,
	PermissionXRole.metadata, Textbook.metadata,
]
