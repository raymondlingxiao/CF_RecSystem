import os
import csv


def get_pos_rates(file_in, file_out):
    # get all the positive ratings of each movie
    with open(file_in) as f_in:
        with open(file_out,'wb') as f_out:
            headers = ['userId', 'movieId', 'rating']
            reader = csv.DictReader(f_in)
            writer = csv.DictWriter(f_out, headers)
            writer.writeheader()
            for row in reader:
                if float(row['rating']) > 3:
                    # begin write a new csv
                    # data_out = {'userId':row['userId'],'movieId':row['movieId'],'rating':row['rating']}
                    row.pop('timestamp')
                    writer.writerow(row)
            f_out.close()
    f_in.close()

def movie_favor_counts(movie_file, rating_file, file_out):
    # get a summary for each movie of their popularity
    with open(movie_file) as movie:
        with open(file_out, 'wb') as out:
            headers = ['movieId','posNum','userId','title','genres']
            writer = csv.DictWriter(out,headers)
            writer.writeheader()
            reader_movie = csv.DictReader(movie)
            for row in reader_movie:
                # search each movie in ratings and start counting
                count = 0
                new_ele_userId = ''
                with open(rating_file) as rating:
                    reader_rating = csv.DictReader(rating)
                    for line in reader_rating:
                        if int(row['movieId']) == int(line['movieId']):
                            count += 1
                            new_ele_userId += line['userId'] + '\\'
                    # end search for one movie
                    # write in files
                    if count != 0:
                        writer.writerow({'movieId':row['movieId'],'posNum':count,'userId': new_ele_userId,'title':row['title'],'genres': row['genres']})
                print row['movieId'] + ' Finished..'
                rating.close()
        out.close()
    movie.close()

# get_pos_rates('./data_set/ratings.csv','./data_set/ratings_pos.csv')
movie_favor_counts('./data_set/movies.csv','./data_set/ratings_pos.csv','./data_set/movie_sum.csv')





