import sys

import pandas as pd
from PyQt6.QtWidgets import QApplication
from app.css_cache import css_cache
from app.tablexfer import get_dataframe, load_build_order
from app.BaseWidgets import OverlayWidget, NavigationButtons, ResourceWidget, MinimizeWidget
from app.ResourceImages import ImageTextDisplay


class DataframeNavigator:
    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.current_index = 0
        self.displayedFirstInstruction = False

    def get_row_as_dict(self):
        row = self.df.iloc[self.current_index]
        map = {
            'description': row.iloc[1],
            'food': row.iloc[2],
            'wood': row.iloc[3],
            'gold': row.iloc[4],
            'stone': row.iloc[5]
        }

        return map

    def back(self):
        if self.current_index > 0:
            self.current_index -= 1
        return self.get_row_as_dict()

    def next(self):
        if self.displayedFirstInstruction:
            if self.current_index < len(self.df) - 1:
                self.current_index += 1
        else:
            self.displayedFirstInstruction = True

        return self.get_row_as_dict()


def build_order_files():
    BO_files = {
        "1": 'French 3 38 Feudal All-in_Castle Timing.bo',
        "2": 'Ayyubids desert raider opening into FC by VortiX.bo',
        "3": "Beastyqt mongol kashik.bo",
        "4": "Zhu Xi's Legacy Fast Aggression [ Beasty ].bo",
        "5": "Rus 2 TC.bo"

    }
    loaded = {
        '1': 'French Rush Good VS all EXCEPT RUS & Chinese',
        '2': 'Ayyubids desert raiders',
        '3': 'Mongols kashik',
        '4': 'Zhu Xi Legacy',
        '5': 'RUS 2 TC'
    }
    print("""
            [1] French Rush Good VS all EXCEPT RUS & Chinese
            [2] Ayyubids desert raiders
            [3] Mongols kashik
            [4] Zhu Xi's Legacy Fast Aggression
            [5] Rus 2TC
            """)
    # selected = input("Enter your choice:")
    while BO_files.get(selected) is None:
        print("\n Invalid choice. Please try again.")
        selected = input("Enter your choice:")

    df = load_build_order(BO_files.get(selected))
    return df


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
        self.MinimizeWidget = MinimizeWidget(self, css=css_cache.load('Minimize.css'))

        self.update_map(self.default_values)

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
