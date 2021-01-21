
# https://geometrycollective.github.io/geometry-processing-js/docs/index.html


class Corner:
    def __init__(self, halfedge, index):
        assert isinstance(halfedge, Halfedge)
        self.halfedge = halfedge
        assert isinstance(index, int)
        self.index = index
# class Corner {
#     /**
#      * This class represents a corner in a {@link module:Core.Mesh Mesh}. It is a convenience
#      * wrapper around {@link module:Core.Halfedge Halfedge} - each corner stores the halfedge opposite to it.
#      * @constructor module:Core.Corner
#      * @property {module:Core.Halfedge} halfedge The halfedge opposite to this corner.
#      */
#     constructor() {
#         this.halfedge = undefined;
#         this.index = -1; // an ID between 0 and |C| - 1, where |C| is the number of corners in a mesh
#     }
# 
#     /**
#      * The vertex this corner lies on.
#      * @member module:Core.Corner#vertex
#      * @type {module:Core.Vertex}
#      */
#     get vertex() {
#         return this.halfedge.prev.vertex;
#     }
# 
#     /**
#      * The face this corner is contained in.
#      * @member module:Core.Corner#face
#      * @type {module:Core.Face}
#      */
#     get face() {
#         return this.halfedge.face;
#     }
# 
#     /**
#      * The next corner (in CCW order) in this corner's face.
#      * @member module:Core.Corner#next
#      * @type {module:Core.Corner}
#      */
#     get next() {
#         return this.halfedge.next.corner;
#     }
# 
#     /**
#      * The previous corner (in CCW order) in this corner's face.
#      * @member module:Core.Corner#prev
#      * @type {module:Core.Corner}
#      */
#     get prev() {
#         return this.halfedge.prev.corner;
#     }
# 
#     /**
#      * Defines a string representation for this corner as its index.
#      * @ignore
#      * @method module:Core.Corner#toString
#      * @returns {string}
#      */
#     toString() {
#         return this.index;
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
#       this.halfedge = undefined;
#       this.index = -1; // an ID between 0 and |E| - 1, where |E| is the number of edges in a mesh
#   }
# 
#   /**
#    * Checks whether this edge lies on a boundary.
#    * @method module:Core.Edge#onBoundary
#    * @returns {boolean}
#    */
#   onBoundary() {
#       return (this.halfedge.onBoundary || this.halfedge.twin.onBoundary);
#   }
    @property
    def onBoundary(self):
        return this.halfedge.onBoundary or this.halfedge.twin.onBoundary
# 
#   /**
#    * Defines a string representation for this edge as its index.
#    * @ignore
#    * @method module:Core.Edge#toString
#    * @returns {string}
#    */
#   toString() {
#       return this.index;
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
            self.positions[v] = p;
  
        if (normalizePositions):
            normalize(self.positions, mesh.vertices);
# 
#   /**
#    * Computes the vector along a halfedge.
#    * @method module:Core.Geometry#vector
#    * @param {module:Core.Halfedge} h The halfedge along which the vector needs to be computed.
#    * @returns {module:LinearAlgebra.Vector}
#    */
    def vector(self, h):
        a = this.positions[h.vertex];
        b = this.positions[h.next.vertex];
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
        return this.vector(e.halfedge).norm();
# 
#   /**
#    * Computes the midpoint of an edge.
#    * @method module:Core.Geometry#midpoint
#    * @param {module:Core.Edge} e The edge whose midpoint needs to be computed.
#    * @returns {number}
#    */
    def midpoint(self, e):
        h = e.halfedge;
        a = this.positions[h.vertex];
        b = this.positions[h.twin.vertex];
  
        # return (a.plus(b)).over(2);
        return (a + b) * 0.5
# 
#   /**
#    * Computes the mean edge length of all the edges in a mesh.
#    * @method module:Core.Geometry#meanEdgeLength
#    * @returns {number}
#    */
    def meanEdgeLength(self):
        return sum([this.length(e) for e in edges] / float(len(this.edges)))
        # sum = 0;
        # edges = this.mesh.edges;
        # for (e of edges) {
        #   sum += this.length(e);
        # }
    
        # return sum / edges.length;
# 
#   /**
#    * Computes the area of a face.
#    * @method module:Core.Geometry#area
#    * @param {module:Core.Face} f The face whose area needs to be computed.
#    * @returns {number}
#    */
    def area(f):
        if (f.isBoundaryLoop()): return 0.0;
        u = this.vector(f.halfedge);
        v = this.vector(f.halfedge.prev).negated();
        return 0.5 * u.cross(v).norm();
# 
#   /**
#    * Computes the total surface area of a mesh.
#    * @method module:Core.Geometry#totalArea
#    * @returns {number}
#    */
    def totalArea(self):
        return sum([self.area(f) for f in self.mesh.faces])
        # sum = 0.0;
        # for (f of this.mesh.faces) {
        #   sum += this.area(f);
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
  
        u = this.vector(f.halfedge);
        # TODO Sid: negated?! why?
        v = this.vector(f.halfedge.prev).negated();
  
        return u.cross(v).unit();
# 
#   /**
#    * Computes the centroid of a face.
#    * @method module:Core.Geometry#centroid
#    * @param {module:Core.Face} f The face whose centroid needs to be computed.
#    * @returns {module:LinearAlgebra.Vector}
#    */
    def centroid(self, f):
        h = f.halfedge;
        a = this.positions[h.vertex];
        b = this.positions[h.next.vertex];
        c = this.positions[h.prev.vertex];
  
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
        a = this.positions[h.vertex];
        b = this.positions[h.next.vertex];
        c = this.positions[h.prev.vertex];
  
        # TODO: Sid: what does it mean to be a boundary loop?
        if (f.isBoundaryLoop()):
            return a.plus(b).over(2);
  
        # TODO: what does this computation do? how does this work?
        ac = c.minus(a);
        ab = b.minus(a);
        w = ab.cross(ac);
        
        u = (w.cross(ab)).times(ac.norm2());
        v = (ac.cross(w)).times(ab.norm2());
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
        # Note that this works in 3D due to the existence of the cross product.
        e1 = this.vector(f.halfedge).unit();
        normal = this.faceNormal(f);

        # guaranteed to have unit magnitude:
        # |e1 x normal| = |e1| x |normal| = 1x1 = 1
        e2 = normal.cross(e1);
    
        return [e1, e2];
# 
#   /**
#    * Computes the angle (in radians) at a corner.
#    * @method module:Core.Geometry#angle
#    * @param {module:Core.Corner} c The corner at which the angle needs to be computed.
#    * @returns {number} The angle clamped between 0 and π.
#    */
    def angle(self, c):
        u = this.vector(c.halfedge.prev).unit();
        v = this.vector(c.halfedge.next).negated().unit();
  
        return Math.acos(Math.max(-1.0, Math.min(1.0, u.dot(v))));
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

        u = this.vector(h.prev);
        v = this.vector(h.next).negated();
  
        # TODO: write a succinct derivation.
        return u.dot(v) / u.cross(v).norm();
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
  
        n1 = this.faceNormal(h.face);
        n2 = this.faceNormal(h.twin.face);
        w = this.vector(h).unit();
  
        cosTheta = n1.dot(n2);
        sinTheta = n1.cross(n2).dot(w);
  
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
            area += this.area(f) / 3;
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
            u2 = this.vector(h.prev).norm2();
            v2 = this.vector(h).norm2();
            cotAlpha = this.cotan(h.prev);
            cotBeta = this.cotan(h);
    
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
            normal = this.faceNormal(f);
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
            normal = this.faceNormal(f);
            area = this.area(f);
  
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
            normal = this.faceNormal(c.halfedge.face);
            angle = this.angle(c);
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
            weight = 0.5 * this.dihedralAngle(h) / this.length(h.edge);
  
            n.decrementBy(this.vector(h).times(weight));
  
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
            weight = 0.5 * (this.cotan(h) + this.cotan(h.twin));
            n.decrementBy(this.vector(h).times(weight));
  
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
            u = this.vector(c.halfedge.prev);
            v = this.vector(c.halfedge.next).negated();
   
            n.incrementBy(u.cross(v).over(u.norm2() * v.norm2()));

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
            angleSum += this.angle(c);
    
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
        return this.angleDefect(v);
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
            s += 0.5 * this.length(h.edge) * this.dihedralAngle(h);
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
        for v in this.mesh.vertices:
            totalDefect += this.angleDefect(v);
   
        return totalDefect;
   
#   /**
#    * Computes the (pointwise) minimum and maximum principal curvature values at a vertex.
#    * @method module:Core.Geometry#principalCurvatures
#    * @param {module:Core.Vertex} v The vertex on which the principal curvatures need to be computed.
#    * @returns {number[]} An array containing the minimum and maximum principal curvature values at a vertex.
#   TODO: add explanation for what this is
#    */
    def principalCurvatures(self, v):
        A = this.circumcentricDualArea(v);
        H = this.scalarMeanCurvature(v) / A;
        K = this.angleDefect(v) / A;
   
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
        V = this.mesh.vertices.length;
        # TODO: what is Triplet?
        T = Triplet(V, V);
        for v in this.mesh.vertices:
            i = vertexIndex[v];
            sum = 1e-8;
    
            for h in v.adjacentHalfedges():
                j = vertexIndex[h.twin.vertex];
                weight = (this.cotan(h) + this.cotan(h.twin)) / 2;
                sum += weight;
                T.addEntry(-weight, i, j);
            T.addEntry(sum, i, i);
    
        return SparseMatrix.fromTriplet(T);
# 
#   /**
#    * Builds a sparse diagonal mass matrix containing the barycentric dual area of each vertex
#    * of a mesh.
#    * @method module:Core.Geometry#massMatrix
#    * @param {Object} vertexIndex A dictionary mapping each vertex of a mesh to a unique index.
#    * @returns {module:LinearAlgebra.SparseMatrix}
#    */
    def massMatrix(self, vertexIndex):
        V = this.mesh.vertices.length;
        T = Triplet(V, V);
        for v in this.mesh.vertices:
            i = vertexIndex[v];
            T.addEntry(this.barycentricDualArea(v), i, i);
  
        return SparseMatrix.fromTriplet(T);
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
        V = this.mesh.vertices.length;
        T = ComplexTriplet(V, V);
        for v in this.mesh.vertices:
            i = vertexIndex[v];
            sum = 1e-8;
  
            for h in v.adjacentHalfedges():
                j = vertexIndex[h.twin.vertex];
                weight = (this.cotan(h) + this.cotan(h.twin)) / 2;
                sum += weight;  
                T.addEntry(Complex(-weight), i, j);
            T.addEntry(Complex(sum), i, i);
  
        return ComplexSparseMatrix.fromTriplet(T);
# }
# 
# /**
#  * Centers a mesh about the origin and rescales it to unit radius.
#  * @global
#  * @function module:Core.normalize
#  * @param {module:LinearAlgebra.Vector[]} positions The position of each vertex in the vertices array.
#  * @param {module:Core.Vertex[]} vertices The vertices of a mesh.
#  * @param {boolean} rescale A flag indicating whether mesh positions should be scaled to a unit radius.
#  */
# function normalize(positions, vertices, rescale = true) {
#   // compute center of mass
#   N = vertices.length;
#   cm = Vector();
#   for (v of vertices) {
#       p = positions[v];
# 
#       cm.incrementBy(p);
#   }
#   cm.divideBy(N);
# 
#   // translate to origin and determine radius
#   radius = -1;
#   for (v of vertices) {
#       p = positions[v];
# 
#       p.decrementBy(cm);
#       radius = Math.max(radius, p.norm());
#   }
# 
#   // rescale to unit radius
#   if (rescale) {
#       for (v of vertices) {
#           p = positions[v];
# 
#           p.divideBy(radius);
#       }
#   }
# }


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
    def __init__(self, vertex, edge, face, corner, next_, prev, twin, onBoundary, index):
        self.vertex = vertex;
        self.edge = edge;
        self.face = face;
        self.corner = corner;
        self.next = next_;
        self.prev = prev;
        self.twin = twin;
        self.onBoundary = onBoundary;
        self.index = index;

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
#       this.vertex = undefined;
#       this.edge = undefined;
#       this.face = undefined;
#       this.corner = undefined;
#       this.next = undefined;
#       this.prev = undefined;
#       this.twin = undefined;
#       this.onBoundary = undefined;
#       this.index = -1; // an ID between 0 and |H| - 1, where |H| is the number of halfedges in a mesh
#   }
# 
#   /**
#    * Defines a string representation for this halfedge as its index.
#    * @ignore
#    * @method module:Core.Halfedge#toString
#    * @returns {string}
#    */
#   toString() {
#       return this.index;
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
    def __init__():
        this.vertices = [];
        this.edges = [];
        this.faces = [];
        this.corners = [];
        this.halfedges = [];
        this.boundaries = [];
        this.generators = [];
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
    def build(self, positions, indices):
        # preallocate elements
        # positions = polygonSoup["v"];
        # indices = polygonSoup["f"];
        # this.preallocateElements(positions, indices);
  
        # create and insert vertices
        self.vertices = [None for _ in positions]
        for i in range(len(positions)):
            self.vertices[i] = Vertex()
  
        # create and insert halfedges, edges and non boundary loop faces
        eIndex = 0;
        edgeCount = {}
        existingHalfedges = {}
        hasTwinHalfedge = {}
        # for (I = 0; I < indices.length; I += 3) {
        for I in range(len(indices), 3):
            # create face
            f = Face();
            this.faces[I // 3] = f;
  
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
                h = this.halfedges[I + J];
                h.next = this.halfedges[I + K];
                h.prev = this.halfedges[I + (J + 3 - 1) % 3];
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
                    this.edges.append(e)
                    #this.edges[eIndex] = e;
                    # eIndex += 1
                    h.edge = e;
                    e.halfedge = h;
  
                    # record the newly created edge and halfedge from vertex i to j
                    # existingHalfedges.set(key, h);
                    existingHalfedges[key] = h
                    # edgeCount.set(key, 1);
                    edgeCount[key] = 1
  
                # check for non-manifold edges
                if edgeCount[key] > 2:
                    raise ValueError("Mesh has non-manifold edges! between (%s)" % (key, ))
                    return False;
        #### ----- end loop edges
        # ----- end loop indices

        # create and insert boundary halfedges and "imaginary" faces for boundary cycles
        # also create and insert corners
        hIndex = len(indices);
        cIndex = 0;
        # for (i = 0; i < indices.length; i++) {
        for i in range(len(indices)):
            # if a halfedge has no twin halfedge, create a face and
            # link it the corresponding boundary cycle
            h = this.halfedges[i];

            if not hasTwinHalfedge[h]:
                # create face
                f = Face();
                this.boundaries.append(f);
  
                # walk along boundary cycle
                boundaryCycle = [];
                he = h;
                while True:
                    # create a halfedge
                    bH = Halfedge();
                    this.halfedges[hIndex] = bH;
                    hIndex += 1
                    boundaryCycle.append(bH);
  
                    # grab the next halfedge along the boundary that does not have a twin halfedge
                    nextHe = he.next;
                    while (hasTwinHalfedge.get(nextHe)):
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
                    if he == h:
                        break
  
                # link the cycle of boundary halfedges together
                n = boundaryCycle.length;
                # for (j = 0; j < n; j++) {
                for j in range(n):
                    # boundary halfedges are linked in clockwise order
                    boundaryCycle[j].next = boundaryCycle[(j + n - 1) % n];
                    boundaryCycle[j].prev = boundaryCycle[(j + 1) % n];
                    hasTwinHalfedge.set(boundaryCycle[j], true);
                    hasTwinHalfedge.set(boundaryCycle[j].twin, true);
  
            # ^^^ end not having twin halfedge processing ^^^
            # point the newly created corner and its halfedge to each other
            if (not h.onBoundary):
                c = Corner();
                c.halfedge = h;
                h.corner = c;
                this.corners[cIndex] = c;
                cIndex += 1

  
        # check if mesh has isolated vertices, isolated faces or
        # non-manifold vertices
        this.assertHasNoIsolatedVertices()
        this.assertHasNoIsolatedFaces()
        this.assertHasOnlyManifoldVertices()
        
        # index elements
        this.indexElements();
  
  
#   /**
#    * Preallocates mesh elements.
#    * @private
#    * @method module:Core.Mesh#preallocateElements
#    * @param {module:LinearAlgebra.Vector[]} positions The vertex positions of a polygon soup mesh.
#    * @param {number[]} indices The indices of a polygon soup mesh.
#    */
#   preallocateElements(positions, indices) {
#       nBoundaryHalfedges = 0;
#       sortedEdges = Map();
#       for (I = 0; I < indices.length; I += 3) {
#           for (J = 0; J < 3; J++) {
#               K = (J + 1) % 3;
#               i = indices[I + J];
#               j = indices[I + K];
# 
#               // swap if i > j
#               if (i > j) j = [i, i = j][0];
# 
#               value = [i, j]
#               key = value.toString();
#               if (sortedEdges.has(key)) {
#                   nBoundaryHalfedges--;
# 
#               } else {
#                   sortedEdges.set(key, value);
#                   nBoundaryHalfedges++;
#               }
#           }
#       }
# 
#       nVertices = positions.length;
#       nEdges = sortedEdges.size;
#       nFaces = indices.length / 3;
#       nHalfedges = 2 * nEdges;
#       nInteriorHalfedges = nHalfedges - nBoundaryHalfedges;
# 
#       // clear arrays
#       this.vertices.length = 0;
#       this.edges.length = 0;
#       this.faces.length = 0;
#       this.halfedges.length = 0;
#       this.corners.length = 0;
#       this.boundaries.length = 0;
#       this.generators.length = 0;
# 
#       // allocate space
#       this.vertices = Array(nVertices);
#       this.edges = Array(nEdges);
#       this.faces = Array(nFaces);
#       this.halfedges = Array(nHalfedges);
#       this.corners = Array(nInteriorHalfedges);
#   }
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
        for f in this.faces:
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
#   hasNonManifoldVertices() {
#       adjacentFaces = Map();
#       for (v of this.vertices) {
#           adjacentFaces.set(v, 0);
#       }
# 
#       for (f of this.faces) {
#           for (v of f.adjacentVertices()) {
#               adjacentFaces.set(v, adjacentFaces.get(v) + 1);
#           }
#       }
# 
#       for (b of this.boundaries) {
#           for (v of b.adjacentVertices()) {
#               adjacentFaces.set(v, adjacentFaces.get(v) + 1);
#           }
#       }
# 
#       for (v of this.vertices) {
#           if (adjacentFaces.get(v) !== v.degree()) {
#               return true;
#           }
#       }
# 
#       return false;
#   }
# 
#   /**
#    * Assigns indices to this mesh's elements.
#    * @private
#    * @method module:Core.Mesh#indexElements
#    */
#   indexElements() {
#       index = 0;
#       for (v of this.vertices) {
#           v.index = index++;
#       }
# 
#       index = 0;
#       for (e of this.edges) {
#           e.index = index++;
#       }
# 
#       index = 0;
#       for (f of this.faces) {
#           f.index = index++;
#       }
# 
#       index = 0;
#       for (h of this.halfedges) {
#           h.index = index++;
#       }
# 
#       index = 0;
#       for (c of this.corners) {
#           c.index = index++;
#       }
# 
#       index = 0;
#       for (b of this.boundaries) {
#           b.index = index++;
#       }
#   }
# }
# 
# 
# /**
#  * Assigns an index to each element in elementList. Indices can be accessed by using
#  * elements as keys in the returned dictionary.
#  * @global
#  * @function module:Core.indexElements
#  * @param {Object[]} elementList An array of any one of the following mesh elements -
#  * vertices, edges, faces, corners, halfedges, boundaries.
#  * @returns {Object} A dictionary mapping each element in elementList to a unique index
#  * between 0 and |elementList|-1.
#  * @example
#  * vertexIndex = indexElements(mesh.vertices);
#  * v = mesh.vertices[0];
#  * i = vertexIndex[v];
#  * console.log(i); // prints 0
#  */
# function indexElements(elementList) {
#   i = 0;
#   index = {};
#   for (element of elementList) {
#       index[element] = i++;
#   }
# 
#   return index;
# }

class Face:
    # /**
    #  * This class represents a face in a {@link module:Core.Mesh Mesh}.
    #  * @constructor module:Core.Face
    #  * @property {module:Core.Halfedge} halfedge One of the halfedges associated with this face.
    #  */
    def __init__(self, halfedge, index):
        self.halfedge = halfedge
        self.index = -1
        # this.halfedge = undefined;
        # this.index = -1; // an ID between 0 and |F| - 1 if this face is not a boundary loop
        # // or an ID between 0 and |B| - 1 if this face is a boundary loop, where |F| is the
        # // number of faces in the mesh and |B| is the number of boundary loops in the mesh
  
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
        return FaceHalfedgeIterator(this.halfedge, ccw);
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
#       return this.index;
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
#        this._halfedge = halfedge;
#        this._ccw = ccw;
#    }
    def __init__(self, halfedge, ccw):
        self._halfedge = halfedge;
        self._ccw = ccw;
        self._current = this._halfedge;
        self._end = this._halfedge;
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

#   [Symbol.iterator]() {
#       return {
#           current: this._halfedge,
#           end: this._halfedge,
#           ccw: this._ccw,
#           justStarted: true,
#           next() {
#               if (!this.justStarted && this.current === this.end) {
#                   return {
#                       done: true
#                   };
# 
#               } else {
#                   this.justStarted = false;
#                   vertex = this.current.vertex;
#                   this.current = this.ccw ? this.current.next : this.current.prev;
#                   return {
#                       done: false,
#                       value: vertex
#                   }
#               }
#           }
#       }
#   }
# }

class FaceEdgeIterator:    
# /**
#  * This class represents an adjacent edge iterator for a {@link module:Core.Face Face}.
#  * @ignore
#  * @memberof module:Core
#  */
# class FaceEdgeIterator {
#   // constructor
#   constructor(halfedge, ccw) {
#       this._halfedge = halfedge;
#       this._ccw = ccw;
#   }

    def __init__(self, halfedge, ccw):
        self._halfedge = halfedge;
        self._ccw = ccw;
        self._current = self._halfedge;
        self._justStared = True;

    def __next__(self):
        if not this._justStared and this.current == this.enumerate:
            raise StopIteration
        else:
            this._justStared = False
            e = this.current.edge
            if self._ccw:
                self.current = self._current.next
            else:
                self.current = self._current.prev
            return e
#   [Symbol.iterator]() {
#       return {
#           current: this._halfedge,
#           end: this._halfedge,
#           ccw: this._ccw,
#           justStarted: true,
#           next() {
#               if (!this.justStarted && this.current === this.end) {
#                   return {
#                       done: true
#                   };
# 
#               } else {
#                   this.justStarted = false;
#                   edge = this.current.edge;
#                   this.current = this.ccw ? this.current.next : this.current.prev;
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
#       this._halfedge = halfedge;
#       this._ccw = ccw;
#   }
    def __init__(self, halfedge, ccw):
        self._halfedge = halfedge;
        self._ccw = ccw;
        self._current = self._halfedge;
        self._justStared = True;


#   [Symbol.iterator]() {
#       return {
#           current: this._halfedge,
#           end: this._halfedge,
#           ccw: this._ccw,
#           justStarted: true,
#           next() {
#               while (this.current.twin.onBoundary) {
#                   this.current = this.ccw ? this.current.next : this.current.prev;
#               } // twin halfedge must not be on the boundary
#               if (!this.justStarted && this.current === this.end) {
#                   return {
#                       done: true
#                   };
# 
#               } else {
#                   this.justStarted = false;
#                   face = this.current.twin.face;
#                   this.current = this.ccw ? this.current.next : this.current.prev;
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
        if not this._justStared and this.current == this.enumerate:
            raise StopIteration
        else:
            while this.current.twin.onBoundary:
                self.current = self.current.next if self._ccw else self.current.prev

        if not this._justStared and this.current == this.enumerate:
            raise StopIteration
        else:
            this._justStared = False
            e = this.current.edge
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
#       this._halfedge = halfedge;
#       this._ccw = ccw;
#   }
# 
class FaceHalfedgeIterator:
    def __init__(self, halfedge, ccw):
        self._halfedge = halfedge;
        self._ccw = ccw;
        self._current = self._halfedge;
        self._justStared = True;

# 
#   [Symbol.iterator]() {
#       return {
#           current: this._halfedge,
#           end: this._halfedge,
#           ccw: this._ccw,
#           justStarted: true,
#           next() {
#               if (!this.justStarted && this.current === this.end) {
#                   return {
#                       done: true
#                   };
# 
#               } else {
#                   this.justStarted = false;
#                   halfedge = this.current;
#                   this.current = this.ccw ? this.current.next : this.current.prev;
#                   return {
#                       done: false,
#                       value: halfedge
#                   }
#               }
#           }
#       }
#   }
# }


    def __next__(self):
        if not this._justStared and this.current == this.end:
            raise StopIteration
        else:
            this._justStared = False
            h = this.current
            self.current = self.current.next if self._ccw else self.current.prev
            return h

# /**
#  * This class represents an adjacent corner iterator for a {@link module:Core.Face Face}.
#  * @ignore
#  * @memberof module:Core
#  */
class FaceCornerIterator:
#   // constructor
#   constructor(halfedge, ccw) {
#       this._halfedge = halfedge;
#       this._ccw = ccw;
#   }
    def __init__(self, halfedge, ccw):
        self._halfedge = halfedge;
        self._ccw = ccw;
        self._current = self._halfedge;
        self._justStared = True;

#   [Symbol.iterator]() {
#       return {
#           current: this._halfedge,
#           end: this._halfedge,
#           ccw: this._ccw,
#           justStarted: true,
#           next() {
#               if (!this.justStarted && this.current === this.end) {
#                   return {
#                       done: true
#                   };
# 
#               } else {
#                   this.justStarted = false;
#                   this.current = this.ccw ? this.current.next : this.current.prev;
#                   corner = this.current.corner; // corner will be undefined if this face is a boundary loop
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
        if not this._justStared and this.current == this.end:
            raise StopIteration
        else:
            this._justStared = False
            c = this.current.corner # corner will be undefined if face is boundary loop
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
        # this.index = -1; // an ID between 0 and |V| - 1, where |V| is the number of vertices in a mesh
# 
#     /**
#      * Counts the number of edges adjacent to this vertex.
#      * @method module:Core.Vertex#degree
#      * @returns {number}
#      */
      # @property
    def degree(self):
        return len(self.adjacentEdges())
# 
#     /**
#      * Checks whether this vertex is isolated, i.e., it has no neighboring vertices.
#      * @method module:Core.Vertex#isIsolated
#      * @returns {boolean}
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
      return VertexVertexIterator(this.halfedge, ccw);
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
        return VertexEdgeIterator(this.halfedge, ccw);
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
        return VertexFaceIterator(this.halfedge, ccw);
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
        return VertexCornerIterator(this.halfedge, ccw);
# 
#     /**
#      * Defines a string representation for this vertex as its index.
#      * @ignore
#      * @method module:Core.Vertex#toString
#      * @returns {string}
#      */
#     toString() {
#         return this.index;
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
#         this._halfedge = halfedge;
#         this._ccw = ccw;
#     }
class VertexVertexIterator:
    def __init__(self, halfedge, ccw):
        self.halfedge = halfedge;
        self.ccw = ccw
        self.current = self.halfedge
        self.justStared = True


#     [Symbol.iterator]() {
#         return {
#             current: this._halfedge,
#             end: this._halfedge,
#             ccw: this._ccw,
#             justStarted: true,
#             next() {
#                 if (!this.justStarted && this.current === this.end) {
#                     return {
#                         done: true
#                     };
# 
#                 } else {
#                     this.justStarted = false;
#                     vertex = this.current.twin.vertex;
#                     this.current = this.ccw ? this.current.twin.next : this.current.prev.twin;
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
            return StopIteration
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
#         this._halfedge = halfedge;
#         this._ccw = ccw;
#     }
class VertexEdgeIterator:
    def __init__(self, halfedge, ccw):
        self.halfedge = halfedge;
        self.ccw = ccw
        self.current = self.halfedge
        self.justStared = True

#     [Symbol.iterator]() {
#         return {
#             current: this._halfedge,
#             end: this._halfedge,
#             ccw: this._ccw,
#             justStarted: true,
#             next() {
#                 if (!this.justStarted && this.current === this.end) {
#                     return {
#                         done: true
#                     };
# 
#                 } else {
#                     this.justStarted = false;
#                     edge = this.current.edge;
#                     this.current = this.ccw ? this.current.twin.next : this.current.prev.twin;
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
        if not self.justStarted and self.current == self.halfedge:
            return StopIteration
        else:
            self.justStarted = False;
            e = self.current.edge
            self.current = self.current.twin.next if self.ccw else self.current.prev.twin
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
#         this._halfedge = halfedge;
#         this._ccw = ccw;
#     }
    def __init__(self, halfedge, ccw):
        self.halfedge = halfedge;
        self.ccw = ccw
        self.current = self.halfedge
        self.justStared = True

#     [Symbol.iterator]() {
#         return {
#             current: this._halfedge,
#             end: this._halfedge,
#             ccw: this._ccw,
#             justStarted: true,
#             next() {
#                 while (this.current.onBoundary) {
#                     this.current = this.ccw ? this.current.twin.next : this.current.prev.twin;
#                 } // halfedge must not be on the boundary
#                 if (!this.justStarted && this.current === this.end) {
#                     return {
#                         done: true
#                     };
# 
#                 } else {
#                     this.justStarted = false;
#                     face = this.current.face;
#                     this.current = this.ccw ? this.current.twin.next : this.current.prev.twin;
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
        while self.current.onBoundary:
            self.current = self.current.twin.next if self.ccw else self.current.prev.twin

        if not self.justStarted and self.current == self.halfedge:
            return StopIteration
        else:
            self.justStarted = False;
            e = self.current.edge
            self.current = self.current.twin.next if self.ccw else self.current.prev.twin
            return e

# /**
#  * This class represents an adjacent halfedge iterator for a {@link module:Core.Vertex Vertex}.
#  * @ignore
#  * @memberof module:Core
#  */
class VertexHalfedgeIterator:
#     // constructor
#     constructor(halfedge, ccw) {
#         this._halfedge = halfedge;
#         this._ccw = ccw;
#     }
    def __init__(self, halfedge, ccw):
        self.halfedge = halfedge;
        self.ccw = ccw
        self.current = self.halfedge
        self.justStared = True

#     [Symbol.iterator]() {
#         return {
#             current: this._halfedge,
#             end: this._halfedge,
#             ccw: this._ccw,
#             justStarted: true,
#             next() {
#                 if (!this.justStarted && this.current === this.end) {
#                     return {
#                         done: true
#                     };
# 
#                 } else {
#                     this.justStarted = false;
#                     halfedge = this.current;
#                     this.current = this.ccw ? this.current.twin.next : this.current.prev.twin;
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
        if not self.justStarted and self.current == self.halfedge:
            return StopIteration
        else:
            self.justStarted = False;
            h = self.current
            self.current = self.current.twin.next if self.ccw else self.current.prev.twin
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
#         this._halfedge = halfedge;
#         this._ccw = ccw;
#     }
    def __init__(self, halfedge, ccw):
        self.halfedge = halfedge;
        self.ccw = ccw
        self.current = self.halfedge
        self.justStared = True

#     [Symbol.iterator]() {
#         return {
#             current: this._halfedge,
#             end: this._halfedge,
#             ccw: this._ccw,
#             justStarted: true,
#             next() {
#                 while (this.current.onBoundary) {
#                     this.current = this.ccw ? this.current.twin.next : this.current.prev.twin;
#                 } // halfedge must not be on the boundary
#                 if (!this.justStarted && this.current === this.end) {
#                     return {
#                         done: true
#                     };
# 
#                 } else {
#                     this.justStarted = false;
#                     corner = this.current.next.corner;
#                     this.current = this.ccw ? this.current.twin.next : this.current.prev.twin;
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
            return StopIteration
        else:
            self.justStarted = False;
            c = self.current.next.corner;
            self.current = self.current.twin.next if self.ccw else self.current.prev.twin
            return c


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
        this.geometry = geometry;
        this.vertexIndex = indexElements(geometry.mesh.vertices);
  
        # build laplace and flow matrices
        t = Math.pow(geometry.meanEdgeLength(), 2);
        M = geometry.massMatrix(this.vertexIndex);
        this.A = geometry.laplaceMatrix(this.vertexIndex);
        this.F = M.plus(this.A.timesReal(t));
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
        for f in this.geometry.mesh.faces:
            normal = this.geometry.faceNormal(f);
            area = this.geometry.area(f);
            gradU = Vector();
   
            for h in f.adjacentHalfedges():
                i = this.vertexIndex[h.prev.vertex];
                ui = u.get(i, 0);
                ei = this.geometry.vector(h);
   
                gradU.incrementBy(normal.cross(ei).times(ui));
   
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
        vertices = this.geometry.mesh.vertices;
        V = vertices.length;
        div = DenseMatrix.zeros(V, 1);
  
        for v in vertices:
            i = this.vertexIndex[v];
            sum = 0;
            for h in v.adjacentHalfedges():
                if (not h.onBoundary):
                    Xj = X[h.face];
                    e1 = this.geometry.vector(h);
                    e2 = this.geometry.vector(h.prev.twin);
                    cotTheta1 = this.geometry.cotan(h);
                    cotTheta2 = this.geometry.cotan(h.prev);
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
        llt = this.F.chol();
        u = llt.solvePositiveDefinite(delta);
  
        # compute unit vector field X and divergence ∇.X
        X = this.computeVectorField(u);
        div = this.computeDivergence(X);
  
        # solve poisson equation Δφ = ∇.X
        llt = this.A.chol();
        phi = llt.solvePositiveDefinite(div.negated());
  
        # since φ is unique up to an additive constant, it should
        # be shifted such that the smallest distance is zero
        this.subtractMinimumDistance(phi);

        return phi;

def parse_obj_data(data):
    raise RuntimeError("don't know how to parse!")

def test_halfedge_mesh():
    import sage.ddg.bunny as bunny
    bunnymesh = parse_obj_data(bunny.bunny)
    # now that we have the mesh, run geodesics
    # https://raw.githubusercontent.com/GeometryCollective/geometry-processing-js/master/projects/geodesic-distance/index.html
