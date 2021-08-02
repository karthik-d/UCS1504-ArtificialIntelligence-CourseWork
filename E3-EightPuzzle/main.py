from copy import deepcopy
import time

INITIAL_STATE = (
	(7, 2, 4),
	(5, 0, 6),
	(8, 3, 1),
)

GOAL_STATE = (
	(0, 1, 2),
	(3, 4, 5),
	(6, 7, 8),
)

NUM_ROWS = len(INITIAL_STATE)
NUM_COLS = len(INITIAL_STATE[0])

class Queue:
	# [HEAD, ....... , TAIL]
	def __init__(self, data_list=None):
		self.data = list()
		self.size = 0
		if data_list is not None:
			self.data.extend(data_list)
			self.size = len(data_list)
    
	def enqueue(self, data_list):
		self.data.extend(data_list)
		self.size += len(data_list)

	def dequeue(self):
		if self.size == 0:
			return None
		self.size -= 1
		return self.data.pop(0)

	def get_contents(self):
		return self.data

	def is_empty(self):
		return self.size==0


def get_next_states(state):
	# Swap 0 with any of its neighbors

	def locate_empty_space():
		for i in range(NUM_ROWS):
			for j in range(NUM_COLS):
				if state[i][j] == 0:
					return i,j

	def make_state(initial, final):
		# By moving 0 from initial to final
		new_state = [list(row) for row in state]
		new_state[initial[0]][initial[1]] = state[final[0]][final[1]]
		new_state[final[0]][final[1]] = 0
		new_state = tuple(map(tuple, new_state))
		return new_state

	result = list()
	row, col = locate_empty_space()
	
	# Move left
	if (col-1)>-1:
		result.append(make_state((row, col), (row, col-1)))
	# Move right
	if (col+1)<NUM_COLS:
		result.append(make_state((row, col), (row, col+1)))

	# Move up
	if (row-1)>-1:
		result.append(make_state((row, col), (row-1, col)))
	# Move down
	if (row+1)<NUM_ROWS:
		result.append(make_state((row, col), (row+1, col)))
	
	return result

# Checking the next state generation function
for state in get_next_states(INITIAL_STATE):
	for row in state:
		print(row)
	print()


def is_goal_state(state):
	for i in range(NUM_ROWS):
		for j in range(NUM_COLS):
			if state[i][j] != GOAL_STATE[i][j]:
				return False 
	return True			

# Compare the current state of `this` direction search
# to the fringe states of `that` direction search
def intersection_test(this_state, that_fringe):
	
	def are_states_same(state_A, state_B):
		for i in range(NUM_ROWS):
			for j in range(NUM_COLS):
				if state_A[i][j] != state_B[i][j]:
					return False 
		return True 
	
	for state in that_fringe:
		if are_states_same(state, this_state):
			return True
	return False

def BFS():
	f_state_space = Queue([INITIAL_STATE])
	f_explored_states = set()

	while(not f_state_space.is_empty()):
		# Forward Search
		f_state = f_state_space.dequeue()
		if f_state not in f_explored_states:
			# Explore now
			f_explored_states.add(f_state)
			if is_goal_state(f_state):
				return f_state 
			fringe = get_next_states(f_state)
			f_state_space.enqueue(fringe)
	
	return False 

def bidirectional_BFS():

	f_state_space = Queue([INITIAL_STATE])
	f_explored_states = set()

	r_state_space = Queue([GOAL_STATE])
	r_explored_states = set()

	while(not f_state_space.is_empty() or not r_state_space.is_empty()):
		# Forward Search
		f_state = f_state_space.dequeue()
		if f_state not in f_explored_states:
			# Explore now
			f_explored_states.add(f_state)
			if intersection_test(f_state, r_state_space.get_contents()):
				return f_state 
			fringe = get_next_states(f_state)
			f_state_space.enqueue(fringe)

		# Reverse Search
		r_state = r_state_space.dequeue()
		if r_state not in r_explored_states:
			# Explore now
			r_explored_states.add(r_state)
			if intersection_test(r_state, f_state_space.get_contents()):
				return r_state 
			fringe = get_next_states(r_state)
			r_state_space.enqueue(fringe)
	
	return False 

time_ = time.time()
print(BFS())
print(time.time()-time_)
time_ = time.time()
print(bidirectional_BFS())
print(time.time()-time_)
			
