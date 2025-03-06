from abc import ABC, abstractmethod

import pandas as pd


class Retriever(ABC):
    def __init__(self):
        self.retrieved_data = None

    @abstractmethod
    def retrieve(self) -> pd.DataFrame():
        pass

    @abstractmethod
    def export(self):
        # export to artifacts // image, document and etc
        pass

    # def get_apt_sale_data(self): # 가변형 인자
    #     pass
    #
    # def get_apt_for_sale_data(self):
    #     pass
