from __future__ import annotations
from core_interfaces import User, History, IUsersRepository, IOperationsRepository, IUnitOfWork
from core_services import BankException
import sqlite3
import re
from datetime import datetime


class DBConnectMethods:
    ''' Содержит метода для подключения к БД и передачи запроса '''
    def __init__(self, db: str):
        self.db = db
        self.connection = sqlite3.connect(self.db)
        self.cursor = self.connection.cursor()

    def execute_query(self, query: str, *args) -> None:
        self.cursor.execute(query, args)

    def get_data(self, query: str, *args) -> list:
        self.cursor.execute(query, args)
        result: list = self.cursor.fetchall()
        return result
    
    def get_one(self, query: str, *args) -> tuple:
        self.cursor.execute(query, args)
        result: tuple = self.cursor.fetchone()
        return result
    
    def close(self) -> None:
        self.connection.close()


class UnitOfWork(IUnitOfWork):
    def __init__(self, db, users, ops) -> None:
        self.db: DBConnectMethods = db
        self.users_repo = users
        self.ops_repo = ops

    def __enter__(self) -> UnitOfWork:
        self.db.execute_query('BEGIN TRANSACTION')
        return self
    
    def __exit__(self, exc_type, exc_value, traceback) -> None:
        if exc_type:
            self.rollback()
        else:
            self.commit()

    def rollback(self) -> None:
        self.db.execute_query('ROLLBACK')
    
    def commit(self) -> None:
        self.db.execute_query('COMMIT')


class UsersRepo(IUsersRepository):
    def __init__(self, db):
        self.db: DBConnectMethods = db
        query = '''
            CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    login VARCHAR(20) UNIQUE,
                    password VARCHAR(20)
                    )
        '''
        self.db.execute_query(query)
        query = '''
            CREATE TABLE IF NOT EXISTS accounts (
                    account_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    balance DECIMAL(10, 2) DEFAULT 0.00,
                    FOREIGN KEY (user_id) REFERENCES users(user_id)
                    )
        '''
        self.db.execute_query(query)
        query = '''
            CREATE TABLE IF NOT EXISTS operations (
                    op_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    date_time DATETIME,
                    op_name VARCHAR(40),
                    sum FLOAT,
                    FOREIGN KEY (user_id) REFERENCES users(user_id)
                    )
        '''
        self.db.execute_query(query)

    def registration(self, login: str, password: str) -> int | None:
        try:
            check_query = "SELECT COUNT(*) FROM users WHERE login = ?"
            check_login = self.db.get_one(check_query, login)
            if check_login[0] == 0:
                check_password = self.check_new_password(password)
                if check_password:
                    query = "INSERT INTO users (login, password) VALUES (?, ?)"
                    self.db.execute_query(query, login, password)
                    query = "SELECT user_id FROM users WHERE login = ?"
                    res = self.db.get_one(query, login)
                    return int(res[0])
                raise BankException("The password must be at least 8 characters long and '\
                                 'contain uppercase and lowercase letters, numbers, and symbols.")
            raise BankException("This username is already taken")
        except BankException as e:
            print(e)
            return
        
    def create_account(self, user_id: int) -> int:
        query = "INSERT INTO accounts (user_id) VALUES (?)"
        self.db.execute_query(query, user_id)
        return user_id
    
    def autorization(self, login: str, password: str) -> int | None:
        query = "SELECT user_id FROM users WHERE login = ? AND password = ?"
        res = self.db.get_one(query, login, password)
        if res is not None:
            return int(res[0])
        return None
         
    def check_user_availibility(self, login: str) -> bool:
        query = "SELECT COUNT(*) FROM users WHERE login = ?"
        check_login = self.db.get_one(query, login)
        if check_login[0] == 1:
            return True
        return False
        
    def check_new_password(self, password: str) -> bool:
        if (len(password) < 8 or
            not re.search(r'[a-z]', password) or
            not re.search(r'[A-Z]', password) or
            not re.search(r'[0-9]', password) or
            not re.search(r'[^a-zA-Z0-9]', password)):
            return False
        return True
    
class OpsRepo(IOperationsRepository):
    def __init__(self, db):
        self.db: DBConnectMethods = db

    def get_balance(self, user_id: int) -> float:
        query = "SELECT balance FROM accounts WHERE user_id = ?"
        res = self.db.get_one(query, user_id)
        return res[0]

    def get_history(self, user_id: int) -> list:
        query = '''
            SELECT date_time, op_name, sum
            FROM operations
            WHERE user_id = ?
        '''
        ops = self.db.get_data(query, user_id)
        return [row for row in ops]

    def withdraw_cash(self, user_id: int, sum: int) -> None:
        query = '''
            UPDATE accounts
            SET balance = balance - ?
            WHERE user_id = ?
        '''
        self.db.execute_query(query, sum, user_id)

    def deposit_cash(self, user_id: int, sum: int) -> None:
        query = '''
            UPDATE accounts
            SET balance = balance + ?
            WHERE user_id = ?
        '''
        self.db.execute_query(query, sum, user_id)

    def record_changes(self, user_id: int, operation: str, sum: int) -> None:
        date_time = datetime.now().strftime("%d.%m.%Y %H:%M")     
        query = '''
            INSERT INTO operations
            (user_id, date_time, op_name, sum)
            VALUES (?, ?, ?, ?)
        '''
        self.db.execute_query(query, user_id, date_time, operation, sum)

    def show_all_records(self, table: str) -> list:
        query = f"SELECT * FROM {table}"
        return self.db.get_data(query)
    
''' def delete_record(self) -> None:
        query = "DELETE FROM users WHERE user_id = 1"
        self.db.execute_query(query)'''