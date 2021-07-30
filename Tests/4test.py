import maya.OpenMaya as om

filename= 'C:\\Users\\DylanSteimel\\Desktop\\text4uNorms.txt'

### Read Points From File
print("Reading File")
f = open(filename, 'r')
full = [line.rstrip().split(' ') for line in f.readlines()[::1000]]
points, colors, normals = [om.MPoint(float(pos[0]), float(pos[1]), float(pos[2])) for pos in full], [om.MPoint(float(pos[3])/255, float(pos[4])/255, float(pos[5])/255) for pos in full], [om.MPoint(float(pos[6]), float(pos[7]), float(pos[8])) for pos in full]
f.close()

### Create OBJs
obj = om.MObject()
meshID = om.MTypeId(296)
node = om.MDagModifier.createNode(meshID, obj)
print("Creating Mesh")
mesh = om.MFnMesh(node)

print("Creating Points Array")
arr = om.MPointArray()
for i in range(0,len(points)):
    arr.append(points[i])

print("Creating Color Array")
arr2 = om.MPointArray()
for i in range(0,len(colors)):
    arr2.append(colors[i])

print("Creating Normal Array")
arr3 = om.MPointArray()
for i in range(0,len(normals)):
    arr3.append(normals[i])
### Set vertices from points
print("Setting Vertices")
mesh.setPoints(arr)
vertexIDs = [i for i in range(0,len(points))]
print("Setting Colors")
mesh.setVertexColors(arr2, vertexIDs, rep='kRGB')
print("Setting Normals")
mesh.setVertexNormals(arr3, vertexIDs)
