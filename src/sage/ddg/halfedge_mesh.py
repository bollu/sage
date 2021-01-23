# https://geometrycollective.github.io/geometry-processing-js/docs/index.html

from sage.rings.all import RDF
from sage.plot.plot3d.index_face_set import IndexFaceSet
from collections import defaultdict
# TODO: the below import looks sus as all hell. 
from sage.modules.free_module_element import vector
from sage.matrix.constructor import *

class Corner:
    def __init__(self):
        self.halfedge = None
        self.index = None

    # def __init__(self, halfedge, index):
    #     assert isinstance(halfedge, Halfedge)
    #     self.halfedge = halfedge
    #     assert isinstance(index, int)
    #     self.index = index
# class Corner {
#     /**
#      * This class represents a corner in a {@link module:Core.Mesh Mesh}. It is a convenience
#      * wrapper around {@link module:Core.Halfedge Halfedge} - each corner stores the halfedge opposite to it.
#      * @constructor module:Core.Corner
#      * @property {module:Core.Halfedge} halfedge The halfedge opposite to this corner.
#      */
#     constructor() {
#         self.halfedge = undefined;
#         self.index = -1; // an ID between 0 and |C| - 1, where |C| is the number of corners in a mesh
#     }
# 
#     /**
#      * The vertex this corner lies on.
#      * @member module:Core.Corner#vertex
#      * @type {module:Core.Vertex}
#      */
#     get vertex() {
#         return self.halfedge.prev.vertex;
#     }
# 
#     /**
#      * The face this corner is contained in.
#      * @member module:Core.Corner#face
#      * @type {module:Core.Face}
#      */
#     get face() {
#         return self.halfedge.face;
#     }
# 
#     /**
#      * The next corner (in CCW order) in this corner's face.
#      * @member module:Core.Corner#next
#      * @type {module:Core.Corner}
#      */
#     get next() {
#         return self.halfedge.next.corner;
#     }
# 
#     /**
#      * The previous corner (in CCW order) in this corner's face.
#      * @member module:Core.Corner#prev
#      * @type {module:Core.Corner}
#      */
#     get prev() {
#         return self.halfedge.prev.corner;
#     }
# 
#     /**
#      * Defines a string representation for this corner as its index.
#      * @ignore
#      * @method module:Core.Corner#toString
#      * @returns {string}
#      */
#     toString() {
#         return self.index;
#     }
# }

class Edge:
    def __init__(self):
        self.halfedge = None
        self.index = -1
# class Edge {
#   /**
#    * This class represents an edge in a {@link module:Core.Mesh Mesh}.
#    * @constructor module:Core.Edge
#    * @property {module:Core.Halfedge} halfedge One of the halfedges associated with this edge.
#    */
#   constructor() {
#       self.halfedge = undefined;
#       self.index = -1; // an ID between 0 and |E| - 1, where |E| is the number of edges in a mesh
#   }
# 
#   /**
#    * Checks whether this edge lies on a boundary.
#    * @method module:Core.Edge#onBoundary
#    * @returns {boolean}
#    */
#   onBoundary() {
#       return (self.halfedge.onBoundary || self.halfedge.twin.onBoundary);
#   }
    @property
    def onBoundary(self):
        return self.halfedge.onBoundary or self.halfedge.twin.onBoundary
# 
#   /**
#    * Defines a string representation for this edge as its index.
#    * @ignore
#    * @method module:Core.Edge#toString
#    * @returns {string}
#    */
#   toString() {
#       return self.index;
#   }
# }


class Geometry:
# class Geometry {
#   /**
#    * This class represents the geometry of a {@link module:Core.Mesh Mesh}. This includes information such
#    * as the position of vertices as well as methods to compute edge lengths, corner
#    * angles, face area, normals, discrete curvatures etc.
#    * @constructor module:Core.Geometry
#    * @param {module:Core.Mesh} mesh The mesh this class describes the geometry of.
#    * @param {module:LinearAlgebra.Vector[]} positions An array containing the position of each vertex in a mesh.
#    * @param {boolean} normalizePositions flag to indicate whether positions should be normalized. Default value is true.
#    * @property {module:Core.Mesh} mesh The mesh this class describes the geometry of.
#    * @property {Object} positions A dictionary mapping each vertex to a normalized position.
#    */
    def __init__(self, mesh, positions, normalizePositions = True):
        self.mesh = mesh
        self.positions = {}
        assert len(positions) == len(self.mesh.vertices)
        # TODO: consider using a `zip`?
        for (i, p) in enumerate(positions):
            v = self.mesh.vertices[i];
            self.positions[v] = vector(p);
  
        if (normalizePositions):
            self.normalize(self.positions, mesh.vertices);
# 
#   /**
#    * Computes the vector along a halfedge.
#    * @method module:Core.Geometry#vector
#    * @param {module:Core.Halfedge} h The halfedge along which the vector needs to be computed.
#    * @returns {module:LinearAlgebra.Vector}
#    */
    def vector(self, h):
        a = self.positions[h.vertex];
        b = self.positions[h.next.vertex];
        return b - a;
#   }
# 
#   /**
#    * Computes the length of an edge.
#    * @method module:Core.Geometry#length
#    * @param {module:Core.Edge} e The edge whose length needs to be computed.
#    * @returns {number}
#    */
    def length(self, e):
        return self.vector(e.halfedge).norm();
# 
#   /**
#    * Computes the midpoint of an edge.
#    * @method module:Core.Geometry#midpoint
#    * @param {module:Core.Edge} e The edge whose midpoint needs to be computed.
#    * @returns {number}
#    */
    def midpoint(self, e):
        h = e.halfedge;
        a = self.positions[h.vertex];
        b = self.positions[h.twin.vertex];
  
        # return (a.plus(b)).over(2);
        return (a + b) * 0.5
# 
#   /**
#    * Computes the mean edge length of all the edges in a mesh.
#    * @method module:Core.Geometry#meanEdgeLength
#    * @returns {number}
#    */
    def meanEdgeLength(self):
        es = self.mesh.edges
        return sum([self.length(e) for e in es]) / float(len(es))
        # sum = 0;
        # edges = self.mesh.edges;
        # for (e of edges) {
        #   sum += self.length(e);
        # }
    
        # return sum / edges.length;
# 
#   /**
#    * Computes the area of a face.
#    * @method module:Core.Geometry#area
#    * @param {module:Core.Face} f The face whose area needs to be computed.
#    * @returns {number}
#    */
    def area(self, f):
        assert isinstance(f, Face)
        if (f.isBoundaryLoop()): return 0.0;
        u = self.vector(f.halfedge);
        v = -1 * self.vector(f.halfedge.prev)
        # TODO: should I encode 1/2 in some other way?
        return 0.5 * u.cross_product(v).norm();
# 
#   /**
#    * Computes the total surface area of a mesh.
#    * @method module:Core.Geometry#totalArea
#    * @returns {number}
#    */
    def totalArea(self):
        return sum([self.area(f) for f in self.mesh.faces])
        # sum = 0.0;
        # for (f of self.mesh.faces) {
        #   sum += self.area(f);
        # }
  
        # return sum;
# 
#   /**
#    * Computes the normal of a face.
#    * @method module:Core.Geometry#faceNormal
#    * @param {module:Core.Face} f The face whose normal needs to be computed.
#    * @returns {module:LinearAlgebra.Vector}
#    */
    def faceNormal(self, f):
        assert not f.isBoundaryLoop()
        # if (f.isBoundaryLoop()) return undefined;
  
        u = self.vector(f.halfedge);
        # TODO Sid: negated?! why?
        v = self.vector(f.halfedge.prev).negated();
  
        return u.cross_product(v).unit();
# 
#   /**
#    * Computes the centroid of a face.
#    * @method module:Core.Geometry#centroid
#    * @param {module:Core.Face} f The face whose centroid needs to be computed.
#    * @returns {module:LinearAlgebra.Vector}
#    */
    def centroid(self, f):
        h = f.halfedge;
        a = self.positions[h.vertex];
        b = self.positions[h.next.vertex];
        c = self.positions[h.prev.vertex];
  
        # TODO: what does it mean to be a boundary loop, formally?
        if (f.isBoundaryLoop()):
            return a.plus(b).over(2);
  
        return a.plus(b).plus(c).over(3);
# 
#   /**
#    * Computes the circumcenter of a face.
#    * @method module:Core.Geometry#circumcenter
#    * @param {module:Core.Face} f The face whose circumcenter needs to be computed.
#    * @returns {module:LinearAlgebra.Vector}
#    */
    def circumcenter(self, f):
        h = f.halfedge;
        a = self.positions[h.vertex];
        b = self.positions[h.next.vertex];
        c = self.positions[h.prev.vertex];
  
        # TODO: Sid: what does it mean to be a boundary loop?
        if (f.isBoundaryLoop()):
            return a.plus(b).over(2);
  
        # TODO: what does this computation do? how does this work?
        ac = c.minus(a);
        ab = b.minus(a);
        w = ab.cross_product(ac);
        
        u = (w.cross_product(ab)).times(ac.norm2());
        v = (ac.cross_product(w)).times(ab.norm2());
        x = (u.plus(v)).over(2 * w.norm2());
  
        return x.plus(a);
# 
#   /**
#    * Computes an orthonormal bases for a face.
#    * @method module:Core.Geometry#orthonormalBases
#    * @param {module:Core.Face} f The face on which the orthonormal bases needs to be computed.
#    * @returns {module:LinearAlgebra.Vector[]} An array containing two orthonormal vectors tangent to the face.
#    */
    def orthonormalBases(f):
        # Basis of tangent U Basis of normal spans R^3
        # so pick the first vector in the "basis of tangent" as e1.
        # pick the single vector in "basis of normal" as the face normal.
        # find e2 by finding the unique vector perpendicular to both
        # e1 and normal.
        # Note that this works in 3D due to the existence of the cross_product product.
        e1 = self.vector(f.halfedge).unit();
        normal = self.faceNormal(f);

        # guaranteed to have unit magnitude:
        # |e1 x normal| = |e1| x |normal| = 1x1 = 1
        e2 = normal.cross_product(e1);
    
        return [e1, e2];
# 
#   /**
#    * Computes the angle (in radians) at a corner.
#    * @method module:Core.Geometry#angle
#    * @param {module:Core.Corner} c The corner at which the angle needs to be computed.
#    * @returns {number} The angle clamped between 0 and π.
#    */
    def angle(self, c):
        u = self.vector(c.halfedge.prev).unit();
        v = self.vector(c.halfedge.next).negated().unit();
  
        # there should be an `atan2` somewhere? this seems to clunky
        return acos(max(-1.0, Math.min(1.0, u.dot_product(v))));
# 
#   /**
#    * Computes the cotangent of the angle opposite to a halfedge.
#    * @method module:Core.Geometry#cotan
#    * @param {module:Core.Halfedge} h The halfedge opposite to the angle whose cotangent needs to be computed.
#    * @returns {number}
#    */
    def cotan(self, h):
        if (h.onBoundary):
            return 0.0;

        u = self.vector(h.prev);
        v = -1 * self.vector(h.next)
  
        # TODO: write a succinct derivation.
        return u.dot_product(v) / u.cross_product(v).norm();
# 
#   /**
#    * Computes the signed angle (in radians) between two adjacent faces.
#    * @method module:Core.Geometry#dihedralAngle
#    * @param {module:Core.Halfedge} h The halfedge (shared by the two adjacent faces) on which
#    * the dihedral angle is computed.
#    * @returns {number} The dihedral angle.
#    */
    def dihedralAngle(self, h):
        if (h.onBoundary or h.twin.onBoundary):
            return 0.0;
  
        n1 = self.faceNormal(h.face);
        n2 = self.faceNormal(h.twin.face);
        w = self.vector(h).unit();
  
        cosTheta = n1.dot(n2);
        sinTheta = n1.cross_product(n2).dot(w);
  
        # TODO: draw a picture
        return Math.atan2(sinTheta, cosTheta);
# 
#   /**
#    * Computes the barycentric dual area of a vertex.
#    * @method module:Core.Geometry#barycentricDualArea
#    * @param {module:Core.Vertex} v The vertex whose barycentric dual area needs to be computed.
#    * @returns {number}
#    */
    # TODO: add an explanation for barycentric dual area.
    def barycentricDualArea(self, v):
        area = 0.0;
        for f in v.adjacentFaces():
            area += self.area(f) / 3;
        return area;
# 
#   /**
#    * Computes the circumcentric dual area of a vertex.
#    * @see {@link http://cs.cmu.edu/~kmcrane/Projects/Other/TriangleAreasCheatSheet.pdf}
#    * @method module:Core.Geometry#circumcentricDualArea
#    * @param {module:Core.Vertex} v The vertex whose circumcentric dual area needs to be computed.
#    * @returns {number}
#    */
    # TODO: add an explanation for circumcentric dual area.
    def circumcentricDualArea(self, v):
        area = 0.0;
        for h in v.adjacentHalfedges():
            u2 = self.vector(h.prev).norm2();
            v2 = self.vector(h).norm2();
            cotAlpha = self.cotan(h.prev);
            cotBeta = self.cotan(h);
    
            area += (u2 * cotAlpha + v2 * cotBeta) / 8;
    
        return area;
# 
#   /**
#    * Computes the normal at a vertex using the "equally weighted" method.
#    * @method module:Core.Geometry#vertexNormalEquallyWeighted
#    * @param {module:Core.Vertex} v The vertex on which the normal needs to be computed.
#    * @returns {module:LinearAlgebra.Vector}
#    */
    # TODO: what is the equally weighted method?
    def vertexNormalEquallyWeighted(self, v):
        n = Vector();
        for f in v.adjacentFaces():
            normal = self.faceNormal(f);
            n.incrementBy(normal);
        n.normalize();    
        return n;
# 
#   /**
#    * Computes the normal at a vertex using the "face area weights" method.
#    * @method module:Core.Geometry#vertexNormalAreaWeighted
#    * @param {module:Core.Vertex} v The vertex on which the normal needs to be computed.
#    * @returns {module:LinearAlgebra.Vector}
#    */
    def vertexNormalAreaWeighted(self, v):
        n = Vector();
        for f in v.adjacentFaces():
            normal = self.faceNormal(f);
            area = self.area(f);
  
            n.incrementBy(normal.times(area));
        n.normalize();
        return n;
# 
#   /**
#    * Computes the normal at a vertex using the "tip angle weights" method.
#    * @method module:Core.Geometry#vertexNormalAngleWeighted
#    * @param {module:Core.Vertex} v The vertex on which the normal needs to be computed.
#    * @returns {module:LinearAlgebra.Vector}
#    */
    # TODO: write documentation
    def vertexNormalAngleWeighted(self, v):
        n = Vector();
        for c in v.adjacentCorners():
            normal = self.faceNormal(c.halfedge.face);
            angle = self.angle(c);
            n.incrementBy(normal.times(angle));
   
        n.normalize();
        return n;
# 
#   /**
#    * Computes the normal at a vertex using the "gauss curvature" method.
#    * @method module:Core.Geometry#vertexNormalGaussCurvature
#    * @param {module:Core.Vertex} v The vertex on which the normal needs to be computed.
#    * @returns {module:LinearAlgebra.Vector}
#    */
    # TODO: write explanation
    def vertexNormalGaussCurvature(v):
        n = Vector();
        for h in v.adjacentHalfedges():
            weight = 0.5 * self.dihedralAngle(h) / self.length(h.edge);
  
            n.decrementBy(self.vector(h).times(weight));
  
        n.normalize();
        return n;
  
#   /**
#    * Computes the normal at a vertex using the "mean curvature" method (same as the "area gradient" method).
#    * @method module:Core.Geometry#vertexNormalMeanCurvature
#    * @param {module:Core.Vertex} v The vertex on which the normal needs to be computed.
#    * @returns {module:LinearAlgebra.Vector}
#    */
    def vertexNormalMeanCurvature(self, v):
        n = Vector();
        for h in  v.adjacentHalfedges():
            weight = 0.5 * (self.cotan(h) + self.cotan(h.twin));
            n.decrementBy(self.vector(h).times(weight));
  
        n.normalize();
        return n;
# 
#   /**
#    * Computes the normal at a vertex using the "inscribed sphere" method.
#    * @method module:Core.Geometry#vertexNormalSphereInscribed
#    * @param {module:Core.Vertex} v The vertex on which the normal needs to be computed.
#    * @returns {module:LinearAlgebra.Vector}
#    */
    def vertexNormalSphereInscribed(self, v): 
        n = Vector();
        for c in v.adjacentCorners():
            u = self.vector(c.halfedge.prev);
            v = self.vector(c.halfedge.next).negated();
   
            n.incrementBy(u.cross_product(v).over(u.norm2() * v.norm2()));

        n.normalize();
        return n;
# 
#   /**
#    * Computes the angle defect at a vertex (= 2π minus the sum of incident angles
#    * at an interior vertex or π minus the sum of incident angles at a boundary vertex).
#    * @method module:Core.Geometry#angleDefect
#    * @param {module:Core.Vertex} v The vertex whose angle defect needs to be computed.
#    * @returns {number}
#    */
    # TODO: explain how this is a measure of curvature
    def angleDefect(self, v):
        angleSum = 0.0;
        for c in v.adjacentCorners():
            angleSum += self.angle(c);
    
#       return v.onBoundary() ? Math.PI - angleSum : 2 * Math.PI - angleSum;
#   }
# 
#   /**
#    * Computes the (integrated) scalar gauss curvature at a vertex.
#    * @method module:Core.Geometry#scalarGaussCurvature
#    * @param {module:Core.Vertex} v The vertex whose gauss curvature needs to be computed.
#    * @returns {number}
#    */
    def scalarGaussCurvature(self, v):
        return self.angleDefect(v);
# 
#   /**
#    * Computes the (integrated) scalar mean curvature at a vertex.
#    * @method module:Core.Geometry#scalarMeanCurvature
#    * @param {module:Core.Vertex} v The vertex whose mean curvature needs to be computed.
#    * @returns {number}
#    TODO: add explanation for WTF this is
#    */
    def scalarMeanCurvature(self, v):
        s = 0.0;
        for h in v.adjacentHalfedges():
            s += 0.5 * self.length(h.edge) * self.dihedralAngle(h);
        return s;
# 
#   /**
#    * Computes the total angle defect (= 2π times the euler characteristic of the mesh).
#    * @method module:Core.Geometry#totalAngleDefect
#    * @returns {number}
#    */
     # TODO: check that this is indeeed 2π times the euler characteristic
    def totalAngleDefect(self):
        totalDefect = 0.0;
        for v in self.mesh.vertices:
            totalDefect += self.angleDefect(v);
   
        return totalDefect;
   
#   /**
#    * Computes the (pointwise) minimum and maximum principal curvature values at a vertex.
#    * @method module:Core.Geometry#principalCurvatures
#    * @param {module:Core.Vertex} v The vertex on which the principal curvatures need to be computed.
#    * @returns {number[]} An array containing the minimum and maximum principal curvature values at a vertex.
#   TODO: add explanation for what this is
#    */
    def principalCurvatures(self, v):
        A = self.circumcentricDualArea(v);
        H = self.scalarMeanCurvature(v) / A;
        K = self.angleDefect(v) / A;
   
        # TODO: why do we clamp the discriminant?
        # This might make it harder to do "symbolic" stuff.
        discriminant = H * H - K;
        if (discriminant > 0): discriminant = Math.sqrt(discriminant);
        else: discriminant = 0;
   
        k1 = H - discriminant;
        k2 = H + discriminant;
   
        return [k1, k2];
# 
#   /**
#    * Builds a sparse laplace matrix. The laplace operator is negative semidefinite;
#    * instead we build a positive definite matrix by multiplying the entries of the
#    * laplace matrix by -1 and shifting the diagonal elements by a small constant (e.g. 1e-8).
#    * @method module:Core.Geometry#laplaceMatrix
#    * @param {Object} vertexIndex A dictionary mapping each vertex of a mesh to a unique index.
#    * @returns {module:LinearAlgebra.SparseMatrix}
#    TODO: why do we build positive definite operator?
#    */
    def laplaceMatrix(self, vertexIndex):
        # V = self.mesh.vertices.length;
        # TODO: what is Triplet?
        # T = Triplet(V, V);
        laplace = {}
        for v in self.mesh.vertices:
            i = vertexIndex[v];
            total = 1e-8;
    
            for h in v.adjacentHalfedges():
                j = vertexIndex[h.twin.vertex];
                weight = (self.cotan(h) + self.cotan(h.twin)) / 2;
                total += weight;
                laplace[(i, j)] = -1  * weight
                # T.addEntry(-weight, i, j);
            # T.addEntry(total, i, i);
            laplace[(i, i)] = total
    
        return Matrix(len(self.mesh.vertices), laplace, sparse=True)
# 
#   /**
#    * Builds a sparse diagonal mass matrix containing the barycentric dual area of each vertex
#    * of a mesh.
#    * @method module:Core.Geometry#massMatrix
#    * @param {Object} vertexIndex A dictionary mapping each vertex of a mesh to a unique index.
#    * @returns {module:LinearAlgebra.SparseMatrix}
#    */
    def massMatrix(self, vertexIndex):
        # V = len(self.mesh.vertices);
        # T = Triplet(V, V);
        # VxV matrix
        # mass = Matrix(len(self.mesh.vertices), sparse=True)
        mass = {}
        for v in self.mesh.vertices:
            i = vertexIndex[v];
            # T.addEntry(self.barycentricDualArea(v), i, i);
            mass[(i,i)] = self.barycentricDualArea(v)
  
        return Matrix(len(self.mesh.vertices), mass, sparse=True)
# 
#   /**
#    * Builds a sparse complex laplace matrix. The laplace operator is negative semidefinite;
#    * instead we build a positive definite matrix by multiplying the entries of the
#    * laplace matrix by -1 and shifting the diagonal elements by a small constant (e.g. 1e-8).
#    * @method module:Core.Geometry#complexLaplaceMatrix
#    * @param {Object} vertexIndex A dictionary mapping each vertex of a mesh to a unique index.
#    * @returns {module:LinearAlgebra.ComplexSparseMatrix}
#    */
#    TODO: What is a complex laplace matrix?
    def complexLaplaceMatrix(self, vertexIndex):
        V = self.mesh.vertices.length;
        T = ComplexTriplet(V, V);
        for v in self.mesh.vertices:
            i = vertexIndex[v];
            sum = 1e-8;
  
            for h in v.adjacentHalfedges():
                j = vertexIndex[h.twin.vertex];
                weight = (self.cotan(h) + self.cotan(h.twin)) / 2;
                sum += weight;  
                T.addEntry(Complex(-weight), i, j);
            T.addEntry(Complex(sum), i, i);
  
        return ComplexSparseMatrix.fromTriplet(T);
# 
# /**
#  * Centers a mesh about the origin and rescales it to unit radius.
#  * @global
#  * @function module:Core.normalize
#  * @param {module:LinearAlgebra.Vector[]} positions The position of each vertex in the vertices array.
#  * @param {module:Core.Vertex[]} vertices The vertices of a mesh.
#  * @param {boolean} rescale A flag indicating whether mesh positions should be scaled to a unit radius.
#  */
    def normalize(self, positions, vertices, rescale=True):
        # compute center of mass
        N = len(vertices);
        cm = vector((0, 0, 0));
        for v in vertices:
            p = positions[v];
            # cm.incrementBy(p);
            cm += p
        # cm.divideBy(N);     
        cm /= N
        radius = -1;
        for v in vertices:
            # p.decrementBy(cm);
            positions[v] = positions[v] - cm
            radius = max(radius, p.norm())
        
        if rescale:
            for v in vertices:
                positions[v] = positions[v] / radius

# /**
#  * This module implements a halfedge mesh data structure and its associated geometry.
#  * A halfedge mesh stores mesh elements such as vertices, edges and faces as well as
#  * their connectivity information. The latter is particulary important in geometry
#  * processing, as algorithms often exploit local connectivity of mesh elements. At
#  * the cost of slightly higher memory consumption compared to other data structures,
#  * a halfedge mesh enables quick access of mesh elements. For example, it is possible to
#  * enumerate the vertices and edges contained in and faces adjacent to any single face
#  * in a mesh. Similar enumerations are also possible for any vertex or edge in a mesh.
#  * Additionally, its possible to perform global traversals that enumerate over all mesh
#  * vertices, edges and faces in an unspecified but fixed order.
#  *
#  * <img src="../imgs/halfedge.png">
#  *
#  * The diagram above illustrates how connectivity information is stored locally in a
#  * halfedge mesh. The key idea is to split a edge into two directed halfedges. Each
#  * halfedge stores a reference to the vertex at its base, the edge it lies on, the
#  * face adjacent to it, the next halfedge in counter clockwise order, and the opposite
#  * (or twin) halfedge. Each vertex, edge and face of a mesh in turn stores a reference
#  * to one of the halfedges (outgoing in the case of a vertex) its incident on.
#  *
#  * @module Core
#  */
class Halfedge:
    def __init__(self):
        self.vertex =     None
        self.edge =       None
        self.face =       None
        self.corner =     None
        self.next =       None
        self.prev =       None
        self.twin =       None
        self.onBoundary = None
        self.index =      None

    # def __init__(self, vertex, edge, face, corner, next_, prev, twin, onBoundary, index):
    #     self.vertex = vertex;
    #     self.edge = edge;
    #     self.face = face;
    #     self.corner = corner;
    #     self.next = next_;
    #     self.prev = prev;
    #     self.twin = twin;
    #     self.onBoundary = onBoundary;
    #     self.index = index;

# class Halfedge {
#   /**
#    * This class defines the connectivity of a {@link module:Core.Mesh Mesh}.
#    * @constructor module:Core.Halfedge
#    * @property {module:Core.Vertex} vertex The vertex at the base of this halfedge.
#    * @property {module:Core.Edge} edge The edge associated with this halfedge.
#    * @property {module:Core.Face} face The face associated with this halfedge.
#    * @property {module:Core.Corner} corner The corner opposite to this halfedge. Undefined if this halfedge is on the boundary.
#    * @property {module:Core.Halfedge} next The next halfedge (in CCW order) in this halfedge's face.
#    * @property {module:Core.Halfedge} prev The previous halfedge (in CCW order) in this halfedge's face.
#    * @property {module:Core.Halfedge} twin The other halfedge associated with this halfedge's edge.
#    * @property {boolean} onBoundary A flag that indicates whether this halfedge is on a boundary.
#    */
#   constructor() {
#       self.vertex = undefined;
#       self.edge = undefined;
#       self.face = undefined;
#       self.corner = undefined;
#       self.next = undefined;
#       self.prev = undefined;
#       self.twin = undefined;
#       self.onBoundary = undefined;
#       self.index = -1; // an ID between 0 and |H| - 1, where |H| is the number of halfedges in a mesh
#   }
# 
#   /**
#    * Defines a string representation for this halfedge as its index.
#    * @ignore
#    * @method module:Core.Halfedge#toString
#    * @returns {string}
#    */
#   toString() {
#       return self.index;
#   }
# }



class Mesh:
     # This class represents a Mesh.
     # @constructor module:Core.Mesh
     # @property {module:Core.Vertex[]} vertices The vertices contained in this mesh.
     # @property {module:Core.Edge[]} edges The edges contained in this mesh.
     # @property {module:Core.Face[]} faces The faces contained in this mesh.
     # @property {module:Core.Corner[]} corners The corners contained in this mesh.
     # @property {module:Core.Halfedge[]} halfedges The halfedges contained in this mesh.
     # @property {module:Core.Face[]} boundaries The boundary loops contained in this mesh.
     # @property {Array.<module:Core.Halfedge[]>} generators An array of halfedge arrays, i.e.,
     # [[h11, h21, ..., hn1], [h12, h22, ..., hm2], ...] representing this mesh's
     # {@link https://en.wikipedia.org/wiki/Homology_(mathematics)#Surfaces homology generators}.
    # def __init__():
    #     self.vertices = [];
    #     self.edges = [];
    #     self.faces = [];
    #     self.corners = [];
    #     self.halfedges = [];
    #     self.boundaries = [];
    #     self.generators = [];
# 
#   /**
#    * Computes the euler characteristic of this mesh.
#    * @method module:Core.Mesh#eulerCharacteristic
#    * @returns {number}
#    */
    def eulerCharacteristic(self):
        return self.vertices.length - self.edges.length + self.faces.length;
# 
#   /**
#    * Constructs this mesh.
#    * @method module:Core.Mesh#build
#    * @param {Object} polygonSoup A polygon soup mesh containing vertex positions and indices.
#    * @param {module:LinearAlgebra.Vector[]} polygonSoup.v The vertex positions of the polygon soup mesh.
#    * @param {number[]} polygonSoup.f The indices of the polygon soup mesh.
#    * @returns {boolean} True if this mesh is constructed successfully and false if not
#    * (when this mesh contains any one or a combination of the following - non-manifold vertices,
#    *  non-manifold edges, isolated vertices, isolated faces).
#    */
    def __init__(self, polysoup):
        assert isinstance(polysoup, PolygonSoup)
        self.vertices = [];
        self.edges = [];
        self.faces = [];
        self.corners = [];
        self.halfedges = [];
        self.boundaries = [];
        self.generators = [];

        # preallocate elements
        positions = polysoup.vertex_positions
        indices = polysoup.face_vertex_indices
        self.preallocateElements(positions, indices);
  
        # create and insert vertices
        indexToVertex = {} # ix -> processed vertex (?)
        for i in range(len(positions)):
            v = Vertex()
            self.vertices[i] = v
            indexToVertex[i] = v
  
        # create and insert halfedges, edges and non boundary loop faces
        eIndex = 0;
        edgeCount = defaultdict(int)
        existingHalfedges = {}
        hasTwinHalfedge = defaultdict(bool)
        # for (I = 0; I < indices.length; I += 3) {
        for I in range(0, len(indices), 3):
            # create face
            f = Face();
            self.faces[I // 3] = f;
  
            # create a halfedge for each edge of the newly created face
            for J in range(3):
                h = Halfedge();
                self.halfedges[I + J] = h;
  
            # initialize the newly created halfedges
            for J in range(3):
                # current halfedge goes from vertex i to vertex j
                K = (J + 1) % 3;
                i = indices[I + J];
                j = indices[I + K];
  
                # set the current halfedge's attributes
                h = self.halfedges[I + J];
                h.next = self.halfedges[I + K];
                h.prev = self.halfedges[I + (J + 3 - 1) % 3];
                h.onBoundary = False;
                hasTwinHalfedge[h] = False;
  
                # point the halfedge and vertex i to each other
                v = indexToVertex[i]
                h.vertex = v;
                v.halfedge = h;
  
                # point the halfedge and face to each other
                h.face = f;
                f.halfedge = h;
  
                # swap if i > j
                if (i > j): (i, j) = (j, i)
  
                # value = [i, j]
                # key = value.toString();
                key = (i, j)
                # if (existingHalfedges.has(key)) {
                if key in existingHalfedges:
                    # if a halfedge between vertex i and j has been created in the past, then it
                    # is the twin halfedge of the current halfedge
                    twin = existingHalfedges[key]
                    h.twin = twin;
                    twin.twin = h;
                    h.edge = twin.edge;
  
                    # why do we store it here? we can just ask h for a twin?
                    hasTwinHalfedge[h] = True
                    hasTwinHalfedge[twin] = True
                    edgeCount[key] += 1
                    # edgeCount.set(key, edgeCount.get(key) + 1);
  
                else:
                    # create an edge and set its halfedge
                    e = Edge();
                    self.edges[eIndex] = e;
                    eIndex += 1
                    h.edge = e;
                    e.halfedge = h;
  
                    # record the newly created edge and halfedge from vertex i to j
                    existingHalfedges[key] = h
                    edgeCount[key] = 1
  
                # check for non-manifold edges
                if edgeCount[key] > 2:
                    raise ValueError("Mesh has non-manifold edges! between (%s)" % (key, ))
                    return False;
        #### ----- end loop edges
        # ----- end loop indices

        # create and insert boundary halfedges and "imaginary" faces for boundary cycles
        # also create and insert corners
        # WAT?
        print("## len(indices): %s | len(halfedges): %s" % (len(indices), len(self.halfedges)))
        print("creating halfedge...")
        hIndex = len(indices);
        cIndex = 0;
        # for (i = 0; i < indices.length; i++) {
        for i in range(len(indices)):
            # if a halfedge has no twin halfedge, create a face and
            # link it the corresponding boundary cycle
            h = self.halfedges[i];
            print("considering h: %s" % h)
            if not hasTwinHalfedge[h]:
                # create face
                f = Face();
                self.boundaries.append(f);
  
                # walk along boundary cycle
                boundaryCycle = [];
                he = h;
                while True:
                    # create a halfedge
                    bH = Halfedge();
                    self.halfedges[hIndex] = bH;
                    hIndex += 1
                    boundaryCycle.append(bH);
  
                    # grab the next halfedge along the boundary that does not have a twin halfedge
                    nextHe = he.next;
                    while hasTwinHalfedge[nextHe]:
                        nextHe = nextHe.twin.next;
  
                    # set the current halfedge's attributes
                    bH.vertex = nextHe.vertex;
                    bH.edge = he.edge;
                    bH.onBoundary = True;
  
                    # point the halfedge and face to each other
                    bH.face = f;
                    f.halfedge = bH;
  
                    # point the halfedge and he to each other
                    bH.twin = he;
                    he.twin = bH;
  
                    # continue walk
                    he = nextHe;

                    # break walking the boundary when done.
                    print("h: %s | he: %s" % (h, he))
                    if he == h:
                        break
  
                # link the cycle of boundary halfedges together
                n = len(boundaryCycle)
                # for (j = 0; j < n; j++) {
                for j in range(n):
                    # boundary halfedges are linked in clockwise order
                    boundaryCycle[j].next = boundaryCycle[(j + n - 1) % n];
                    boundaryCycle[j].prev = boundaryCycle[(j + 1) % n];
                    hasTwinHalfedge[boundaryCycle[j]] = True
                    hasTwinHalfedge[boundaryCycle[j]] = True
  
            # ^^^ end not having twin halfedge processing ^^^
            # point the newly created corner and its halfedge to each other
            if not h.onBoundary:
                c = Corner();
                c.halfedge = h;
                h.corner = c;
                self.corners[cIndex] = c;
                cIndex += 1

        # convert dictionary into list. I need the dictionary because the 
        # original code does weird as fuck shit to index out of the
        # pre-allocated space.
        halfedgesList = []
        for i in range(len(self.halfedges)):
            assert i in self.halfedges
            halfedgesList.append(self.halfedges[i])
        self.halfedges = halfedgesList

        # check if mesh has isolated vertices, isolated faces or
        # non-manifold vertices
        print("verifying self: no isolated vs")
        self.assertHasNoIsolatedVertices()
        print("verifying self: no isolated fs")
        self.assertHasNoIsolatedFaces()
        print("verifying self: no non manifold vs")
        self.assertHasNoNonManifoldVertices()
        
        # index elements
        print("indexing self")
        self.indexElements();
  
  
    # /**
    #  * Preallocates mesh elements.
    #  * @private
    #  * @method module:Core.Mesh#preallocateElements
    #  * @param {module:LinearAlgebra.Vector[]} positions The vertex positions of a polygon soup mesh.
    #  * @param {number[]} indices The indices of a polygon soup mesh.
    #  */
    def preallocateElements(self, positions, indices):
        nBoundaryHalfedges = 0;
        sortedEdges = set()
        for I in range(0, len(indices), 3):
            for J in range(3):
                K = (J + 1) % 3;
                i = indices[I + J]
                j = indices[I + K]
  
                # swap if i > j
                if (i > j): (i, j) = (j, i)

                value = (i, j)
                if value in sortedEdges:
                    nBoundaryHalfedges -= 1;
                else:
                    sortedEdges.add(value)
                    nBoundaryHalfedges += 1;
        # end I loop for 
        nVertices = len(positions)
        nEdges = len(sortedEdges)
        assert len(indices) % 3 == 0
        nFaces = len(indices) // 3
        nHalfedges = 2 * nEdges;
        nInteriorHalfedges = nHalfedges - nBoundaryHalfedges;
   
        # allocate space
        self.vertices =  [None for _ in range(nVertices)] # Array(nVertices);
        self.edges =     [None for _ in range(nEdges)] # Array(nEdges);
        self.faces =     [None for _ in range(nFaces)] # Array(nFaces);
        self.halfedges = {}
        self.corners =   [None for _ in range(nInteriorHalfedges)] # Array(nInteriorHalfedges);
# 
#   /**
#    * Checks whether this mesh has isolated vertices.
#    * @private
#    * @method module:Core.Mesh#hasIsolatedVertices
#    * @returns {boolean}
#    */
    def assertHasNoIsolatedVertices(self): 
        for v in self.vertices:
            if  v.isIsolated(): 
                raise RuntimeError("Mesh has isolated vertex (%s)" % v)
# 
#   /**
#    * Checks whether this mesh has isolated faces.
#    * @private
#    * @method module:Core.Mesh#hasIsolatedFaces
#    * @returns {boolean}
#    */
    def assertHasNoIsolatedFaces(self):
        for f in self.faces:
            boundaryEdges = 0;
            for h in f.adjacentHalfedges():
                if (h.twin.onBoundary):
                    boundaryEdges += 1;
  
            if (boundaryEdges == 3):
                raise RuntimeError("Mesh has isolated face (%s)" % f);
  
#   /**
#    * Checks whether this mesh has non-manifold vertices.
#    * @private
#    * @method module:Core.Mesh#hasNonManifoldVertices
#    * @returns {boolean}
#    */
    def assertHasNoNonManifoldVertices(self):
        adjacentFaces = {}
        for v in self.vertices:
            adjacentFaces[v] = 0

        print("assertHasNoNonManifoldVertices: 1")
        for f in self.faces:
            for v in f.adjacentVertices():
                adjacentFaces[v] +=  1

        print("assertHasNoNonManifoldVertices: 2")
        for b in self.boundaries:
            for v in b.adjacentVertices():
                adjacentFaces[v] += 1

        print("assertHasNoNonManifoldVertices: 3")
        # TODO: convert this to an asswert here
        for v in self.vertices:
            if adjacentFaces[v] != v.degree():
                raise RuntimeError("expected number of adjacent faces to be equal to degree")
        print("assertHasNoNonManifoldVertices: 4")
# 
#   /**
#    * Assigns indices to this mesh's elements.
#    * @private
#    * @method module:Core.Mesh#indexElements
#    */
    def indexElements(self):
        index = 0;
        for v in self.vertices:
            v.index = index;
            index += 1
  
        index = 0;
        for e in self.edges:
            e.index = index;
            index += 1
  
        index = 0;
        for f in self.faces:
            f.index = index
            index += 1
  
        index = 0;
        for h in self.halfedges:
            h.index = index
            index += 1 
  
        index = 0;
        for c in self.corners:
            c.index = index
            index += 1
  
        index = 0;
        for b in self.boundaries:
            b.index = index
            index += 1

class Face:
    # /**
    #  * This class represents a face in a {@link module:Core.Mesh Mesh}.
    #  * @constructor module:Core.Face
    #  * @property {module:Core.Halfedge} halfedge One of the halfedges associated with this face.
    #  */
    def __init__(self):
        self.halfedge = None
        self.index = None

    # def __init__(self, halfedge, index):
    #     self.halfedge = halfedge
    #     self.index = -1
    #     # self.halfedge = undefined;
    #     # self.index = -1; // an ID between 0 and |F| - 1 if this face is not a boundary loop
    #     # // or an ID between 0 and |B| - 1 if this face is a boundary loop, where |F| is the
    #     # // number of faces in the mesh and |B| is the number of boundary loops in the mesh
  
    # /**
    #  * Checks whether this face is a boundary loop.
    #  * @method module:Core.Face#isBoundaryLoop
    #  * @returns {boolean}
    #  */
    def isBoundaryLoop(self):
        return self.halfedge.onBoundary;
# 
#   /**
#    * Convenience function to iterate over the vertices in this face.
#    * Iterates over the vertices of a boundary loop if this face is a boundary loop.
#    * @method module:Core.Face#adjacentVertices
#    * @param {boolean} ccw A flag indicating whether iteration should be in CCW or CW order.
#    * @returns {module:Core.Vertex}
#    * @example
#    * f = mesh.faces[0]; // or b = mesh.boundaries[0]
#    * for (v of f.adjacentVertices()) {
#    *     // Do something with v
#    * }
#    */
    def adjacentVertices(self, ccw = True):
        return FaceVertexIterator(self.halfedge, ccw);

# 
#   /**
#    * Convenience function to iterate over the edges in this face.
#    * Iterates over the edges of a boundary loop if this face is a boundary loop.
#    * @method module:Core.Face#adjacentEdges
#    * @param {boolean} ccw A flag indicating whether iteration should be in CCW or CW order.
#    * @returns {module:Core.Edge}
#    * @example
#    * f = mesh.faces[0]; // or b = mesh.boundaries[0]
#    * for (e of f.adjacentEdges()) {
#    *     // Do something with e
#    * }
#    */
    def adjacentEdges(self, ccw = True):
        return FaceEdgeIterator(self.halfedge, ccw);
# 
#   /**
#    * Convenience function to iterate over the faces neighboring this face.
#    * @method module:Core.Face#adjacentFaces
#    * @param {boolean} ccw A flag indicating whether iteration should be in CCW or CW order.
#    * @returns {module:Core.Face}
#    * @example
#    * f = mesh.faces[0]; // or b = mesh.boundaries[0]
#    * for (g of f.adjacentFaces()) {
#    *     // Do something with g
#    * }
#    */
    def adjacentFaces(self, ccw = True):
        return FaceFaceIterator(self.halfedge, ccw);
# 
#   /**
#    * Convenience function to iterate over the halfedges in this face.
#    * Iterates over the halfedges of a boundary loop if this face is a boundary loop.
#    * @method module:Core.Face#adjacentHalfedges
#    * @param {boolean} ccw A flag indicating whether iteration should be in CCW or CW order.
#    * @returns {module:Core.Halfedge}
#    * @example
#    * f = mesh.faces[0]; // or b = mesh.boundaries[0]
#    * for (h of f.adjacentHalfedges()) {
#    *     // Do something with h
#    * }
#    */
    def adjacentHalfedges(self, ccw = True):
        return FaceHalfedgeIterator(self.halfedge, ccw);
# 
#   /**
#    * Convenience function to iterate over the corners in this face. Not valid if this face
#    * is a boundary loop.
#    * @method module:Core.Face#adjacentCorners
#    * @param {boolean} ccw A flag indicating whether iteration should be in CCW or CW order.
#    * @returns {module:Core.Corner}
#    * @example
#    * f = mesh.faces[0];
#    * for (c of f.adjacentCorners()) {
#    *     // Do something with c
#    * }
#    */
    def adjacentCorners(self, ccw = True):
        assert not self.BoundaryLoop()
        return FaceCornerIterator(self.halfedge, ccw);
# 
#   /**
#    * Defines a string representation for this face as its index.
#    * @ignore
#    * @method module:Core.Face#toString
#    * @returns {string}
#    */
#   toString() {
#       return self.index;
#   }
# }

# 
# /**
#  * This class represents an adjacent vertex iterator for a {@link module:Core.Face Face}.
#  * @ignore
#  * @memberof module:Core
#  */
class FaceVertexIterator:
#   // constructor
#    constructor(halfedge, ccw) {
#        self._halfedge = halfedge;
#        self._ccw = ccw;
#    }
    def __init__(self, halfedge, ccw):
        self._halfedge = halfedge;
        self._ccw = ccw;
        self._current = self._halfedge;
        self._end = self._halfedge;
        self._justStared = True

        def __iter__(self):
            if not self._justStared and self.current == self._halfedge:
                raise StopIteration
            else:
                self._justStared = False
                if self._ccw:
                    self.current = self.current.next
                else:
                    self.current = self.current.prev
                v = self.current.vertex
                return v

    def __iter__(self):
        return self
        
#   [Symbol.iterator]() {
#       return {
#           current: self._halfedge,
#           end: self._halfedge,
#           ccw: self._ccw,
#           justStarted: true,
#           next() {
#               if (!self.justStarted && self.current === self.end) {
#                   return {
#                       done: true
#                   };
# 
#               } else {
#                   self.justStarted = false;
#                   vertex = self.current.vertex;
#                   self.current = self.ccw ? self.current.next : self.current.prev;
#                   return {
#                       done: false,
#                       value: vertex
#                   }
#               }
#           }
#       }
#   }
# }

    def __next__(self):
        if not self._justStared and self._current == self._end:
            raise StopIteration
        else:
            self._justStared = False
            v = self._current.vertex
            if self._ccw:
                self._current = self._current.next
            else:
                self._current = self._current.prev
            return v

class FaceEdgeIterator:    
# /**
#  * This class represents an adjacent edge iterator for a {@link module:Core.Face Face}.
#  * @ignore
#  * @memberof module:Core
#  */
# class FaceEdgeIterator {
#   // constructor
#   constructor(halfedge, ccw) {
#       self._halfedge = halfedge;
#       self._ccw = ccw;
#   }


    def __init__(self, halfedge, ccw):
        self._halfedge = halfedge;
        self._ccw = ccw;
        self._current = self._halfedge;
        self._justStared = True;

    def __next__(self):
        if not self._justStared and self.current == self.enumerate:
            raise StopIteration
        else:
            self._justStared = False
            e = self.current.edge
            if self._ccw:
                self.current = self._current.next
            else:
                self.current = self._current.prev
            return e

    def __iter__(self):
        return self
#   [Symbol.iterator]() {
#       return {
#           current: self._halfedge,
#           end: self._halfedge,
#           ccw: self._ccw,
#           justStarted: true,
#           next() {
#               if (!self.justStarted && self.current === self.end) {
#                   return {
#                       done: true
#                   };
# 
#               } else {
#                   self.justStarted = false;
#                   edge = self.current.edge;
#                   self.current = self.ccw ? self.current.next : self.current.prev;
#                   return {
#                       done: false,
#                       value: edge
#                   }
#               }
#           }
#       }
#   }
# }
# 
# /**
class FaceFaceIterator:
    pass
# 
#  * This class represents an adjacent face iterator for a {@link module:Core.Face Face}.
#  * @ignore
# 
#  * @memberof module:Core
#  */
# class FaceFaceIterator {
#   // constructor
#   constructor(halfedge, ccw) {
#       while (halfedge.twin.onBoundary) {
#           halfedge = halfedge.next;
#       } // twin halfedge must not be on the boundary
#       self._halfedge = halfedge;
#       self._ccw = ccw;
#   }
    def __init__(self, halfedge, ccw):
        self._halfedge = halfedge;
        self._ccw = ccw;
        self._current = self._halfedge;
        self._justStared = True;


#   [Symbol.iterator]() {
#       return {
#           current: self._halfedge,
#           end: self._halfedge,
#           ccw: self._ccw,
#           justStarted: true,
#           next() {
#               while (self.current.twin.onBoundary) {
#                   self.current = self.ccw ? self.current.next : self.current.prev;
#               } // twin halfedge must not be on the boundary
#               if (!self.justStarted && self.current === self.end) {
#                   return {
#                       done: true
#                   };
# 
#               } else {
#                   self.justStarted = false;
#                   face = self.current.twin.face;
#                   self.current = self.ccw ? self.current.next : self.current.prev;
#                   return {
#                       done: false,
#                       value: face
#                   }
#               }
#           }
#       }
#   }
# }
    def __next__(self):
        if not self._justStared and self.current == self.enumerate:
            raise StopIteration
        else:
            while self.current.twin.onBoundary:
                self.current = self.current.next if self._ccw else self.current.prev

        if not self._justStared and self.current == self.enumerate:
            raise StopIteration
        else:
            self._justStared = False
            e = self.current.edge
            self.current = self.current.next if self._ccw else self.current.prev
            return f


# /**
#  * This class represents an adjacent halfedge iterator for a {@link module:Core.Face Face}.
#  * @ignore
#  * @memberof module:Core
#  */
# class FaceHalfedgeIterator {
#   // constructor
#   constructor(halfedge, ccw) {
#       self._halfedge = halfedge;
#       self._ccw = ccw;
#   }
# 
class FaceHalfedgeIterator:
    def __init__(self, halfedge, ccw):
        self._halfedge = halfedge;
        self._end = self._halfedge;
        self._ccw = ccw;
        self._current = self._halfedge;
        self._justStared = True;

# 
#   [Symbol.iterator]() {
#       return {
#           current: self._halfedge,
#           end: self._halfedge,
#           ccw: self._ccw,
#           justStarted: true,
#           next() {
#               if (!self.justStarted && self.current === self.end) {
#                   return {
#                       done: true
#                   };
# 
#               } else {
#                   self.justStarted = false;
#                   halfedge = self.current;
#                   self.current = self.ccw ? self.current.next : self.current.prev;
#                   return {
#                       done: false,
#                       value: halfedge
#                   }
#               }
#           }
#       }
#   }
# }
    def __iter__(self):
        return self

    def __next__(self):
        if not self._justStared and self._current == self._end:
            raise StopIteration
        else:
            self._justStared = False
            h = self._current
            self._current = self._current.next if self._ccw else self._current.prev
            return h

# /**
#  * This class represents an adjacent corner iterator for a {@link module:Core.Face Face}.
#  * @ignore
#  * @memberof module:Core
#  */
class FaceCornerIterator:
#   // constructor
#   constructor(halfedge, ccw) {
#       self._halfedge = halfedge;
#       self._ccw = ccw;
#   }
    def __init__(self, halfedge, ccw):
        self._halfedge = halfedge;
        self._ccw = ccw;
        self._current = self._halfedge;
        self._justStared = True;

#   [Symbol.iterator]() {
#       return {
#           current: self._halfedge,
#           end: self._halfedge,
#           ccw: self._ccw,
#           justStarted: true,
#           next() {
#               if (!self.justStarted && self.current === self.end) {
#                   return {
#                       done: true
#                   };
# 
#               } else {
#                   self.justStarted = false;
#                   self.current = self.ccw ? self.current.next : self.current.prev;
#                   corner = self.current.corner; // corner will be undefined if this face is a boundary loop
#                   return {
#                       done: false,
#                       value: corner
#                   }
#               }
#           }
#       }
#   }
# }
    def __next__(self):
        if not self._justStared and self.current == self.end:
            raise StopIteration
        else:
            self._justStared = False
            c = self.current.corner # corner will be undefined if face is boundary loop
            self.current = self.current.next if self._ccw else self.current.prev
            return c


class Vertex:
#     /**
#      * This class represents a vertex in a {@link module:Core.Mesh Mesh}.
#      * @constructor module:Core.Vertex
#      * @property {module:Core.Halfedge} halfedge One of the outgoing halfedges associated with this vertex.
#      */
    def __init__(self):
        self.halfedge = None
        self.index = -1
        # self.index = -1; // an ID between 0 and |V| - 1, where |V| is the number of vertices in a mesh
# 
#     /**
#      * Counts the number of edges adjacent to this vertex.
#      * @method module:Core.Vertex#degree
#      * @returns {number}
#      */
      # @property
    def degree(self):
        d = 0
        print("computing degree...")
        for _ in self.adjacentEdges():
            d += 1
        print("degree done! (%d)" % (d, ))
        return d
        # TODO: check if a faster implementation of degree is possible.
        # return len(list(self.adjacentEdges()))
# 
#     /**
#      * Checks whether this vertex is isolated, i.e., it has no neighboring vertices.
#      * @method module:Core.Vertex#isIsolated
#      * @returns {boolean}
    def isIsolated(self):
        return self.halfedge == None
# 
#     /**
#      * Checks whether this vertex lies on a boundary.
#      * @method module:Core.Vertex#onBoundary
#      * @returns {boolean}
#      */
      # @property
    def onBoundary(self): 
        return any([h.onBoundary() for h in self.adjacentHalfedges()])
# 
#     /**
#      * Convenience function to iterate over the vertices neighboring this vertex.
#      * @method module:Core.Vertex#adjacentVertices
#      * @param {boolean} ccw A flag indicating whether iteration should be in CCW or CW order.
#      * @returns {module:Core.Vertex}
#      * @example
#      * v = mesh.vertices[0];
#      * for (u of v.adjacentVertices()) {
#      *     // Do something with u
#      * }
#      */
    def adjacentVertices(self, ccw = True):
      return VertexVertexIterator(self.halfedge, ccw);
# 
#     /**
#      * Convenience function to iterate over the edges adjacent to this vertex.
#      * @method module:Core.Vertex#adjacentEdges
#      * @param {boolean} ccw A flag indicating whether iteration should be in CCW or CW order.
#      * @returns {module:Core.Edge}
#      * @example
#      * v = mesh.vertices[0];
#      * for (e of v.adjacentEdges()) {
#      *     // Do something with e
#      * }
#      */
    def adjacentEdges(self, ccw = True):
        print("creating adjcent edge iter...")
        return VertexEdgeIterator(self.halfedge, ccw);
# 
#     /**
#      * Convenience function to iterate over the faces adjacent to this vertex.
#      * @method module:Core.Vertex#adjacentFaces
#      * @param {boolean} ccw A flag indicating whether iteration should be in CCW or CW order.
#      * @returns {module:Core.Face}
#      * @example
#      * v = mesh.vertices[0];
#      * for (f of v.adjacentFaces()) {
#      *     // Do something with f
#      * }
#      */
    def adjacentFaces(self, ccw = True): 
        return VertexFaceIterator(self.halfedge, ccw);
# 
#     /**
#      * Convenience function to iterate over the halfedges adjacent to this vertex.
#      * @method module:Core.Vertex#adjacentHalfedges
#      * @param {boolean} ccw A flag indicating whether iteration should be in CCW or CW order.
#      * @returns {module:Core.Halfedge}
#      * @example
#      * v = mesh.vertices[0];
#      * for (h of v.adjacentHalfedges()) {
#      *     // Do something with h
#      * }
#      */
    def adjacentHalfedges(self, ccw = True): 
        return VertexHalfedgeIterator(self.halfedge, ccw); # outgoing halfedges
# 
#     /**
#      * Convenience function to iterate over the corners adjacent to this vertex.
#      * @method module:Core.Vertex#adjacentCorners
#      * @param {boolean} ccw A flag indicating whether iteration should be in CCW or CW order.
#      * @returns {module:Core.Corner}
#      * @example
#      * v = mesh.vertices[0];
#      * for (c of v.adjacentCorners()) {
#      *     // Do something with c
#      * }
#      */
    def adjacentCorners(self, ccw = True):
        return VertexCornerIterator(self.halfedge, ccw);
# 
#     /**
#      * Defines a string representation for this vertex as its index.
#      * @ignore
#      * @method module:Core.Vertex#toString
#      * @returns {string}
#      */
#     toString() {
#         return self.index;
#     }
# }
# 
# /**
#  * This class represents an adjacent vertex iterator for a {@link module:Core.Vertex Vertex}.
#  * @ignore
#  * @memberof module:Core
#  */
# class VertexVertexIterator {
#     // constructor
#     constructor(halfedge, ccw) {
#         self._halfedge = halfedge;
#         self._ccw = ccw;
#     }
class VertexVertexIterator:
    def __init__(self, halfedge, ccw):
        self.halfedge = halfedge;
        self.ccw = ccw
        self.current = self.halfedge
        self.justStarted = True


#     [Symbol.iterator]() {
#         return {
#             current: self._halfedge,
#             end: self._halfedge,
#             ccw: self._ccw,
#             justStarted: true,
#             next() {
#                 if (!self.justStarted && self.current === self.end) {
#                     return {
#                         done: true
#                     };
# 
#                 } else {
#                     self.justStarted = false;
#                     vertex = self.current.twin.vertex;
#                     self.current = self.ccw ? self.current.twin.next : self.current.prev.twin;
#                     return {
#                         done: false,
#                         value: vertex
#                     }
#                 }
#             }
#         }
#     }
# }
    def __iter__(self):
        if not self.justStarted and self.current == self.halfedge:
            raise StopIteration
        else:
            self.justStarted = False;
            v = self.current.twin.vertex
            self.current = self.current.twin.next if self.ccw else self.current.prev.twin
            return v

# 
# /**
#  * This class represents an adjacent edge iterator for a {@link module:Core.Vertex Vertex}.
#  * @ignore
#  * @memberof module:Core
#  */
# class VertexEdgeIterator {
#     // constructor
#     constructor(halfedge, ccw) {
#         self._halfedge = halfedge;
#         self._ccw = ccw;
#     }
class VertexEdgeIterator:
    def __init__(self, halfedge, ccw):
        self._halfedge = halfedge;
        self._end = self._halfedge   
        self._ccw = ccw
        self._current = self._halfedge
        self._justStarted = True

#     [Symbol.iterator]() {
#         return {
#             current: self._halfedge,
#             end: self._halfedge,
#             ccw: self._ccw,
#             justStarted: true,
#             next() {
#                 if (!self.justStarted && self.current === self.end) {
#                     return {
#                         done: true
#                     };
# 
#                 } else {
#                     self.justStarted = false;
#                     edge = self.current.edge;
#                     self.current = self.ccw ? self.current.twin.next : self.current.prev.twin;
#                     return {
#                         done: false,
#                         value: edge
#                     }
#                 }
#             }
#         }
#     }
# }
    def __iter__(self):
        return self

    def __next__(self):
        if (not self._justStarted) and self._current == self._end:
            print("iterator: DONE")
            raise StopIteration
        else:
            self._justStarted = False;
            e = self._current.edge
            if self._ccw:
                self._current = self._current.twin.next
            else:
                self._current = self._current.prev.twin
            print("vertex edge iterator.next: %s" % (e, ));
            return e

# /**
#  * This class represents an adjacent face iterator for a {@link module:Core.Vertex Vertex}.
#  * @ignore
#  * @memberof module:Core
#  */
class VertexFaceIterator:
#     // constructor
#     constructor(halfedge, ccw) {
#         while (halfedge.onBoundary) {
#             halfedge = halfedge.twin.next;
#         } // halfedge must not be on the boundary
#         self._halfedge = halfedge;
#         self._ccw = ccw;
#     }
    def __init__(self, halfedge, ccw):
        self._halfedge = halfedge;
        self._ccw = ccw
        self._current = self._halfedge
        self._justStarted = True

#     [Symbol.iterator]() {
#         return {
#             current: self._halfedge,
#             end: self._halfedge,
#             ccw: self._ccw,
#             justStarted: true,
#             next() {
#                 while (self.current.onBoundary) {
#                     self.current = self.ccw ? self.current.twin.next : self.current.prev.twin;
#                 } // halfedge must not be on the boundary
#                 if (!self.justStarted && self.current === self.end) {
#                     return {
#                         done: true
#                     };
# 
#                 } else {
#                     self.justStarted = false;
#                     face = self.current.face;
#                     self.current = self.ccw ? self.current.twin.next : self.current.prev.twin;
#                     return {
#                         done: false,
#                         value: face
#                     }
#                 }
#             }
#         }
#     }
# }
# 
    def __iter__(self):
        return self

    def __next__(self):
        while self._current.onBoundary:
            self._current = self._current.twin.next if self._ccw else self._current.prev.twin

        if not self._justStarted and self._current == self._halfedge:
            raise StopIteration
        else:
            self._justStarted = False;
            f = self._current.face
            self._current = self._current.twin.next if self._ccw else self._current.prev.twin
            return f

# /**
#  * This class represents an adjacent halfedge iterator for a {@link module:Core.Vertex Vertex}.
#  * @ignore
#  * @memberof module:Core
#  */
class VertexHalfedgeIterator:
#     // constructor
#     constructor(halfedge, ccw) {
#         self._halfedge = halfedge;
#         self._ccw = ccw;
#     }
    def __init__(self, halfedge, ccw):
        self._halfedge = halfedge;
        self._ccw = ccw
        self._current = self._halfedge
        self._justStarted = True

#     [Symbol.iterator]() {
#         return {
#             current: self._halfedge,
#             end: self._halfedge,
#             ccw: self._ccw,
#             justStarted: true,
#             next() {
#                 if (!self.justStarted && self.current === self.end) {
#                     return {
#                         done: true
#                     };
# 
#                 } else {
#                     self.justStarted = false;
#                     halfedge = self.current;
#                     self.current = self.ccw ? self.current.twin.next : self.current.prev.twin;
#                     return {
#                         done: false,
#                         value: halfedge
#                     }
#                 }
#             }
#         }
#     }
# }
    def __iter__(self):
        return self
    
    def __next__(self):
        if not self._justStarted and self._current == self._halfedge:
            raise StopIteration
        else:
            self._justStarted = False;
            h = self._current
            self._current = self._current.twin.next if self._ccw else self._current.prev.twin
            return h

# 
# /**
#  * This class represents an adjacent corner iterator for a {@link module:Core.Vertex Vertex}.
#  * @ignore
#  * @memberof module:Core
#  */
class VertexCornerIterator:
#     // constructor
#     constructor(halfedge, ccw) {
#         while (halfedge.onBoundary) {
#             halfedge = halfedge.twin.next;
#         } // halfedge must not be on the boundary
#         self._halfedge = halfedge;
#         self._ccw = ccw;
#     }
    def __init__(self, halfedge, ccw):
        self.halfedge = halfedge;
        self.ccw = ccw
        self.current = self.halfedge
        self.justStarted = True

#     [Symbol.iterator]() {
#         return {
#             current: self._halfedge,
#             end: self._halfedge,
#             ccw: self._ccw,
#             justStarted: true,
#             next() {
#                 while (self.current.onBoundary) {
#                     self.current = self.ccw ? self.current.twin.next : self.current.prev.twin;
#                 } // halfedge must not be on the boundary
#                 if (!self.justStarted && self.current === self.end) {
#                     return {
#                         done: true
#                     };
# 
#                 } else {
#                     self.justStarted = false;
#                     corner = self.current.next.corner;
#                     self.current = self.ccw ? self.current.twin.next : self.current.prev.twin;
#                     return {
#                         done: false,
#                         value: corner
#                     }
#                 }
#             }
#         }
#     }
# }
    def __iter__(self):
        while self.current.onBoundary:
            self.current = self.current.twin.next if self.ccw else self.current.prev.twin

        if not self.justStarted and self.current == self.halfedge:
            raise StopIteration
        else:
            self.justStarted = False;
            c = self.current.next.corner;
            self.current = self.current.twin.next if self.ccw else self.current.prev.twin
            return c

#  Assigns an index to each element in elementList. Indices can be accessed by using
#  elements as keys in the returned dictionary.
#  @global
#  @function module:Core.indexElements
#  @param {Object[]} elementList An array of any one of the following mesh elements -
#  vertices, edges, faces, corners, halfedges, boundaries.
#  @returns {Object} A dictionary mapping each element in elementList to a unique index
#  between 0 and |elementList|-1.
#  @example
#  let vertexIndex = indexElements(mesh.vertices);
#  let v = mesh.vertices[0];
#  let i = vertexIndex[v];
#  console.log(i); // prints 0
def indexElements(elementList):
    i = 0;
    index = {}
    for element in elementList:
        index[element] = i
        i += 1
    return index;



class HeatMethod:
#   /**
#    * This class implements the {@link http://cs.cmu.edu/~kmcrane/Projects/HeatMethod/ heat method} to compute geodesic distance
#    * on a surface mesh.
#    * @constructor module:Projects.HeatMethod
#    * @param {module:Core.Geometry} geometry The input geometry of the mesh this class acts on.
#    * @property {module:Core.Geometry} geometry The input geometry of the mesh this class acts on.
#    * @property {Object} vertexIndex A dictionary mapping each vertex of the input mesh to a unique index.
#    * @property {module:LinearAlgebra.SparseMatrix} A The laplace matrix of the input mesh.
#    * @property {module:LinearAlgebra.SparseMatrix} F The mean curvature flow operator built on the input mesh.
#    */
    def __init__(self, geometry):
        self.geometry = geometry;
        self.vertexIndex = indexElements(geometry.mesh.vertices);
  
        # build laplace and flow matrices
        t = pow(geometry.meanEdgeLength(), 2);
        M = geometry.massMatrix(self.vertexIndex);
        self.A = geometry.laplaceMatrix(self.vertexIndex);
        self.F = M + self.A*t;
# 
#   /**
#    * Computes the vector field X = -∇u / |∇u|.
#    * @private
#    * @method module:Projects.HeatMethod#computeVectorField
#    * @param {module:LinearAlgebra.DenseMatrix} u A dense vector (i.e., u.nCols() == 1) representing the
#    * heat that is allowed to diffuse on the input mesh for a brief period of time.
#    * @returns {Object} A dictionary mapping each face of the input mesh to a {@link module:LinearAlgebra.Vector Vector}.
#    */
    def computeVectorField(self, u):
        X = {};
        for f in self.geometry.mesh.faces:
            normal = self.geometry.faceNormal(f);
            area = self.geometry.area(f);
            gradU = Vector();
   
            for h in f.adjacentHalfedges():
                i = self.vertexIndex[h.prev.vertex];
                ui = u.get(i, 0);
                ei = self.geometry.vector(h);
   
                gradU.incrementBy(normal.cross_product(ei).times(ui));
   
            gradU.divideBy(2 * area);
            gradU.normalize();
   
            X[f] = gradU.negated();
   
        return X;
# 
#   /**
#    * Computes the integrated divergence ∇.X.
#    * @private
#    * @method module:Projects.HeatMethod#computeDivergence
#    * @param {Object} X The vector field -∇u / |∇u| represented by a dictionary
#    * mapping each face of the input mesh to a {@link module:LinearAlgebra.Vector Vector}.
#    * @returns {module:LinearAlgebra.DenseMatrix}
#    */
    def computeDivergence(self, X):
        vertices = self.geometry.mesh.vertices;
        V = len(vertices);
        div = DenseMatrix.zeros(V, 1);
  
        for v in vertices:
            i = self.vertexIndex[v];
            sum = 0;
            for h in v.adjacentHalfedges():
                if (not h.onBoundary):
                    Xj = X[h.face];
                    e1 = self.geometry.vector(h);
                    e2 = self.geometry.vector(h.prev.twin);
                    cotTheta1 = self.geometry.cotan(h);
                    cotTheta2 = self.geometry.cotan(h.prev);
                    sum += (cotTheta1 * e1.dot(Xj) + cotTheta2 * e2.dot(Xj));
            div.set(0.5 * sum, i, 0);
        return div;
# 
#   /**
#    * Shifts φ such that its minimum value is zero.
#    * @private
#    * @method module:Projects.HeatMethod#subtractMinimumDistance
#    * @param {module:LinearAlgebra.DenseMatrix} phi The (minimum 0) solution to the poisson equation Δφ = ∇.X.
#    */
    def subtractMinimumDistance(self, phi):
        min = Infinity;
        for i in range(phi.nRows()): 
            min = Math.min(phi.get(i, 0), min);
  
        for i in range(phi.nRows):
            phi.set(phi.get(i, 0) - min, i, 0);
# 
#   /**
#    * Computes the geodesic distances φ using the heat method.
#    * @method module:Projects.HeatMethod#compute
#    * @param {module:LinearAlgebra.DenseMatrix} delta A dense vector (i.e., delta.nCols() == 1) containing
#    * heat sources, i.e., u0 = δ(x).
#    * @returns {module:LinearAlgebra.DenseMatrix}
#    */
    def compute(self, delta):
        # integrate heat flow
        llt = self.F.chol();
        u = llt.solvePositiveDefinite(delta);
  
        # compute unit vector field X and divergence ∇.X
        X = self.computeVectorField(u);
        div = self.computeDivergence(X);
  
        # solve poisson equation Δφ = ∇.X
        llt = self.A.chol();
        phi = llt.solvePositiveDefinite(div.negated());
  
        # since φ is unique up to an additive constant, it should
        # be shifted such that the smallest distance is zero
        self.subtractMinimumDistance(phi);

        return phi;


class PolygonSoup:
    def __init__(self, vertex_positions, face_vertex_indices):
        self.vertex_positions = vertex_positions
        self.face_vertex_indices = face_vertex_indices
        assert len(self.face_vertex_indices) % 3 == 0, "face must be comprised of triangles"
        for (i, vi) in enumerate(face_vertex_indices):
            assert vi >= 0, "Error at index %d: face must index vertex in range" % (i, )
            assert vi < len(self.vertex_positions), "Error at index %d: face must index vertex in range" % (i, )
    def __repr__(self):
        return "PolygonSoup object with %d vertices and %d faces" % (len(self.vertex_positions), len(self.face_vertex_indices) // 3)

    def plot3d(self):
        fs = []
        # chunk the face_vertex_indices into groups of 3
        for fix in range(0, len(self.face_vertex_indices), 3):
            fs.append(self.face_vertex_indices[fix:fix+3])

        # return the SAGE class that represents a 3d model
        # TODO: figure out how to get this to work directly in the jupyter
        # notebook when calling 
        return IndexFaceSet(fs, self.vertex_positions)

class MeshIO:
    # /**
    #  * Converts text from an OBJ file to a polygon soup mesh.
    #  * @static
    #  * @param {string} input The text from an OBJ file containing vertex positions
    #  * and indices.
    #  * @returns {Object} A polygon soup mesh containing vertex positions and indices.
    #  * Vertex positions and indices are keyed by "v" and "f" respectively.
    # Reference: https://en.wikipedia.org/wiki/Wavefront_.obj_file
    #  */
    @classmethod
    def readOBJ(cls, rawstr):
        positions = []
        indices = []

        for (linum, line) in enumerate(rawstr.split("\n")):
            line = line.strip();
            tokens = line.split(" ");
            identifier = tokens[0].strip();

            # v x y z
            if identifier == "v":
                assert len(tokens) == 4, "expected 3 coordinates for a vertex at line %s" % (1+linum, )
                positions.append((float(tokens[1]), float(tokens[2]), float(tokens[3])));
            elif identifier == "f":
                if len(tokens) > 4:
                    raise RuntimeError("Line #%d: Only triangle meshes are supported at this time!" % (1+linum));
                # f v1 v2 v3 ... : a face with vertices { vi }
                # f v1/vt1 v2/vt2 v3/vt3 ...  : a face with vertex indexes { vi }
                #  and texture indexes { vti }. We don't care about texture
                # indexes.
                for i in range(1, len(tokens)):
                    index = (tokens[i].split("/")[0]).strip();
                    indices.append(int(index) - 1);
        return PolygonSoup(positions, indices)

    # /**
    #  * Converts a polygon soup mesh to the OBJ file format.
    #  * @static
    #  * @param {Object} polygonSoup A polygon soup mesh containing vertex positions
    #  * and indices. Texture coordinates and normals are optional.
    #  * @param {module:LinearAlgebra.Vector[]} polygonSoup.v The vertex positions of the polygon soup mesh.
    #  * @param {module:LinearAlgebra.Vector[]} polygonSoup.vt The texture coordinates of the polygon soup mesh.
    #  * @param {module:LinearAlgebra.Vector[]} polygonSoup.vn The normals of the polygon soup mesh.
    #  * @param {number[]} polygonSoup.f The indices of the polygon soup mesh.
    #  * @returns {string} Text containing vertex positions, texture coordinates, normals
    #  * and indices in the OBJ format.
    #  */
    @classmethod
    def writeOBJ(cls, polygonSoup):
        output = ""
        # write positions
        positions = polygonSoup.vertex_positions

        # TODO: add code for normals and textures.
        # let uvs = polygonSoup["vt"];
        # let normals = polygonSoup["vn"];
        # for (let i = 0; i < positions.length / 3; i++) {
        #   output += "v " + positions[3 * i + 0] + " " + positions[3 * i + 1] + " " + positions[3 * i + 2] + "\n";
        #   if (uvs) output += "vt " + uvs[3 * i + 0] + " " + uvs[3 * i + 1] + "\n";
        #   if (normals) output += "vn " + normals[3 * i + 0] + " " + normals[3 * i + 1] + " " + normals[3 * i + 2] + "\n";
        # }

        # write indices
        indices = polygonSoup.face_vertex_indices
        for i in range(0, len(indices), 3):
            output += "f ";
            for j in range(3):
                index = indices[i + j] + 1;
                output += str(index);
                # if (uvs) output += "/" + index;
                # if (!uvs && normals) output += "/";
                # if (normals) output += "/" + index;
                output += " ";
            output += "\n";
        return output;

def test_halfedge_mesh():
    import bunny as bunny
    polysoup = MeshIO.readOBJ(bunny.bunny)
    mesh = Mesh.build(polysoup)
    geometry = Geometry(mesh, polysoup.vertex_positions)
    hm = HeatMethod(geometry)
    phi = hm.compute() # compute heat
    return (polysoup, mesh)

    # now that we have the mesh, run geodesics
    # https://raw.githubusercontent.com/GeometryCollective/geometry-processing-js/master/projects/geodesic-distance/index.html
