import kivy
from kivy.app import App
from kivy.uix.label import Label
from book.LoginScreen import LoginScreen

class AddrBook(App):
	def build(self):
		return LoginScreen()


if __name__ == '__main__':
	AddrBook().run()
