from utils.recipient_utils import *
from utils.donor_utils import *
from utils.item_utils import *
from tqdm import tqdm
import time


path = "/home/berezin/Datasets/Converter_datasets/example_1"
save_ptb_path = "/home/berezin/Datasets/Converter_datasets/Ptbxl"


def create():
    print("Hello converter!")
    shape = (10_000, 12, 5000)
    chunk = (1, 12, 5000)
    generator = RandomSamplerDonor(elem_shape=shape[1:], amount=shape[0])
    saver = ZarrArrayRecipient(path=path,
                               shape=shape,
                               chunks=chunk,
                               compressor=Blosc(cname="lz4", clevel=3, shuffle=Blosc.BITSHUFFLE))

    start_time = time.time()
    for idx, item in enumerate(tqdm(generator)):
        saver.save(item)
    end_time = time.time()

    print(f"Time of execution write: {end_time - start_time} seconds")

def resave():
    print("Everything Saved!")
    ## Cоздать нового реципиента
    generator = ZarrArrayDonor(path=path)
    for item in tqdm(generator):
        pass

def read_ptb():
    file_paths = [
        "/home/ecg_data/physionet_data/ptbxl_data_1_0_3/train_map_ptbxl.csv",
        "/home/ecg_data/physionet_data/ptbxl_data_1_0_3/test_map_ptbxl.csv",
    ]

    get_donor = lambda path: NpzArrayDonor(map_path=path, data_path=None)

    start_time = time.time()
    read_donors_by_maps(files=file_paths, get_donor=get_donor)
    end_time = time.time()
    print(f"Time execution of read PTB-XL: {end_time - start_time} seconds")


def resave_ptb():
    file_paths = [
        "/home/ecg_data/physionet_data/ptbxl_data_1_0_3/train_map_ptbxl.csv",
        "/home/ecg_data/physionet_data/ptbxl_data_1_0_3/test_map_ptbxl.csv",
    ]

    get_donor = lambda path: NpzArrayDonor(map_path=path, data_path=None)
    donors = [get_donor(path) for path in file_paths]

    shape = (sum(len(donor) for donor in donors), 12, 5_000)
    chunk = (1, 12, 5000)
    saver = ZarrArrayRecipient(path=save_ptb_path,
                               map_file_name=os.path.basename(file_paths[0]),
                               shape=shape,
                               chunks=chunk,
                               compressor=Blosc(cname="lz4", clevel=3, shuffle=Blosc.BITSHUFFLE))

    start_time = time.time()
    #save_donors_by_maps(files=file_paths, donors=donors, saver=saver)
    end_time = time.time()
    print(f"Time execution of read PTB-XL: {end_time - start_time} seconds")


def read_converted_ptb():
    file_paths = [
        "/home/ecg_data/physionet_data/ptbxl_data_1_0_3/train_map_ptbxl.csv",
        "/home/ecg_data/physionet_data/ptbxl_data_1_0_3/test_map_ptbxl.csv",
    ]


def read():
    generator = ZarrArrayDonor(store_path=os.path.join(path, "Store"),
                               map_path=os.path.join(path, "mapfile.csv"))

    start_time = time.time()
    for item in tqdm(generator):
        pass
    end_time = time.time()
    print(f"Time execution of read: {end_time - start_time} seconds")



def convert_ptb():
    file_paths = [
        "/home/ecg_data/physionet_data/ptbxl_data_1_0_3/train_map_ptbxl.csv",
        "/home/ecg_data/physionet_data/ptbxl_data_1_0_3/test_map_ptbxl.csv",
    ]

    get_donor = lambda path: NpzArrayDonor(map_path=path, data_path=None)
    donors = [get_donor(path) for path in file_paths]

    shape = (sum(len(donor) for donor in donors), 12, 5_000)
    chunk = (1, 12, 5000)
    saver = ZarrArrayRecipient(path=save_ptb_path,
                               map_file_name=os.path.basename(file_paths[0]),
                               shape=shape,
                               chunks=chunk,
                               #compressor=Blosc(cname="lz4", clevel=3, shuffle=Blosc.SHUFFLE))
                               #compressor=Blosc(cname="lz4", clevel=3, shuffle=Blosc.BITSHUFFLE))
                               #compressor=Blosc(cname="lz4", clevel=9, shuffle=Blosc.BITSHUFFLE))
                               compressor=Blosc(cname="zstd", clevel=5, shuffle=Blosc.SHUFFLE))
    converter = Converter(donors=donors, files=file_paths, recipient=saver)
    converter.convert()


def check_read_time_ptb():
    file_paths = [
        "/home/ecg_data/physionet_data/ptbxl_data_1_0_3/train_map_ptbxl.csv",
        "/home/ecg_data/physionet_data/ptbxl_data_1_0_3/test_map_ptbxl.csv",
    ]

    get_donor_npz = lambda path: NpzArrayDonor(map_path=path, data_path=None)
    get_donor_zarr = lambda path: ZarrArrayDonor(store_path=os.path.join(save_ptb_path, "Store"),
                                            map_path=os.path.join(save_ptb_path, os.path.basename(path)))
    donors_npz = [get_donor_npz(path) for path in file_paths]
    donors_zarr = [get_donor_zarr(path) for path in file_paths]

    converter_npz = Converter(donors=donors_npz, files=file_paths)
    converter_zarr = Converter(donors=donors_zarr, files=file_paths)
    print("Check npz time:")
    converter_npz.check_read_time()
    print("Check zarr time:")
    converter_zarr.check_read_time()




if __name__ == "__main__":
    #create()
    #read()
    #resave_ptb()
    #read_ptb()
    #read_converted_ptb()
    convert_ptb()
    check_read_time_ptb()

