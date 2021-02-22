from .matrix_generic_sparse cimport Matrix_generic_sparse

cdef class Matrix_real_double_sparse(Matrix_generic_sparse):
    def cholesky(self):
        print("DEBUG: subclass method")
        return None
