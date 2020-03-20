
from room import Room
from player import Player
from world import World
from util import Stack, Queue  # These may come in handy
from ast import literal_eval
import random

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

# Print an ASCII map
world.print_rooms()

# Initialize a player in the world at starting toom 0
player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []
#empty visited dict 
visited = {}

from util import Stack, Queue, Graph  # These may come in handy

#Step 1) Instantiate Graph to traverse
g = Graph()

#Step 2: Depth first traversal to create the graph (see util.py for code)
g.dft(world.starting_room)

#Step 3: Opposte directions
def reverse_path(dir):
    opposite_directions = {
    "n": "s",
    "s": "n",
    "w": "e",
    "e": "w"
    }
    return opposite_directions[dir]

def rand_neighbor(self, neighbors):
    return random.choice(neighbors)


#Step 3: Find the most efficient path 
# Loop until you've *VISITED* all the rooms in the graph
# Add rooms --> going forward 
def traverse(player):
    #init queue
    q = Queue()
    #init set for visited rooms w list of moves
    visited = set()

    #add player's current room to the queue - FIFO 
    q.enqueue([player.current_room.id])

    #while the queue is not empty
    while q.size()>0:
        print('****THIS IS THE CURRENT QUEUE', q)
        #dequeue first path from the queue
        path = q.dequeue()
        print('heres the path', path)
        # keep track of last room visited
        last_room = path[-1]
        print('heres the last room', last_room)

        if last_room not in visited:
            #add to list of visited
            visited.add(last_room)
            #get exits
            #find all exits ['n', 's', 'w', 'e']
            room_exits= world.rooms[last_room].get_exits()
            neighbors = g.get_neighbors(last_room) #returns {'n': 1, 's': 5, 'w': 7, 'e': 3}

            print('all neighbors', neighbors)
            print('len of room exits', len(room_exits))
                
            print("**************", room_exits[0])
            print("ALL OF THE LENGHTS!", len(visited), len(world.rooms))
            if len(visited) == len(world.rooms):
                return visited
            else: 
                #loop through graph til dead end
                stored_directions=[]

                #  LET'S ENQUEUE A PATH TO ALL OF IT'S NEIGHBORS!!
                for dir in neighbors:
                    #what room is to that direction?
                    next_room = player.current_room.get_room_in_direction(dir)

                    print('here is the new room ', next_room)
                    print('neighbor', dir)

                    next_room_id = neighbors[dir]
                    print('next room id', next_room_id)
                            
                    new_rooms = path + [next_room_id]
                    print('new rooms', new_rooms)
                            
                    #if the next room is NOT in our visited set....
                    if next_room_id not in visited: 

                        print(f'whats in visited right now?------> visited:{visited}, next_room_id:{next_room_id}')
                        #if our next room is not in visited, what do we do? What's in visited right now?
                        ##path right now is just our path to 0. We want to add our next room we travelled to, [5][7] etc
                        print('path and next room', path, next_room_id)
                        q.enqueue(list(path) +[next_room_id])  #enqueue adds to the BACK of the line, we're adding the next id to the back of the queue

                        #After we add the queue [0, 7] then we must keep going right? keep enqueuing the path until we hit a dead end?

                        # visited[next_room_id] = path
                        #Once we've added that to the queue, we want to 
                        print('************************* here is the queue AFTER', q)
                        print('visited after', visited)
        return visited    
    
'''
Player starts at room 0
Run checks against 499 rooms - so while the len of visited is less than 499
rooms are added to the visited list once this occurs
In the event of a dead end, use reversePath to make our way back
add reversePath rooms to total traversal list as well 
'''

opposite_directions = {
    'n':'s',
    's':'n',
    'e':'w',
    'w':'e'
}

traversal_graph={}

##DFT to end end, then BFS to nearest room with an unexplored exit 
print('vertices', len(g.vertices))
print('room graph len', len(room_graph))

traverse(player)
    

# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

print(f"Moves: {len(traversal_path)}")
count=0
for move in traversal_path:
    count+=1
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
