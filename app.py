import psycopg2 as pg
import pandas.io.sql as psql
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

connection = pg.connect("host=localhost dbname=recommendation_system user=setdatauser password=123456789")



def getContentBasedRecommendations(selectedId):
    data = psql.read_sql('SELECT * FROM movies', connection)
    # test_data = data["name"].iloc[1]
    test_data = data.loc[data["id"] == selectedId]
    test_data = test_data["name"].values[0]
    title = test_data
    print(test_data)
    tfidf = TfidfVectorizer()
    data['description'] = data['description'].fillna('')
    tfidf_matrix = tfidf.fit_transform(data['description'])
    cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)
    indices = pd.Series(data.index, index=data['name']).drop_duplicates()
    idx = indices[title]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:10]
    movie_indices = [i[0] for i in sim_scores]
    topMovies = data['name'].iloc[movie_indices]
    topIds = data["id"].iloc[movie_indices]
    movie_ratings = [i[1] for i in sim_scores]
    result = []
    for i in range(len(topMovies)):
        anime = {}
        anime["name"] = topMovies.iloc[i]
        anime["score"] = movie_ratings[i]
        anime["id"] = topIds.iloc[i]
        # anime["database_id"] =
        result.append(anime)
    return result


def getCollaborativeFilteringRecommendation(userId, number, resultFromAnother):
    contentBasedIds = [str(i["id"]) for i in resultFromAnother]
    print(contentBasedIds)
    filterValue = ",".join(contentBasedIds)

    selectQuery = 'SELECT * FROM score'
    if filterValue is not None:
        selectQuery += " where movie_id in (" + (filterValue) + ")"
    scores = psql.read_sql(selectQuery, connection).values
    usersIds = [i[1] for i in scores]
    moviesIds = [i[2] for i in scores]
    ratings = [i[3] for i in scores]
    import pandas as pd
    from surprise import Dataset
    from surprise import Reader
    ratings_dict = {
        "item": moviesIds,
        "user": usersIds,
        "rating": ratings,
    }
    df = pd.DataFrame(ratings_dict)
    reader = Reader(rating_scale=(1, 10))
    data = Dataset.load_from_df(df[["user", "item", "rating"]], reader)
    from surprise import KNNWithMeans
    sim_options = {
        "name": "cosine",
        "user_based": False,
    }
    algo = KNNWithMeans(sim_options=sim_options)
    trainingSet = data.build_full_trainset()
    algo.fit(trainingSet)
    res = []
    predictions_list = []
    someMovies = set(moviesIds)
    count = 0
    for i in someMovies:
        if count == number:
            break
        el = {}
        prediction = algo.predict(userId, i)
        el["movie_id"] = i
        el["predicted_rating"] = prediction.est
        res.append(el)
        count += 1
    from operator import itemgetter
    newlist = sorted(res, key=itemgetter('predicted_rating'), reverse=True)
    return newlist



# print(getContentBasedRecommendations(993))
print(getCollaborativeFilteringRecommendation("447016d2-c75f-4916-87fd-0bb7c3281a80", 994,
                                              getContentBasedRecommendations(994)))
