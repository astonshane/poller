import abc
# https://pymotw.com/3/abc/

class PluginBase(abc.ABCMeta):

    @abc.abstractmethod
    def trigger(self):
        """Trigger your event
        """

    @abc.abstractmethod
    def check(self):
        """Check if your event should fire
        """