import pandas as pd


def get_dict_groups(names_of_groups, indexes_of_groups):
    dictionary = dict()
    for i in range(0, len(indexes_of_groups)):
        dictionary[indexes_of_groups[i]] = names_of_groups[i]
    return dictionary


def get_top_values_dict(dictionary, num=0):
    if num == 0:
        num = len(dictionary)
    sorted_dict = (sorted(dictionary, key=dictionary.get, reverse=True))[0:min(len(dictionary), num)]
    srt_dict = ''
    for el in sorted_dict:
        if dictionary[el] != 0:
            srt_dict += str(el) + ' (' + str(dictionary[el]) + '), '
    return srt_dict[:-2]


def get_skills_columns(df):
    columns = []
    for i in range(0, len(df.columns)):
        name = df.iloc[:, i].name
        if str(name).find("salary") == -1 and \
                str(name).find("name") == -1 and \
                str(name).find("city") == -1 and \
                str(name).find("experience") == -1 and \
                str(name).find("schedule") == -1 and \
                str(name).find("id") == -1 and \
                str(name).find("days") == -1 and \
                str(name).find("group") == -1 and \
                str(name).find("Index") == -1 and \
                str(name).find("employment") == -1:
            columns.append(name)
    return columns


def get_cities_columns(df):
    columns = []
    for i in range(0, len(df.columns)):
        name = df.iloc[:, i].name
        if str(name).find("city") != -1:
            columns.append(name)
    return columns


def get_experiences_columns(df):
    columns = []
    for i in range(0, len(df.columns)):
        name = df.iloc[:, i].name
        if str(name).find("experience") != -1:
            columns.append(name)
    return columns


def get_employments_columns(df):
    columns = []
    for i in range(0, len(df.columns)):
        name = df.iloc[:, i].name
        if str(name).find("employment") != -1:
            columns.append(name)
    return columns


def get_schedules_columns(df):
    columns = []
    for i in range(0, len(df.columns)):
        name = df.iloc[:, i].name
        if str(name).find("schedule") != -1:
            columns.append(name)
    return columns


class Cluster:
    def __init__(self, name, center, center_name):
        self.name = name
        self.center = center
        self.center_name = center_name
        self.count = 0
        self.top_skills = ''
        self.min_salary = 0
        self.max_salary = 0
        self.top_experiences = ''
        self.top_schedules = ''
        self.top_employments = ''
        self.top_cities = ''
        self.values = pd.DataFrame()

    def add(self, vacancy, skills_columns, cities_columns, experiences_columns, employments_columns, schedules_columns):
        self.values = self.values.append(vacancy)
        self.count += 1
        self.min_salary = self.get_mean("min_salary")
        self.max_salary = self.get_mean("max_salary")
        self.top_skills = self.get_top(skills_columns, 5)
        self.top_cities = self.get_top(cities_columns, 3)
        self.top_experiences = self.get_top(experiences_columns, 3)
        self.top_schedules = self.get_top(schedules_columns, 3)
        self.top_employments = self.get_top(employments_columns, 3)

    def get_mean(self, column):
        return round(self.values[column].mean(), 3)

    def get_top(self, columns, num):
        values = dict()
        for name in columns:
            values[name] = self.values[self.values[name] == 1][name].sum()
        return get_top_values_dict(values, num)

    def center_to_str(self):
        return ' '.join(self.center.to_string().replace("\n", "; ").split())

    def __str__(self):
        return 'Кластер {}:\n' \
               'Центр: Название вакансии: {} \n\t{} \n' \
               'Количество элементов: {} \n' \
               'Среднее: минимальная: {}, максимальная - {}\n' \
               'Топ-5 ключевых навыков: {}\n' \
               'Топ-3 городов: {}\n' \
               'Топ-3 опыта работы: {}\n' \
               'Топ-3 графиков работы: {}\n' \
               'Топ-3 занятости: {}\n' \
            .format(self.name, self.center_name, self.center_to_str(), self.count, self.min_salary, self.max_salary, self.top_skills, self.top_cities, self.top_experiences, self.top_schedules, self.top_employments)
