__author__ = 'rcope'
from yapsy.IPlugin import IPlugin

#TODO: Correctly implement this with abc and ABCMeta
class CAPlugin(IPlugin):
    """
        This is the base class all plug-ins must inherit from.
    """
    def run(self, parent, plugin_state_var, ca_state):
        """
            The state of the CA automation is fed in. The plug-in can do something with this.
        """
        return

    def update(self, ca_state):
        """
            Occasionally the program will make update calls to the plug-in.
        """
        return

    def stop(self):
        """
            Stop the plug-in.
        """
        return