import hou
import os
import os.path
import random


def createSeparateGeoNode(file):
    geoN = hou.node('/obj').createNode('geo')
    bNo = file[14:16]
    print(bNo)
    geoN.setName('bullet'+bNo+'_geo')
    geoN.node('file1').destroy()
    alembicN = geoN.createNode('alembic')
    alembicN.setName(file[7:])
    alembicN.parm('fileName').set('$HIP/balls_import/'+file)
    alembicN.moveToGoodPosition()
    matN = geoN.createNode('material')
    randNo = random.randint(1, 5)
    matName = '/shop/car_paint'+str(randNo)
    matN.parm('shop_materialpath1').set(matName)
    matN.setInput(0, alembicN)
    matN.moveToGoodPosition()


#create a node for the import
geoNode = hou.node('/obj').createNode('geo')
geoNode.setName('ImportBalls_Geo')
geoNode.node('file1').destroy()
#create a merge node to merge all the nodes for viewing
mergeN = geoNode.createNode('merge')
mergeN.setName('ImportGeo_merge')

connectionNo = 0
xpos = 0
ypos = 6
#set the path for importing the files to be imported
importPath = "C:/Users/Prethish/Project_Pang/Work_Files/Houdini/shot50/balls_import/frame24"
for root, dirs, files in os.walk(importPath):
    for file in files:
        if os.path.isfile(os.path.join(importPath, file)):
            if(file.find('bullet', 0, len(file)) != -1):
                createSeparateGeoNode(file)
            else:
                alembicN = geoNode.createNode('alembic')
                alembicN.setName(file[7:])
                alembicN.parm('fileName').set('$HIP/balls_import/'+file)
                alembicN.setPosition(hou.Vector2(xpos, ypos))
                matN = geoNode.createNode('material')
                randNo = random.randint(1, 5)
                matName = '/shop/car_paint'+str(randNo)
                matN.parm('shop_materialpath1').set(matName)
                matN.setInput(0, alembicN)
                matN.setPosition(hou.Vector2(xpos, ypos-2))
                mergeN.setInput(connectionNo, matN)
                connectionNo += 1
                xpos += 4

mergeN.moveToGoodPosition()
