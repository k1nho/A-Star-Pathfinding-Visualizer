import pygame
from queue import PriorityQueue
import math

# set the window height and width
WIDTH = 800
WINDOW = pygame.display.set_mode((WIDTH, WIDTH))
# set caption
pygame.display.set_caption("A* Pathfinder Visualizer")
# colors
GREEN = (0, 255,0)
RED = (255, 0, 0)
BLUE = (0,255,0)
YELLOW = (255,255,0)
BLACK =(0,0,0)
WHITE =(255,255,255)
PURPLE = (128,0,128)
ORANGE = (255,165,0)
TURQUOISE = (64,224,208)
GREY = (128,128,128)

# cell object to represent a cell on the grid
class Cell:
	# constructor for the Cell class
	def __init__(self, row, col, width, total_rows):
		self.row = row
		self.col = col
		self.width = width
		self.total_rows = total_rows
		self.x = row * width
		self.y = col * width
		self.color = WHITE
		self.neightbors = []

	# get the position of the cell
	def get_pos(self):
		return self.row, self.col
	# function to check if a cell is occupied
	def is_occupied(self):
		return self.color == RED
	# check if a cell is open
	def is_open(self):
		return self.color == GREEN
	# check if a cell is part of a barrier
	def is_barrier(self):
		return self.color == BLACK
	# check if a cell is the starting point
	def is_start(self):
		return self.color == ORANGE
	# check if a cell is the end point
	def is_end(self):
		return self.color == TURQUOISE
	# set a cell to to non-occupied
	def reset(self):
		self.color = WHITE
	#set a cell to be open
	def make_open(self):
		self.color = GREEN
	# set a cell to be ocuppied
	def make_occupied(self):
		self.color = RED
	# set a cell to be part of a barrier
	def make_barrier(self):
		self.color = BLACK
	# set the cell to be the start
	def make_start(self):
		self.color  = ORANGE
	# set the cell to be the end
	def make_end (self):
		self.color = TURQUOISE
	def make_path(self):
		self.color = PURPLE

	def draw_cell(self, win):
		pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

	def update_neightbors(self, grid):
		
		self.neightbors = []
		# check the down neightbor
		if self.row < self.total_rows -1 and not grid[self.row + 1][self.col].is_barrier():
			self.neightbors.append(grid[self.row + 1][self.col])
		# check the up neightbor
		if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():
			self.neightbors.append(grid[self.row - 1][self.col])
		# check the right neightbor
		if self.col < self.total_rows -1 and not grid[self.row][self.col +1].is_barrier():
			self.neightbors.append(grid[self.row][self.col + 1])
		# check the left neightbor
		if self.col > 0 and not grid[self.row][self.col -1].is_barrier():
			self.neightbors.append(grid[self.row][self.col -1])

	def __lt__(self, other):
		return False
# heuristic function
def h(point1,point2):
	# coordinates for the points
	x1, y1 = point1
	x2, y2 = point2
	# return the approximate distance to a point
	return abs(x1 - x2) + abs(y1 - y2)

def create_path(path, current, draw):
	while current in path:
		current = path[current]
		current.make_path()
		draw()

def a_star_pathfinding(draw, grid, start_pos, endpoint):
	# count 
	count = 0
	# create the open set with a priority queue and a copy set to keep track of our node
	open_set = PriorityQueue()
	# add the start node with the f(n) score in the open set
	open_set.put((0, count, start_pos))
	# set to keep track of the path (backtracking to the correct path)
	path = {}
	# g_values
	g_values = {cell :float("inf") for row in grid for cell in row}
	g_values[start_pos] = 0
	# set the heuristic
	f_values = {cell: float("inf") for row in grid for cell in row}
	f_values[start_pos] = h(start_pos.get_pos(), endpoint.get_pos())

	open_hash_set = {start_pos}

	# run until the open set is empty
	while not open_set.empty():
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit() 
		# keep track of current node and remove from the copy set
		current = open_set.get()[2]
		open_hash_set.remove(current)

		if current == endpoint:
			create_path(path, endpoint, draw)
			endpoint.make_end() 
			return True

		for node_neightbor in current.neightbors:
			# record the current g_score and add 1 to take into account the next node
			g_val = g_values[current] + 1

			if g_val < g_values[node_neightbor]:
				path[node_neightbor] = current
				g_values[node_neightbor] = g_val
				f_values[node_neightbor] = g_val + h(node_neightbor.get_pos(), endpoint.get_pos())

				if node_neightbor not in open_hash_set:
					count +=1
					open_set.put((f_values[node_neightbor], count, node_neightbor))
					open_hash_set.add(node_neightbor)
					node_neightbor.make_open()
		draw()

		if current != start_pos:
			current.make_occupied()

	return False

# create grid
def grid(rows, width):
	# array for all the cells
	grid =[]
	# width of each cell
	cell_width = width // rows

	for x in range(rows):
		grid.append([])
		for y in range(rows):
			cell = Cell(x,y,cell_width,rows)
			grid[x].append(cell)

	return grid
# UI for grid
def draw_grid(win, rows, width):
	cell_width = width // rows
	# horizontal lines drawn
	for i in range(rows):
		pygame.draw.line(win, GREY, (0, i * cell_width), (width, i *cell_width))
		# vertical lines
		for j in range(rows):
			pygame.draw.line(win, GREY, (j*cell_width, 0), (j *cell_width, width))
# UI for canvas 
def draw(win, rows, width, grid):
	# fill the window with white 
	win.fill(WHITE)

	for row in grid:
		for cell in row:
			cell.draw_cell(win)

	draw_grid(win,rows, width)
	# update the display
	pygame.display.update()

# function to determine the cell clicked by the mouse
def position_click(pos, rows, width):

	cell_width = width // rows
	y, x = pos

	col = x //cell_width
	row = y // cell_width

	return row, col

def main(win, width):

	ROWS = 50
	new_grid = grid(ROWS, width)

	start_pos = None
	endpoint = None
	run = True

	while run:
		draw(win, ROWS, width, new_grid)
		# check events
		for event in pygame.event.get():
			# check if user quit
			if event.type  == pygame.QUIT:
				run = False

			# left click
			if pygame.mouse.get_pressed()[0]:
				pos = pygame.mouse.get_pos()
				row, col = position_click(pos, ROWS, width)
				cell = new_grid[row][col]

				# check if the start point has been set
				if not start_pos and cell != endpoint:
					start_pos = cell
					start_pos.make_start()

				# check if the endpoint has been set
				elif not endpoint and cell != start_pos:
					endpoint = cell
					endpoint.make_end()

				# if the start point and the endpoint has been set
				elif cell != start_pos and cell != endpoint:
					cell.make_barrier()

			# right click
			elif pygame.mouse.get_pressed()[2]:
				pos = pygame.mouse.get_pos()
				row, col = position_click(pos, ROWS, width)
				cell = new_grid[row][col]
				cell.reset()

				if cell == start_pos:
					start_pos = None
				if cell == endpoint:
					endpoint = None

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE and start_pos and endpoint:
					for row in new_grid:
						for cell in row:
							cell.update_neightbors(new_grid)

					a_star_pathfinding(lambda: draw(win, ROWS, width, new_grid), new_grid , start_pos, endpoint)

				if event.key == pygame.K_c:
					start_pos = None
					endpoint = None
					new_grid = grid(ROWS, width)

	# end the visualizer once the x is clicked
	pygame.quit()

main(WINDOW, WIDTH)





