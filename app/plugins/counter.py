__author__ = 'rcope'
from yapsy.IPlugin import IPlugin

try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk


class _CounterPluginGUI(tk.Toplevel):
    def __init__(self, parent, plugin_state_var, *args, **kwargs):
        tk.Toplevel.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.plugin_state_var = plugin_state_var
        self.sum_var = tk.DoubleVar(self)
        tk.Label(self, text='Current Sum:').pack()
        tk.Label(self, textvar=self.sum_var, relief=tk.SUNKEN).pack(expand=True, fill=tk.X)

    def update_sum(self, new_sum):
        self.sum_var.set(new_sum)

    def quit(self):
        if self.plugin_state_var.get():
            self.plugin_state_var.set(False)
        tk.Toplevel.quit(self)

    def destroy(self):
        if self.plugin_state_var.get():
            self.plugin_state_var.set(False)
        tk.Toplevel.destroy(self)


class CounterPlugin(IPlugin):
    def __init__(self):
        IPlugin.__init__(self)
        self.dialog = None
        self.plugin_state_var = None
        self.parent = None

    def run(self, parent, plugin_state_var, ca_state):
        self.parent = parent
        self.plugin_state_var = plugin_state_var
        self.dialog = _CounterPluginGUI(parent, plugin_state_var)
        grid = ca_state['grid']
        self.dialog.update_sum(sum([sum(row) for row in grid]))

    def update(self, ca_state):
        grid = ca_state['grid']
        self.dialog.update_sum(sum([sum(row) for row in grid]))

    def stop(self):
        self.dialog.destroy()