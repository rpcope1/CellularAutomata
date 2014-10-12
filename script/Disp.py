from Tkinter import Tk, Menu, Canvas, SUNKEN
import tkFileDialog
import tkMessageBox

import logging

from CA import __version__, __author__, __application_name__
from CA import load_rules, evolve_system, evolve_system_multi, build_blank_grid, build_default_start_row

disp_logger = logging.getLogger(__name__)
if not disp_logger.handlers:
    ch = logging.StreamHandler()
    disp_logger.addHandler(ch)
    disp_logger.setLevel(logging.INFO)

disp_logger.info('Cellular Automata display library loading.')


class GridDisplay(Canvas):
    def __init__(self, master, grid, w, h):
        Canvas.__init__(self, master, width=w-80, height=h-80, relief=SUNKEN)
        self.grid(row=0, column=0, padx=20, pady=20)
        self.box_h = h / len(grid)
        self.box_w = w / len(grid[0])
        self.draw_grid(grid)

    def draw_grid(self, grid):
        y_count = 0
        for line in grid:
            x_count = 0
            for entry in line:
                if entry == 0:
                    self.create_rectangle(x_count * self.box_w, y_count * self.box_h, (x_count + 1) * self.box_w,
                                          (y_count + 1) * self.box_h, fill='white')
                elif entry == 1:
                    self.create_rectangle(x_count * self.box_w, y_count * self.box_h, (x_count + 1) * self.box_w,
                                          (y_count + 1) * self.box_h, fill='black')
                x_count += 1
            y_count += 1

    def clear_canvas(self):
        self.delete("all")


class CellularAutomataMain(Tk):
    GRID_WIDTH_PX = 800
    GRID_HEIGHT_PX = 800

    def __init__(self, width_cells = 120, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        self.state = {}

        #Build top menus
        self.menubar = Menu(self)
        try:
            self.config(menu=self.Menu)
        except AttributeError:
            self.tk.call(self, 'config', '-menu', self.menubar)
        self.file_menu = Menu(self)
        self.file_menu.add_command(label="Load", command=self.load_dialogue)
        self.file_menu.add_command(label="Quit", command=self.quit)
        self.menubar.add_cascade(menu=self.file_menu, label='File')
        self.menubar.add_command(label="About", command=self.about)

        #Load blank grid
        self.width_cells = width_cells
        self.grid_display = GridDisplay(self, build_blank_grid(width_cells, width_cells),
                                        self.GRID_WIDTH_PX, self.GRID_HEIGHT_PX)

    def load_dialogue(self):
        new_rule_file = tkFileDialog.askopenfilename(parent=self, title='Open Rule File', defaultextension=".txt",
                                                     filetypes=[('Rules Files', '*.txt'), ('All Files', '*')])
        try:
            self.load(new_rule_file)
        except:
            disp_logger.exception('Faulted loading rules file!')

    def load(self, rule_file):
        rules = load_rules(rule_file)
        self.state['rules'] = rules
        start_row = build_default_start_row(self.width_cells)
        grid = evolve_system_multi(start_row, rules, len(start_row) / 2)
        self.state['grid'] = grid
        self.grid_display.draw_grid(grid)

    @staticmethod
    def about():
        tkMessageBox.showinfo('About', '{app} ({ver})\nby {auth}, 2014'
                                       ''.format(ver=__version__, auth=__author__, app=__application_name__))
