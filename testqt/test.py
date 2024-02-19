import sys
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout
from PyQt6.QtCore import Qt


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Button Container Example')
        self.setGeometry(100, 100, 300, 200)  # x, y, width, height

        # Create a container widget
        self.container = QWidget(self)
        self.container.setStyleSheet("background-color: #f0f0f0; border-radius: 10px;")

        # Create a vertical layout
        self.layout = QVBoxLayout()

        # Create and style buttons
        for i in range(3):
            button = QPushButton(f'Button {i + 1}', self)
            button.setStyleSheet("""
                QPushButton {
                    background-color: #007bff;
                    color: white;
                    border-radius: 5px;
                    padding: 10px;
                    margin: 5px;
                }
                QPushButton:hover {
                    background-color: #0056b3;
                }
            """)
            self.layout.addWidget(button)

        # Set the layout for the container and add it to the main window
        self.container.setLayout(self.layout)

        # Create and set the main layout
        self.mainLayout = QVBoxLayout()
        self.mainLayout.addWidget(self.container)
        self.setLayout(self.mainLayout)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec())
