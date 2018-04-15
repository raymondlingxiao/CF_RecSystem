import numpy as np
import csv
import math
from collections import defaultdict

# build inverted list based on raw data
def inverted_list(raw_csv, movie_id_start, movie_id_end):
    # list structure: {userId:{movie1:rating, movie2: rating}}
    inverted_list = {}
    with open(raw_csv) as file_in:
        reader = csv.DictReader(file_in)
        for row in reader:
            if int(row['movieId']) >= movie_id_start and int(row['movieId']) <= movie_id_end:
                if int(row['userId']) not in inverted_list.keys():
                    inverted_list[int(row['userId'])] = {int(row['movieId']):float(row['rating'])}
                else:
                    inverted_list[int(row['userId'])][int(row['movieId'])] = float(row['rating'])
    file_in.close()

    with open('./data_set/inverted_list_'+str(movie_id_start)+'_'+str(movie_id_end)+'.txt','w') as file_out:
        file_out.write(str(inverted_list))
    file_out.close()

# build co-occurrence matrix for inverted list
def build_co_matrix(file_path):
    with open(file_path) as file_in:
        inverted_list = eval(file_in.read())
    file_in.close()
    # for co_max's key represents every movieId
    # for each key's value, it represents the [people share mutual interests of another movie: number]
    co_matrix = defaultdict(defaultdict)
    num_maxtrix = defaultdict(defaultdict)
    for user, items in inverted_list.items():
        for i in items.keys():
            if i not in num_maxtrix.keys():
                num_maxtrix[i] = 0
            num_maxtrix[i] += 1
            for j in items.keys():
                if i == j:
                    continue
                if j not in co_matrix[i].keys():
                    co_matrix[i][j] = 0
                co_matrix[i][j] += 1
    return co_matrix,num_maxtrix


# Compute the similarity for a pair of movies
def similarity_matrix(co_matrix, num_matrix):
    sim_matrix = defaultdict(defaultdict)
    for movie, related_movie_dict in co_matrix.items():
        for related_movie, number in related_movie_dict.items():
            # Cosine Similarity
            sim_matrix[movie][related_movie] = number / math.sqrt(num_matrix[movie] * num_matrix[related_movie])
    return sim_matrix


def recommend(sim_matrix, user_id, inverted_list_path, topN=20):
    # Based on the formula: Potential Interest of movie i = interest of movie j * sim(movie i&j)
    # Then get the top(sim) N movies

    with open(inverted_list_path) as file_in:
        inverted_list = eval(file_in.read())
    file_in.close()
    user_history = inverted_list[user_id]
    print(user_history)
    rankings = {}
    for has_movie, rating in user_history.items():
        sim_matrix_top = sorted(sim_matrix[has_movie].items(), key=lambda s:s[1], reverse=True)
        for related_movie, sim in sim_matrix_top:
            if related_movie not in user_history.keys():
                if related_movie not in rankings.keys():
                    rankings[related_movie] = sim * rating
                else:
                    rankings[related_movie] += sim * rating
    return sorted(rankings.items(), key= lambda r:r[1], reverse= True)

def ref_movie(rank_list, movie_file_path, final_file_out):
    with open(final_file_out, 'wb') as file_out:
        for movie, sim in rank_list:
            with open(movie_file_path) as file_in:
                reader = csv.DictReader(file_in)
                for row in reader:
                    if movie == int(row['movieId']):
                        headers = ['movieId','title','genres','rankScore']
                        writer = csv.DictWriter(file_out,headers)
                        writer.writeheader()
                        writer.writerow({'movieId':row['movieId'],'title':row['title'],'genres':row['genres'],'rankScore':sim})
    file_out.close()

rating_path = './data_set/ratings_pos.csv'
inverted_list_path = './data_set/inverted_list_1_100.txt'
# inverted_list(rating_path,1,100)
co_matrix, num_matrix = build_co_matrix(inverted_list_path)
sim_matrix = similarity_matrix(co_matrix, num_matrix)
# print(sim_matrix)
userId = 2
ranking_list = recommend(sim_matrix, userId,inverted_list_path)
# for item in ranking_list:
#     print(item)
ref_movie(ranking_list, './data_set/movies.csv','./data_set/'+str(userId)+'_Recommendation.csv')
