from sage import *
import sage.ddg.bunny
from sage.ddg.halfedge_mesh import *

polysoup = MeshIO.readOBJ(sage.ddg.bunny.bunny)
print(polysoup)
mesh = Mesh(polysoup)
