import numpy as np
import csv
from collections import defaultdict

# build inverted list based on raw data
def inverted_list(raw_csv, movie_id_start, movie_id_end):
    inverted_list = {}
    with open(raw_csv) as file_in:
        reader = csv.DictReader(file_in)
        for row in reader:
            if int(row['movieId']) >= movie_id_start and int(row['movieId']) <= movie_id_end:
                if int(row['userId']) not in inverted_list.keys():
                    inverted_list[int(row['userId'])] = [int(row['movieId'])]
                else:
                    inverted_list[int(row['userId'])] += [int(row['movieId'])]
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
    favor_num = defaultdict(defaultdict)
    for u, items in inverted_list.items():
        for i in items:
            if i not in favor_num.keys():
                favor_num[i] = 0
            favor_num[i] += 1
            for j in items:
                if i == j:
                    continue
                if j not in co_matrix[i].keys():
                    co_matrix[i][j] = 0
                co_matrix[i][j] += 1



# inverted_list('./data_set/ratings_pos.csv',1,100)
build_co_matrix('./data_set/inverted_list_1_100.txt')
