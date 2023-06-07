from app.db.base_repository import BaseRepository
from app.models import Users


class UsersRepository(BaseRepository[Users]):
    pass


users = UsersRepository(Users)
