from Tkinter import *

class GridDisplay(Canvas):
	def __init__(self, master,grid, w, h):
		Canvas.__init__(self, master, width=w, height=h)
		self.pack(fill=X, padx=20, pady=20)
		
		box_h = h/len(grid)
		box_w = w/len(grid[0])
	
		y_count = 0
		for line in grid:
			x_count = 0
			for entry in line:
				if entry == 0:
					self.create_rectangle(x_count*box_w, y_count*box_h, (x_count+1)*box_w, (y_count+1)*box_h, fill = 'white')
				elif entry == 1:
					self.create_rectangle(x_count*box_w, y_count*box_h, (x_count+1)*box_w, (y_count+1)*box_h, fill = 'black')
				x_count += 1
			y_count += 1