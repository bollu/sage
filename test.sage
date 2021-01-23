# https://doc.sagemath.org/html/en/thematic_tutorials/numerical_sage/cvxopt.html
from cvxopt.base import spmatrix
from cvxopt import cholmod
from cvxopt import amd
from sage import *
import sage.ddg.bunny
import sage.ddg.triangle
from sage.ddg.halfedge_mesh import *


def choldoc():
    F = RealField(100)
    # F = RDF
    A = matrix(F, [[ 78, -30, -37,  -2], [-30, 102, 179, -18], [-37, 179, 326, -38], [ -2, -18, -38,  15]], sparse=True) 
    # A = matrix(QQ, [[1.0, 3.0], [3.0, -6.0]], sparse=True)
    # print(A.cholesky())
    # A = Matrix(RDF, 6, {(0,0):3, (1,1):42}, sparse=True)
    cholesky(A)
    print("###cholesky from impl:###")
    print(A.cholesky())


def cholesky(A):
# A = Matrix(RDF, 6, {(0,0):3, (1,1):42}, sparse=True)
# print(A)
    # print("sparse? %s" % A.is_sparse())
    # cholmod.options['supernodal']=0
    nonzero = A.nonzero_positions()
    print(nonzero)
    rs = [r for (r, c) in nonzero]
    cs = [c for (r, c) in nonzero]
    vs = [float(A[ix]) for ix in nonzero]
    # vs = [1.0, 2.0]
    print(rs)
    print(cs)
    print(vs)
    Acvx = spmatrix(vs, rs, cs)
    Pcvx = amd.order(Acvx)
    Fcvx = cholmod.symbolic(Acvx, Pcvx)
    print(Acvx)
    print(Fcvx)
    numeric = cholmod.numeric(Acvx,Fcvx)
    chol = cholmod.getfactor(Fcvx)
    print(chol)
    Cvals = {}
    for i in range(len(chol.I)):
        Cvals[(chol.I[i], chol.J[i])] = chol.V[i]
    C = Matrix(A.base_ring(), chol.size[0], chol.size[1], Cvals, sparse=True)
    C.set_immutable()
    print(C)
    return C

choldoc()
# 
# polysoup = MeshIO.readOBJ(sage.ddg.triangle.triangle)
# print(polysoup)
# mesh = Mesh(polysoup)
# geometry = Geometry(mesh, polysoup.vertex_positions)
# hm = HeatMethod(geometry)
# srcs = []
# hm.compute(srcs)
