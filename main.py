import kivy
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.properties import NumericProperty

class LoginScreen(GridLayout):
	cols = NumericProperty(2)

class AddrBook(App):
	def build(self):
		return LoginScreen()


if __name__ == '__main__':
	AddrBook().run()
