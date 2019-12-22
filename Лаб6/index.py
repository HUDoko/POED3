import pandas as pd
import AllMethods as my

df = my.ReadFilesToDf('E:\\7 семестр\\ПЭОЭД\\Лаб5\\NewCities')
my.TransformCategories(df)
df = df.fillna(0)
new_df = my.ReadFilesToDf('E:\\7 семестр\\ПЭОЭД\\Лаб5\\Moscow')
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


new_df = new_df.drop('name', 1)
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

# Определить лучший классификатор
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
