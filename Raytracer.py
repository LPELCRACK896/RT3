from gl import Raytracer, V3
from texture import *
from figures import *
from lights import *


width = 1600
height = 800
centrox = 0
centroy = -1
# Materiales

material_opaco1 = Material(diffuse = (0.0546, 0.472, 0.0664), spec=32, matType=OPAQUE)
material_opaco2 = Material(diffuse = (0.994, 0.186, 0.233), spec=32, matType=OPAQUE)

material_reflectivo1 = Material(diffuse = (0.384, 0.501, 0.605), spec=32, matType=REFLECTIVE)
material_reflectivo2 =Material(diffuse = (0.9, 0.9, 0.9), spec = 64, matType = REFLECTIVE)

material_transparente1 = Material(diffuse = (0.805, 0.513, 0.303), spec=32, matType=TRANSPARENT)
material_transparente2 = Material(diffuse = (0.804, 0.707, 0.973), spec=32,ior=2 ,matType=TRANSPARENT)

brick = Material(diffuse = (0.8, 0.3, 0.3), spec = 16)
stone = Material(diffuse = (0.4, 0.4, 0.4), spec = 8)
earth = Material(texture=Texture('earthDay.bmp'))
mirror = Material(diffuse = (0.9, 0.9, 0.9), spec = 64, matType = REFLECTIVE)
glass = Material(diffuse = (0.9, 0.9, 0.9), spec = 64, ior = 1.5, matType = TRANSPARENT)

blueMirror = Material(diffuse = (0.2, 0.2, 0.9), spec = 64, matType = REFLECTIVE)
yellowMirror = Material(diffuse = (0.9, 0.9, 0.2), spec = 64, matType = REFLECTIVE)

rtx = Raytracer(width, height)

rtx.envMap = Texture("casita.bmp")

rtx.lights.append( AmbientLight(intensity = 0.1 ))
rtx.lights.append( DirectionalLight(direction = (-1,-1,-1), intensity = 0.8 ))
#rtx.lights.append( PointLight(point = (0,0,0)))

""" rtx.scene.append( Sphere(V3(-3+centrox,3+centroy,-10), 1, material_opaco1)  )
rtx.scene.append( Sphere(V3(0+centrox,3+centroy,-10), 1, material_opaco2)  )
rtx.scene.append( Sphere(V3(3+centrox,3+centroy,-10), 1, material_reflectivo1)  )

rtx.scene.append( Sphere(V3(-3+centrox,0+centroy,-10),1, material_reflectivo2)  )
rtx.scene.append( Sphere(V3(0+centrox,0+centroy,-10), 1, material_transparente1)  )
rtx.scene.append( Sphere(V3(3+centrox,0+centroy,-10), 1, material_transparente2)  ) 
 """
# rtx.scene.append(Plane(position=(0, -10,0), normal=(-1, -1, -1), material=mirror))

rtx.scene.append(AABB(position=(-3, -3, -10), size = (2, 2, 2), material=brick))
rtx.glRender()

rtx.glFinish("output.bmp")