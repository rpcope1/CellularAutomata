#Tkinter stuff for GUI
try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk
import tkFileDialog
import tkMessageBox
import tkColorChooser
from CADialogs import DimensionsDialog

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

from CAGUI import MainCAFrame

from config import DisplayConfiguration, ApplicationConfiguration

app_logger = logging.getLogger(__name__)
if not app_logger.handlers:
    ch = logging.StreamHandler()
    app_logger.addHandler(ch)
    app_logger.setLevel(logging.INFO)

app_logger.info('Cellular Automata display library loading.')


class CellularAutomataMain(tk.Tk):
    GRID_WIDTH_PX = DisplayConfiguration.CA_CANVAS_MAX_PIX_X
    GRID_HEIGHT_PX = DisplayConfiguration.CA_CANVAS_MAX_PIX_Y

    def __init__(self, width_cells=DisplayConfiguration.DEFAULT_WIDTH, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.resizable(width=False, height=False)
        self.state = {'rules': None, 'rules_file': None, 'grid': None}

        self.random_start = tk.BooleanVar(self)
        self.random_start.trace('w', self.random_start_callback)

        #Load blank grid
        self.width_cells = width_cells
        self.height_cells = width_cells  # Default setting should probably have the grid be square.
        canvas_width = self.GRID_WIDTH_PX-80
        canvas_height = self.GRID_HEIGHT_PX-80
        self.state['grid'] = build_blank_grid(width_cells, width_cells)
        self.main_frame = MainCAFrame(self, self.state['grid'], self.GRID_WIDTH_PX, self.GRID_HEIGHT_PX,
                                      canvas_width, canvas_height)
        self.main_frame.pack(expand=True, fill=tk.BOTH)

        #Build top menus
        self.menubar = tk.Menu(self)
        try:
            self.config(menu=self.Menu)
        except AttributeError:
            self.tk.call(self, 'config', '-menu', self.menubar)
        self.file_menu = tk.Menu(self, tearoff=False)
        self.file_menu.add_command(label="Load Ruleset", command=self.load_dialogue)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Save Automata (Image)", command=self.save_image_dialogue)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Quit", command=self.quit)
        self.menubar.add_cascade(menu=self.file_menu, label='File')

        self.config_menu = tk.Menu(self, tearoff=False)
        self.config_menu.add_command(label='Set Dimensions', command=self.config_dimensions)
        self.config_menu.add_checkbutton(label='Set Grid Wrap')
        self.config_menu.add_checkbutton(label='Random Start Row', variable=self.random_start)
        self.config_menu.add_command(label="Set Background Color...", command=self.set_background_color)
        self.config_menu.add_command(label="Set Fill Color...", command=self.set_fill_color)
        self.config_menu.add_separator()
        self.config_menu.add_command(label='Configure Plug-ins')
        self.config_menu.add_command(label='Reload Plug-ins', command=self.reload_plugins)
        self.plugin_menu = tk.Menu(self, tearoff=False)
        self.config_menu.add_cascade(menu=self.plugin_menu, label="Plugins...")
        self.menubar.add_cascade(menu=self.config_menu, label='Configure')
        self.menubar.add_command(label="About", command=self.about)


        #Build plugin manager
        app_logger.info('Loading plug-in manager')
        self.main_frame.set_status_bar('Loading plug-in manager...')
        self.plugin_manager = PluginManager()
        self.plugins = {}
        self.plugin_manager.setPluginPlaces([ApplicationConfiguration.DEFAULT_PLUGIN_DIR_LOCATION])

        self.reload_plugins()
        app_logger.info('Plug-in manager loaded. {} plug-ins were loaded.'
                         ''.format(len(self.plugin_manager.getAllPlugins())))

    def reload_plugins(self):
        self.plugin_manager.collectPlugins()
        self.plugin_menu.delete(0, tk.END)
        self.plugins.clear()

        def build_plugin_callback(plugin, plugin_var):
            def callback(*args, **kwargs):
                if plugin_var.get():
                    app_logger.info("Activating plugin {}".format(plugin.name))
                    plugin.plugin_object.activate()
                    plugin.plugin_object.run(self, plugin_var, self.state)
                else:
                    app_logger.info("Deactivating plugin {}".format(plugin.name))
                    plugin.plugin_object.stop()
                    plugin.plugin_object.deactivate()
            return callback

        for plugin in self.plugin_manager.getAllPlugins():
            plugin_var = tk.BooleanVar(self)
            self.plugin_menu.add_checkbutton(label=plugin.name, variable=plugin_var)
            plugin_var.trace('w', build_plugin_callback(plugin, plugin_var))
            self.plugins[plugin.name] = (plugin, plugin_var)

    def _update_plugins(self):
        for plugin, plugin_var in self.plugins.values():
            if plugin_var.get():
                plugin.plugin_object.update(self.state)

    def load_dialogue(self):
        new_rule_filename = tkFileDialog.askopenfilename(parent=self, title='Open Rule File', defaultextension=".txt",
                                                         filetypes=[('Rules Files', '*.txt'), ('All Files', '*')])
        if not new_rule_filename:
            return
        try:
            self.load(new_rule_filename)
        except:
            app_logger.exception('Faulted loading rules file!')

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
                self.main_frame.system_canvas.postscript(file='tmp.eps')
                img = Image.open('tmp.eps')
                img.save(automata_image_filename)
                os.remove('tmp.eps')
            else:
                self.main_frame.system_canvas.postscript(file=automata_image_filename)
            self.main_frame.set_status_bar('Saved automata image file as: {}'.format(automata_image_filename))
        except:
            app_logger.exception('Faulted saving automata image!')

    def load(self, rule_file):
        app_logger.info('Attempting to load new rules file: {}'.format(rule_file))
        rules = load_rules(rule_file)
        self.state['rules'] = rules
        self.state['rules_file'] = rule_file
        self._build_grid(rules)
        self.main_frame.set_status_bar('Loaded rules file: {}'.format(rule_file))

    def _build_grid(self, rules):
        grid = []
        if self.random_start.get():
            start_row = build_random_start_row(self.width_cells)
        else:
            start_row = build_default_start_row(self.width_cells)
        grid.append(start_row)
        grid.extend(evolve_system_multi(start_row, rules, self.height_cells))
        self._on_grid_update(grid)

    def _on_grid_update(self, new_grid):
        self.state['grid'] = new_grid
        self.main_frame.system_canvas.draw_grid(new_grid)
        self._update_plugins()

    def config_dimensions(self):
        new_width, new_height = DimensionsDialog(self, title='Set Automata Dimensions',
                                                 prompt='Set Automata Dimensions', x_name='Width', y_name='Height',
                                                 x_default=self.width_cells, y_default=self.height_cells)
        if not new_width or not new_height:
            return
        app_logger.info('Resizing automata to new width: {}, height: {}'.format(new_width, new_height))
        self.width_cells = new_width
        self.height_cells = new_height
        self._build_grid(self.state['rules'])

    def set_fill_color(self):
        new_color = tkColorChooser.askcolor(self.main_frame.system_canvas.fill_color, parent=self)
        if new_color[1]:
            self.main_frame.system_canvas.fill_color = new_color[1]
            self.main_frame.system_canvas.draw_grid(self.state['grid'])

    def set_background_color(self):
        new_color = tkColorChooser.askcolor(self.main_frame.system_canvas.bg_color, parent=self)
        if new_color[1]:
            self.main_frame.system_canvas.bg_color = new_color[1]
            self.main_frame.system_canvas.draw_grid(self.state['grid'])

    def random_start_callback(self, *args):
        self._build_grid(self.state['rules'])

    @staticmethod
    def about():
        tkMessageBox.showinfo('About', '{app} ({ver})\nby {auth}, 2014'
                                       ''.format(ver=__version__, auth=__author__, app=__application_name__))

    @staticmethod
    def build_selector_menu(parent, choices, set_fxn, update_fxn=None, default=None):
        new_menu = tk.Menu(parent, tearoff=False)
        choice_map = {}

        def build_selector_trace(var):
            def callback(*args):
                set_fxn(choice_map[var.get()])
                if update_fxn:
                    update_fxn()
            return callback

        if not default:
            default = choices[0]
        new_var = tk.StringVar(new_menu)
        new_var.set(str(default))
        new_var.trace('w', build_selector_trace(new_var))
        for choice in choices:
            choice_map[str(choice)] = choice
            new_menu.add_radiobutton(label=str(choice).capitalize(), variable=new_var, value=str(choice))
        return new_menu
