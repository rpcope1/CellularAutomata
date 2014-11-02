try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk

#-----------------------------
#   Set Dimensions Dialog
#-----------------------------


def DimensionsDialog(master, title="Set Dimensions", prompt="Set Dimensions", x_name="X", y_name="Y",
                 var_type=tk.IntVar, x_default=0, y_default=0, *args, **kwargs):
    dialog = _DimensionsDialog(master, title, prompt, x_name, y_name, var_type, x_default, y_default, *args, **kwargs)
    master.wait_window(dialog)
    return dialog.x_var, dialog.y_var


class _DimensionsDialog(tk.Toplevel):
    BUTTON_WIDTH = 15

    def __init__(self, master, title, prompt, x_name, y_name, var_type, x_default, y_default, *args, **kwargs):
        tk.Toplevel.__init__(self, master, *args, **kwargs)
        self.title(title)

        #TODO: Can this be done in a smarter manner?
        self._x_var = var_type(self)
        self._y_var = var_type(self)
        self._x_var.set(x_default)
        self._y_var.set(y_default)
        self.canceled = True

        self.prompt_label = tk.Label(self, text=prompt)
        self.prompt_label.grid(row=0, column=0, columnspan=2, pady=2)

        self.x_label = tk.Label(self, text="{}:".format(x_name))
        self.x_input = tk.Entry(self, textvariable=self._x_var)
        self.y_label = tk.Label(self, text="{}:".format(y_name))
        self.y_input = tk.Entry(self, textvariable=self._y_var)

        self.x_label.grid(row=1, column=0, pady=2)
        self.x_input.grid(row=1, column=1, pady=2)
        self.y_label.grid(row=2, column=0, pady=2)
        self.y_input.grid(row=2, column=1, pady=2)

        self.ok_button = tk.Button(self, text="OK", command=self.ok, width=self.BUTTON_WIDTH)
        self.cancel_button = tk.Button(self, text="Cancel", command=self.cancel, width=self.BUTTON_WIDTH)
        self.ok_button.grid(row=3, column=0, sticky="NS", padx=5, pady=2)
        self.cancel_button.grid(row=3, column=1, sticky="NS", padx=5, pady=2)

    def cancel(self):
        self.destroy()

    def ok(self):
        self.canceled = False
        self.destroy()

    @property
    def x_var(self):
        return None if self.canceled else self._x_var.get()

    @property
    def y_var(self):
        return None if self.canceled else self._y_var.get()

