import re
import pandas as pd
import datetime as dt
import pytz



def AddToGroup(group, vacancy):
    regex = re.compile('[ ,:()/-]')
    for gr in group["param"]:
        s = re.sub(regex, '', vacancy.name)
        if s.lower().find(gr) != -1:
            group["values"].append(vacancy)
            return 1
    return 0


def CountSalary(data_frame):
    categories = pd.unique(data_frame["city"])
    for category in categories:
        unique_cities = data_frame[data_frame["city"] == category]
        avg_min = unique_cities[unique_cities["min_salary"] != 0]["min_salary"].mean()
        avg_max = unique_cities[unique_cities["max_salary"] != 0]["max_salary"].mean()
        data_frame.update(data_frame[data_frame["city"] == category]["min_salary"].replace(0, round(avg_min, 2)))
        data_frame.update(data_frame[data_frame["city"] == category]["max_salary"].replace(0, round(avg_max, 2)))



def GetSkills(data_frame):
    skills = dict()
    for vacancy in data_frame.itertuples():
        if str(vacancy.key_skills) != 'nan':
            for skill in vacancy.key_skills.split(';'):
                skills[skill] = skills.get(skill, 0) + 1
    str_skills = ';'.join((sorted(skills, key=skills.get, reverse=True))[0:min(len(skills), 5)])
    data_frame.update(data_frame["key_skills"].fillna(str_skills))


def devideIntoGroups(groups):
    df = pd.read_csv("Vacancies.csv", sep=';', low_memory=False, index_col=0)
    df["min_salary"] = df["min_salary"].fillna(0)
    df["max_salary"] = df["max_salary"].fillna(0)
    df["schedule"] = df["schedule"].fillna("любой")
    df["employment"] = df["employment"].fillna("любой")
    df["id"] = range(0, len(df.index))

    date = pd.to_datetime(df['published_at'], utc=True).dt.tz_convert('US/Eastern')
    df["days"] = (dt.datetime.now(pytz.timezone('US/Eastern')) - date).astype('timedelta64[D]')

    for vacancy in df.itertuples():
        for group in groups:
            if AddToGroup(group, vacancy) == 1:
                break

    for group in groups:
        group["values"] = pd.DataFrame(group["values"])
        CountSalary(group["values"])
        GetSkills(group["values"])

    for group in groups:
        pd.DataFrame(group["values"]).to_csv("1/" + group["name"] + ".csv", sep=';', encoding='UTF-8-sig')


def normalize_column(data_frame, column_name):
    data_days_from_publication = data_frame[column_name]
    min_values = data_days_from_publication.min()
    max_values = data_days_from_publication.max()
    data_frame[column_name] = ((data_frame[column_name] - min_values) / (max_values - min_values)).fillna(0)


def discretize_column(data_frame, column_name, num):
    step = (data_frame[column_name].max() - data_frame[column_name].min()) / num
    data_frame[column_name] = data_frame[column_name] // step


def dummy_skills(group, num):
    skills = get_popular_skills(group, num).split(';')
    skills.append("Другие навыки")
    for skill in skills:
        group[skill] = 0
    for vacancy in group.itertuples():
        for vacancy_skill in str(vacancy.key_skills).split(';'):
            if vacancy_skill in skills:
                group.update(
                    group[group["id"] == vacancy.id][vacancy_skill].replace(0, 1))
            else:
                group.update(
                    group[group["id"] == vacancy.id]["Другие навыки"].replace(0, 1))


def get_popular_skills(data_frame, num):
    skills = get_unique_skills(data_frame["key_skills"])
    return ';'.join((sorted(skills, key=skills.get, reverse=True))[0:min(len(skills), num)])


def get_unique_skills(all_skills):
    skills_dict = dict()
    for skills in all_skills:
        if str(skills) != 'nan':
            for skill in skills.split(';'):
                skills_dict[skill] = skills_dict.get(skill, 0) + 1
    return skills_dict