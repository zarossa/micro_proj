import sys
from typing import Dict, List
from loguru import logger


class Splitter:
    def __init__(self):
        self.givers = {}
        self.receivers = {}
        self.list_of_receivers = []
        self.list_of_givers = set()
        self.names = self.make_list_names()
        self.spending = self.make_list_of_spending()
        self.full_sum, self.per_sum = self.summarize()
        self.get_split_data()

    def get_split_data(self):
        print("Список трат:")
        for name in self.spending:
            print(f'\t{name}: {", ".join(map(lambda x: str(x), self.spending[name])) if self.spending[name] else 0}')
        logger.debug(self.spending)
        print(f"Итого общее: {self.full_sum}")
        print(f"Итого на человека: {self.per_sum}")
        self.splitter()

    @staticmethod
    def make_list_names():
        logger.warning("Write a list of people:")
        names = []
        tmp = input()
        while tmp != " ":
            names.append(tmp)
            tmp = input()
        return names

    def make_list_of_spending(self) -> Dict[str, List[int]]:
        spending = {}
        logger.warning("Type a list of expenses.\nSplit spends by 1 space")
        for name in self.names:
            spend = list(map(lambda x: int(x), input(f"{name}:\n").split()))
            spending[name] = spend
        return spending

    def summarize(self):
        full_sum = 0
        num_people = 0
        for name in self.spending:
            if "/" in name:
                num_people += 2
            else:
                num_people += 1
            full_sum += sum(self.spending[name])
        return full_sum, round(full_sum / num_people, 1)

    def splitter(self):
        for name in self.spending:  # Подсчет разницы трат
            if "/" in name:
                self.spending[name] = round(sum(self.spending[name]) - (2 * self.per_sum), 1)
            else:
                self.spending[name] = round(sum(self.spending[name]) - self.per_sum, 1)
        logger.debug(self.spending)
        for name in self.spending:  # Определение должников и доноров
            if self.spending[name] <= 0:
                self.givers[name] = self.spending[name]
                self.list_of_givers.add(name)
            else:
                self.receivers[name] = self.spending[name]
                self.list_of_receivers.append(name)
        for name in self.givers:
            debt = self.givers[name]
            while debt:
                receiver = self.list_of_receivers[0]
                if -debt >= self.receivers[receiver]:
                    transfer = self.receivers.pop(receiver)
                    self.list_of_receivers.pop(0)
                    debt = round(debt + transfer, 1)
                    print(f"{name} -> {receiver} = {round(transfer)}")
                    if len(self.list_of_receivers) == 0:
                        break
                else:
                    transfer = -debt
                    self.receivers[receiver] -= transfer
                    print(f"{name} -> {receiver} = {round(transfer)}")
                    self.list_of_givers.pop()
                    debt = 0


if __name__ == "__main__":
    logger.remove()
    logger.add(sys.stderr, level="INFO")  # INFO
    Splitter()
    logger.critical("Нажми enter для выхода")
