# distutils: libraries = flint
# distutils: depends = flint/fmpz_mat.h

from sage.libs.flint.types cimport fmpz_t, fmpz_poly_t, fmpz_mat_t

# flint/fmpz_mat.h
cdef extern from "flint_wrap.h":
    void fmpz_mat_init(fmpz_mat_t mat, unsigned long rows, unsigned long cols)
    void fmpz_mat_init_set(fmpz_mat_t mat, const fmpz_mat_t src)
    void fmpz_mat_set(fmpz_mat_t result, fmpz_mat_t mat)
    void fmpz_mat_clear(fmpz_mat_t mat)
    int fmpz_mat_print_pretty(const fmpz_mat_t mat)
    fmpz_t fmpz_mat_entry(fmpz_mat_t mat, long i, long j)
    long fmpz_mat_nrows(fmpz_mat_t mat)
    long fmpz_mat_ncols(fmpz_mat_t mat)
    void fmpz_mat_one(fmpz_mat_t mat)
    void fmpz_mat_zero(fmpz_mat_t mat)
    void fmpz_mat_neg(fmpz_mat_t f, fmpz_mat_t g)
    void fmpz_mat_scalar_mul_si(fmpz_mat_t B, const fmpz_mat_t A, long c)
    void fmpz_mat_scalar_mul_fmpz(fmpz_mat_t B, const fmpz_mat_t A, const fmpz_t c)
    void fmpz_mat_mul(fmpz_mat_t C, const fmpz_mat_t A, const fmpz_mat_t B)
    void fmpz_mat_sqr(fmpz_mat_t B, const fmpz_mat_t A)
    void fmpz_mat_add(fmpz_mat_t C, const fmpz_mat_t A, const fmpz_mat_t B)
    void fmpz_mat_sub(fmpz_mat_t C, const fmpz_mat_t A, const fmpz_mat_t B)
    void fmpz_mat_pow(fmpz_mat_t C, const fmpz_mat_t A, unsigned long n)
    bint fmpz_mat_is_zero(const fmpz_mat_t mat)
    bint fmpz_mat_is_one(const fmpz_mat_t mat)
    void fmpz_mat_charpoly(fmpz_poly_t cp, const fmpz_mat_t mat)
    void fmpz_mat_det(fmpz_t det, const fmpz_mat_t A)
    int fmpz_mat_inv(fmpz_mat_t Ainv, fmpz_t den, const fmpz_mat_t A)
    void fmpz_mat_transpose(fmpz_mat_t B, const fmpz_mat_t A)
    long fmpz_mat_rref(fmpz_mat_t B, fmpz_t den, const fmpz_mat_t A)
    long fmpz_mat_fflu(fmpz_mat_t B, fmpz_poly_t den, long *perm, const fmpz_mat_t A, int rank_check)
    long fmpz_mat_rref_fraction_free(long * perm, fmpz_mat_t B, fmpz_t den, const fmpz_mat_t A)
    long fmpz_mat_rank(const fmpz_mat_t A)
    int fmpz_mat_solve(fmpz_mat_t X, fmpz_t den, const fmpz_mat_t A, const fmpz_mat_t B)
    long fmpz_mat_nullspace(fmpz_mat_t B, const fmpz_mat_t A)
    void fmpz_mat_hnf(fmpz_mat_t H , const fmpz_mat_t A)
    void fmpz_mat_hnf_transform(fmpz_mat_t H, fmpz_mat_t U, const fmpz_mat_t A)
