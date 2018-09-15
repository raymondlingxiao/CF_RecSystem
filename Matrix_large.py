import csv
import math
from collections import defaultdict
import pickle

class CFR_sys():

    def __init__(self, raw_rating_path, raw_movie_path, movie_id_start, movie_id_end ):
        self.rating_path = raw_rating_path
        self.movie_path = raw_movie_path
        self.movie_id_start = movie_id_start
        self.movie_id_end = movie_id_end
        self.inverted_list_dict = {}
        self.co_matrix = defaultdict(defaultdict)
        self.num_matrix = defaultdict(defaultdict)
        self.sim_matrix = defaultdict(defaultdict)
        self.train_id = []
        self.test_id = []

    # build inverted list based on raw data
    def inverted_list(self):
        # list structure: {userId:{movie1:rating, movie2: rating}}
        with open(self.rating_path) as file_in:
            reader = csv.DictReader(file_in)
            for row in reader:
                if int(row['movieId']) >= self.movie_id_start and int(row['movieId']) <= self.movie_id_end:
                    if int(row['userId']) not in self.inverted_list_dict.keys():
                        self.inverted_list_dict[int(row['userId'])] = {int(row['movieId']):float(row['rating'])}
                    else:
                        self.inverted_list_dict[int(row['userId'])][int(row['movieId'])] = float(row['rating'])
        file_in.close()

        # save inverted list to local
        with open('./data_set/inverted_list_'+str(self.movie_id_start)+'_'+str(self.movie_id_end)+'.txt','w') as file_out:
            file_out.write(str(self.inverted_list_dict))
        file_out.close()
        print("Inverted list finished..")

    # build co-occurrence matrix for inverted list
    def build_co_matrix(self):
        inverted_list = self.inverted_list_dict
        # for co_max's key represents every movieId
        # for each key's value, it represents the [people share mutual interests of another movie: number]
        for user, items in inverted_list.items():
            for i in items.keys():
                if i not in self.num_matrix.keys():
                    self.num_matrix[i] = 0
                self.num_matrix[i] += 1
                for j in items.keys():
                    if i == j:
                        continue
                    if j not in self.co_matrix[i].keys():
                        self.co_matrix[i][j] = 0
                    self.co_matrix[i][j] += 1
        print("Co-occurrence matrix finished..")

    # Compute the similarity for a pair of movies
    def build_similarity_matrix(self):
        for movie, related_movie_dict in self.co_matrix.items():
            for related_movie, number in related_movie_dict.items():
                # Cosine Similarity
                self.sim_matrix[movie][related_movie] = number / math.sqrt(self.num_matrix[movie] * self.num_matrix[related_movie])
        print("Similarity matrix finished..")

    def recommend(self, user_id, topN=20):
        # Based on the formula: Potential Interest of movie i = interest of movie j * sim(movie i&j)
        # Then get the top(sim) N movies
        inverted_list = self.inverted_list_dict
        user_history = inverted_list[user_id]
        self.split_test_train(user_id,0.5)
        rankings = {}
        for has_movie, rating in user_history.items():
            if has_movie in self.train_id:
                sim_matrix_top = sorted(self.sim_matrix[has_movie].items(), key=lambda s:s[1], reverse=True)
                for related_movie, sim in sim_matrix_top:
                    if related_movie not in self.train_id:
                        if related_movie not in rankings.keys():
                            rankings[related_movie] = sim * rating
                        else:
                            rankings[related_movie] += sim * rating
        print("Recommendation list finished..")
        print("Done for User "+str(user_id)+"..")
        return sorted(rankings.items(), key= lambda r:r[1], reverse= True)[0:topN]


    def ref_movie(self, rank_list, final_file_out):
        with open(final_file_out, 'wb') as file_out:
            headers = ['movieId', 'title', 'genres', 'rankScore']
            writer = csv.DictWriter(file_out, headers)
            writer.writeheader()
            for movie, sim in rank_list:
                with open(self.movie_path) as file_in:
                    reader = csv.DictReader(file_in)
                    for row in reader:
                        if movie == int(row['movieId']):
                            writer.writerow({'movieId':row['movieId'],'title':row['title'],'genres':row['genres'],'rankScore':sim})
        file_out.close()

    def save_matrix(self):
        with open('./data_Set_large/inverted_list_'+str(self.movie_id_end),'wb') as il:
            pickle.dump(self.inverted_list_dict,il)
        with open('./data_Set_large/co_matrix_'+str(self.movie_id_end),'wb') as out:
            # out.write(str(self.co_matrix))
            pickle.dump(self.co_matrix,out)
        with open('./data_Set_large/sim_matrix_'+str(self.movie_id_end),'wb') as out_:
            pickle.dump(self.sim_matrix, out_)
            # out_.write(str(self.sim_matrix))

    def split_test_train(self, user_id, train_perct):
        user_history = self.inverted_list_dict[user_id]
        size = 0
        for key in user_history.keys():
            size += 1
        train_size = round(size * train_perct)
        test_size = size - train_size
        if (test_size == 0 or train_size == 0):
            print(str(user_id)+" User is invalid..")
            return
        else:
            counter = 0
            for key in user_history.keys():
                if counter <= train_size:
                    self.train_id.append(key)
                if counter > train_size and counter <= size:
                    self.test_id.append(key)
                counter += 1

    def precision_count(self, rank_list):
        # print(len(rank_list))
        # print(len(self.test_id))
        test_size = 0
        for id in self.test_id:
            if id < self.movie_id_end:
                test_size += 1
            else:
                print(id)
        count_match = 0
        rank = 1
        for key in rank_list:
            if key[0] in self.test_id:
                # print("**************************************")
                # print(key, rank)
                # print("**************************************")
                count_match += 1
            rank += 1
        result = float(count_match)/float(test_size)
        print(result)
        return result


    def rec_sum(self):
        user_count = 0
        sum = 0
        user_list = self.inverted_list_dict.keys()
        for id in user_list:
            ranking_list = self.recommend(id)
            # compute precision
            sum += self.precision_count(ranking_list)
            self.test_id = []
            self.train_id = []
            user_count += 1
        print(sum/user_count)



if __name__ == "__main__":
    rating_path = './data_Set_Large/ratings_pos.csv'
    movie_path = './data_Set_Large/movies.csv'
    # movie Id
    start = 1
    end  = 10000
    system = CFR_sys(rating_path, movie_path, start, end)
    # build inverted list
    system.inverted_list()
    # build co-occurrence matrix based on the inverted list for users
    system.build_co_matrix()
    # compute the similarity for each pair, and get the similarity matrix
    system.build_similarity_matrix()
    #
    # # for more users
    # # system.rec_sum()
    #
    # # get recommendation list for a user
    # userId = 2
    # ranking_list = system.recommend(userId)
    # # compute precision
    # system.precision_count(ranking_list)
    # # generate the recommendation list as a csv file
    # # file_out = './data_set/'+str(userId)+'_Recommendation.csv'
    # # system.ref_movie(ranking_list,file_out)
    # # dump matrix
    system.save_matrix()


    # load from history
    # rating_path = './data_set/ratings_pos.csv'
    # movie_path = './data_set/movies.csv'
    # # movie Id
    # start = 1
    # end  = 10000
    # system = CFR_sys(rating_path, movie_path, start, end)
    # # build inverted list
    # # system.inverted_list()
    # # load sim matrix
    # with open('./sim_matrix') as f:
    #     system.sim_matrix = pickle.load(f)
    # # load inverted list
    # with open('./inverted_list') as f1:
    #     system.inverted_list_dict = pickle.load(f1)
    # # for more users
    # system.rec_sum()
    # rec
    # userId = 21
    # ranking_list = system.recommend(userId)
    # compute precision
    # system.precision_count(ranking_list)