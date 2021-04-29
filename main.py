import kivy
from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen
from db_connect.sql_connect import connect, do_query, read_query, close_connection, path
from db_connect.sql_connect import create_user_contacts, path


class BookScreen(Screen):
    pass


class AddrTable(Widget):
    pass


class LoginScreen(Screen):
    def register(self):
        connection = connect(path)
        create_user_contacts(connection)
        close_connection(connection)

    def sing_in(self, user_id, password, *args):
        print(f'User: {user_id}, password: {password}')
        connection = connect(path)
        close_connection(connection)


class RegisterScreen(Screen):
    def register(self, user, pass1, pass2):
        connection = connect(path)
        query = '''SELECT user FROM users'''
        user_exists = read_query(connection, query)
        if user_exists:
            print('Login exists, choose other name')
        elif pass1 != pass2:
            print('Passwords do not match')
        else:
            query = ''' INSERT INTO users(user, password) VALUES (?, ?)  '''
            task = (user, pass1)
            do_query(connection, query, task)
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
