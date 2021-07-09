import game
import gui
import sys
from PyQt5.QtWidgets import *


if __name__ == '__main__':
	app = QApplication(sys.argv)
	widget = game.setup_GUI()
	app.exec()
	p1, p2 = widget.currentWidget().return_data()
	player_names = [p1, p2]
	game.measure(player_names, widget, app)


