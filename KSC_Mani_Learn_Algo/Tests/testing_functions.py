#################################################################################
#################################################################################
#################################################################################
# Testing some functions
import numpy as np
import random
# Plotting
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
# sklearn. Maybe do import sklearn * or something?
import sklearn.cluster
from sklearn.neighbors import NearestNeighbors
from sklearn.linear_model import LogisticRegression
# From scipy for kmeans:
import scipy
from scipy import cluster
# Other
import itertools # For permutations
import csv # To make csv's
import time # To time things
rng = np.random.RandomState(0) # Random number generator


################################################################################
################################################################################
################################################################################
# Test manifold estimation:
sigma_tilde = np.array((0,0,0,0,0,1,1,1,1,1))
n = 10
p = 5
rho = p
k = 2
nc = 2 # Number of centers
K = 3
X = np.array(range(n*p)).reshape(n,p)
X[4,:] = np.array((0,1,2,3,4)).reshape(1,p)
nb_size = np.repeat(1,k)



# Initialization:

coeff = np.repeat(1,n**2).reshape(n,n)
# Manifold weighted average estimation:
mani_est = np.zeros((n, p)) 
l=0
X_sub = X[sigma_tilde==l,]
coeff_sub = coeff[sigma_tilde==l,]
mani_sub = mani_est[sigma_tilde==l,]



nbrs = NearestNeighbors(n_neighbors=int(nb_size[l]), algorithm='ball_tree').fit(X_sub)

distances, indices = nbrs.kneighbors(X_sub)



i=0
np.average(X_sub[indices[i,],], axis=0, weights=coeff_sub[i,indices[i,]])


coeff_sub[0,indices[0,]]


#####
for i in range(len(X_sub)):
        mani_sub[i,] = np.array(np.average(X_sub[indices[i,],], axis=0, weights=coeff_sub[i,indices[i,]]))
        
mani_est[sigma_tilde==l,] = mani_sub



















################################################################################
################################################################################
################################################################################
# Testing functions for kmeans and dimension reduction:
sigma_tilde = np.array((0,0,0,0,0,1,1,1,1,1))
n = 10
p = 5
k = 2
nc = 2 # Number of centers
K = 3
X = np.array(range(n*p), dtype='float64').reshape(n,p)
sigma_centers = np.repeat(np.arange(0,k), nc)


################################################################################
def reduce_dimension(X, sigma_tilde, n, p, k, nc):
    X_nc = np.zeros((n, p)) 
    for l in range(k):
        X_sub = X[sigma_tilde==l,]
        U, D, V = np.linalg.svd(X_sub, full_matrices=True)
        U_nc = U[:,:nc]
        D_nc = np.diag(D[:nc])
        V_nc = V[:nc,]
        X_sub_nc = U_nc.dot(D_nc.dot(V_nc))
        X_nc[sigma_tilde==l,] = X_sub_nc
    return X_nc



################################################################################
# Can put in dimension reduced data for X here:
def estimate_manifold_kmeans(X, sigma_tilde, sigma_centers, n, p, k, nc):
    centers = np.empty((nc*k, p))
    for l in range(k):
        centers[sigma_centers==l] = scipy.cluster.vq.kmeans(X[sigma_tilde==l,], nc, iter=20, thresh=1e-05)[0]
    return centers



################################################################################
# This should work for any refinement...

def test_dr(X, centers, sigma_centers, n, nc, k, K):

    distance = np.zeros((n,nc*k)).reshape(n, nc*k)
    distance.shape
    for i in range(n):
        for j in range(nc_full):
            distance[i,j] = np.linalg.norm(X[i,] - centers[j,])

    sigma_hat = np.empty(n)

    for i in range(n):
        ind = np.argpartition(distance[i,], K)[:K]
        nbs = sigma_centers[ind]
        counts = np.empty(k)
        for j in range(k):
            counts[j] = np.sum(nbs == j)
        sigma_hat[i] = np.where(counts == counts.max())[0]

    return sigma_hat



# Some tests:
centers = estimate_manifold_kmeans(X, sigma_tilde, sigma_centers, n, p, k, nc)
test_dr(X, centers, sigma_centers, n, nc, k, K)
centers













################################################################################
################################################################################
################################################################################
# Dimension reduction 
sigma_tilde = np.array((0,0,0,0,0,1,1,1,1,1))
n = 10
p = 5
k = 2
nc = 2 # Number of centers
K = 3
X = np.array(range(n*p)).reshape(n,p)
sigma_centers = np.repeat(np.arange(0,k), nc)
centers = np.empty((nc*k, p))


# First time:
X_sub0 = X[sigma_tilde == 0,:]
U, D, V = np.linalg.svd(X_sub0, full_matrices=True)
U_nc = U[:,:nc]
D_nc = np.diag(D[:nc])
V_nc = V[:nc,]
X_sub0_nc = U_nc.dot(D_nc.dot(V_nc))
centers_0 = scipy.cluster.vq.kmeans(X_sub0_nc, nc, iter=20, thresh=1e-05)[0]

# Second time:
X_sub1 = X[sigma_tilde == 1,:]
U, D, V = np.linalg.svd(X_sub1, full_matrices=True)
U_nc = U[:,:nc]
D_nc = np.diag(D[:nc])
V_nc = V[:nc,]
X_sub1_nc = U_nc.dot(D_nc.dot(V_nc))
centers_1 = scipy.cluster.vq.kmeans(X_sub1_nc, nc, iter=20, thresh=1e-05)[0]

# Fill in:
X_nc = np.zeros((n,p))
X_nc[sigma_tilde==0,:] = X_sub0_nc
X_nc[sigma_tilde==1,:] = X_sub1_nc




'''
################################################################################
################################################################################
################################################################################
# More dimension reduction








LR = LogisticRegression(penalty='l2', dual=False, tol=0.0001, C=lam, fit_intercept=True, intercept_scaling=1, class_weight=None, random_state=None, solver='newton-cg', max_iter=100, multi_class='multinomial', verbose=0, warm_start=False, n_jobs=1)
LR.fit(X_glass, sigma_glass)
coef = LR.coef_.ravel()
coef.shape


# Supervised learning for dimension reduction:
clf_l1_LR = LogisticRegression(C=lam, penalty='l1', tol=0.01)
clf_l1_LR.fit(X, sigma_tilde)
coef_l1 = clf_l1_LR.coef_.ravel()
features = np.where(coef_l1 != 0)[0]
extra = np.zeros((n, p-len(features)))
X_lasso = np.concatenate((X[:,features], extra), axis=1)


# Estimate the manifolds via PCA:
def estimate_manifols_pca(X, sigma_tilde, n, k, p, nb_size):
    mani_est = np.zeros((n,p))
    for l in range(k):
        X_sub = X[sigma_tilde==l,]
        mani_sub = mani_est[sigma_tilde==l,]
        nbrs = NearestNeighbors(n_neighbors=int(nb_size[l]), algorithm='ball_tree').fit(X_sub)
        distances, indices = nbrs.kneighbors(X_sub)
        for i in range(len(X_sub)):
            X_new = X_sub[indices[i,],]
            sample_mean = np.mean(X_new, axis=0)
            X_new_centered = X_new - sample_mean
            sample_cov = np.dot(X_new_centered.T, X_new_centered)/nb_size[l]
            U, s, V = np.linalg.svd(sample_cov)
            mani_sub[i,] = U[1,]
        mani_est[sigma_tilde==l,] = mani_sub
    return mani_est
'''

################################################################################
################################################################################
################################################################################
# Finding rho:
rho_vec = np.arange(650000, 900000, 100)
error_init_vec = np.empty(len(rho_vec))

for i in range(len(rho_vec)):
    rho = rho_vec[i]
    A = r.create_adjacency_matrix(n, X, rho)
    sigma_tilde = r.create_sc_sigma_tilde(A, n, k)
    sigma_tilde_final = r.perm_true(sigma, sigma_tilde, n, k, perms)
    error_init_vec[i] = np.sum(sigma_tilde_final != sigma)

print error_init_vec
rho_vec[np.where(error_init_vec == error_init_vec.min())]
