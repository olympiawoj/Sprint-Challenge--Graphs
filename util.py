
# Note: This Queue class is sub-optimal. Why?
# Bc it's not using a linked list, it's using an array
# denqueue add to front is inefficient - bc you have to reindex every el when you pop -> O(n)
# removing from front is expensive
# deqneueue removes from front 
# enqueue adds to back
import pprint

class Queue():
    def __init__(self):
        self.queue = []

    def enqueue(self, value):
        self.queue.append(value)
    def dequeue(self):
        if self.size() > 0:
            return self.queue.pop(0)
        else:
            return None
    def size(self):
        return len(self.queue)
    def __repr__(self):
        for el in self.queue:
            return f"{el}"

class Stack():
    def __init__(self):
        self.stack = []
    def push(self, value):
        self.stack.append(value)
    def pop(self):
        if self.size() > 0:
            return self.stack.pop()
        else:
            return None
    def size(self):
        return len(self.stack)

    # def __str__(self):
    #     return f"{el}"


#crate a graph
class Graph:
    """
    Represent a graph of ancestor nodes, mapping parents relationship to children
    """
    def __init__(self):
        self.vertices = {}
    def add_vertex(self, vertex_id):
        #add a vertext to the graph
        self.vertices[vertex_id] = {} #this is a object 
    def add_edge(self, v1, v2, direction):
        #add relationship/edge to graph between ancestor/descendent DIRECTED means 1  way
        if v1 in self.vertices and v2 in self.vertices:
            # print("*******************************")
            # print(f"vertices: {self.vertices}, v1: {v1}, v2: {v2}, direction: {direction}")
            #adds edge betwen v1 and v2 in north direction
            self.vertices[v1][direction] = v2
            print(f"Vertices: \n{pprint.pformat(self.vertices)}")
        else:
            raise ValueError("Value Error: Vertex does not exist")

    def get_neighbors(self, vertex_id):
        """
        Get all neighbors (edges) of a vertex.
        """
        if vertex_id in self.vertices:
            return self.vertices[vertex_id]
        else:
            raise ValueError("Error: Vertex does not exist")
    
    def dft(self,starting_vertex):
        """
        Print each vertex in depth-first order
        beginning from starting_vertex.

        """

        stack = Stack()
        # Add starting room
        stack.push(starting_vertex)
         #Initialize an empty set to store visited rooms
        visited = set()
         # Loop until the stack is empty 
        while stack.size() > 0:
            #Pop the first room class
            room = stack.pop()
            room_id = room.id
             # Add first room node to stack
            if room_id not in self.vertices:
                self.add_vertex(room_id)
            #Find exits, returns array of n s e w
            neighbors = room.get_exits()  
            #Loop over every direction 
            for direction in neighbors:
                new_room = room.get_room_in_direction(direction) 
                if new_room.id not in self.vertices:
                    self.add_vertex(new_room.id )
                self.add_edge(room_id, new_room.id , direction)
                #After adding to graph, add to stack
                if new_room.id not in visited:
                    stack.push(new_room)
            visited.add(room_id)
        
    def traverse_rooms_df(self):
        visited = set()
        directions = []
        stack = [(0, None)]
        current_room = 0

        visited.add(current_room)
        print('LENGTH****',len(g.vertices), visited)
        while len(visited) < len(self.vertices):
            valid_neighbors = self.get_neighbors(current_room, visited)
            print('here are the valid neighbors', valid_neighbors)
            if valid_neighbors:
                random_neighbor, random_direction = self.select_neighbor(
                    valid_neighbors)
                stack.append((current_room, random_direction))
                current_room = random_neighbor
                # print(current_room, random_direction.value)
                directions.append(random_direction.value)
                visited.add(current_room)
            elif stack:
                room, direction = stack.pop()
                current_room = room
                # print(current_room, self.get_reverse_direction(direction).value)
                directions.append(self.get_reverse_direction(direction).value)
        print('here are the directions', directions
        )
        return directions

    


