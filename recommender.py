import pickle
import sklearn.preprocessing as pp
from scipy.sparse import csr_matrix
import numpy as np
import pandas as pd


def inference_row(list_tid, ps_matrix):
    ps_matrix_norm = pp.normalize(ps_matrix, axis=1)
    length_tid = len(list_tid)
    n_songs = ps_matrix.shape[1]
    sparse_row = csr_matrix((np.ones(length_tid), (np.zeros(length_tid), list_tid)), shape=(1, n_songs))
    sparse_row_norm = pp.normalize(sparse_row, axis=1)

    return sparse_row_norm * ps_matrix_norm.T, sparse_row


def get_best_tid(current_list, ps_matrix_row, K=100, MAX_tid=10):
    df_ps_train = pd.read_hdf('data/df_data/df_playlistSong/df_ps_train_new.hdf')
    sim_vector, sparse_row = inference_row(current_list, ps_matrix_row)
    sim_vector = sim_vector.toarray()[0].tolist()

    # Enumerate index and rating
    counter_list = list(enumerate(sim_vector, 0))

    # Sort by rating
    sortedList = sorted(counter_list, key=lambda x: x[1], reverse=True)

    topK_pid = [i for i, _ in sortedList[1:K + 1]]

    n = 0

    while (1):

        top_pid = topK_pid[n]

        add_tid_list = df_ps_train.loc[top_pid].tid

        # Form new list
        new_tid_list = current_list + add_tid_list

        # Check number of songs and Add to data for prediction
        total_song = len(new_tid_list)
        #            print("n: {}\t total_song: {}".format(n,total_song))
        if (total_song > MAX_tid):
            new_tid_list = new_tid_list[:MAX_tid]
            # Add
            current_list = new_tid_list
            break
        else:
            current_list = new_tid_list
        n += 1
        if (n == K):
            break

    return current_list


def inference_from_tid(list_tid, K=100, MAX_tid=10):
    pickle_path = 'data/giantMatrix_new.pickle'
    # pickle_path = 'data/giantMatrix_truth_new.pickle'

    with open(pickle_path, 'rb') as f:
        ps_matrix = pickle.load(f)

    ps_matrix_row = ps_matrix.tocsr()

    return get_best_tid(list_tid, ps_matrix.tocsr())


def inference_from_uri(list_uri, K=100, MAX_tid=10):
    with open('dict_uri2tid.pkl', 'rb') as f:
        dict_uri2tid = pickle.load(f)
    list_tid = [dict_uri2tid[x] for x in list_uri if x in dict_uri2tid]
    best_tid = inference_from_tid(list_tid, K, MAX_tid)

    with open('dict_tid2uri.pkl', 'rb') as f:
        dict_tid2uri = pickle.load(f)
    best_uri = [dict_tid2uri[x] for x in best_tid]
    return best_uri