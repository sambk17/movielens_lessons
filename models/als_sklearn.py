# ALS Model (Implicit) using sklearn
# Do To: ALS Model (Explicit) using Sklearn

# Best Article (Implicit): https://www.kaggle.com/code/shivendra91/recommendation-als
# Best Article (Explicit): https://blog.insightdatascience.com/explicit-matrix-factorization-als-sgd-and-all-that-jazz-b00e4d9b21ea

import pandas as pd
import numpy as np
import scipy.sparse as sp
from sklearn.model_selection import train_test_split
from sklearn.metrics.pairwise import cosine_similarity

# from scipy.sparse.linalg import spsolve
# from sklearn.preprocessing import MinMaxScaler

users_items = pd.read_csv("../data/ratings.csv")
print(users_items.dtypes)
print(users_items.describe())

n_users = users_items['userId'].unique().shape[0]

# Note: There will be unused movie columns/rows as the max > count (and not max == count)
n_items = users_items['movieId'].max()

print (str(n_users) +" " +  str(n_items))

users_items_matrix = sp.dok_matrix((n_users+1, n_items+2), dtype=np.int8)
ratings = np.zeros((n_users, n_items))
print(users_items_matrix.shape)

# We assume every rating is because the user viewed.
# Note: This is where we could add an additional weight depending on the interaction: e.g. viewed, impression (not viewed, but displayed).  
# However, MovieLens does not provide this.

method = 'implicit'

for row in users_items.itertuples():
    
    # row[1] = userId; row[2] = movieId
    if method == 'implicit':
        users_items_matrix[row[1], row[2]] = 1
    if method == 'explicit':
        # row[3] = rating
        users_items_matrix[row[1], row[2]] = row[3]

users_items_matrix = users_items_matrix.tocsr()
print(users_items_matrix.shape)

# sparsity = n / (U * D) * 100 = 100836 / (611 * 193611) * 100
sparsity = float(len(users_items_matrix.nonzero()[0]))
sparsity /= (users_items_matrix.shape[0] * users_items_matrix.shape[1])
sparsity *= 100
print("Sparsity: {:4.2f}%".format(sparsity))

X_train, X_test = train_test_split(users_items_matrix, test_size=0.20)

cosine_similarity_matrix = cosine_similarity(X_train, X_train, dense_output=False)
cosine_similarity_matrix.setdiag(0)

# Woah!  I need to understand this
cosine_similarity_matrix_ll = cosine_similarity_matrix.tolil()

def implicit_weighted_ALS(training_set, lambda_val = 0.1, alpha = 40, iterations = 10, rank_size = 20, seed = 0):
    '''
    Implicit weighted ALS taken from Hu, Koren, and Volinsky 2008. Designed for alternating least squares and implicit
    feedback based collaborative filtering. 
    
    parameters:
    
    training_set - Our matrix of ratings with shape m x n, where m is the number of users and n is the number of items.
    Should be a sparse csr matrix to save space. 
    
    lambda_val - Used for regularization during alternating least squares. Increasing this value may increase bias
    but decrease variance. Default is 0.1. 
    
    alpha - The parameter associated with the confidence matrix discussed in the paper, where Cui = 1 + alpha*Rui. 
    The paper found a default of 40 most effective. Decreasing this will decrease the variability in confidence between
    various ratings.
    
    iterations - The number of times to alternate between both user feature vector and item feature vector in
    alternating least squares. More iterations will allow better convergence at the cost of increased computation. 
    The authors found 10 iterations was sufficient, but more may be required to converge. 
    
    rank_size - The number of latent features in the user/item feature vectors. The paper recommends varying this 
    between 20-200. Increasing the number of features may overfit but could reduce bias. 
    
    seed - Set the seed for reproducible results
    
    returns:
    
    The feature vectors for users and items. The dot product of these feature vectors should give you the expected 
    "rating" at each point in your original matrix. 
    '''
    
    # first set up our confidence matrix
    
    conf = (alpha*training_set) # To allow the matrix to stay sparse, I will add one later when each row is taken 
                                # and converted to dense. 
    
    num_user = conf.shape[0]
    num_item = conf.shape[1]
    
    # initialize our X/Y feature vectors randomly with a set seed
    rstate = np.random.RandomState(seed)
    
    X = sp.csr_matrix(rstate.normal(size = (num_user, rank_size))) # Random numbers in a m x rank shape
    Y = sp.csr_matrix(rstate.normal(size = (num_item, rank_size))) # Normally this would be rank x n but we can 
                                                                 # transpose at the end. Makes calculation more simple.
    X_eye = sp.eye(num_user)
    Y_eye = sp.eye(num_item)
    lambda_eye = lambda_val * sp.eye(rank_size) # Our regularization term lambda*I. 
    
    # We can compute this before iteration starts. 
    
    # Begin iterations
   
    for iter_step in range(iterations): # Iterate back and forth between solving X given fixed Y and vice versa
        # Compute yTy and xTx at beginning of each iteration to save computing time
        yTy = Y.T.dot(Y)
        xTx = X.T.dot(X)
        # Being iteration to solve for X based on fixed Y
        for u in range(num_user):
            conf_samp = conf[u,:].toarray() # Grab user row from confidence matrix and convert to dense
            pref = conf_samp.copy() 
            pref[pref != 0] = 1 # Create binarized preference vector 
            CuI = sp.diags(conf_samp, [0]) # Get Cu - I term, don't need to subtract 1 since we never added it 
            yTCuIY = Y.T.dot(CuI).dot(Y) # This is the yT(Cu-I)Y term 
            yTCupu = Y.T.dot(CuI + Y_eye).dot(pref.T) # This is the yTCuPu term, where we add the eye back in
                                                      # Cu - I + I = Cu
            X[u] = sp.linalg.spsolve(yTy + yTCuIY + lambda_eye, yTCupu) 
            # Solve for Xu = ((yTy + yT(Cu-I)Y + lambda*I)^-1)yTCuPu, equation 4 from the paper  
        # Begin iteration to solve for Y based on fixed X 
        for i in range(num_item):
            conf_samp = conf[:,i].T.toarray() # transpose to get it in row format and convert to dense
            pref = conf_samp.copy()
            pref[pref != 0] = 1 # Create binarized preference vector
            CiI = sp.diags(conf_samp, [0]) # Get Ci - I term, don't need to subtract 1 since we never added it
            xTCiIX = X.T.dot(CiI).dot(X) # This is the xT(Cu-I)X term
            xTCiPi = X.T.dot(CiI + X_eye).dot(pref.T) # This is the xTCiPi term
            Y[i] = sp(xTx + xTCiIX + lambda_eye, xTCiPi)
            # Solve for Yi = ((xTx + xT(Cu-I)X) + lambda*I)^-1)xTCiPi, equation 5 from the paper
    # End iterations
    return X, Y.T # Transpose at the end to make up for not being transposed at the beginning. 
                         # Y needs to be rank x n. Keep these as separate matrices for scale reasons.

user_vecs, item_vecs = implicit_weighted_ALS(X_train, lambda_val = 0.1, alpha = 15, iterations = 1,
                                            rank_size = 20)

print(user_vecs)
print(item_vecs)

def max_n(row_data, row_indices, n):
        i = row_data.argsort()[-n:]
        # i = row_data.argpartition(-n)[-n:]
        top_values = row_data[i]
        top_indices = row_indices[i]  # do the sparse indices matter?
        return top_values, top_indices, i

def predict_topk(ratings, similarity, kind='user', k=40):
    pred = sp.csr_matrix((0,ratings.shape[1]), dtype=np.int8)
    if kind == 'user':
        for i in range(similarity.shape[0]):
            top_k_values, top_k_users = max_n(np.array(similarity.data[i]),np.array(similarity.rows[i]),k)[:2]
            current = top_k_values.reshape(1,-1).dot(ratings[top_k_users].todense())
            current /= np.sum(np.abs(top_k_values))+1
            sp.vstack([pred, current])
    if kind == 'item':
        for j in range(ratings.shape[1]):
            top_k_items = [np.argsort(similarity[:,j])[:-k-1:-1]]
            for i in range(ratings.shape[0]):
                pred[i, j] = similarity[j, :][top_k_items].dot(ratings[i, :][top_k_items].T) 
                pred[i, j] /= np.sum(np.abs(similarity[j, :][top_k_items]))        
    
    return pred

# pred = predict_topk(X_train, cosine_similarity_matrix_ll, kind='user', k=5)