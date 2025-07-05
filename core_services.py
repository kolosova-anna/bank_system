from core_interfaces import User, UserAccount, IUsersRepository, IOperationsRepository


class UsersService:

    def __init__(self, users_repo: IUsersRepository):
        self.users_repo = users_repo

    def registrarion(self, login: str, password: str) -> User:
        return self.users_repo.registration(login, password)
    
    def create_account(self, user_id: int) -> UserAccount:
        return self.users_repo.create_account(user_id)

    def autorization(self, login: str, password: str) -> UserAccount:
        return self.users_repo.autorization(login, password)

    def get_user_by_id(self, user_id: int) -> UserAccount:
        return self.users_repo.get_user_by_id(user_id)


class Operations:

    def __init__(self, ops_repo: IOperationsRepository):
        self.ops_repo = ops_repo

    def get_balance(self, user_id: int) -> float:
        return self.ops_repo.get_balance(user_id)

    def get_history(self, user_id: int) -> list:
        return self.ops_repo.get_history(user_id)

    def withdraw_cash(self, user_id: int, sum: int) -> None:
        return self.withdraw_cash(user_id, sum)

    def up_user_balance(self, user_id: int, sum: int) -> None:
        return self.up_user_balance(user_id, sum)
