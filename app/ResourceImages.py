from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QGraphicsDropShadowEffect
from PyQt6.QtGui import QPixmap, QFont, QColor
from PyQt6.QtCore import Qt
import os

class ImageTextDisplay(QWidget):
    resource_images = {
        'food': 'resource_food.png',
        'gold': 'resource_gold.png',
        'stone': 'resource_stone.png',
        'wood': 'resource_wood.png'
    }
    images = {
        resource_name: os.path.join('../pictures', 'resource', file_name)
        for resource_name, file_name in resource_images.items()
    }
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Main layout
        self.layout = QHBoxLayout()

        # Store QLabel references for updating texts
        self.labels = {}

        for resource_type , resource_image_path in self.images.items():
            # Vertical box for each image and its text
            vbox = QVBoxLayout()

            # Label for the text
            text_label = QLabel('0') # default text is 0.
            text_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

            # font size
            font = QFont('Segoe UI', 28)  # Specify font name and size here
            text_label.setFont(font)
            vbox.addWidget(text_label)

            # Creating the shadow effect
            shadow_effect = QGraphicsDropShadowEffect()
            shadow_effect.setOffset(3, 3)  # Shadow offset
            shadow_effect.setBlurRadius(5)  # Shadow blur radius
            shadow_effect.setColor(QColor('grey'))  # Shadow color

            # Label for the image
            img_label = QLabel()

            pixmap = QPixmap(resource_image_path)
            if pixmap.isNull():
                print(f"Failed to load image at {resource_image_path}")
            else:
                print(f"Image loaded successfully: {resource_image_path}")
                scaled_pixmap = pixmap.scaled(75, 75, Qt.AspectRatioMode.KeepAspectRatio)
                img_label.setPixmap(scaled_pixmap)

            # Apply image widget
            img_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            vbox.addWidget(img_label)

            # Apply the shadow effect to the label
            text_label.setGraphicsEffect(shadow_effect)

            # Add vertical box to the main layout
            self.layout.addLayout(vbox)

            # Add to dict: text_label to list for later access
            self.labels[resource_type] = text_label

        self.setLayout(self.layout)
        self.setWindowTitle('Image and Text Display')

    def update_text(self, resource_type, new_text):
        """ Update the text above a specific image. """
        resource_text = self.labels.get(resource_type)
        if resource_text:
            resource_text.setText(new_text)
        else:
            print(f'{resource_type} not in self.labels.')




if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    # Initial images and texts

    ex = ImageTextDisplay()
    ex.show()
    sys.exit(app.exec())
