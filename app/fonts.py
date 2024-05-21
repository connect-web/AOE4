from PyQt6.QtGui import QFontDatabase, QFont
import os

class FontCache:
    def __init__(self):
        self._fonts = {}

    def get_font_id(self, name="open-sans.regular.ttf"):
        font_id = self._fonts.get(name)
        if font_id is not None and font_id != -1:
            return font_id
        font_id = QFontDatabase.addApplicationFont(os.path.join('css',name))
        if font_id == -1:
            print("Failed to load font")
        else:
            print("Font loaded successfully")
            self._fonts[name] = font_id

        return font_id

font_storage = FontCache()

def get_font_object(font_name: str = None):
    font_id = font_storage.get_font_id() if font_name is None else font_storage.get_font_id(font_name)
    print(f"new font_id: {font_id}")
    font_families = QFontDatabase.applicationFontFamilies(font_id)
    if font_families:
        return font_families[0]

