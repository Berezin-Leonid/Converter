from tqdm import tqdm
import os
import time


class Converter:
    def __init__(self, donors, files, recipient=None):
        self.donors = donors
        self.recipient = recipient
        self.files = files
    
    def convert(self):
        map_names = [os.path.basename(path) for path in self.files]
        for idx, donor in enumerate(self.donors):
            self.convert_donor(donor=donor, recipient=self.recipient)
            if idx != len(self.donors) - 1:
                self.recipient.update_csv(map_names[idx + 1])
            pass

    def convert_donor(self, donor, recipient):
        for item in tqdm(donor):
            self.recipient.save(item)
    def check_read_time(self):
        start_time = time.time()
        for donor in self.donors:
            for item in tqdm(donor):
                pass
        end_time = time.time()
        print(f"Time of read: {end_time - start_time} seconds")




