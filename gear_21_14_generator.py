# 21/14 internal/external involute gear tool profile generator for Blender
# offset 3.9197
# http://www.otvinta.com/instantinternal.html

import bpy
from math import *

def createMeshFromData(name, origin, verts, edges):
	# Create mesh and object
	me = bpy.data.meshes.new(name+'Mesh')
	ob = bpy.data.objects.new(name, me)
	ob.location = origin
	ob.show_name = False

	# Link object to scene and make active
	bpy.context.collection.objects.link(ob)
	ob.select_set(True)

	# Create mesh from given verts, faces.
	me.from_pydata(verts, edges, [])
	# Update mesh with new data
	me.update()
	return ob

def TurnPoint( pt, degrees, centerx, centery ):
	fR = sqrt((pt[0] - centerx) * (pt[0] - centerx) + (pt[1] - centery) * (pt[1] - centery))
	fAngle = atan2(pt[1] - centery, pt[0] - centerx)
	fAngle = fAngle + degrees * pi / 180.0

	pt[0] = centerx + fR * cos(fAngle)
	pt[1] = centery + fR * sin(fAngle)

def CreateInvoluteGear( name, points, teeth, centerx, centery ):
	pointlen = len(points)
	edges = [[0, 0] for _ in range(pointlen * teeth) ]
	verts = [[0, 0, 0] for _ in range(pointlen * teeth) ]

	for t in range(teeth):
		for i in range(pointlen):
			verts[t * pointlen + i][0] = points[i][0]
			verts[t * pointlen + i][1] = points[i][1]
			verts[t * pointlen + i][2] = 0
			TurnPoint( verts[t * pointlen + i], t * 360.0 / teeth, 0, 0)
			edges[t * pointlen + i][0] = t * pointlen + i
			edges[t * pointlen + i][1] = t * pointlen + i + 1

	# connect last point with first
	edges[pointlen * teeth - 1][1] = 0

	createMeshFromData( name, [centerx, 0, 0], verts, edges )

points1 = [[6.525,-.834],[6.540,-.835],[6.588,-.836],[6.666,-.832],[6.776,-.819],[6.915,-.793]
,[7.083,-.750],[7.277,-.684],[7.496,-.594],[7.735,-.475],[7.980,-.331],[7.993,-.323]
,[7.993,.323],[7.980,.331],[7.735,.475],[7.496,.594],[7.277,.684],[7.083,.750]
,[6.915,.793],[6.776,.819],[6.666,.832],[6.588,.836],[6.540,.835],[6.525,.834]
,[6.408,.818],[6.290,.825],[6.176,.852],[6.068,.901],[5.971,.968],[5.888,1.052]
,[5.822,1.150],[5.775,1.258],[5.749,1.373],[5.745,1.491],[5.762,1.607],[5.800,1.719]
,[5.858,1.821],[5.934,1.912],[6.025,1.986],[6.128,2.043]]

points2 = [[-10.003,1.070],[-10.124,1.056],[-10.274,1.029],[-10.450,.989],[-10.653,.930],[-10.879,.851]
,[-11.129,.748],[-11.399,.619],[-11.687,.461],[-11.992,.272],[-12.294,.062],[-12.310,.050]
,[-12.310,-.050],[-12.294,-.062],[-11.992,-.272],[-11.687,-.461],[-11.399,-.619],[-11.129,-.748]
,[-10.879,-.851],[-10.653,-.930],[-10.450,-.989],[-10.274,-1.029],[-10.124,-1.056],[-10.003,-1.070]
]

CreateInvoluteGear( "m1_z14_x0", points1, 14, 0, 0 )
CreateInvoluteGear( "m1_z21_x0.56", points2, 21, 3.9197, 0 )
