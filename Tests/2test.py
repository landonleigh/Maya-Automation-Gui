import math
#import maya.cmds as cmds
import matplotlib.pyplot as plt

def distance(pt1, pt2):

    d = math.sqrt(math.pow(pt2[0] - pt1[0], 2) +
                math.pow(pt2[1] - pt1[1], 2) +
                math.pow(pt2[2] - pt1[2], 2)* 1.0)

    return d

filename = r'C:\Users\DylanSteimel\Desktop\text4u.xyz'

f = open(filename, 'r')
full = [line.rstrip().split(' ') for line in f.readlines()[::1000]]
particleList = [(float(pos[0]), float(pos[1]), float(pos[2])) for pos in full]
f.close()

distances = []
print('Calculating avg distance')
for i in range(0,len(particleList)-1):
    distances.append(distance(particleList[i],particleList[i+1]))


print(distances[:10])

top_70 = (len(distances)*7)//10
distances.sort()
filtered = distances[:top_70]
avgDistance = sum(filtered)/len(filtered)
ballDiameter = avgDistance*1.1

plt.bar(range(0,len(filtered)), filtered)
plt.show()


tri_count = 0
for i in range(0,len(particleList)):
    print('Ball on point ' + str(i) + ' of ' + str(len(particleList)))
    pt1 = particleList[i]
    print('Finding Neighboring Points')
    neighbors = [pt2 for pt2 in particleList if (distance(pt1,pt2) < ballDiameter)]
    print('Finding Triangles')
    for k in range(0,len(neighbors)):
        pt2 = neighbors[k]
        for j in range(0,len(particleList)):
            pt3 = particleList[j]
            if pt3!=pt1 and pt3!=pt2 and distance(pt1,pt3)<ballDiameter and distance(pt2,pt3):
                tri_count += 1
                print('Create Triange '+  str(tri_count) + '! (:')
                #cmds.polyCreateFacet(p=[pt1,pt2,pt3])
