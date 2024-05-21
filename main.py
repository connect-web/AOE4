from app import (
    ResourceWidget, DataframeNavigator, MinimizeWidget,
    NavigationButtons, OverlayWidget, css_cache,
    get_dataframe
)
from PyQt6.QtWidgets import QApplication
import sys


class Resources(ResourceWidget):
    default_values = {'food': "", "wood": "", "stone": "", "gold": ""}

    def __init__(self):
        super().__init__()
        self.df_manager = DataframeNavigator(df=get_dataframe('ottomans_2.html'))
        self.app = QApplication(sys.argv)
        self.navigationButtons = NavigationButtons(self)
        self.description = OverlayWidget(text=f"Loaded ottomans",
                                         size=(10, 200, 400, 200),
                                         css=css_cache.load('description.css')
                                         )
        self.update_map(self.default_values)
        self.MinimizeWidget = MinimizeWidget(self, css=css_cache.load('Minimize.css'))



    def back(self):
        self.update_overlays(self.df_manager.back())

    def next(self):
        self.update_overlays(self.df_manager.next())

    def update_overlays(self, update_dict):
        self.update_map(update_dict)
        self.description.setText(
            update_dict.get('description', '')
        )

    def run(self):
        sys.exit(self.app.exec())


if __name__ == "__main__":
    Resources().run()
