import copy, time
amt_expanded = 0
amt_generated = 1


class TreeNode: 
    def __init__(self, state, path_cost, v_row, v_col, moves, prev):
        self.state = state # State of the node
        self.path_cost = path_cost # Complete path cost
        self.v_row = v_row # Vacuum row
        self.v_col = v_col # Vacuum column
        self.moves = moves # Total moves
        self.closed = False
        self.children = []
        self.prev = prev


def goal_test(node):
    # Check squares for dirty rooms
    for row in node.state:
        for col in row: 
            if col == 1 or col == 3: return False
    return True

    
def expand(node):
    global amt_expanded, amt_generated
    amt_expanded += 1
    # List of generated nodes
    generated = []
    # Left, Right, Up, Down
    moves = [(0,-1), (0,1), (-1,0), (1,0)]
    costs = [1.0, 0.9, 0.8, 0.7]
    # For each move, check if the move after the action is valid, if so then add its state
    for move, cost in zip(moves, costs):
        after_move = (node.v_row + move[0], node.v_col + move[1]) # Determine pos after move
        if after_move[0] >= 0 and after_move[0] <= 3 and after_move[1] >= 0 and after_move[1] <= 4:
            new_state = copy.deepcopy(node.state) # Create duplicate of state
            new_state[node.v_row][node.v_col] -= 2 # Remove vacuum from previous square
            new_state[after_move[0]][after_move[1]] += 2 # Add vacuum to new square
            generated.insert(0, TreeNode(new_state, node.path_cost + cost, after_move[0], after_move[1], node.moves + 1, node)) # Push on
            amt_generated += 1
    # Add Suck
    new_state = copy.deepcopy(node.state)
    if node.state[node.v_row][node.v_col] == 3: new_state[node.v_row][node.v_col] -= 1
    generated.insert(0, TreeNode(new_state, node.path_cost + 0.6, node.v_row, node.v_col, node.moves + 1, node))
    amt_generated += 1
    return generated


def print_state(node):
    for row in node.state: print(row)
    print("e:", amt_expanded, "g:", amt_generated, "total cost:", node.path_cost, "moves:", node.moves)
    print("*************")


def get_priority_child(node):
    for child in node.children:
        if child.closed: continue
        else: return child
    return None


def generate_tree(root, allowed_depth):
    if allowed_depth == 0: return
    current_level = [root] # Starting tree level
    current_depth = 0
    while current_depth < allowed_depth:
        new_level = [] # New tree level
        # Generate children for each parent
        for parent in current_level:
            generated = expand(parent)
            parent.children.extend(generated)
            new_level.extend(generated)
        current_level = new_level
        current_depth += 1


def dls_tree(root, allowed_depth):
    stack = [root] # Begin stack
    children_closed = False # Variable to check if all children for a given node are closed
    while True:
        if len(stack) == 0: return None
        print_state(stack[-1])
        if goal_test(stack[-1]): return stack[-1] # If top stack node is goal, return it
        # If top stack node is at the max depth or all children are closed, then pop it
        if stack[-1].moves == allowed_depth or children_closed:
            children_closed = False
            stack[-1].closed = True
            stack.pop()
        else: 
            priority_child = get_priority_child(stack[-1]) # Get the priority child of top stack node 
            if priority_child is None: children_closed = True
            else: stack.append(priority_child) # Push highest priority node onto stack


def ids_tree(root):
    depth = 0
    while True:
        generate_tree(root, depth)
        result = dls_tree(root, depth)
        if result is not None: return result
        depth += 1
        # if depth == 2: quit()


def print_path(node):
    path = []
    current = node
    while True:
        path.insert(0, current)
        current = current.prev
        if current is None: break
    print("************* PATH *************")
    for path_node in path: print_state(path_node)


if __name__ == "__main__":
    start_time = time.time()
    # Indexed as row, column
    # 0 = clean 1 = dirty 2 = clean with vacuum 3 = dirty with vacuum
    state1 = [
        [0, 1, 0, 0, 0], 
        [0, 2, 0, 1, 0], 
        [0, 0, 0, 0, 1], 
        [0, 0, 0, 0, 0]]

    state2 = [
        [0, 1, 0, 0, 0], 
        [1, 0, 0, 1, 0], 
        [0, 2, 1, 0, 0], 
        [0, 0, 0, 0, 0]]

    # root = TreeNode(state1, 0, 1, 1, 0, None)
    root = TreeNode(state2, 0, 2, 1, 0, None)

    goal = ids_tree(root)
    print_path(goal)
    print("--- %s seconds ---" % (time.time() - start_time))


