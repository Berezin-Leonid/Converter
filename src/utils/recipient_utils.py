from utils.item_utils import Item
import zarr
from numcodecs import Blosc
from utils.info_utils import *
import csv
import os


class Recipient:
    def __init__(self):
        pass

    def save(self, item: Item):
        index = self.set_index(item)
        self.set_data(item, index)


class ZarrArrayRecipient(Recipient):
    def __init__(self, path, map_file_name="mapfile.csv", compressor=None, shape=None, chunks=None, dtype="float32"):

        self.path = path
        self.map_path = os.path.join(path, map_file_name)
        self.store_path = os.path.join(path, "Store")

        self.store = zarr.DirectoryStore(self.store_path)
        self.root = zarr.group(store=self.store, overwrite=True)
        self.data = self.root.require_group("data")

        if compressor is None:
            compressor = Blosc(cname="lz4", clevel=3, shuffle=Blosc.SHUFFLE)
        self.compressor = compressor
        self.chunks = chunks
        self.count_map_files = 0

        self.array = self.data.create_dataset(
            name="array_1",
            shape=shape,
            chunks=self.chunks,
            dtype=dtype,
            compressor=self.compressor
        )

        self.count = 0
        self.csv_writer = None
        self.csv_file = None
        self.fieldnames = None
    
    def _init_csv(self, map_path, item=None):
        self.fieldnames = ["array_path"] + ["index"] + list(item.info.keys()) if item is not None else self.fieldnames
        self.csv_file = open(map_path, "w", newline="")
        self.csv_writer = csv.DictWriter(self.csv_file, fieldnames=self.fieldnames)
        self.csv_writer.writeheader()
        self.count_map_files += 1

    def update_csv(self, file_name="mapfile.csv"):
        if file_name == "mapfile.csv":
            file_name = f"{self.count_map_files}_{file_name}"
        self.map_path = os.path.join(self.path, file_name)
        self._init_csv(map_path=self.map_path)

    def set_index(self, item: Item):
        count = self.count

        row = {"array_path": 'data/array_1' ,"index": count, **item.info}
        self.csv_writer.writerow(row)
        self.csv_file.flush()

        self.count += 1
        return count
    
    def set_data(self, index, item: Item):
        #self.array.resize(index + 1 ,500, 500) 
        self.array[index] = item.data
    
    def save(self, item: Item):
        if self.csv_writer is None:
            self._init_csv(item=item, map_path=self.map_path)
        index = self.set_index(item)
        self.set_data(index, item)

    def close(self):
        if self.csv_file:
            self.csv_file.close()
    
class ISPEcgRecipient(ZarrArrayRecipient):
    def __init__(self):
        super().__init__(...)
    
    # saving ecg with map files
