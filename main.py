import kivy
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen
from db_connect.sql_connect import connect, do_query, read_contacts, read_query, close_connection, path
from db_connect.sql_connect import create_user_contacts, path


class BookScreen(Screen):
    def add_contact(self):
        popup = AddContact()
        popup.open()

    def logout(self):
        kv.user = None
        kv.current = 'log'

    def read_contacts(self):
        connection = connect(path)
        query = '''SELECT * FROM contacts WHERE user_id=?'''
        contacts = read_contacts(connection, query, kv.user)
        close_connection(connection)
        self.ids['bl'].clear_widgets()
        for i, contact in enumerate(contacts):
            contact_widget = Contact()
            contact_widget.ids['index'].text = str(i + 1)
            contact_widget.ids['name'].text = str(contact[2])
            contact_widget.ids['second'].text = str(contact[3])
            contact_widget.ids['email'].text = str(contact[4])
            contact_widget.ids['phone'].text = str(contact[5])
            self.ids['bl'].add_widget(contact_widget)


class Contact(BoxLayout):
    def remove_contact(self, name, second, email, phone):
        connection = connect(path)
        query = '''DELETE FROM contacts WHERE name=? AND second_name=? AND email=? AND phone=?'''
        do_query(connection, query, (name, second, email, phone))
        close_connection(connection)
        self.parent.parent.parent.read_contacts()

    def change_contact(self, name, second, email, phone):
        popup = AddContact()
        popup.ids['name'].text = name
        popup.ids['second'].text = second
        popup.ids['email'].text = email
        popup.ids['phone'].text = phone
        popup.open()


class AddContact(Popup):
    def insert(self, name, second, e_mail, phone):
        query = 'INSERT INTO contacts(user_id, name, second_name, email, phone) VALUES (?, ?, ?, ?, ?)'
        connection = connect(path)
        do_query(connection, query, (kv.user, name, second, e_mail, phone))
        close_connection(connection)


class UserExists(Popup):
    pass


class LoginScreen(Screen):
    def register(self):
        connection = connect(path)
        create_user_contacts(connection)
        close_connection(connection)
        kv.current = 'reg'

    def sing_in(self, user_id, password):
        connection = connect(path)
        query = '''SELECT login FROM users WHERE login=?'''
        user_exists = read_query(connection, query, user_id)
        popup = UserExists()
        if user_exists:
            query = '''SELECT password FROM users WHERE login=?'''
            pass_check = read_query(connection, query, user_id)[0]
            if password == pass_check:
                kv.user = user_id
                kv.current = 'book'
            else:
                popup.title = 'Wrong password, try again...'
                popup.open()
        else:
            popup.title = 'Bad credentials: login'
            popup.open()

        close_connection(connection)


class RegisterScreen(Screen):
    def register(self, log, pass1, pass2):
        connection = connect(path)
        query = '''SELECT login FROM users WHERE login=?'''
        user_exists = read_query(connection, query, log)
        popup = UserExists()
        if user_exists:
            popup.open()
        elif len(pass1) < 6:
            popup.title = 'Password too short'
            popup.open()
        elif pass1 != pass2:
            popup.title = "Passwords don't match"
            popup.open()
        else:
            query = ''' INSERT INTO users(login, password)
                        VALUES (?, ?)'''
            do_query(connection, query, (log, pass1,))
            kv.current = 'log'
        close_connection(connection)


class Manager(ScreenManager):
    pass


kv = Builder.load_file('app.kv')


class AddrBook(App):
    def build(self):
        kv.user = None
        kv.contacts = None
        return kv


if __name__ == '__main__':
    AddrBook().run()
