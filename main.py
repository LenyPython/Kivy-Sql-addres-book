import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from db_connect.sql_connect import connect, do_query, read_query, close_connection, path
from db_connect.sql_connect import create_table, create_user, create_contacts

class LoginScreen(Widget):
	def register(self):
		connection = connect(path)
		create_table(connection, create_user)
		create_table(connection, create_contacts)

		close_connection(connection)

	def sing_in(self, user_id, password, *args):
		print(f'User: {user_id}, password: {password}')
		connection = connect(path)

class AddrBook(App):
	def build(self):
		login = LoginScreen()
		return login


if __name__ == '__main__':
	AddrBook().run()
