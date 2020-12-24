import time
from mock_data import generate_mockdata
from geolife_data import get_data
from models import GeoTimeTree

num_samples = 1000000000
batch_size = 10000
data_path = '/home/colin/Data/Geolife Trajectories 1.3/Data'
tree_path = './tree.pkl'

data = get_data(data_path, num_samples)
# data = generate_mockdata(num_samples)

# for x in data:
#     print(x)

def batches(instances, batch_size):
    batch = []
    for instance in instances:
        if len(batch) == batch_size:
            yield batch
            batch = []
        batch.append(instance)
    yield batch

tree = GeoTimeTree()

for i, batch in enumerate(batches(data, batch_size)):

    print(f'\nIteration: {i}')
    print(f'Instances: {(i+1) * batch_size}')
    print(f'Tree size: {tree.size}')

    start = time.time()
    tree.add(batch)
    print(f"Tree building time: {time.time() - start:.2f}s")
    # print(tree)

    start = time.time()
    tree.save(tree_path)
    print(f"Tree saving time: {time.time() - start:.2f}s")

    # start = time.time()
    # tree = GeoTimeTree.load(tree_path)
    # print(f"Tree loading time: {time.time() - start:.2f}s")
    # print(tree)