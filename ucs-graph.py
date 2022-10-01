# L, R, U, D, S in the queue

import copy, time
amt_expanded = 0
amt_generated = 1


class GraphNode: 
    def __init__(self, state, path_cost, v_row, v_col, moves, prev):
        self.state = state # State of the node
        self.path_cost = path_cost # Complete path cost
        self.v_row = v_row # Vacuum row
        self.v_col = v_col # Vacuum column
        self.moves = moves # Total moves
        self.prev = prev


# Priority queue based on lowest path_cost
class PriorityQueue: 
    def __init__(self):
        self.queue = []

    def __str__(self):
        return ' '.join([str(i) for i in self.queue])

    def isEmpty(self):
        return len(self.queue) == 0
    
    def insert(self, node):
        self.queue.append(node)

    def delete(self): 
        try: 
            min_val = 0
            for i in range(len(self.queue)):
                if self.queue[i].path_cost < self.queue[min_val].path_cost: 
                    min_val = i
                elif self.queue[i].path_cost == self.queue[min_val].path_cost:
                    if (self.queue[i].v_row < self.queue[min_val].v_row) or (self.queue[i].v_col < self.queue[min_val].v_col): 
                        min_val = i
            item = self.queue[min_val]
            del self.queue[min_val]
            return item
        except IndexError:
            print()
            exit()


def goal_test(node):
    # Check squares for dirty rooms
    for row in node.state:
        for col in row: 
            if col == 1 or col == 3: return False
    return True

    
def expand(node, closed):
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
            if str(new_state) not in closed: 
                generated.insert(0, GraphNode(new_state, node.path_cost + cost, after_move[0], after_move[1], node.moves + 1, node)) # Push on
                amt_generated += 1
    # Add Suck
    new_state = copy.deepcopy(node.state)
    if node.state[node.v_row][node.v_col] == 3: new_state[node.v_row][node.v_col] -= 1
    if str(new_state) not in closed:
        generated.insert(0, GraphNode(new_state, node.path_cost + 0.6, node.v_row, node.v_col, node.moves + 1, node))
        amt_generated += 1
    return generated

def print_state(node):
    for row in node.state: print(row)
    print("e:", amt_expanded, "g:", amt_generated, "total cost:", node.path_cost, "moves:", node.moves)
    print("*************")

def ucs_graph(root):
    closed = set()
    fringe = PriorityQueue()
    fringe.insert(root)
    # steps = 0
    while True:
        if fringe.isEmpty(): return 1 # Failure
        current = fringe.delete() # Dequeue highest priority node
        if str(current.state) in closed: continue
        print_state(current)
        # if steps == 5: break
        if goal_test(current): return current
        # Create new fringe with generated nodes
        closed.add(str(current.state))
        generated = expand(current, closed)
        for node in generated: fringe.insert(node)
        # steps += 1


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

    root = GraphNode(state1, 0, 1, 1, 0, None)
    # root = GraphNode(state2, 0, 2, 1, 0, None)

    goal = ucs_graph(root)
    print_path(goal)
    print("--- %s seconds ---" % (time.time() - start_time))

    