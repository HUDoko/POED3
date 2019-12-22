import AllMethods as my
import pandas as pd
import plotly.graph_objects as go
from wordcloud import WordCloud, STOPWORDS







df = my.read_files_to_df("E:\\7 семестр\\ПЭОЭД\\Лаб5\\NewCities")
df = df.fillna(0)
sings = [[' XML', 'SQL'], ["Directum", " Электронный документооборот"], [" HTML5", " CSS3"], [" Kotlin", "Java"], ['C#', ' ASP.NET']]
signs_df = []
corrs = df.corr().fillna(0)
for elem in sings:
    d = dict()
    d["skill1"] = elem[0]
    d["skill2"] = elem[1]
    d["value"] = corrs[elem[0]][elem[1]]
    signs_df.append(d)
signs_df = pd.DataFrame(signs_df)

#кореляции
corrs = df.corr().fillna(0)
fig = go.Figure(data=go.Heatmap(z=corrs.values, x=list(corrs.columns), y=list(corrs.index)))
fig.update_layout(title="Матрица корреляции")
fig.write_html("E:\\7 семестр\\ПЭОЭД\\Лаб7\\cor.html", auto_open=True)
#линейная
fig = go.Figure()
fig.add_trace(go.Scatter(x=signs_df["skill1"], y=signs_df["value"], text=signs_df["skill2"], mode="lines+markers+text"))
fig.update_layout(title="Линейная зависимость")
fig.write_html("E:\\7 семестр\\ПЭОЭД\\Лаб7\\line.html", auto_open=True)
#Гистограма
trace = go.Bar(
        x=signs_df["skill1"],
        y=signs_df["value"],
        text=signs_df["skill2"],
        textposition='auto'
    )
fig = go.Figure(data=trace, layout=go.Layout(barmode='stack'))
fig.update_layout(title="Гистограма")
fig.write_html("E:\\7 семестр\\ПЭОЭД\\Лаб7\\gist.html", auto_open=True)
#Матрица рассеевания
fig = go.Figure(data=go.Splom(
        dimensions=[dict(label='skill1',
                         values=signs_df['skill1']),
                    dict(label='skill2',
                         values=signs_df['skill2']),
                    dict(label='value',
                         values=signs_df['value'])],
        text=signs_df['skill2'],
    ))
fig.update_layout(title="Матрица рассеяния")
fig.write_html("E:\\7 семестр\\ПЭОЭД\\Лаб7\\matrix.html", auto_open=True)
#Облако
text = ""
for skills in df["key_skills"].values:
    for el in skills.split(';'):
        text += el + ' '
wordcloud = WordCloud(
    width=3000,
    height=2000,
    background_color='black').generate(str(text))
wordcloud.to_file("E:\\7 семестр\\ПЭОЭД\\Лаб7\\cloud.png")
#размах выбросов
print(len(my.FindVibros(df, "min_salary")))
print(len(my.FindVibros(df, "max_salary")))
trace1 = df["min_salary"]
trace2 = df["max_salary"]
fig = go.Figure()
fig.add_trace(go.Box(y=trace1, name='min salary', marker_color='darkblue'))
fig.add_trace(go.Box(y=trace2, name='max salary', marker_color='lightseagreen'))
fig.update_layout(title="Диаграмма размаха выбросов")
fig.write_html("E:\\7 семестр\\ПЭОЭД\\Лаб7\\vibros.html", auto_open=True)
df.to_csv("E:\\7 семестр\\ПЭОЭД\\Лаб7\\vibros.csv", sep=';', encoding='UTF-8-sig')
#изменение и удаление
df = my.ChangeVibros(df, "min_salary")
df = my.ChangeVibros(df, "max_salary")
print(len(my.FindVibros(df, "min_salary")))
print(len(my.FindVibros(df, "max_salary")))
df = my.DeleteVibros(df, "min_salary")
df = my.DeleteVibros(df, "max_salary")
#размах выбросов без выбросов
print(len(my.FindVibros(df, "min_salary")))
print(len(my.FindVibros(df, "max_salary")))
trace1 = df["min_salary"]
trace2 = df["max_salary"]
fig = go.Figure()
fig.add_trace(go.Box(y=trace1, name='min salary', marker_color='darkblue'))
fig.add_trace(go.Box(y=trace2, name='max salary', marker_color='lightseagreen'))
fig.update_layout(title="Диаграмма размаха выбросов")
fig.write_html("E:\\7 семестр\\ПЭОЭД\\Лаб7\\without_vibros.html", auto_open=True)
df.to_csv("E:\\7 семестр\\ПЭОЭД\\Лаб7\\without_vibros.csv", sep=';', encoding='UTF-8-sig')
