import kivy
from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen
from db_connect.sql_connect import connect, do_query, read_query, close_connection, path
from db_connect.sql_connect import create_user_contacts, path


class BookScreen(Screen):
    def add_contact():
        print('add contact')

    def remove_contact():
        pass

    def change_contact():
        pass


class AddrTable(Widget):
    pass


class ErrorMsg(Popup):
    pass


class LoginScreen(Screen):
    def register(self):
        connection = connect(path)
        create_user_contacts(connection)
        close_connection(connection)

    def sing_in(self, user_id, password, *args):
        connection = connect(path)
        query = '''SELECT login FROM users WHERE login=?'''
        user_exists = read_query(connection, query, user_id)
        if user_exists:
            query = '''SELECT password FROM users WHERE login=?'''
            pass_check = read_query(connection, query, user_id)[0]
            if password == pass_check:
                print(pass_check)
                kv.current = 'book'

        close_connection(connection)


class RegisterScreen(Screen):
    def register(self, log, pass1, pass2):
        connection = connect(path)
        query = '''SELECT login FROM users WHERE login=?'''
        user_exists = read_query(connection, query, log)
        if user_exists:
            print(user_exists)
            print('Login exists, choose other name')
        elif len(pass1) < 6:
            print('Too short password')
        elif pass1 != pass2:
            print('Passwords do not match')
        else:
            query = ''' INSERT INTO users(login, password)
                        VALUES (?, ?)'''
            do_query(connection, query, (log, pass1,))
        close_connection(connection)


class Manager(ScreenManager):
    pass


kv = Builder.load_file('app.kv')


class AddrBook(App):
    def build(self):
        Window.clearcolor = (55/255, 30/255, 35/255, 1)
        return kv


if __name__ == '__main__':
    AddrBook().run()
