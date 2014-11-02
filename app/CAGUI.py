__author__ = 'rcope'

import logging
try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk

disp_logger = logging.getLogger(__name__)
if not disp_logger.handlers:
    ch = logging.StreamHandler()
    disp_logger.addHandler(ch)
    disp_logger.setLevel(logging.INFO)

disp_logger.info('Cellular Automata display library loading.')


def _rgb_to_tkinter(red, green, blue):
    """
        Convert RGB value of 0 to 255 to
        hex Tkinter color string.
    """
    assert 256 > red >= 0 and 256 > green >=0 and 256 > blue >= 0
    return '#{r:2x}{g:2x}{b:2x}'.format(r=red, g=green, b=blue)


#TODO: Make resize on this behave better, now that we have scrollbars.
#TODO: Add ability to zoom in and out.
#TODO: Make scrollbars not scroll out of grid.
class SystemCanvas(tk.Frame):
    def __init__(self, master, grid, w, h, *args, **kwargs):
        tk.Frame.__init__(self, master)

        #Setup the actual canvas and internal widgets.
        self._canvas = tk.Canvas(self, *args, **kwargs)
        self._canvas.grid(row=0, column=0, sticky="NSEW")
        self._hbar = tk.Scrollbar(self, orient=tk.HORIZONTAL)
        self._hbar.grid(row=1, column=0, sticky="EW")
        self._vbar = tk.Scrollbar(self, orient=tk.VERTICAL)
        self._vbar.grid(row=0, column=1, sticky="NS")
        self._canvas.config(xscrollcommand=self._hbar.set, yscrollcommand=self._vbar.set)
        self._hbar.config(command=self._canvas.xview)
        self._vbar.config(command=self._canvas.yview)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.width = w
        self.height = h
        self.max_width = w
        self.max_height = h
        self.fill_color = 'black'
        self.bg_color = 'white'
        self._grid_line_width = 1
        self.draw_grid(grid)

    def set_grid_lines(self, on=True):
        self._grid_line_width = 1 if on else 0

    def draw_grid(self, grid):
        self.clear_canvas()
        box_h = self.max_height / len(grid)
        box_w = self.max_width / len(grid[0])
        self.width = box_w * len(grid[0])
        self.height = box_h * len(grid)
        y_count = 0
        for line in grid:
            x_count = 0
            for entry in line:
                if entry == 0:
                    self._canvas.create_rectangle(x_count * box_w, y_count * box_h, (x_count + 1) * box_w,
                                                  (y_count + 1) * box_h, fill=self.bg_color,
                                                  width=self._grid_line_width)
                elif entry == 1:
                    self._canvas.create_rectangle(x_count * box_w, y_count * box_h, (x_count + 1) * box_w,
                                                  (y_count + 1) * box_h, fill=self.fill_color,
                                                  width=self._grid_line_width)
                x_count += 1
            y_count += 1
        self._canvas.update()
        self._canvas.config(width=self.width, height=self.height)

    def clear_canvas(self):
        self._canvas.delete("all")


class MainCAFrame(tk.Frame):
    def __init__(self, parent, grid, grid_width, grid_height, canvas_width, canvas_height, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)

        self._system_canvas = SystemCanvas(self, grid, grid_width, grid_height,
                                         width=canvas_width, height=canvas_height,
                                         relief=tk.GROOVE, bd=4)
        self._system_canvas.grid(row=0, column=0, padx=20, pady=20)

        #Load status bar
        self.status_bar_var = tk.StringVar(self)
        self.status_bar_var.set('Initialized.')
        self.status_bar = tk.Label(self, textvar=self.status_bar_var, relief=tk.SUNKEN, justify=tk.LEFT, anchor=tk.W)
        self.status_bar.grid(row=1, column=0, sticky="EW", padx=2, pady=2)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)


    def set_status_bar(self, message):
        self.status_bar_var.set(str(message))

    @property
    def system_canvas(self):
        return self._system_canvas