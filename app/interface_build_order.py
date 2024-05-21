import pandas as pd

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



