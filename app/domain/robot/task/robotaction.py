from abc import ABCMeta, abstractmethod


class IRobotAction(metaclass=ABCMeta):
    @abstractmethod
    def execute(self):
        pass
