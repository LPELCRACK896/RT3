from gl import Raytracer, V3
from texture import *
from figures import *
from lights import *


width = 120
height = 120
centrox = 0
centroy = -1
centroz = 0
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

# rtx.envMap = Texture("casita.bmp")

rtx.lights.append( AmbientLight(intensity = 0.1 ))
rtx.lights.append( DirectionalLight(direction = (-1,-1,-1), intensity = 0.8 ))
rtx.lights.append( DirectionalLight(direction = (-1,0,0), intensity = 0.2 ))

#rtx.lights.append( PointLight(point = (0,0,0)))

""" rtx.scene.append( Sphere(V3(-3+centrox,3+centroy,-10), 1, material_opaco1)  )
rtx.scene.append( Sphere(V3(0+centrox,3+centroy,-10), 1, material_opaco2)  )
rtx.scene.append( Sphere(V3(3+centrox,3+centroy,-10), 1, material_reflectivo1)  )

rtx.scene.append( Sphere(V3(-3+centrox,0+centroy,-10),1, material_reflectivo2)  )
rtx.scene.append( Sphere(V3(0+centrox,0+centroy,-10), 1, material_transparente1)  )
rtx.scene.append( Sphere(V3(3+centrox,0+centroy,-10), 1, material_transparente2)  ) 
 """
""" rtx.scene.append(Plane(position=(0, -10,0), normal=(0, 1, 0), material=brick))
rtx.scene.append(Plane(position=(centro, 0,0), normal=(2, 0, 1), material=brick)) """

# rtx.scene.append(Plane(position=(0, -10, 0), normal=(0, 1,0), material=brick))
""" rtx.scene.append(Plane(position=(-40, 10, 0), normal=(1, 0,0), material=brick))
rtx.scene.append(Plane(position=(-40, 10, 0), normal=(-1, 0,0), material=brick)) """
# rtx.scene.append(Plane(position=(-40, 10, 0), normal=(0, 1,0), material=brick))
""" rtx.scene.append(Plane(position=(-40, 10, 0), normal=(0, -1,0), material=brick))
"""
plano_1 = Plane(position=(centrox, centroy, centroz-70), normal=(0, 0, 1), material=brick) # Fondo
plano_2 = Plane(position=(centrox, centroy, centroz-100), normal=(1, 0, -0.5), material=stone) #Plane() #Derecha
plano_3 =  Plane(position=(centrox, centroy, centroz-100), normal=(-1, 0, -0.5), material=material_opaco1) #Plane() #Izquierda
plano_4 = Plane(position=(centrox, centroy, centroz-100), normal=(0, 1, 0.5), material=material_opaco2) #Plane() #Abajo
plano_5 = None #Plane(position=(centrox, centroy+40, centroz-100), normal=(0, 1, 0.5), material=material_opaco2) #Plane() #Arriba
cubo_1 = None # AABB
cubo_2 = None # AABB
elementos_escena = [plano_1, plano_2, plano_3, plano_4, plano_5, cubo_1, cubo_2]
for element in elementos_escena:
    if element: rtx.scene.append(element)


# rtx.scene.append(Plane(position=(100, 10, 0), normal=(0, 1,0), material=brick))

# rtx.scene.append(AABB(position=(0, 0, 0), size = (.1, 1, 1), material=brick))
# rtx.scene.append(AABB(position=(-3, -3, -10), size = (2, 2, 2), material=brick))
# rtx.scene.append(Disk(position=(-3, -3, -10), radius=1, normal=(-1, -1, -1), material=brick))

rtx.glRender()

rtx.glFinish("output.bmp")