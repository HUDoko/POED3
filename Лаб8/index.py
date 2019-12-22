import AllMethods as my
import clustering as klys
from sklearn.cluster import KMeans
from sklearn.metrics import pairwise_distances_argmin_min


df = my.read_files_to_df("E:\\7 семестр\\ПЭОЭД\\Лаб8\\NewCities")
# Записать названия групп
names = df["name"]
my.transform_categories(df)
df = df.drop('name', 1)
df = df.drop('company', 1)
df = df.drop('description', 1)
df = df.drop('conditions', 1)
df = df.drop('requirement', 1)
df = df.drop('responsibility', 1)
df = df.drop('key_skills', 1)
df = df.drop('published_at', 1)
df = df.drop('Другие навыки', 1)
df = df.fillna(0)
skills_columns = klys.get_skills_columns(df)
cities_columns = klys.get_cities_columns(df)
experiences_columns = klys.get_experiences_columns(df)
employments_columns = klys.get_employments_columns(df)
schedules_columns = klys.get_schedules_columns(df)
n = 3
kmeans_clusters = []
kmeans = KMeans(n_clusters=n, random_state=0).fit_predict(df)
closest, _ = pairwise_distances_argmin_min(KMeans(n_clusters=n, random_state=0).fit(df).cluster_centers_, df)
for i in range(0, n):
    kmeans_clusters.append(klys.Cluster(i, df.iloc[closest[i]], names.iloc[closest[i]]))
for i in range(0, len(kmeans)):
    kmeans_clusters[kmeans[i]].add(df.iloc[i], skills_columns, cities_columns, experiences_columns, employments_columns, schedules_columns)
print(kmeans_clusters[0])
