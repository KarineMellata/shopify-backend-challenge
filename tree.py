import json

class Node:
    """
    A generic tree node
    """
    def __init__(self, id, name, children):
        self.name = name
        self.id = id
        self.children = children

    def is_root(self):
        return self.name == 'root'

    def get_id(self):
        return self.id

    def get_children(self):
        return self.children



class Tree():
    """
    A generic tree in JSON and utility functions
    """
    def __init__(self):
        self.graph = {}

    def graph(self):
        return dict(self.graph)

    def create_tree(self,object):
        """
        :param data:
        :return:
        """
        for item in object:
            id = item['id']
            children = item['child_ids']
            if 'parent_id' in item:
                self.graph[id] = Node(id=id,name='child',children=children)
            else:
                self.graph[id] = Node(id=id, name='root', children=children)

    def get_node(self, id):
        if self.graph.get(id) == None:
            return 0
        return self.graph[id]

# if __name__ == "__main__":
#     tree = Tree()
#     j = json.loads('[{"id": 1, "data": "House", "child_ids": [3]}, {"id": 2, "data": "Company", "child_ids": [4, 5, 8]}, {"id": 3, "data": "Living Room", "parent_id": 1, "child_ids": [7]}, {"id": 4, "data": "Meeting Rooms", "parent_id": 2, "child_ids": []}, {"id": 5, "data": "Kitchen", "parent_id": 2, "child_ids": [6]}, {"id": 6, "data": "Oven", "parent_id": 5, "child_ids": []}, {"id": 7, "data": "Table", "parent_id": 3, "child_ids": [15]}, {"id": 8, "data": "HR", "parent_id": 2, "child_ids": []}, {"id": 9, "data": "Computer", "child_ids": [10, 11, 12]}, {"id": 10, "data": "CPU", "parent_id": 9, "child_ids": []}, {"id": 11, "data": "Motherboard", "parent_id": 9, "child_ids": []}, {"id": 12, "data": "Peripherals", "parent_id": 9, "child_ids": [13, 14]}, {"id": 13, "data": "Mouse", "parent_id": 12, "child_ids": []}, {"id": 14, "data": "Keyboard", "parent_id": 12, "child_ids": []}, {"id": 15, "data": "Chair", "parent_id": 7, "child_ids": [1]}]')
#     tree.create_tree(j)
#     print(str(tree.graph))


