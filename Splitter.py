class Splitter:
    def __init__(self):
        self.givers = {}
        self.receivers = {}
        self.list_of_receivers = []
        self.list_of_givers = set()
        # self.names = self.make_list_names()
        # self.spending = self.make_list_of_spending(self.names)
        self.spending = {'Ярик/Таня': [410, 53, 56, 277, 200, 64], 'Глеб/Вика': [350, 230, 180], 'Ден/Аня': [200, 82, 100, 30], 'Андрей': [106, 6, 208, 62, 92, 170], 'Вано': [65], 'Соня': [137], 'Саня': [0]}
        self.full_sum, self.per_sum = self.summarize(self.spending)

    def listed(self):
        print('Список трат:')
        for name in self.spending:
            print(f'\t{name}: {", ".join(map(lambda x: str(x), self.spending[name])) if self.spending[name] else 0}')
        print(self.spending)
        print(f'Итого общее: {self.full_sum}')
        print(f'Итого на человека: {self.per_sum}')
        self.splitter(self.spending, self.per_sum)

    @staticmethod
    def make_list_names():
        print('Write a list of people:')
        names = []
        tmp = input()
        while tmp != ' ':
            names.append(tmp)
            tmp = input()
        return names

    @staticmethod
    def make_list_of_spending(names):
        spending = {}
        print('Type a list of expenses.\nSplit spends by 1 space')
        for name in names:
            spend = list(map(lambda x: int(x), input(f'{name}:\n').split()))
            spending[name] = spend
        return spending

    @staticmethod
    def summarize(spending):
        full_sum = 0
        num_people = 0
        for name in spending:
            if '/' in name:
                num_people += 2
            else:
                num_people += 1
            full_sum += sum(spending[name])
        return full_sum, round(full_sum / num_people, 1)

    def splitter(self, spending, spend_by_pers):
        for name in spending:  # Подсчет разницы трат
            if '/' in name:
                spending[name] = round(sum(spending[name]) - 2 * spend_by_pers, 1)
            else:
                spending[name] = round(sum(spending[name]) - spend_by_pers, 1)
        print(spending)
        for name in spending:  # Определение должников и доноров
            if spending[name] <= 0:
                self.givers[name] = spending[name]
                self.list_of_givers.add(name)
            else:
                self.receivers[name] = spending[name]
                self.list_of_receivers.append(name)
        # print(self.givers)
        # print(self.receivers)
        for name in self.givers:
            # print(name)
            debt = self.givers[name]
            while debt:
                receiver = self.list_of_receivers[0]
                if - debt >= self.receivers[receiver]:
                    transfer = self.receivers.pop(receiver)
                    self.list_of_receivers.pop(0)
                    debt = round(debt + transfer, 1)
                    print(f'{name} -> {receiver} = {round(transfer)}')
                else:
                    transfer = - debt
                    self.receivers[receiver] -= transfer
                    print(f'{name} -> {receiver} = {round(transfer)}')
                    self.list_of_givers.pop()
                    debt = 0


Splitter().listed()
input('Нажми enter для выхода')
