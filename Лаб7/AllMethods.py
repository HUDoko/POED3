import re
import pandas as pd
import datetime as dt
import pytz
from sklearn.preprocessing import LabelEncoder
import glob
import os
from sklearn import model_selection, svm
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
import numpy as np


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


def DiscretizeColumn(data_frame, column_name, num):
    step = (data_frame[column_name].max() - data_frame[column_name].min()) / num
    data_frame[column_name] = data_frame[column_name] // step


def DummySkills(group, num):
    skills = GetPopularSkills(group, num).split(';')
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


def GetPopularSkills(data_frame, num):
    skills = GetUniqueSkills(data_frame["key_skills"])
    return ';'.join((sorted(skills, key=skills.get, reverse=True))[0:min(len(skills), num)])


def GetUniqueSkills(all_skills):
    skills_dict = dict()
    for skills in all_skills:
        if str(skills) != 'nan':
            for skill in skills.split(';'):
                skills_dict[skill] = skills_dict.get(skill, 0) + 1
    return skills_dict


def UpdateGroups(data_frame, all_groups):
    for group in all_groups:
        new_gr = pd.DataFrame()
        for value in group["values"].itertuples():
            new_gr = new_gr.append(data_frame[data_frame["id"] == value.id])
        group["values"] = new_gr
    return all_groups


def read_files_to_df(dir_name):
    df = pd.DataFrame()
    os.chdir(dir_name)
    for file in glob.glob("*.csv"):
        df = df.append(pd.read_csv(file, sep=';', low_memory=False, index_col=0), ignore_index=True, sort=False)
    os.chdir("../")
    return df


def transform_categories(data_frame):
    le = LabelEncoder()
    le.fit(data_frame['group'])
    data_frame['group'] = le.transform(data_frame['group'])


def find_the_best_classifier(train, target, test_size):
    kfold = 5
    itog_val = {}
    test = model_selection.train_test_split(train, target, test_size=test_size)
    model_rfc = RandomForestClassifier(n_estimators=100)
    model_rfc.fit(train, target)
    model_knc = KNeighborsClassifier(n_neighbors=100)
    model_knc.fit(train, target)
    model_dtc = DecisionTreeClassifier(max_depth=20, random_state=0)
    model_dtc.fit(train, target)
    model_lr = LogisticRegression(penalty='l1', tol=0.01, multi_class='ovr', solver='liblinear')
    model_lr.fit(train, target)
    model_svc = svm.SVC(gamma='scale')
    model_svc.fit(train, target)
    scores = model_selection.cross_val_score(model_rfc, train, target, cv=kfold)
    itog_val['RandomForestClassifier'] = scores.mean()
    scores = model_selection.cross_val_score(model_knc, train, target, cv=kfold)
    itog_val['KNeighborsClassifier'] = scores.mean()
    scores = model_selection.cross_val_score(model_dtc, train, target, cv=kfold)
    itog_val['DecisionTreeClassifier'] = scores.mean()
    scores = model_selection.cross_val_score(model_lr, train, target, cv=kfold)
    itog_val['LogisticRegression'] = scores.mean()
    scores = model_selection.cross_val_score(model_svc, train, target, cv=kfold)
    itog_val['SVC'] = scores.mean()
    print(itog_val)


def predict(new_df, train_l, target_l, train_t, target_t):
    model_rfc = RandomForestClassifier(n_estimators=100)
    #model_rfc = KNeighborsClassifier(n_neighbors=100)
    model_rfc = model_rfc.fit(train_l, target_l)
    print(model_rfc.score(train_l, target_l))
    print(model_rfc.score(train_t, target_t))
    return model_rfc.predict(new_df)

def FindVibros(df, column):
    return df[np.abs(df[column] - df[column].mean()) > (3 * df[column].std())]


def ChangeVibros(df, column):
    outbursts = FindVibros(df, column)
    mean = round(df[column].mean(), 0)
    std = round(df[column].std(), 0)
    for elem in outbursts["id"]:
        df.update(df[df["id"] == elem][column].apply(lambda x: mean - 3*std if (x-mean < 0) else mean + 3*std))
    return df


def DeleteVibros(df, column):
    outbursts = FindVibros(df, column)
    for elem in outbursts["id"]:
        df = df[df["id"] != elem]
    return df