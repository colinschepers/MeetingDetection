import statistics
from datetime import datetime 
from logger import logger 
import pickle
import struct


class GeoTimeInstance():
    def __init__(self, id, lat, lon, t):
        self.id = id
        self.data = [lat, lon, t]

    def __repr__(self):
        return str(self)

    def __str__(self):
        dt = datetime.fromtimestamp(self.data[2])
        return f"({self.id}, {self.data[0]:.5f}, {self.data[1]:.5f}, {dt})"


class GeoTimeNode():
    def __init__(self, depth, instances):
        self.depth = depth
        self.left = None
        self.right = None
        self.axis = depth % 3
        self.value = None
        self.instances = instances
        
    def next(self, instance):
        if self.is_leaf():
            return None  
        return self.left if instance.data[self.axis] < self.value else self.right

    def is_leaf(self):
        return not self.left and not self.right
    
    def __repr__(self):
        return str(self)

    def __str__(self):
        if self.is_leaf():
            return f'Leaf(n={len(self.instances)})'
        axis = ['lat', 'lon', 't'][self.axis]
        val = f'{self.value:.10F}' if self.axis < 2 else f'{int(self.value)}'
        return f'Node({axis}={val})'
    

class GeoTimeTree():
    def __init__(self):
        self.root = GeoTimeNode(0, [])
        self.size = 1
        self.split_k = 10

    @staticmethod
    def load(path):
        tree = GeoTimeTree()
        with open(path, 'rb') as f:
            tree.size = struct.unpack('>i', f.read(4))[0]
            stack = [tree.root]
            for i in range(tree.size):
                node = stack.pop()
                is_leaf = struct.unpack('>?', f.read(1))[0]
                if not is_leaf:
                    if node.axis < 2:
                        node.value = struct.unpack('>d', f.read(8))[0]
                    else:
                        node.value = struct.unpack('>i', f.read(4))[0]
                    node.left = GeoTimeNode(node.depth + 1, [])
                    node.right = GeoTimeNode(node.depth + 1, [])
                    stack.append(node.left)
                    stack.append(node.right)
                # else:
                #     instance_count = struct.unpack('>i', f.read(4))[0]
                #     for i in range(instance_count):
                #         instance = GeoTimeInstance(
                #             struct.unpack('>i', f.read(4))[0],
                #             struct.unpack('>d', f.read(8))[0],
                #             struct.unpack('>d', f.read(8))[0],
                #             struct.unpack('>d', f.read(8))[0])
                #         node.instances.append(instance)
        return tree

    def save(self, path):
        with open(path, 'wb') as f:
            f.write(struct.pack('>i', self.size))
            for node in self.preorder():
                if not node.is_leaf():
                    f.write(struct.pack('>?', False))
                    if node.axis < 2:
                        f.write(struct.pack('>d', node.value))
                    else:
                        f.write(struct.pack('>i', int(node.value)))
                else:
                    f.write(struct.pack('>?', True))
                #     f.write(struct.pack('>i', len(node.instances)))
                #     for instance in node.instances:
                #         f.write(struct.pack('>i', instance.id))
                #         f.write(struct.pack('>d', instance.data[0]))
                #         f.write(struct.pack('>d', instance.data[1]))
                #         f.write(struct.pack('>d', instance.data[2]))

    def add(self, instances):
        if isinstance(instances, GeoTimeInstance):
            instances = [instances]
        self.root.instances.extend(instances)
        self._update(self.root)
        
    def _update(self, node):
        stack = [node]
        while stack:
            node = stack.pop()
            if not node.is_leaf():
                left, right = self._split_instances(node.instances, node.axis, node.value)
                node.left.instances.extend(left)
                node.right.instances.extend(right)
                stack.append(node.left)
                stack.append(node.right)
                node.instances = []
            elif self.split_policy(node):
                self.split(node)
                stack.append(node.left)
                stack.append(node.right)
                # if (self.size - 1) % 10000 == 0:
                #     print(self.size)
                
    def find(self, instance):
        node = self.root
        while not node.is_leaf():
            node = node.next(instance)
        return node

    def preorder(self):
        stack = [self.root]
        while stack:
            node = stack.pop()
            yield node
            if not node.is_leaf():
                stack.append(node.left)
                stack.append(node.right)

    def split_policy(self, node):
        return len(node.instances) >= self.split_k

    def split(self, node):
        node.value = statistics.mean(x.data[node.axis] for x in node.instances)
        left, right = self._split_instances(node.instances, node.axis, node.value)
        node.left = GeoTimeNode(node.depth + 1, left)
        node.right = GeoTimeNode(node.depth + 1, right)
        node.instances = []
        self.size += 2

    def _split_instances(self, instances, axis, value):
        left, right = [], []
        for x in instances:
            (left if x.data[axis] < value else right).append(x)
        return left, right

    def __repr__(self):
        return f'Tree({self.size})'

    def __str__(self):
        nodes = '\n'.join('  ' * n.depth + str(n) for n in self.preorder())
        return f'Tree({self.size}):\n{nodes}\n'
            
