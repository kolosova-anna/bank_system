from infrastructure import UnitOfWork, DBConnectMethods, UsersRepo, OpsRepo
from core_services import UsersService, Operations
from ui import BankScreen


def main():
    db = 'new_bank_system'
    conn = DBConnectMethods(db)
    users_repo = UsersRepo(conn)
    ops_repo = OpsRepo(conn)
    uow = UnitOfWork(conn, users_repo, ops_repo)
    users = UsersService(uow)
    ops = Operations(uow)
    ui = BankScreen(users, ops)
    ui.run()
    conn.close()

if __name__ == "__main__":
    main()