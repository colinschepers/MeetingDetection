import os
import csv
from pathlib import Path
from datetime import datetime
from models import GeoTimeInstance


def get_data(path, num_samples):
    cnt = 0
    for file in plt_files(path):
        user_id = file.parts[-3]
        for lat, lon, _, d, t in read_file(file):
            yield to_instance(user_id, lat, lon, d, t)
            cnt += 1
            if cnt >= num_samples:
                return

def plt_files(root):
    for root, folders, files in os.walk(root):
        for f in files:
            if f.endswith(".plt"):
                yield Path(os.path.join(root, f))


def read_file(path):
    with open(path, "r") as f:
        reader = csv.reader(f, delimiter=",")
        for _ in range(6):
            next(reader)
        for lat, lon, _, _, me, d, t in reader:
            yield lat, lon, me, d, t


def to_instance(user_id, lat, lon, d, t):
    timestamp = datetime.strptime(f"{d} {t}", "%Y-%m-%d %H:%M:%S").timestamp()
    return GeoTimeInstance(int(user_id), float(lat), float(lon), timestamp)