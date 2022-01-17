import pandas as pd

# 1. Считываем файл
filename = input('Введи название файла:\n')
hard = input('Информация получена от сборки? Y/N\n')
print('Читаем файл')
with open(filename + '.txt', 'r') as file:
    names = file.readline().strip().split('\t')
    text = [i.replace(',', '.').split('\t') for i in file.read().strip().split('\n')]
time = [float(text[line][0]) for line in range(len(text))]
data = [[float(text[j][i * 2 + 1]) for j in range(int(len(text)))] for i in range(int(len(text[0]) / 2))]
del text

# 2. Выдернуть названия
print('Собираем имена')
nameComponents = [names[1].split('/')[-2] + '_' + names[1].split('/')[-1]]  # Название для компонентов в объектах
k = 3
while True:
    nameTemp = names[k].split('/')[-2] + '_' + names[k].split('/')[-1]
    if nameComponents[0] == nameTemp:
        break
    nameComponents.append(nameTemp)
    k += 2

nameList = []  # Название объектов
for i in range(int(len(names) / 2 / len(nameComponents))):
    if hard == 'Y' or hard == 'y':
        temp = names[i * (len(nameComponents) * 2) + 1].split('/')
        nameList.append(temp[-4] + '|' + temp[-3])
    else:
        nameList.append(names[i * (len(nameComponents) * 2) + 1].split('/')[-3])
del names

# 3. Подготовить лист со средними значениями
print('Готовим массив')
componentsAverage = [
    ["=СРЗНАЧ('" + nameList[j] + "'!" + chr(i + 66) + "3600:" + chr(i + 66) + "4600)" for j in range(len(nameList))] for
    i in range(len(nameComponents))]  # собираем все заготовки средних значений

summary_sheets = {'Name': nameList}  # Создаем словарь со ссылками на средние значения
for i in range(len(nameComponents)):
    summary_sheets[nameComponents[i]] = componentsAverage[i]
Sheet = pd.DataFrame(summary_sheets)

# 4. Собрать основные данные на листы
print('Собираем информацию в общий словарь')

diction_sheets = {'Summary': Sheet}
Sheets = []
column = 0
for i in range(len(nameList)):
    data_sheets = {'Time(sec)': time}
    for j in range(len(nameComponents)):
        data_sheets[nameComponents[j]] = data[column]
        column += 1
    Sheets.append(pd.DataFrame(data_sheets))
    del data_sheets
    diction_sheets[nameList[i]] = Sheets[i]

# 5. Собрать Эксель таблицу
print('Начинаем экспорт')
writer = pd.ExcelWriter(filename + '.xlsx')

for sheet_name in diction_sheets.keys():
    diction_sheets[sheet_name].to_excel(writer, sheet_name=sheet_name, index=False)

writer.save()
print('Готово!')
