import os
class CssCache:
    def __init__(self):
        self._files = {}

    def save_content(self, filename, content):
        self._files[filename] = content

    def load(self, filename):
        """
        Loads Css file and caches the contents in dict.

        :return:
        """
        content = self._files.get(filename)

        if content is None:
            with open(os.path.join('css',filename),'r', encoding='utf-8') as x:
                content = x.read()
            self.save_content(filename, content)

        return content

css_cache = CssCache()