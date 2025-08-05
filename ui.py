from core_services import UsersService, Operations
import pandas as pd


class BankScreen:
    def __init__(self, users: UsersService, ops: Operations):
        self.users = users
        self.ops = ops

    def run(self) -> None:
        print('\nBank welcomes you!')
        self._show_menu_main()
        while True:
            choise = self._get_num()
            match choise:
                case '1':
                    self._registration()
                case '2':
                    while True:
                        user_id = self._autorization()
                        if user_id is not None:
                            self._run_user_menu(user_id)
                            break
                        else:
                            print('There was a mistake in your login or password. Please, repeat') 
                case '0':
                    print('Program stopped')
                    break
                case _:
                    print("The section with the entered number wasn't found")

    def _run_user_menu(self, user_id: int) -> None:
        print('\n Dear client, you are logged in')
        self._show_user_menu()
        while True:
            choise = self._get_num()
            match choise:
                case '1':
                    sum = self._get_sum()
                    self.ops.deposit_cash(user_id, sum)
                    self._show_user_menu()
                case '2':
                    sum = self._get_sum()
                    self.ops.withdraw_cash(user_id, sum)
                    self._show_user_menu()
                case '3':
                    self._show_balance(user_id)
                    self._show_user_menu()
                case '4':
                    self._show_history(user_id)
                    self._show_user_menu()
                case '0':
                    return
                case _:
                    print("The section with entered number wasn't found")
                    self._show_user_menu()

    def _get_login(self) -> str:
        while True:
                self.login: str = input('\nEnter username: ')
                if self.login:
                    return self.login
                else:
                    print("Username can't be blank: ")

    def _get_password(self) -> str | None:
        attempt = 0
        while attempt <= 5:
            self.password = input('\nEnter password: ')
            if self.users.check_new_password(self.password):
                password_2 = input('\nRepeat password: ')
                if self.password == password_2:
                    return self.password
                print('There was a mistake. Please, repeat')
            else:
                print('The password must be at least 8 characters long and '\
                      'contain uppercase and lowercase letters, numbers, and symbols.')
        print('Password attempt limit reached')

    def _registration(self) -> None:
        attempt = 0
        while attempt <= 3:
            login = self._get_login()
            password = self._get_password()
            if password is not None:
                user_id = self.users.registration(login, password)
                if user_id is not None:
                    print('Your account has been successfully registrated')
                else:
                    print('There was a mistake. Please, repeat')
            else:
                print('Try again later')
            attempt += 1
        print('Password attempt limit reached')

    def _autorization(self) -> int | None:
        login = input('\nEnter username: ')
        password = input('\nEnter password: ')
        user_id = self.users.autorization(login, password)
        return user_id     
    
    def _show_menu_main(self) -> None:
        print('Select menu item you are interested in:')
        print('1. Sign up')
        print('2. Log in')
        print('0. Exit')

    def _show_user_menu(self) -> None:
        print('Select action:')
        print('1. Deposit cash')
        print('2. Withdraw cash')
        print('3. Check balance')
        print('4. View transaction history')
        print('0. Log out')

    def _show_balance(self, user_id: int) -> None:
        balance = self.ops.get_balance(user_id)
        print(f'Current balance: {balance}')

    def _show_history(self, user_id: int) -> None:
        data = self.ops.get_history(user_id)
        if data:
            df = pd.DataFrame(data, columns=['date', 'operation', 'sum'])
            print(df)
        else:
            print('No transactions have been found on your account')

    def _check_input(self) -> int:
        while True:
            try:
                number = int(input())
                if number > 0:
                    return number
                return abs(number)
            except ValueError:
                print('Error. Enter number ')

    def _get_num(self) -> str:
        print('\nEnter the menu section number:\n')
        self.number = self._check_input()
        return str(self.number)
    
    def _get_sum(self) -> int:
        print('\nEnter sum: ')
        return self._check_input()