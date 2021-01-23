from sage import *
import sage.ddg.bunny
import sage.ddg.triangle
from sage.ddg.halfedge_mesh import *

polysoup = MeshIO.readOBJ(sage.ddg.triangle.triangle)
print(polysoup)
mesh = Mesh(polysoup)
geometry = Geometry(mesh, polysoup.vertex_positions)
hm = HeatMethod(geometry)
srcs = []
hm.compute(srcs)
