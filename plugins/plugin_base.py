__author__ = 'rcope'
from yapsy.IPlugin import IPlugin

class CAPlugin(IPlugin):
    """
        This is the base class all plug-ins must inherit from.
    """
    def run(self, ca_state):
        """
            The state of the CA automation is fed in. The plug-in can do something with this.
        """
        raise NotImplementedError