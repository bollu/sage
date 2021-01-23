# https://doc.sagemath.org/html/en/thematic_tutorials/numerical_sage/cvxopt.html
from cvxopt.base import spmatrix
from cvxopt import cholmod
from sage import *
import sage.ddg.bunny
import sage.ddg.triangle
from sage.ddg.halfedge_mesh import *


def choldoc():
    F = RealField(100)
    A = matrix(F, [[1.0, 3.0], [3.0, -6.0]])
    cholesky(A)


def cholesky(A):
# A = Matrix(RDF, 6, {(0,0):3, (1,1):42}, sparse=True)
# print(A)
    # print("sparse? %s" % A.is_sparse())
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
    Fcvx = cholmod.symbolic(Acvx)
    print(Acvx)
    print(Fcvx)
    numeric = cholmod.numeric(Acvx,Fcvx)
    chol = cholmod.getfactor(Fcvx)
    print(chol)
    print(type(chol))

choldoc()
# 
# polysoup = MeshIO.readOBJ(sage.ddg.triangle.triangle)
# print(polysoup)
# mesh = Mesh(polysoup)
# geometry = Geometry(mesh, polysoup.vertex_positions)
# hm = HeatMethod(geometry)
# srcs = []
# hm.compute(srcs)
