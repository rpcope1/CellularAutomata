__author__ = 'Robert P. Cope'

from yapsy.IPlugin import IPlugin
import abc

class BaseSystem(IPlugin):
    __metaclass__ = abc.ABCMeta
    @abc.abstractmethod
    def evolve(cls, grid):
        """
            :param cls:
            :param grid: The current system grid.
            :return:
        """
        return grid

    @abc.abstractmethod
    def get_system_params(cls):
        return {}

    @abc.abstractmethod
    def set_system_params(cls, **kwargs):
        return
