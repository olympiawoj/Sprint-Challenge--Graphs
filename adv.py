
from room import Room
from player import Player
from world import World
from util import Stack, Queue  # These may come in handy
from ast import literal_eval
import random
''' 
     possible dirs --> path
0 --> n, s, e, w --> n
1 --> n, s --> n n
2 --> s --> n n s
1 --> s --> n n s s
0 --> s e w --> n n s s s 
5 --> n, s --> n n s s s s 
6 --> n --> n n s s s s n
5 --> n --> n n s s s s n n 
0 --> e w --> n n s s s s n n w 
7 --> e w --> n n s s s s n n w w 
8 --> e --> n n s s s s n n w w e 
7 --> e --> n n s s s s n n w w e e
0 --> e --> n n s s s s n n w w e e e e
3 --> e w --> n n s s s s n n w w e e e e e
4 --> w --> n n s s s s n n w w e e e e e w
3 --> w -->n n s s s s n n w w e e e e e w w
0 --> ALL VISITED!! 
'''

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
# map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)
print("the rooms", world.rooms)
# Print an ASCII map
world.print_rooms()

# Initialize a player in the world at starting toom 0
player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []

from util import Stack, Queue, Graph  # These may come in handy

#Step 1) Instantiate Graph to traverse
g = Graph()

# #run depth first traversal to create the graph
# g.dft(world.starting_room)

opposite_directions = {
    'n':'s',
    's':'n',
    'e':'w',
    'w':'e'
}

def dft_recursive(starting_room):
    '''
    Should take a starting room 
    Use a dft + a visited dict to pick random directions and travel. 

    Keep dft'ing until we hit a dead end
    Once we hit a dead end, BFS for a '?' to find a room that hasn't been visited

    Repeat
    '''
        
    def add_to_path_recursive(room, visited=None):

        #add starting roomn node to visited
        visited.add(room.id)
        traversal_path=[] #should be ['n', 's', 'e', 'w']

        # will start at starting_room, and then keep looping to next room as it recurses
        for direction in room.get_exits():
            print(f"direction:{direction}, visited:{visited}, traversal_path:{traversal_path}")

            #Get next room 
            next_room = room.get_room_in_direction(direction)

            print(f"next room: {next_room.id}")
            print("***********************")

            if next_room.id not in visited:
                #Recurse path function - which will add the next_room to visited & stack
                next_room_path = add_to_path_recursive(next_room, visited)
                
                #Is there a path to the next room?
                if next_room_path: 
                    print(f"direction:{direction}, 'next room path: {next_room_path}, oppy dir:{opposite_directions[direction]} ")
                    #If there is, add create a new path to the room
                    #*splat operator unpacks an iterable
                    new_path = [direction, *next_room_path, opposite_directions[direction]]
                    print(f"new_path in IF: {new_path}"
                    )
                #If there's not a path to the next room, create a path with the oppy direction
                else:
                    new_path = [direction, opposite_directions[direction]]
                    print(f"new_path in ELSE: {new_path}")
                #Once all next_room.ids are in visited, merge the traversal_path and new_path
                traversal_path = [*traversal_path, *new_path]

        #if no other direction, return traversal path
        return traversal_path
    
    visited = set()
    traversal_path = add_to_path_recursive(starting_room, visited)
    print(f"traversal_path: {traversal_path}")
    return traversal_path

traversal_path = dft_recursive(world.starting_room)

# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
player.current_room.print_room_description(player)
while True:
    cmds = input("-> ").lower().split(" ")
    if cmds[0] in ["n", "s", "e", "w"]:
        player.travel(cmds[0], True)
    elif cmds[0] == "q":
        break
    else:
        print("I did not understand that command.")
