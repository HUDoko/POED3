import pandas as pd
import AllMethods as my

df = my.ReadFilesToDf('E:\\7 семестр\\ПЭОЭД\\Лаб9\\NewCities')
my.TransformCategories(df)
df = df.fillna(0)
new_df = my.ReadFilesToDf('E:\\7 семестр\\ПЭОЭД\\Лаб9\\Moscow')
gr = new_df["group"]
my.TransformCategories(new_df)
new_df = new_df.fillna(0)

# Добавить нужные признаки
tmp = pd.DataFrame()
for column in df:
    if column in new_df.columns.values:
        tmp[column] = new_df[column]
    else:
        tmp[column] = 0
for vacancy in new_df.itertuples():
    for skill in vacancy.key_skills.split(';'):
        if skill in tmp.columns.values:
            tmp.update(tmp[tmp["id"] == vacancy.id][skill].replace(0, 1))
new_df = tmp

# Удалить ненужные признаки
tmp = new_df
tmp = tmp.drop(['group'], axis=1)
df = df.drop('name', 1)
df = df.drop('company', 1)
df = df.drop('description', 1)
df = df.drop('conditions', 1)
df = df.drop('requirement', 1)
df = df.drop('responsibility', 1)
df = df.drop('key_skills', 1)
df = df.drop('published_at', 1)
df = df.drop('Другие навыки', 1)
df = df.drop('schedule_Гибкий график', 1)
df = df.drop('schedule_Полный день', 1)
df = df.drop('schedule_Сменный график', 1)
df = df.drop('schedule_Удаленная работа', 1)
df = df.drop('employment_Полная занятость', 1)
df = df.drop('employment_Проектная работа', 1)
df = df.drop('employment_Стажировка', 1)
df = df.drop('employment_Частичная занятость', 1)
df = df.drop('min_salary', 1)
df = df.drop('max_salary', 1)


#new_df = new_df.drop('name', 1)
new_df = new_df.drop('company', 1)
new_df = new_df.drop('description', 1)
new_df = new_df.drop('conditions', 1)
new_df = new_df.drop('requirement', 1)
new_df = new_df.drop('responsibility', 1)
new_df = new_df.drop('key_skills', 1)
new_df = new_df.drop('published_at', 1)
new_df = new_df.drop('Другие навыки', 1)
new_df = new_df.drop('schedule_Гибкий график', 1)
new_df = new_df.drop('schedule_Полный день', 1)
new_df = new_df.drop('schedule_Сменный график', 1)
new_df = new_df.drop('schedule_Удаленная работа', 1)
new_df = new_df.drop('employment_Полная занятость', 1)
new_df = new_df.drop('employment_Проектная работа', 1)
new_df = new_df.drop('employment_Стажировка', 1)
new_df = new_df.drop('employment_Частичная занятость', 1)
new_df = new_df.drop('min_salary', 1)
new_df = new_df.drop('max_salary', 1)

# 1C
sum = new_df['1С программирование'] + new_df[' 1С: Предприятие 8'] + new_df[' 1С: Зарплата и управление персоналом'] + new_df[' 1С программирование']
sum=sum//4
new_df['1C_key_skills'] = sum

sum = df['1С программирование'] + df[' 1С: Предприятие 8'] + df[' 1С: Зарплата и управление персоналом'] + df[' 1С программирование']
sum=sum//4
df['1C_key_skills'] = sum
# C#C++
sum = new_df[' C#'] + new_df['C++'] + new_df['C#'] + new_df[' C++'] + new_df[' ООП'] + new_df[' ASP.NET']
sum=sum//4
new_df['C#C++_key_skills'] = sum

sum = df[' C#'] + df['C++'] + df['C#'] + df[' C++'] + df[' ООП'] + df[' ASP.NET']
sum=sum//4
df['C#C++_key_skills'] = sum

#PHP
sum = new_df['PHP'] + new_df[' PHP'] + new_df[' PHP5']
sum = 0 if sum < 1 else 1
new_df['PHP_key_skills'] = sum
sum = df['PHP'] + df[' PHP'] + df[' PHP5']
sum = 0 if sum < 1 else 1
df['PHP_key_skills'] = sum


new_df.to_csv("test.csv", sep=';', encoding='UTF-8-sig')

"""
# Добавить нужные признаки
tmp = pd.DataFrame()
for column in df:
    if column in new_df.columns.values:
        tmp[column] = new_df[column]
    else:
        tmp[column] = 0
for vacancy in new_df.itertuples():
    for skill in vacancy.key_skills.split(';'):
        if skill in tmp.columns.values:
            tmp.update(tmp[tmp["id"] == vacancy.id][skill].replace(0, 1))
av.all_numerical_to_int(tmp, ["days_from_publication", "id"])
new_df = tmp
dm.add_skill_signs(new_df)
# Удалить ненужные признаки
tmp = new_df
tmp = tmp.drop(['group'], axis=1)

"""

"""
target = df.group
df = df.drop(['group'], axis=1)
#my.FindTheBestClassifier(df, target, 0.3)
# Предсказать группы
groups = new_df['group']
target_t = new_df.group
new_df = new_df.drop(['group'], axis=1)
tmp['predicted_group'] = my.predict(new_df, df, target, new_df, target_t)
tmp['factual_group'] = groups
tmp['gr'] = gr
tmp.to_csv("Groups_vacancies.csv", sep=';', encoding='UTF-8-sig')
"""