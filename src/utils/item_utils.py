

class Item:
    def __init__(self, data, info):
        # check that data is ndarray or torch.tensor
        self.data = data
        self.info = info
    def __repr__(self):
        return f"""
=======================================
Info:
{self.info}
---------------------------------------
Data:
{self.data}
=======================================
        """

