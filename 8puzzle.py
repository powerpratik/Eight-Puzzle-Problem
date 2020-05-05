
''' Copyright <2020> <Pratik>

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

'''

import pydot
from time import time

class Stack:
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop()

    def peek(self):
        return self.items[len(self.items) - 1]

    def size(self):
        return len(self.items)

class Puzzle:

    goal_state=[4,3,2,
                1,0,5,
                6,7,8]

    num_of_instances=0
    def __init__(self,state,parent,action,depth):
        self.parent=parent
        self.state=state
        self.action=action
        self.depth=depth
        if self.goal_test():
            color="blue"
        elif self.depth>=5:
            color="grey"
        else:
            color="green"
        self.graph_node = pydot.Node(str(self), style="filled", fillcolor=color)
        Puzzle.num_of_instances+=1

    def display(self):
        list=self.state

        string=""

        for i in range(9):
            if (i + 1) % 3 != 0:
                if list[i]==0:
                    string += ("|   ")
                else:
                    string+=("| %d "% list[i])
            else:
                if list[i]==0:
                    string += ("|   \n")
                else:
                    string+=("| %d |\n" %list[i])
        string+="\n"
        return string

    def __str__(self):
        return self.display()

    def goal_test(self):
        if self.state == self.goal_state:
            return True
        return False

    @staticmethod
    def check_valid_moves(i,j):
        valid_move = ['UP', 'DOWN', 'LEFT', 'RIGHT']
        if i == 0:  # up is disable
            valid_move.remove('UP')
        elif i == 2:  # down is disable
            valid_move.remove('DOWN')
        if j == 0:
            valid_move.remove('LEFT')
        elif j == 2:
            valid_move.remove('RIGHT')
        return valid_move

    def generate_child(self):
        children=[]
        x = self.state.index(0)
        i = int(x / 3)
        j = int(x % 3)
        valid_moves=self.check_valid_moves(i,j)
        depth=self.depth+1

        for action in valid_moves:
            new_state = self.state[:]
            if action is 'UP':
                new_state[x], new_state[x-3] = new_state[x-3], new_state[x]
            elif action is 'DOWN':
                new_state[x], new_state[x+3] = new_state[x+3], new_state[x]
            elif action is 'LEFT':
                new_state[x], new_state[x-1] = new_state[x-1], new_state[x]
            elif action is 'RIGHT':
                new_state[x], new_state[x+1] = new_state[x+1], new_state[x]
            children.append(Puzzle(new_state,self,action,depth))
        return children

    def find_solution(self):
        solution = []
        solution.append(self.action)
        path = self
        while path.parent != None:
            path = path.parent
            solution.append(path.action)
        solution = solution[:-1]
        solution.reverse()
        return solution

def index(graph):
    graphlegend = pydot.Cluster(graph_name="legend", label="Legend", fontsize="20", color="red",
                                fontcolor="blue", style="filled", fillcolor="white")

    processed_node = pydot.Node('Processed node', shape="plaintext")
    graphlegend.add_node(processed_node)
    depth_lnode = pydot.Node("Depth limit reached", shape="plaintext")
    graphlegend.add_node(depth_lnode)
    gol_node = pydot.Node('Goal Node', shape="plaintext")
    graphlegend.add_node(gol_node)

    node1 = pydot.Node("1", style="filled", fillcolor="green", label="")
    graphlegend.add_node(node1)
    node2 = pydot.Node("2", style="filled", fillcolor="grey", label="")
    graphlegend.add_node(node2)
    node3 = pydot.Node("3", style="filled", fillcolor="blue", label="")
    graphlegend.add_node(node3)

    graph.add_subgraph(graphlegend)
    graph.add_edge(pydot.Edge(processed_node, depth_lnode, style="invis"))
    graph.add_edge(pydot.Edge(depth_lnode, gol_node, style="invis"))

    graph.add_edge(pydot.Edge(node1, node2, style="invis"))
    graph.add_edge(pydot.Edge(node2, node3, style="invis"))



def dfs(initial_state):
    graph = pydot.Dot(graph_type='digraph', label="8 Puzzle State Space (DFS)", fontsize="30", color="red",
                      fontcolor="red", style="filled", fillcolor="black")
    start_node = Puzzle(initial_state, None, None,0)
    if start_node.goal_test():
        return start_node.find_solution()
    s=Stack()
    s.push(start_node)
    explored=[]
    print("The starting node is \ndepth=%d\n" % start_node.depth)
    print(start_node.display())
    while not(s.isEmpty()):
        node=s.pop()
        print("the node selected to expand is\n")
        print("depth=%d\n" % node.depth)
        print(node.display())
        explored.append(node.state)
        graph.add_node(node.graph_node)
        if node.parent:
            graph.add_edge(pydot.Edge(node.parent.graph_node, node.graph_node,label=str(node.action)))
        if node.depth<5:
            children=node.generate_child()
            print("Childrens:\n")
            for child in children:
                if child.state not in explored :
                    print("depth=%d\n"%child.depth)
                    print(child.display())
                    if child.goal_test():
                        print("This is the goal state")
                        graph.add_node(child.graph_node)
                        graph.add_edge(pydot.Edge(child.parent.graph_node, child.graph_node, label=str(child.action)))
                        index(graph)
                        graph.write_png('8puzzlestate.png')
                        return child.find_solution()
                    s.push(child)
        else:
            print("Depth limit exceeded, so we don't expand this node.\n")
    return

def main():
    #
    s = Stack()
    explored = []
    #InitialState
    initial_state= [3, 1, 2,
                    4, 0, 5,
                    6, 7, 8]

    Puzzle.num_of_instances=0
    t0=time()
    solution=dfs(initial_state)
    t1=time()-t0
    print('Solution:', solution)
    print('space:',Puzzle.num_of_instances)
    print('time:',t1,"seconds")


main()

''' Copyright <2020> <Pratik>

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

'''

