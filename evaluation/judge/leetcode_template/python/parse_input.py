from leetcode_class import construct_ListNode_from_list, construct_Node_from_list, construct_TreeNode_from_list

def parse_bool(input_str):
    ret = eval(input_str)
    if isinstance(ret, bool):
        return ret
    else:
        raise ValueError(f"input_str: {input_str} is not a bool")

def parse_float(input_str):
    return float(input_str)

def parse_int(input_str):
    return int(input_str)

def parse_str(input_str):
    if not isinstance(input_str, str):
        raise ValueError(f"input_str: {input_str} is not a str")
    return input_str

def parse_treeNode(input_str):
    data_list = eval(input_str)
    return construct_TreeNode_from_list(data_list)

def parse_listNode(input_str):
    data_list = eval(input_str)
    return construct_ListNode_from_list(data_list)

def parse_node(input_str):
    data_list = eval(input_str)
    return construct_Node_from_list(data_list)

def parse_list_bool(input_str):
    data_list = eval(input_str)
    for data in data_list:
        if not isinstance(data, bool):
            raise ValueError(f"input_str: {input_str} is not a list of bool")
    return data_list

def parse_list_float(input_str):
    data_list = eval(input_str)
    ret = []
    for data in data_list:
        if isinstance(data, int):
            ret.append(float(data))
        elif isinstance(data, float):
            ret.append(data)
        else:
            raise ValueError(f"input_str: {input_str} is not a list of float")
    return ret

def parse_list_int(input_str):
    data_list = eval(input_str)
    ret = []
    for data in data_list:
        if isinstance(data, int):
            ret.append(data)
        else:
            raise ValueError(f"input_str: {input_str} is not a list of int")
    return ret

def parse_list_str(input_str):
    data_list = eval(input_str)
    for data in data_list:
        if not isinstance(data, str):
            raise ValueError(f"input_str: {input_str} is not a list of str")
    return data_list

def parse_list_treeNode(input_str):
    data_list = eval(input_str)
    ret = []
    for data in data_list:
        ret.append(construct_TreeNode_from_list(data))
    return ret

def parse_list_listNode(input_str):
    data_list = eval(input_str)
    ret = []
    for data in data_list:
        ret.append(construct_ListNode_from_list(data))
    return ret

def parse_list_node(input_str):
    data_list = eval(input_str)
    ret = []
    for data in data_list:
        ret.append(construct_Node_from_list(data))
    return ret

def parse_list_list_bool(input_str):
    data_list = eval(input_str)
    ret = []
    for data in data_list:
        ret.append(parse_list_bool(data))
    return ret

def parse_list_list_float(input_str):
    data_list = eval(input_str)
    ret = []
    for data in data_list:
        ret.append(parse_list_float(data))
    return ret

def parse_list_list_int(input_str):
    data_list = eval(input_str)
    ret = []
    for data in data_list:
        ret.append(parse_list_int(str(data)))
    return ret

def parse_list_list_str(input_str):
    data_list = eval(input_str)
    ret = []
    for data in data_list:
        ret.append(parse_list_str(str(data)))
    return ret

def parse_list_list_treeNode(input_str):
    data_list = eval(input_str)
    ret = []
    for data in data_list:
        ret.append(parse_list_treeNode(data))
    return ret

def parse_list_list_listNode(input_str):
    data_list = eval(input_str)
    ret = []
    for data in data_list:
        ret.append(parse_list_listNode(data))
    return ret

def parse_list_list_node(input_str):
    data_list = eval(input_str)
    ret = []
    for data in data_list:
        ret.append(parse_list_node(data))
    return ret
