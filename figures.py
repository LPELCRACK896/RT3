from pickletools import read_unicodestring1
from turtle import pos
import lpmath as lpm
import numpy as np
from math import pi
WHITE = (1,1,1)
BLACK = (0,0,0)

OPAQUE = 0
REFLECTIVE = 1
TRANSPARENT = 2


class Intersect(object):
    def __init__(self, distance, point, normal, sceneObj, textCoords):
        self.distance = distance
        self.point = point
        self.normal = normal
        self.sceneObj = sceneObj
        self.textCoords = textCoords

class Material(object):
    def __init__(self, diffuse = WHITE, spec = 1.0, ior = 1.0, matType = OPAQUE, texture = None):
        self.diffuse = diffuse
        self.spec = spec
        self.ior = ior
        self.matType = matType
        self.texture = texture


class Sphere(object):
    def __init__(self, center, radius, material):
        self.center = center
        self.radius = radius
        self.material = material

    def ray_intersect(self, orig, dir):
        L = lpm.suma_o_resta_vectores(self.center, orig, True)
        tca = lpm.productoPunto(L, dir)
        d = (lpm.magnitud_vector(L) ** 2 - tca ** 2) ** 0.5

        if d > self.radius:
            return None

        thc = (self.radius ** 2 - d ** 2) ** 0.5

        t0 = tca - thc
        t1 = tca + thc

        if t0 < 0:
            t0 = t1
        if t0 < 0:
            return None
        
        # P = O + t0 * D
        P = lpm.suma_o_resta_vectores(orig, [t0 * d for d in dir])
        normal = lpm.suma_o_resta_vectores(P, self.center, True)
        normal = lpm.normalizaVector(normal)

        u = np.arctan2(normal[2], normal[0])/ (2 * pi) + 0.5
        v = np.arccos(-normal[1])/pi
        uvs  = (u, v)
        return Intersect(distance = t0,
                         point = P,
                         normal = normal,
                         sceneObj = self,
                         textCoords=uvs)
 
class Plane(object):
    def __init__(self, position, normal, material ) -> None:
        self.position = position
        self.normal = lpm.normalizaVector(normal)
        self.material = material
    
    def ray_intersect(self, orig, dir) -> Intersect:
        denom = lpm.productoPunto(dir, self.normal) #denominado de una formula        
        # Distancia  = ((planePos - origRayo) o normal) / (direccionRayo o normal)
        if abs(denom)> 0.0001:
            num = lpm.productoPunto(lpm.suma_o_resta_vectores(self.position, orig, True), self.normal)#numerador de la formula
            t = num/denom #Distancia del origen del rayo con el plano... Debe ser positivo
            if t>0:
                # P = Origen + t*D
                P = lpm.suma_o_resta_vectores(orig, [t*d for d in dir])
                return Intersect(distance=t, point= P, normal=self.normal, textCoords=None, sceneObj=self)
        return None

class AABB(object):
    """Axis Aligned Bounding box
    Como en maincra, dice Carlos. Alineado a los ejes que no hay que guardar rotacion.  
    OBB: 

    Args:
        object (_type_): _description_
    """
    def __init__(self, position, size, material) -> None:
        self.position = position
        self.size = size 
        self.material = material

        self.planes = []
        halfSize = [0, 0, 0]
        halfSize[0] = size[0]/2
        halfSize[1] = size[1]/2
        halfSize[2] = size[2]/2
        #Sides
        self.planes.append(Plane(lpm.suma_o_resta_vectores(position, (halfSize[0], 0, 0)), (1, 0, 0), material))
        self.planes.append(Plane(lpm.suma_o_resta_vectores(position, (-halfSize[0], 0, 0)), (-1, 0, 0), material))
        #Up and down
        self.planes.append(Plane(lpm.suma_o_resta_vectores(position, (0, halfSize[1], 0)), (0, 1, 0), material))
        self.planes.append(Plane(lpm.suma_o_resta_vectores(position, (0, -halfSize[1], 0)), (0, -1, 0), material))
        #Front and back
        self.planes.append(Plane(lpm.suma_o_resta_vectores(position, (0, 0, halfSize[2] )), (0, 0, 1), material))
        self.planes.append(Plane(lpm.suma_o_resta_vectores(position, (0, 0, -halfSize[2])), (0, 0, -1), material))

        self.boundsMin = [0, 0, 0]
        self.boundsMax = [0, 0, 0]

        epsilon = 0.001

        for i in range(3):
            self.boundsMin[i] = self.position[i] - (epsilon + halfSize[i])
            self.boundsMax[i] = self.position[i] + (epsilon +  halfSize[i])
    
    def ray_intersect(self, orig, dir):
        intersect = None
        t = float('inf')
        for plane in self.planes:
            planeInter = plane.ray_intersect(orig, dir)
            if planeInter:
                planePoint = planeInter.point
                if self.boundsMin[0] <=planePoint[0] <= self.boundsMax[0] and self.boundsMin[1] <=planePoint[1] <= self.boundsMax[1] and self.boundsMin[2] <=planePoint[2] <= self.boundsMax[2]:
                    if planeInter.distance < t:
                        t = planeInter.distance
                        intersect = planeInter
                        # Tex coords
                        u, v = 0, 0
                        # Las uvs de las caras de los lados
                        ur= None
                        vr = None
                        if abs(plane.normal[0]) > 0 :
                            #Mapear uvs para el eje x, usando coordenads de y y z
                            u = (planeInter.point[1]-self.boundsMin[1])/ self.size[1]
                            v = (planeInter.point[2]-self.boundsMin[2])/ self.size[2]
                        elif abs(plane.normal[1]) > 0 :
                            u = (planeInter.point[0]-self.boundsMin[1])/ self.size[0]
                            v = (planeInter.point[2]-self.boundsMin[2])/ self.size[2]
                        elif abs(plane.normal[2]) > 0 :
                            u = (planeInter.point[0]-self.boundsMin[0])/ self.size[0]
                            v = (planeInter.point[1]-self.boundsMin[1])/ self.size[1]
        if not intersect: return None
        
        return Intersect(distance=t, point=intersect.point, normal = intersect.normal, textCoords=(u, v), sceneObj=self)

class Disk(object):

    def __init__(self, position, radius, normal, material) -> None:
        self.plane = Plane(position, normal, material)
        self.radius = radius 
        self.material = material
    
    def ray_intersect(self, orig, dir):
        intersect = self.plane.ray_intersect(orig, dir)
        if not intersect: return None
        contact =  lpm.magnitud_vector(lpm.suma_o_resta_vectores(intersect.point, self.plane.position, True))
        if contact > self.radius: return None 
        return Intersect(distance=intersect.distance, point=intersect.point, normal=self.plane.normal, textCoords=None, sceneObj=self)