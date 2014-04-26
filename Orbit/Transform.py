"""Contains utility class for matrix transformations"""
import numpy as np


class Transform(object):
    """Class for transforming a vector from basis V to basis U"""

    def __init__(self, M,):
        """Initialize the transform from V to U with the given  M.
        M should be a list of numpy arrays containing the transformation applied to each
        of the basis vectors of basis V. The list should express each vector in the V basis
        in the U basis. I.E.
        Basis of V = (v_1, v_2, ... , v_m)
        Basis of U = (u_1, u_2, ..., u_n)
        M[0] = [a_1,1, a_1,2, ..., a_1,n] = T(V_1) = a_1,1 * u_1 + a_1,2 * u_2 ... + a_1,n * u_n
        .
        .
        .
        M[m] = [a_m,1, a_m,2, ..., a_m,n] = T(V_m) = a_m,1 * u_1 + a_m,2 * u_2 ... + a_m,n * u_n

        V and U should be lists of basis vectors
        """
        #transpose because we are given column vectors not row vectors
        self.M = np.transpose(np.matrix(M))

    def transform(self, v):
        """Transform the vector v from basis V to basis U. V should be expressed as a linear combination of
        the vectors in basis V. After transformation it
        will be expressed as a linear combination of vectors in basis U"""
        #matrix vector multiply, convert from matrix to array type at the end
        return np.array( v * self.M )