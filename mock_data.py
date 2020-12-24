import random
import time
from datetime import datetime
from models import GeoTimeInstance


random.seed(1988)

def generate_mockdata(n):
    amsterdam = (52.3676, 4.9041)
    christmas = datetime(2020, 12, 26)
    christmas = time.mktime(christmas.timetuple())
    mockdata = [GeoTimeInstance(i + 1,
        random.gauss(amsterdam[0], 0.05), 
        random.gauss(amsterdam[1], 0.05),
        christmas + random.randint(0, 2 * 24 * 60 * 60),
    ) for i in range(n)]
    return mockdata