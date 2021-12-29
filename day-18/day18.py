import sys

class Node:

    def __init__(self, val=None, left=None, right=None, parent=None):
        self.val = val
        self.left = left
        self.right = right
        self.parent = parent

    def __str__(self):
        if self.val is None:
            return f"None"
        else:
            return f"{self.val}"


def create_tree(input_str):
    root_node, idx = create_tree_helper(input_str, idx=0)
    return root_node

def create_tree_helper(input_str : str, idx : int, parent:Node=None):
    if input_str[idx] == "[":
        new_node = Node(parent=parent)
        new_node.left, idx = create_tree_helper(input_str, idx + 1, new_node)
        new_node.right, idx = create_tree_helper(input_str, idx + 1, new_node)
        return new_node, idx + 1
    else:
        val = int(input_str[idx])
        new_node = Node(val=val, parent=parent)
        return new_node, idx + 1

def get_depth(root:Node, curr_depth=0):
    if root is None:
        return curr_depth - 1
    left_depth = get_depth(root.left, curr_depth+1)
    right_depth = get_depth(root.right, curr_depth+1)
    return max(left_depth, right_depth)

def get_exploding_node(root:Node):
    n = get_exploding_node_helper(root)
    return n.parent

def get_exploding_node_helper(root:Node, curr_depth=0) -> Node:
    if root is None:
        return None
    if curr_depth == 5:
        return root
    return get_exploding_node_helper(root.left, curr_depth + 1) or get_exploding_node_helper(root.right, curr_depth + 1)

def print_tree(root:Node, indent=0):
    if root is None:
        return
    if root.val is not None:
        print('\t'*indent + str(root.val))
    else:
        print('\t'*indent + 'r')
    print_tree(root.left,  indent + 1)
    print_tree(root.right, indent + 1)


def print_tree_compressed(root:Node, result:str=""):
    if root.val is not None:
        result += str(root.val)
        return result

    result += "["
    result = print_tree_compressed(root.left, result)
    result += ","
    result = print_tree_compressed(root.right, result)
    result += "]"
    return result

def get_inorder_vec(root:Node, vec):
    if root is None:
        return
    get_inorder_vec(root.left, vec)
    vec.append(root)
    get_inorder_vec(root.right, vec)

def explode_node(root:Node, target:Node):
    vec = []
    get_inorder_vec(root, vec)

    target_idx = vec.index(target)
    t_left = target_idx - 3
    t_right = target_idx + 3
    if t_left >= 0:
        vec[t_left].val += vec[target_idx].left.val
    if t_right < len(vec):
        vec[t_right].val += vec[target_idx].right.val

    new_node = Node(val=0, parent=target.parent)
    if target.parent.left == target:
        target.parent.left = new_node
    else:
        target.parent.right = new_node

def get_splitting_node(root:Node):
    vec = []
    get_inorder_vec(root, vec)
    for node in vec:
        if node.val is not None and node.val >= 10:
            return node
    return None

def split_node(node:Node):
    l_val = node.val // 2
    r_val = (node.val + 1) // 2

    new_node = Node(parent=node.parent)
    new_node.left = Node(val=l_val, parent=new_node)
    new_node.right = Node(val=r_val, parent=new_node)

    if node.parent.left == node:
        node.parent.left = new_node
    else:
        node.parent.right = new_node

def add_snailfish(root1:Node, root2:Node):
    root = Node(left=root1, right=root2)
    root1.parent = root
    root2.parent = root
    return root

def reduce(root):
    while reduce_step(root):
        pass

def reduce_step(root):
    if get_depth(root) >= 5:
        # print(f"Explode")
        node = get_exploding_node(root)
        explode_node(root, node)
        return True
    
    node = get_splitting_node(root)
    if node:
        # print(f"Split")
        split_node(node)
        return True
    
    return False


def calculate_magnitude(root:Node):
    if root is None:
        return 0
    if root.val is not None:
        return root.val

    return 3 * calculate_magnitude(root.left)  + 2 * calculate_magnitude(root.right)

def parse_input(fname):
    strs = []
    with open(fname) as file:
        for line in file.readlines():
            strs.append(line.strip())

    return strs


def main():
    fname = sys.argv[1]
    input_strs = parse_input(fname)

    root = None
    for input_str in input_strs:
        tmp_root = create_tree(input_str)
        if root is None:
            root = tmp_root
        else:
            root = add_snailfish(root, tmp_root)

        # print(print_tree_compressed(root))
        reduce(root)
        # print(print_tree_compressed(root))
    print(f"Final magnitude {calculate_magnitude(root)}")


    max_mag = 0
    for i, input_str1 in enumerate(input_strs):
        for j, input_str2 in enumerate(input_strs):
            if i == j:
                continue
            root1 = create_tree(input_str1)
            root2 = create_tree(input_str2)
            root = add_snailfish(root1, root2)
            reduce(root)
            magnitude = calculate_magnitude(root)
            max_mag = max(max_mag, magnitude)

    print(f"Max magnitude {max_mag}")



  



if __name__ == "__main__":
    main()