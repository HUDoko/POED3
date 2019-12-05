import glob
import pandas as pd
import AllMethods as my

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

df = pd.DataFrame()
for file in glob.glob("1\*.csv"):
    tmp_df = pd.read_csv(file, sep=';', low_memory=False, index_col=0)
    df = df.append(tmp_df)

my.normalize_column(df, "days")
my.discretize_column(df, "min_salary", 10)
my.discretize_column(df, "max_salary", 10)
df = df.drop('max_experience', 1)
df = pd.get_dummies(data=df, columns=['city', 'min_experience', 'schedule', 'employment'])
pd.DataFrame(df.to_csv("V.csv", sep=';', encoding='UTF-8-sig'))
for vacancy in df.itertuples():
    for group in groups:
        if my.AddToGroup(group, vacancy) == 1:
            break

my.dummy_skills(group["values"], 10)

for group in groups:
    pd.DataFrame(group["values"]).to_csv("11/" + group["name"] + ".csv", sep=';', encoding='UTF-8-sig')
