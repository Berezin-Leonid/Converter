

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



class Item_ICL10(Item):
    def __init__(self, data, info):
        super().__init__(data=data, info=info)


        self.map = [
            [],
            []
        ]
        
    
    def map_disease(self, info):
        # delete all fields with ICL10
        # add scp_codes
        return info



