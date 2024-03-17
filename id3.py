import math
from models import Node, TerminalNode

def check_if_its_the_leaf(table, class_name):
    all_classes = table[class_name].tolist()
    current_class = None
    num_in_one_class = 1
    for row_class in all_classes:
        if current_class == None:
            current_class = row_class
        elif current_class == row_class:
            num_in_one_class = num_in_one_class + 1
    if num_in_one_class == len(all_classes):
        return True
    else:
        return False


def get_entrophy(table, class_name):
    class_values = table[class_name].tolist()
    class_dictionary = {}
    for class_value in class_values:
        if class_value in class_dictionary:
            class_dictionary[class_value] += 1
        else:
            class_dictionary[class_value] = 1
    # print(class_dictionary)
    entrophy = 0
    count = len(table[class_name].tolist())
    dict_len = len(class_dictionary)
    for key, value in class_dictionary.items():
        pom = value / count
        entrophy += -pom * math.log(pom, dict_len)
    return entrophy


def init_class_dictionary(table, class_name):
    class_dict = {}
    for class_value in table[class_name]:
        class_dict[class_value] = 0
    return class_dict


def get_gain_for_attribute(table, class_name, column):
    column_class_dict = {}
    # global data
    count = 0
    for ind in table.index:
        class_division_dict = init_class_dictionary(table, class_name)
        column_value = table[column][ind]
        if column_value in column_class_dict:
            column_class_dict[column_value]["count"] += 1

        else:
            column_class_dict[column_value] = {}
            column_class_dict[column_value]["count"] = 1
            column_class_dict[column_value]["classes"] = class_division_dict
        class_value = table[class_name][ind]
        if class_value in column_class_dict[column_value]["classes"]:
            column_class_dict[column_value]["classes"][class_value] += 1
        else:
            column_class_dict[column_value]["classes"][class_value] = 1
        count += 1
    # print(column_class_dict)
    gain = 1
    for attribute_value in column_class_dict:
        local_count = 0
        # print(attribute_value)
        H = 0
        for class_value in column_class_dict[attribute_value]["classes"]:
            local_count += 1
            pom = int(column_class_dict[attribute_value]["classes"][class_value]) / int(
                column_class_dict[attribute_value]["count"]
            )
            # print()
            if pom != 0:
                H += -pom * math.log(pom, 2)
                H = round(H, 2)
                # print(H)
        gain -= local_count / count * H
    # print(gain)
    return gain


def get_highest_gain_attribute(table, class_name):
    enthropy = get_entrophy(table, class_name)
    # print(enthropy)
    gain_dict = {}
    for column in table.columns:
        if column != class_name:
            gain_dict[column] = get_gain_for_attribute(table, class_name, column)
    # print(gain_dict)
    max_attribute_gain = max(gain_dict.items(), key=lambda x: x[1])
    # print(max_attribute_gain[0])
    return max_attribute_gain[0]


def get_all_attribute_values(table, attribute_name):
    all_attribute_values = []
    for i in table[attribute_name]:
        if i not in all_attribute_values:
            all_attribute_values.append(i)
    return all_attribute_values


def id3_algorithm(table, class_name, node):
    if check_if_its_the_leaf(table, class_name):
        return TerminalNode(None, table[class_name].tolist()[0])
    else:
        highest_gain_attribute = get_highest_gain_attribute(table, class_name)
        # print(highest_gain_attribute)
        all_attribute_values = get_all_attribute_values(table, highest_gain_attribute)
        node = Node(table, highest_gain_attribute)
        children_names = []
        children_names_dict = {}
        count = 0
        for i in all_attribute_values:
            t1 = table[table[highest_gain_attribute] == i]
            t2 = t1.drop(columns=highest_gain_attribute)
            child = id3_algorithm(t2, class_name, node)

            if child.name not in children_names:
                node.add_child_and_branch(child, i)
                children_names.append(child.name)
                children_names_dict[child.name] = count
                count += 1
            else:
                current_name = str(node.branches[children_names_dict[child.name]])
                current_name = current_name + " or " + str(i)
                node.branches[children_names_dict[child.name]] = current_name
        return node


def print_tree(tree, prev, ind, unique_name, tree_diagraph):
    id = unique_name + str(tree.name) + str(ind)
    tree_diagraph.node(id, label=str(tree.name))
    if tree.children == []:
        return
    else:
        counter = 0
        for child in tree.children:
            print_tree(child, tree, counter, id, tree_diagraph)
            tree_diagraph.edge(
                id,
                id + str(tree.children[counter].name) + str(counter),
                label=str(tree.branches[counter]),
            )
            counter += 1
        return


def classify_unknown(data, tree, class_name):
    for index, row in data.iterrows():
        new_tree = tree
        # print(row)
        # print(new_tree.name)        
        while new_tree.children != []:
            count = 0
            for child in new_tree.children:
                if type(row[new_tree.name]) == bool:
                    if new_tree.branches[count] == row[new_tree.name]:
                        new_tree = child
                        break
                    else:
                        count += 1
                elif type(row[new_tree.name]) == int:
                    if str(row[new_tree.name]) in str(new_tree.branches[count]):
                        new_tree = child
                        break
                    else:
                        count += 1
                else:
                    if str(row[new_tree.name]) in new_tree.branches[count].split(" or "):
                        new_tree = child
                        break
                    count += 1
        data.loc[index, class_name] = new_tree.name
    return data

def get_accuracy_score(data):
    actual_result = list(data["prediction"])
    predicted_result = list(data["enter_elfak"])

    correct_predicted = 0
    for i, result in enumerate(actual_result):
        if (result == 'yes' and predicted_result[i] == True) or (result == 'not' and predicted_result[i] == False):
            correct_predicted += 1
    
    accuracy_score = correct_predicted / len(actual_result)
    return accuracy_score
