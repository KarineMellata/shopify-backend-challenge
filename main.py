import requests
import json

def read_data(specific_url):
    """
    Get menu information on the current page
    :param specific_url: URL for specific page
    :return: Response in JSON format
    """
    try:
        r = requests.get(specific_url)
    except requests.exceptions.RequestException as e:
        print e
    return r.json()

def build_menu(url):
    """
    Builds the entire menu spanned onto separate pages into a list
    :param url: general URL
    :return: list menu_list
    """
    menu_list = []
    page = 1
    json_data = read_data(url + str(page))
    pagination = json_data['pagination']
    per_page = pagination['per_page']
    total = pagination['total']
    while(per_page * (page-1) <= total):
        current_url = url + str(page)
        json_data = read_data(current_url)
        nodes = json_data['menus']
        for node in nodes:
            menu_list.append(node)
        page+=1
    return menu_list

def get_node(id, list):
    """
    Uses list comprehension to get item within list from its IDs
    Assumes there are no duplicate IDs
    :param id: ID to look for
    :param list: list in which we are looking for
    :return: item corresponding to list
    """
    return (item for item in list if item["id"] == id).next()

def is_cyclic(menu_list,root,menus):
    """

    :param menu_list:
    :param root:
    :param menus:
    :return:
    """
    visited = set()
    children = []
    def visit(vertex):
        """
        Recursively look through the graph to find circular reference.
        Saves visited children
        :param vertex: starting point, which is in this case the root
        :return:
        """
        visited.add(vertex['id'])
        children.append(vertex['id'])
        for neighbour in vertex['child_ids']:
            if neighbour in visited or visit(get_node(neighbour,menu_list)):
                return True
        visited.remove(vertex['id'])
        return False
    cyclic = visit(root)
    output = build_output(children)
    if(cyclic):
        menus['invalid_menus'].append(output)
    else:
        menus['valid_menus'].append(output)

def validate(menu_list,menus):
    """
    Validate whether or not there is a cyclical reference
    :param menu_list:
    :param menus:
    :return:
    """
    for node in menu_list:
        if 'parent_id' not in node:
            is_cyclic(menu_list,node,menus)

def build_output(list):
    """
    Build output in format with root_id and children separated
    :param list: one instance of a menu
    :return: output in desired format
    """
    output = {}
    output['children'] = list[1:]
    output['root_id'] = list[0]
    return output

def main():
    url = 'https://backend-challenge-summer-2018.herokuapp.com/challenges.json?id=1&page='
    menus = {
        'invalid_menus' : [],
        'valid_menus' : []
    }
    menu = build_menu(url)
    validate(menu,menus)
    print(menus)

if __name__ == '__main__':
    main()