#Tkinter stuff for GUI
from Tkinter import Tk, Menu, Canvas, SUNKEN, StringVar, Label, W, LEFT, GROOVE, BooleanVar
import tkFileDialog
import tkMessageBox
import tkSimpleDialog
from utils import DimensionsDialog

#For image saving
from PIL import Image
import os

import logging

#Yapsy for plug-ins
from yapsy.PluginManager import PluginManager

#Internal functions for handling cellular automata
from CATools import __version__, __author__, __application_name__
from CATools import load_rules, evolve_system, evolve_system_multi, build_blank_grid, build_default_start_row
from CATools import build_random_start_row

from config import DisplayConfiguration

disp_logger = logging.getLogger(__name__)
if not disp_logger.handlers:
    ch = logging.StreamHandler()
    disp_logger.addHandler(ch)
    disp_logger.setLevel(logging.INFO)

disp_logger.info('Cellular Automata display library loading.')


class GridDisplay(Canvas):
    ALLOWED_COLORS = ['black', 'white', 'red', 'green', 'blue', 'dark green', 'yellow', 'gray', 'orange', 'navy',
                      'cyan', 'goldenrod', 'gold', 'dim gray', 'pink', 'purple']

    def __init__(self, master, grid, w, h, *args, **kwargs):
        Canvas.__init__(self, master, *args, **kwargs)
        self.max_width = w
        self.max_height = h
        self.width = w
        self.height = h
        self._fill_color = 'black'
        self._bg_color = 'white'
        self._grid_line_width = 1
        self.draw_grid(grid)

    def set_bg_color(self, new_color):
        self._bg_color = new_color

    def set_fill_color(self, new_color):
        self._fill_color = new_color

    def set_grid_lines(self, on=True):
        self._grid_line_width = 1 if on else 0

    def draw_grid(self, grid):
        self.clear_canvas()
        box_h = self.max_height / len(grid)
        box_w = self.max_width / len(grid[0])
        self.width = box_w * len(grid[0])
        self.height = box_h *len(grid)
        y_count = 0
        for line in grid:
            x_count = 0
            for entry in line:
                if entry == 0:
                    self.create_rectangle(x_count * box_w, y_count * box_h, (x_count + 1) * box_w,
                                          (y_count + 1) * box_h, fill=self._bg_color, width=self._grid_line_width)
                elif entry == 1:
                    self.create_rectangle(x_count * box_w, y_count * box_h, (x_count + 1) * box_w,
                                          (y_count + 1) * box_h, fill=self._fill_color, width=self._grid_line_width)
                x_count += 1
            y_count += 1
        self.update()
        self.config(width=self.width, height=self.height)

    def clear_canvas(self):
        self.delete("all")


class CellularAutomataMain(Tk):
    GRID_WIDTH_PX = DisplayConfiguration.CA_CANVAS_MAX_PIX_X
    GRID_HEIGHT_PX = DisplayConfiguration.CA_CANVAS_MAX_PIX_Y

    def __init__(self, width_cells=DisplayConfiguration.DEFAULT_WIDTH, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.resizable(width=False, height=False)
        self.state = {'rules': None, 'rules_file': None, 'grid': None}

        self.random_start = BooleanVar(self)
        self.random_start.trace('w', self.random_start_callback)

        #Load blank grid
        self.width_cells = width_cells
        self.height_cells = width_cells  # Default setting should probably have the grid be square.
        canvas_width = self.GRID_WIDTH_PX-80
        canvas_height = self.GRID_HEIGHT_PX-80
        self.state['grid'] = build_blank_grid(width_cells, width_cells)
        self.grid_display = GridDisplay(self, self.state['grid'],
                                        self.GRID_WIDTH_PX, self.GRID_HEIGHT_PX,
                                        width=canvas_width, height=canvas_height, relief=GROOVE, bd=4)
        self.grid_display.grid(row=0, column=0, padx=20, pady=20)

        #Build top menus
        self.menubar = Menu(self)
        try:
            self.config(menu=self.Menu)
        except AttributeError:
            self.tk.call(self, 'config', '-menu', self.menubar)
        self.file_menu = Menu(self, tearoff=False)
        self.file_menu.add_command(label="Load Ruleset", command=self.load_dialogue)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Save Automata (Image)", command=self.save_image_dialogue)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Quit", command=self.quit)
        self.menubar.add_cascade(menu=self.file_menu, label='File')

        self.config_menu = Menu(self, tearoff=False)
        self.config_menu.add_command(label='Set Dimensions', command=self.config_dimensions)
        self.config_menu.add_checkbutton(label='Set Grid Wrap')
        self.config_menu.add_checkbutton(label='Random Start Row', variable=self.random_start)
        self.bg_color_menu = self.build_selector_menu(GridDisplay.ALLOWED_COLORS, self.grid_display.set_bg_color,
                                                      lambda: self.grid_display.draw_grid(self.state['grid']), 'white')
        self.fill_color_menu = self.build_selector_menu(GridDisplay.ALLOWED_COLORS, self.grid_display.set_fill_color,
                                                        lambda: self.grid_display.draw_grid(self.state['grid']), 'black')
        self.config_menu.add_cascade(menu=self.bg_color_menu, label="Set Background Color...")
        self.config_menu.add_cascade(menu=self.fill_color_menu, label="Set Fill Color...")
        self.config_menu.add_separator()
        self.config_menu.add_command(label='Configure Plug-ins')
        self.plugin_menu = Menu(self)
        self.config_menu.add_cascade(menu=self.plugin_menu, label="Plugins...")
        self.menubar.add_cascade(menu=self.config_menu, label='Configure')
        self.menubar.add_command(label="About", command=self.about)

        #Load status bar
        self.status_bar_var = StringVar(self)
        self.status_bar_var.set('Initialized.')
        self.status_bar = Label(self, textvar=self.status_bar_var, relief=SUNKEN, justify=LEFT, anchor=W)
        self.status_bar.grid(row=1, column=0, sticky="EW", padx=2, pady=2)


        #Build plugin manager
        disp_logger.info('Loading plug-in manager')
        self.status_bar_var.set('Loading plug-in manager...')
        self.plugin_manager = PluginManager()
        self.plugin_manager.setPluginPlaces(['../plugins/'])
        self.plugin_manager.collectPlugins()
        disp_logger.info('Plug-in manager loaded. {} plug-ins were loaded.'
                         ''.format(len(self.plugin_manager.getAllPlugins())))

    def load_dialogue(self):
        new_rule_filename = tkFileDialog.askopenfilename(parent=self, title='Open Rule File', defaultextension=".txt",
                                                         filetypes=[('Rules Files', '*.txt'), ('All Files', '*')])
        if not new_rule_filename:
            return
        try:
            self.load(new_rule_filename)
        except:
            disp_logger.exception('Faulted loading rules file!')

    def save_image_dialogue(self):
        automata_image_filename = tkFileDialog.asksaveasfilename(parent=self, title='Save Automata Image',
                                                                 defaultextension='.eps',
                                                                 filetypes=[('Postscript', '.eps'),
                                                                            ('PNG', '.png'),
                                                                            ('JPEG', '.jpg')])
        if not automata_image_filename:
            return
        try:

            #TODO: Should we be converting, or should I have a local image representation instead?
            if not automata_image_filename.endswith('.eps'):
                self.grid_display.postscript(file='tmp.eps')
                img = Image.open('tmp.eps')
                img.save(automata_image_filename)
                os.remove('tmp.eps')
            else:
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
        grid = []
        if self.random_start.get():
            start_row = build_random_start_row(self.width_cells)
        else:
            start_row = build_default_start_row(self.width_cells)
        grid.append(start_row)
        grid.extend(evolve_system_multi(start_row, rules, self.height_cells))
        self.state['grid'] = grid
        self.grid_display.draw_grid(grid)

    def config_dimensions(self):
        new_width, new_height = DimensionsDialog(self, title='Set Automata Dimensions',
                                                 prompt='Set Automata Dimensions', x_name='Width', y_name='Height',
                                                 x_default=self.width_cells, y_default=self.height_cells)
        if not new_width or not new_height:
            return
        disp_logger.info('Resizing automata to new width: {}, height: {}'.format(new_width, new_height))
        self.width_cells = new_width
        self.height_cells = new_height
        self._build_grid(self.state['rules'])


    def random_start_callback(self, *args):
        self._build_grid(self.state['rules'])

    @staticmethod
    def about():
        tkMessageBox.showinfo('About', '{app} ({ver})\nby {auth}, 2014'
                                       ''.format(ver=__version__, auth=__author__, app=__application_name__))

    def build_selector_menu(self, choices, set_fxn, update_fxn=None, default=None):
        new_menu = Menu(self)
        choice_map = {}

        def build_selector_trace(var):
            def callback(*args):
                set_fxn(choice_map[var.get()])
                if update_fxn:
                    update_fxn()
            return callback

        if not default:
            default = choices[0]
        new_var = StringVar(new_menu)
        new_var.set(str(default))
        new_var.trace('w', build_selector_trace(new_var))
        for choice in choices:
            choice_map[str(choice)] = choice
            new_menu.add_radiobutton(label=str(choice).capitalize(), variable=new_var, value=str(choice))
        return new_menu
