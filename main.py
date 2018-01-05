import requests


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
    while (per_page * (page - 1) <= total):
        current_url = url + str(page)
        json_data = read_data(current_url)
        nodes = json_data['menus']
        for node in nodes:
            menu_list.append(node)
        page += 1
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


def handle_cyclic_ref(specific_menu, root, menus):
    """
    Conduct the search through one specific menu and add it to its respective list
    based on the result (invalid or valid)
    :param specific_menu: one instance of a menu
    :param root: root of the menu
    :param menus: final output which contains all menus (invalid, valid)
    :return:
    """
    visited = set()
    children = set()
    root_id = root['id']

    def visit(vertex):
        """
        Recursively look through the graph to find circular reference.
        Saves visited children
        :param vertex: starting point, which is in this case the root
        :return:
        """
        children.add(vertex['id'])
        visited.add(vertex['id'])
        for neighbour in vertex['child_ids']:
            if neighbour in visited or visit(get_node(neighbour, specific_menu)):
                return True
        visited.remove(vertex['id'])
        return False

    cyclic = visit(root)
    if (cyclic):
        l = list(children)
        menus['invalid_menus'].append(build_output(root_id, l))
    else:
        l = [item for item in list(children) if item != root_id]
        menus['valid_menus'].append(build_output(root_id, l))


def validate(menu_list, menus):
    """
    Validate whether or not there is a cyclical reference
    :param menu_list:
    :param menus:
    :return:
    """
    for node in menu_list:
        # only start search at root
        if 'parent_id' not in node:
            handle_cyclic_ref(menu_list, node, menus)


def build_output(root, list):
    """
    Build output in format with root_id and children separated
    :param list: one instance of a menu
    :return: output in desired format
    """
    output = {}
    output['children'] = list
    output['root_id'] = root
    return output


def main():
    """
    Can run for both challenges, only "challenge_nb" needs to be changed
    :return: prints output
    """
    challenge_nb = '1'
    url = 'https://backend-challenge-summer-2018.herokuapp.com/challenges.json?id=' + challenge_nb + '&page='
    validated_menus = {
        'invalid_menus': [],
        'valid_menus': []
    }
    menu = build_menu(url)
    validate(menu, validated_menus)
    print(validated_menus)


if __name__ == '__main__':
    main()
