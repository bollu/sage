

# httpolysoup://doc.sagemath.org/html/en/thematic_tutorials/numerical_sage/cvxopt.html
from cvxopt.base import spmatrix
from cvxopt import cholmod
from cvxopt import amd
from sage import *
import sage.ddg.bunny
import sage.ddg.triangle
from sage.ddg.halfedge_mesh import *


# def choldoc():
#     F = RealField(100)
#     # F = RDF
#     A = matrix(F, [[ 78, -30, -37,  -2], [-30, 102, 179, -18], [-37, 179, 326, -38], [ -2, -18, -38,  15]], sparse=True) 
#     # A = matrix(QQ, [[1.0, 3.0], [3.0, -6.0]], sparse=True)
#     # print(A.cholesky())
#     # A = Matrix(RDF, 6, {(0,0):3, (1,1):42}, sparse=True)
#     cholesky(A)
#     print("###cholesky from impl:###")
#     print(A.cholesky())
# 
# 
# def cholesky(A):
# # A = Matrix(RDF, 6, {(0,0):3, (1,1):42}, sparse=True)
# # print(A)
#     # print("sparse? %s" % A.is_sparse())
#     # cholmod.options['supernodal']=0
#     nonzero = A.nonzero_positions()
#     print(nonzero)
#     rs = [r for (r, c) in nonzero]
#     cs = [c for (r, c) in nonzero]
#     vs = [float(A[ix]) for ix in nonzero]
#     # vs = [1.0, 2.0]
#     print(rs)
#     print(cs)
#     print(vs)
#     Acvx = spmatrix(vs, rs, cs)
#     Pcvx = amd.order(Acvx)
#     Fcvx = cholmod.symbolic(Acvx, Pcvx)
#     print(Acvx)
#     print(Fcvx)
#     numeric = cholmod.numeric(Acvx,Fcvx)
#     chol = cholmod.getfactor(Fcvx)
#     print(chol)
#     Cvals = {}
#     for i in range(len(chol.I)):
#         Cvals[(chol.I[i], chol.J[i])] = chol.V[i]
#     C = Matrix(A.base_ring(), chol.size[0], chol.size[1], Cvals, sparse=True)
#     C.set_immutable()
#     print(C)
#     return C
# 
# choldoc()
# 
# polysoup = MeshIO.readOBJ(sage.ddg.triangle.triangle)
# polysoup = MeshIO.readOBJ(sage.ddg.bunny.bunny)
print(polysoup)
mesh = Mesh(polysoup)
geometry = Geometry(mesh, polysoup.vertex_positions)
srcs = vector(QQ, len(polysoup.vertex_positions)); srcs[0] = 1
print("creating HeatMethod...")
hm = HeatMethod(geometry)
print("created HeatMethod! computing on the source given")
outh = hm.compute(srcs)
print("computed! plotting")

from sage.plot.plot3d.texture import Texture
import random
random.seed(0)
fs= []
ts = []
davgs = []

print(out)
for fix in range(0, len(polysoup.face_vertex_indices), 3):
  fs.append(polysoup.face_vertex_indices[fix:fix+3])
  ds = [out[vix] for vix in polysoup.face_vertex_indices[fix:fix+1]]
  avg = float(sum(ds)) / 3.0
  davgs.append(avg)
  
dmin = min(davgs); dmax = max(davgs)
for d in davgs:
  dclamp = (d - dmin) / (dmax - dmin)
  ts.append(Texture(color=(dclamp, dclamp, dclamp)))
ifs = IndexFaceSet(fs, polysoup.vertex_positions, texture_list=ts)
ifs.plot()

#    function updateColors(phi = undefined) {
#        maxPhi = 0.0;
#        if (phi) {
#            for (let i = 0; i < phi.nRows(); i++) {
#                maxPhi = Math.max(phi.get(i, 0), maxPhi);
#            }
#        }
#
#        for (let v of mesh.vertices) {
#            let i = v.index;
#
#            let color;
#            if (phi) {
#                color = colormap(maxPhi - phi.get(i, 0), 0, maxPhi, hot);
#
#            } else {
#                color = ORANGE;
#            }
#
#            colors[3 * i + 0] = color.x;
#            colors[3 * i + 1] = color.y;
#            colors[3 * i + 2] = color.z;
#        }
#
#        threeGeometry.attributes.color.needsUpdate = true;
#    }
