# Preprocess Item Data
# I only care about Basics and Ratings from IMDB
# I only care about modifying title/title_year
# I only care about modifying genre

import os
import subprocess

def _download_imdb(flag_overwrite=False):
    if os.path.isdir('../data/') is False:
        os.mkdir('../data/')
    DOWNLOAD_INFO = [('title.basics.tsv.gz', 'https://datasets.imdbws.com/title.basics.tsv.gz'),
                     ('title.akas.tsv.gz', 'https://datasets.imdbws.com/title.akas.tsv.gz'),
                     ('title.crew.tsv.gz', 'https://datasets.imdbws.com/title.crew.tsv.gz'),
                     ('name.basics.tsv.gz', 'https://datasets.imdbws.com/name.basics.tsv.gz')]
    for save_name, url in DOWNLOAD_INFO:
        if os.path.isfile(os.path.join('../data/', save_name[:-3])):
            print("Found {}, Skip".format(os.path.join('../data/', save_name)))
        else:
            data_file = request.urlopen(url)
            with open(os.path.join('../data/', save_name), 'wb') as output:
                output.write(data_file.read())
            subprocess.call(['gunzip', '{}/{}'.format('../data/', save_name)])
            subprocess.call(['rm', '{}/{}'.format('../data/', save_name)])

def read_imdb2dic():
    _download_imdb()
    titles2id_dic = {}
    titles2year_dic = {}
    _id2year_dic = {}
    id2info_dic = {}
    id2genre_dic = {}
    with open(os.path.join(IMDB_DIR, "title.basics.tsv"), newline='', encoding='utf-8') as csvfile:
        IMDB_title_name = csv.reader(csvfile, delimiter='\t')
        for row in IMDB_title_name:
            str_id = row[0]
            title_type = row[1].lower()
            title1 = row[2].lower()
            title2 = row[3].lower()
            assert "\n" not in title1 and "\n" not in title2
            start_year = row[5]
            end_year = row[6]

            start_year = None if start_year == '\\N' else start_year
            end_year = None if end_year == '\\N' else end_year
            if start_year is not None and len(row) == 9:
                if str_id not in _id2year_dic:
                    _id2year_dic[str_id] = start_year
                if str_id not in id2info_dic:
                    id2info_dic[str_id] = [(start_year, end_year), title_type]
                if str_id not in id2genre_dic:
                    id2genre_dic[str_id] = row[8].lower().split(",")

                if title1 not in titles2id_dic:
                    titles2id_dic[title1] = {}
                    titles2id_dic[title1][str_id] = start_year
                    titles2year_dic[title1] = {}
                    titles2year_dic[title1][start_year] = [str_id]
                else:
                    if str_id not in titles2id_dic[title1]:
                        titles2id_dic[title1][str_id] = start_year
                    if start_year not in titles2year_dic[title1]:
                        titles2year_dic[title1][start_year] = [str_id]
                    else:
                        titles2year_dic[title1][start_year].append(str_id)

                if title2 != title1:
                    if title2 not in titles2id_dic:
                        titles2id_dic[title2] = {}
                        titles2id_dic[title2][str_id] = start_year
                        titles2year_dic[title2] = {}
                        titles2year_dic[title2][start_year] = [str_id]
                    else:
                        if str_id not in titles2id_dic[title2]:
                            titles2id_dic[title2][str_id] = start_year
                        if start_year not in titles2year_dic[title2]:
                            titles2year_dic[title2][start_year] = [str_id]
                        else:
                            titles2year_dic[title2][start_year].append(str_id)
                else:
                    continue
            else:
                continue

    with open(os.path.join(IMDB_DIR, "title.akas.tsv"), newline='', encoding='utf-8') as csvfile2:
        IMDB_akas_name = csv.reader(csvfile2, delimiter="\t")
        for row in IMDB_akas_name:
            str_id = row[0]
            title3 = row[2].lower()
            if "\n" in title3:
                print("len(title3)", len(title3))
                continue
            assert "\n" not in title3
            if str_id in _id2year_dic:
                year = _id2year_dic[str_id]
                if title3 not in titles2id_dic:
                    titles2id_dic[title3] = {}
                    titles2id_dic[title3][str_id] = year
                    titles2year_dic[title3] = {}
                    titles2year_dic[title3][year] = [str_id]
                else:
                    if str_id not in titles2id_dic[title3]:
                        titles2id_dic[title3][str_id] = year
                    if year not in titles2year_dic[title3]:
                        titles2year_dic[title3][year] = [str_id]
                    else:
                        titles2year_dic[title3][year].append(str_id)
            else:
                continue

    print("#title name: {}".format(len(titles2id_dic)))
    print("#movie id: {}".format(len(id2info_dic)))
    with open(os.path.join(IMDB_DIR,'_title_name2idsdic_dic.pkl'), 'wb') as f:
        pickle.dump(titles2id_dic, f)
    with open(os.path.join(IMDB_DIR,'_title_name2yeardic_dic.pkl'), 'wb') as f:
        pickle.dump(titles2year_dic, f)
    with open(os.path.join(IMDB_DIR, '_id2info_dic.pkl'), 'wb') as f:
        pickle.dump(id2info_dic, f)
    with open(os.path.join(IMDB_DIR, '_id2genre_dic.pkl'), 'wb') as f:
        pickle.dump(id2genre_dic, f)
    ###################################################################################
    ###################################################################################

    id2l_director_dic = {}
    id2l_writer_dic = {}
    with open(os.path.join(IMDB_DIR, "title.crew.tsv"), newline='', encoding='utf-8') as csvfile:
        file_rows = csv.reader(csvfile, delimiter='\t')
        for row in file_rows:
            id = row[0]
            director_str = row[1]
            writer_str = row[2]

            if id in id2l_director_dic:
                print(id, id2l_director_dic[id])
            else:
                if director_str != "\\N" and len(director_str) > 2:
                    director_vec = director_str.split(",")
                    id2l_director_dic[id] = director_vec

            if id in id2l_writer_dic:
                print(id, id2l_writer_dic[id])
            else:
                if writer_str != "\\N" and len(writer_str) > 2:
                    writer_vec = writer_str.split(",")
                    id2l_writer_dic[id] = writer_vec
    with open(os.path.join(IMDB_DIR, '_id2director_dic.pkl'), 'wb') as f:
        pickle.dump(id2l_director_dic, f)
    with open(os.path.join(IMDB_DIR, '_id2writer_dic.pkl'), 'wb') as f:
        pickle.dump(id2l_writer_dic, f)
    ###################################################################################
    ###################################################################################

    people_id2name_dic = {}
    with open(os.path.join(IMDB_DIR, "name.basics.tsv"), newline='', encoding='utf-8') as csvfile:
        file_rows = csv.reader(csvfile, delimiter='\t')
        for row in file_rows:
            id = row[0]
            name = row[1]
            if id in people_id2name_dic:
                print(id, people_id2name_dic[id])
            else:
                people_id2name_dic[id] = name
    with open(os.path.join(IMDB_DIR, '_people_id2name_dic.pkl'), 'wb') as f:
        pickle.dump(people_id2name_dic, f)

    print("IMDb dics generated ...")
    return titles2id_dic, titles2year_dic, id2info_dic, id2genre_dic, \
           id2l_director_dic, id2l_writer_dic, people_id2name_dic


if __name__ == '__main__':
    print("==================================================")

    titles2id_dic, titles2year_dic, id2info_dic, id2genre_dic,\
    id2l_director_dic, id2l_writer_dic, people_id2name_dic = read_imdb2dic()
    # titles2id_dic, titles2year_dic, id2info_dic, id2genre_dic, \
    # id2l_director_dic, id2l_writer_dic, people_id2name_dic = load_imdb_dics()

    ml_id2l_title_year_dic, ml_id21_genre_dic = process_movielens()