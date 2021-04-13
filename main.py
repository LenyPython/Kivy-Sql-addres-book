import kivy
from kivy.app import App
from kivy.uix.widget import Widget

class LoginScreen(Widget):
	def register(self):
		print('reg')

	def sing_in(self, user_id, password, *args):
		print(f'User: {user_id}, password: {password}')

class AddrBook(App):
	def build(self):
		login = LoginScreen()
		return login


if __name__ == '__main__':
	AddrBook().run()
