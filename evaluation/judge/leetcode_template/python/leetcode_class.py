class Node:
    def __init__(self, val = 0, neighbors = None):
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []

    def __str__(self):
        node_list = [self]
        output_list = []
        while node_list:
            node = node_list.pop(0)
            if node:
                node_list.extend(node.neighbors)
                output_list.append(node.val)
            else:
                output_list.append('None')
        return str(output_list)

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

    def __str__(self):
        output_list = []
        p = self
        while p:
            output_list.append(p.val)
            p = p.next
        return str(output_list)
        

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

    def __str__(self):
        node_list = [self]
        output_list = []
        while node_list:
            node = node_list.pop(0)
            if node:
                node_list.append(node.left)
                node_list.append(node.right)
                output_list.append(node.val)
            else:
                output_list.append(None)
        while output_list[-1] is None:
            output_list.pop()
        return str(output_list)


def construct_ListNode_from_list(data):
    if not data:
        return None
    head = ListNode(data[0])
    p = head
    for i in range(1, len(data)):
        p.next = ListNode(data[i])
        p = p.next
    return head

def print_ListNode(head):
    output_list = []
    p = head
    while p:
        output_list.append(p.val)
        p = p.next
    print(output_list)

def construct_TreeNode_from_list(data):
    if not data:
        return None
    root = TreeNode(data[0])
    node_list = [root]
    i = 1
    while i < len(data):
        node = node_list.pop(0)
        if i < len(data) and data[i] is not None:
            node.left = TreeNode(data[i])
            node_list.append(node.left)
        i += 1
        if i < len(data) and data[i] is not None:
            node.right = TreeNode(data[i])
            node_list.append(node.right)
        i += 1
    return root

def print_TreeNode(root):
    node_list = [root]
    output_list = []
    while node_list:
        node = node_list.pop(0)
        if node:
            node_list.append(node.left)
            node_list.append(node.right)
            output_list.append(node.val)
        else:
            output_list.append(None)
    while output_list[-1] is None:
        output_list.pop()
    print(output_list)

def construct_Node_from_list(data):
    if not data:
        return None
    node_list = [Node(data[0])]
    root = node_list[0]
    i = 1
    while i < len(data):
        node = node_list.pop(0)
        for j in range(len(data[i])):
            node.neighbors.append(Node(data[i][j]))
            node_list.append(node.neighbors[-1])
        i += 1
    return root

def print_Node(root):
    node_list = [root]
    output_list = []
    while node_list:
        node = node_list.pop(0)
        if node:
            node_list.extend(node.neighbors)
            output_list.append(node.val)
        else:
            output_list.append('None')
    print(output_list)

if __name__ == '__main__':
    # test TreeNode
    input_data1 = "[1,2,3,None,4]"
    input_data1 = eval(input_data1)
    root1 = construct_TreeNode_from_list(input_data1)
    print_TreeNode(root1)

    input_data2 = "[1,None,2,3]"
    input_data2 = eval(input_data2)
    root2 = construct_TreeNode_from_list(input_data2)
    print_TreeNode(root2)
    
    # test ListNode
    input_data3 = "[1,2,3,4,5,6,7,8,9,10,11,12,13]"
    input_data3 = eval(input_data3)
    head = construct_ListNode_from_list(input_data3)
    print_ListNode(head)