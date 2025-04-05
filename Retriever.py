from abc import ABC, abstractmethod

import pandas as pd


class Retriever(ABC):
    def __init__(self):
        self.retrieved_data = None

    @abstractmethod
    def retrieve(self, **kwargs) -> pd.DataFrame():
        pass

    @abstractmethod
    def export(self):
        # export to artifacts // image, document and etc
        pass
