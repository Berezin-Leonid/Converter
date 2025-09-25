from utils.item_utils import Item
from utils.info_utils import *
from convert import *
from tqdm import tqdm
import numpy as np
import uuid
import zarr
import csv
import os


class Iterator:
    def __init__(self, donor):
        self.donor = donor
        self.index = 0
        self.batch_size = donor.batch_size
    
    def __next__(self):
        if self.index >= len(self.donor):
            raise StopIteration
        item = self.donor[self.index]
        self.index += 1
        #item = self.data[self.index : self.index + self.batch_size]
        #self.index += self.batch_size
        return item


class Donor:
    def __init__(self, class_item, batch_size=1):
        self.class_item = class_item
        self.batch_size = batch_size
    
    def __iter__(self):
        return Iterator(self)
    
    def __getitem__(self, index):
        if index >= len(self):
            return IndexError
        info = self._getinfo(index)
        data = self._getdata(index, info)
        return self.class_item(data=data, info=info)


class RandomSamplerDonor(Donor):
    def __init__(self, elem_shape, amount, class_item=Item):
        super().__init__(class_item=class_item)
        self.elem_shape = elem_shape
        self.amount = amount
    
    def _getinfo(self, index):
        info = {
            "id": str(uuid.uuid4()),
            "sex": True
        }
        return info

    def _getdata(self, index, info):
        data = np.random.rand(*self.elem_shape).astype("float32")
        return data

    def __len__(self):
        return self.amount
    

class ZarrArrayDonor(Donor):
    def __init__(self, store_path, map_path, batch_size=1, class_item=Item):
        super().__init__(batch_size=batch_size, class_item=class_item)
        self.batch_size = batch_size

        self.store = zarr.DirectoryStore(store_path)
        self.root = zarr.open_group(self.store, mode="r")
        complect_info_group(self.root)


        with open(map_path, newline="") as f:
            reader = csv.DictReader(f)
            self.map = [row for row in reader]
        
        self._length = len(self.map)

    
    def __len__(self):
        return self._length
    
    def _getinfo(self, index):
        row = self.map[index]
        info = dict(row)
        return info
    
    def _getdata(self, index, info):
        data = self.root[info["array_path"]][int(info["index"])]
        return data


class NpzArrayDonor(Donor):
    def __init__(self, map_path, data_path, batch_size=1, class_item=Item):
        super().__init__(batch_size=batch_size, class_item=class_item)
        with open(map_path, newline="") as f:
            reader = csv.DictReader(f)
            self.map = [row for row in reader]
        self.data_path = data_path
        self._length = len(self.map)
    
    def __len__(self):
        return self._length


    def _getinfo(self, index):
        info = dict(self.map[index])
        return info

    def _getdata(self, index, info):
        file_path = info["fpath"]
        data = np.load(file_path)["arr_0"].astype("float64")
        return data



class ChapmanArrayDonor(NpzArrayDonor):
    def __init__(self, map_path, data_path, batch_size=1, class_item=Item):
        super().__init__(map_path=map_path, data_path=data_path, batch_size=batch_size, class_item=Item)
    
    def _getdata(self, index, info):
        file_path = info["fpath"]
        data = np.load(file_path)["arr_0"].astype("float64")
        data = data.T
        return data

