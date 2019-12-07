import glob
import pandas as pd
import AllMethods as my
import datetime as dt
import pytz

groups = [
    {"name": "1C", "param": ["1c", "1с", "битрикс", "bitrix"], "values": []},
    {"name": "PHP", "param": ["php", "рhр"], "values": []},
    {"name": "C#_C++", "param": ["c#", "с#", "c++", "с++", ".net", "qt"], "values": []},
    {"name": "Frontend", "param": ["front", "фронт", "javascript", "vue", "node", "react", "three"], "values": []},
    {"name": "Backend", "param": ["back"], "values": []},
    {"name": "Full stack", "param": ["full"], "values": []},
    {"name": "Другие web", "param": ["web", "веб", "laravel"], "values": []},
    {"name": "Android", "param": ["android"], "values": []},
    {"name": "iOS", "param": ["ios"], "values": []},
    {"name": "Питон", "param": ["python"], "values": []},
    {"name": "Delphi", "param": ["delphi"], "values": []},
    {"name": "БД", "param": ["sql", "данных", "oracle"], "values": []},
    {"name": "Java", "param": ["java", "котлин", "kotlin", "ява", "джава"], "values": []},
    {"name": "Go", "param": ["go"], "values": []},
    {"name": "СЭД", "param": ["сэд", "directum"], "values": []},
    {"name": "Erlang_Elixir", "param": ["erlang", "elixir"], "values": []},
    {"name": "Другие разработчики", "param": ["программист", "разработчик"], "values": []},
]

df = pd.read_csv("Vacancies.csv", sep=';', low_memory=False, index_col=0)
df["min_salary"] = df["min_salary"].fillna(0)
df["max_salary"] = df["max_salary"].fillna(0)
df["schedule"] = df["schedule"].fillna("любой")
df["employment"] = df["employment"].fillna("любой")
df["id"] = range(0, len(df.index))
date = pd.to_datetime(df['published_at'], utc=True).dt.tz_convert('US/Eastern')
df["days"] = (dt.datetime.now(pytz.timezone('US/Eastern')) - date).astype('timedelta64[D]')
my.normalize_column(df, "days")


df = df.drop('max_experience', 1)
for vacancy in df.itertuples():
    for group in groups:
        if my.AddToGroup(group, vacancy) == 1:
            break

for group in groups:
    group["values"] = pd.DataFrame(group["values"])
    my.CountSalary(group["values"])
    my.GetSkills(group["values"])

df = pd.DataFrame()
for group in groups:
      df = df.append(pd.DataFrame(group["values"]))
my.discretize_column(df, "min_salary", 10)
my.discretize_column(df, "max_salary", 10)
df = pd.get_dummies(data=df, columns=['city', 'min_experience', 'schedule', 'employment'])
groups = my.update_groups(df, groups)
for group in groups:
    my.dummy_skills(group["values"], 10)
    pd.DataFrame(group["values"]).to_csv("11/" + group["name"] + ".csv", sep=';', encoding='UTF-8-sig')
