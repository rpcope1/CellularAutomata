from Tkinter import Tk, Menu, Canvas, SUNKEN, StringVar, Label, W, LEFT, GROOVE
import tkFileDialog
import tkMessageBox
import tkSimpleDialog

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
    def __init__(self, master, grid, w, h, *args, **kwargs):
        Canvas.__init__(self, master, *args, **kwargs)
        self.w = w
        self.h = h
        self.draw_grid(grid)

    def draw_grid(self, grid):
        box_h = self.h / len(grid)
        box_w = self.w / len(grid[0])
        y_count = 0
        for line in grid:
            x_count = 0
            for entry in line:
                if entry == 0:
                    self.create_rectangle(x_count * box_w, y_count * box_h, (x_count + 1) * box_w,
                                          (y_count + 1) * box_h, fill='white')
                elif entry == 1:
                    self.create_rectangle(x_count * box_w, y_count * box_h, (x_count + 1) * box_w,
                                          (y_count + 1) * box_h, fill='black')
                x_count += 1
            y_count += 1
        self.update()

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
        self.file_menu.add_command(label="Save Automata (Image)", command=self.save_image_dialogue)
        self.file_menu.add_command(label="Load", command=self.load_dialogue)
        self.file_menu.add_command(label="Quit", command=self.quit)
        self.menubar.add_cascade(menu=self.file_menu, label='File')

        self.config_menu = Menu(self)
        self.config_menu.add_command(label='Set Width', command=self.config_width)
        self.menubar.add_cascade(menu=self.config_menu, label='Configure')
        self.menubar.add_command(label="About", command=self.about)

        #Load blank grid
        self.width_cells = width_cells
        canvas_width = self.GRID_WIDTH_PX-80
        canvas_height = self.GRID_HEIGHT_PX-80
        self.grid_display = GridDisplay(self, build_blank_grid(width_cells, width_cells),
                                        self.GRID_WIDTH_PX, self.GRID_HEIGHT_PX,
                                        width=canvas_width, height=canvas_height, relief=GROOVE, bd=4)
        self.grid_display.grid(row=0, column=0, padx=20, pady=20)

        #Load status bar
        self.status_bar_var = StringVar(self)
        self.status_bar_var.set('Initialized.')
        self.status_bar = Label(self, textvar=self.status_bar_var, relief=SUNKEN, justify=LEFT, anchor=W)
        self.status_bar.grid(row=1, column=0, sticky="EW", padx=2, pady=2)


    def load_dialogue(self):
        new_rule_filename = tkFileDialog.askopenfilename(parent=self, title='Open Rule File', defaultextension=".txt",
                                                         filetypes=[('Rules Files', '*.txt'), ('All Files', '*')])
        try:
            self.load(new_rule_filename)
        except:
            disp_logger.exception('Faulted loading rules file!')

    def save_image_dialogue(self):
        automata_image_filename = tkFileDialog.asksaveasfilename(parent=self, title='Save Automata Image',
                                                                 defaultextension='.ps',
                                                                 filetypes=[('Postscript', '.ps')])
        try:
            self.grid_display.postscript(file=automata_image_filename)
            self.status_bar_var.set('Saved automata image file as: {}'.format(automata_image_filename))
        except:
            disp_logger.exception('Faulted saving automata image!')


    def load(self, rule_file):
        disp_logger.info('Attempting to load new rules file: {}'.format(rule_file))
        rules = load_rules(rule_file)
        self.state['rules'] = rules
        self.state['rules_file'] = rule_file
        self._build_grid(rules)
        self.status_bar_var.set('Loaded rules file: {}'.format(rule_file))

    def _build_grid(self, rules):
        start_row = build_default_start_row(self.width_cells)
        grid = evolve_system_multi(start_row, rules, self.width_cells)
        self.state['grid'] = grid
        self.grid_display.draw_grid(grid)

    def config_width(self):
        new_width = tkSimpleDialog.askinteger(parent=self, title='Set New Automata Width',
                                              initialvalue=self.width_cells,
                                              prompt='Set the width of cells for the representation',
                                              minvalue=1, maxvalue=self.GRID_WIDTH_PX/3)
        if new_width:
            self.width_cells = new_width
            self._build_grid(self.state['rules'])

    @staticmethod
    def about():
        tkMessageBox.showinfo('About', '{app} ({ver})\nby {auth}, 2014'
                                       ''.format(ver=__version__, auth=__author__, app=__application_name__))
