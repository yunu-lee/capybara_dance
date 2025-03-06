from abc import ABC, abstractmethod


class Notifier(ABC):
    def __init__(self, config: dict):
        pass

    @abstractmethod
    def notify(self, data: list):
        pass
