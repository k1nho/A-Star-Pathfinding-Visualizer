import pygame
from queue import PriorityQueue
import math

# set the window height and width
WIDTH = 800
WINDOW = pygame.display.set_mode((WIDTH, WIDTH))
# set caption
pygame.display.set_caption("A * pathfinder visualizer")
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

# particular position on the grid
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
		return self.color == PURPLE
	# set a cell to to non-occupied
	def reset(self):
		self.color == WHITE
	# set a cell to be ocuppied
	def make_occupied(self):
		self.color == RED
	# set a cell to be part of a barrier
	def make_barrier(self):
		self.color = BLACK
	# set the cell to be the start
	def make_start(self):
		self.color  = ORANGE
	# set the cell to be the end
	def make_end (self):
		self.color = PURPLE
	def make_path(self):
		self.color = TURQUOISE
	def draw_cell(self, win):
		pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))
	def update_neightbors(self, grid):

	def __lt__(self, other):
		return False

def h(point1,point2):
	# coordinates for the points
	x1, y1 = point1
	x2, y2 = point2
	# return the approximate distance to a point
	return abs(x1 - x2) + abs(y1 - y2)

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

def draw_grid(win, rows, width):
	cell_width = width // rows
	# horizontal lines drawn
	for i in range(rows):
		pygame.draw.line(win, GREY, (0, i * cell_width), (width, i *cell_width))
		# vertical lines
		for j in range(rows):
			pygame.draw.line(win GREY, (j*cell_width, 0), (j *cell_width, width))

def draw



