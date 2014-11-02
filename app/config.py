__author__ = 'rcope'
import os
FS_SEPARATOR = "\\" if os.name in ['os2', 'nt'] else "/"


class DisplayConfiguration(object):
    CA_CANVAS_MAX_PIX_X = 700
    CA_CANVAS_MAX_PIX_Y = 700
    DEFAULT_WIDTH = 120

class ApplicationConfiguration(object):
    DEFAULT_PLUGIN_DIR_LOCATION = FS_SEPARATOR.join([os.path.dirname(os.path.os.path.realpath(__file__)), 'plugins'])