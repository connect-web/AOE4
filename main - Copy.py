import sys
from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QPushButton
from PyQt6.QtCore import Qt

from app.tablexfer import get_dataframe

class OverlayButtons(QWidget):
    def __init__(self, resources):
        super().__init__()
        self.resources = resources
        self.initUI()

    def initUI(self):
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.FramelessWindowHint | Qt.WindowType.Tool)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setGeometry(0, 1050, 260, 60)  # Set the container's position and size

        self.backButton = QPushButton('BACK', self)
        self.backButton.clicked.connect(self.backFunction)
        self.backButton.setGeometry(10, 10, 100, 40)  # Position inside the container

        self.nextButton = QPushButton('NEXT', self)
        self.nextButton.clicked.connect(self.nextFunction)
        self.nextButton.setGeometry(150, 10, 100, 40)  # Position inside the container

        self.backButton.setStyleSheet(
            "QPushButton { background-color: rgb(21,29,38); color: white; font-weight: 900; }")
        self.nextButton.setStyleSheet(
            "QPushButton { background-color: rgb(21,29,38); color: white; font-weight: 900; }")

    def backFunction(self):
        self.resources.back()

    def nextFunction(self):
        self.resources.next()
class OverlayWidget(QWidget):
    def __init__(self, text, x, y):
        super().__init__()
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.FramelessWindowHint | Qt.WindowType.Tool)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setGeometry(x, y, 200, 50)
        label = QLabel(text, self)
        label.setStyleSheet("color: green; font-size: 20px;")

class Resources:

    def vars(self):
        self.y_start = 1220
        self.line_height = 50
        self.y_axis = {
            'food': self.y_start,
            'wood': self.y_start + 1 * self.line_height,
            'gold': self.y_start + (2 * self.line_height),
            'stone': self.y_start + (3 * self.line_height)
        }
        self.x_axis = 220

        self.food = None
        self.wood = None
        self.gold = None
        self.stone = None


    def __init__(self):
        self.vars()
        self.current_index = 0  # Initialize the current index for DataFrame row iteration

        target_dict = {'food': 0, 'wood': 0, 'gold': 0, 'stone': 0}
        self.df = get_dataframe()
        self.app = QApplication(sys.argv)
        self.overlayButtons = OverlayButtons(self)
        self.overlayButtons.show()

    def back(self):
        if self.current_index > 0:
            self.current_index -= 1
        else:
            self.current_index = 0
        self.update_overlays()

    def next(self):
        if self.current_index < len(self.df) - 1:
            self.current_index += 1
        self.update_overlays()

    def update_overlays(self):
        row = self.df.iloc[self.current_index]
        self.set_food(row['food'])
        self.set_wood(row['wood'])
        self.set_gold(row['gold'])
        self.set_stone(row['stone'])

    def set_food(self, value):
        if self.food is None:
            self.food = OverlayWidget(str(value), self.x_axis, self.y_axis.get('food'))  # Set your text and coordinates here
            self.food.show()
        else:
            self.food.setText(str(value))

    def set_wood(self, value):
        if self.wood is None:
            self.wood = OverlayWidget(str(value), self.x_axis, self.y_axis.get('wood'))  # Set your text and coordinates here
            self.wood.show()
        else:
            self.wood.setText(str(value))

    def set_gold(self, value):
        if self.gold is None:
            self.gold = OverlayWidget(str(value), self.x_axis, self.y_axis.get('gold'))  # Set your text and coordinates here
            self.gold.show()
        else:
            self.gold.setText(str(value))

    def set_stone(self, value):
        if self.stone is None:
            self.stone = OverlayWidget(str(value), self.x_axis, self.y_axis.get('stone'))  # Set your text and coordinates here
            self.stone.show()
        else:
            self.stone.setText(str(value))

    def run(self):
        self.set_food(1)
        self.set_wood(2)
        self.set_gold(3)
        self.set_stone(4)
        sys.exit(self.app.exec())


if __name__ == "__main__":
    Resources().run()