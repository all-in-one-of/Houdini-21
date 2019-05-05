import hou
import json
import os

#getting the selected node
sel = hou.selectedNodes()
firstNode = sel[0]
#getting the path of the current hip file
path = os.path.split(hou.hipFile.path())[0]
#creating the empty object dictionary to save out
animData = {}
#get the transforms of the selected node
#as i am not sure how to query only the keyable attributes ,
#I am hardcoding it
#pos -vec3 touple
tx = firstNode.parm("tx").eval()
ty = firstNode.parm("ty").eval()
tz = firstNode.parm("tz").eval()
t = (tx, ty, tz)
#rotation -quaternion convert
rx = firstNode.parm("rx").eval()
ry = firstNode.parm("ry").eval()
rz = firstNode.parm("rz").eval()
quatR = hou.Quaternion(hou.hmath.buildRotate((rx, ry, rz), "xyz"))
#creating the attr dictionary
attrData = {}
attrData.setdefault("t", t)
#json does not recognise hou.Quaternion,so converting to a touple
attrData.setdefault("qr", [quatR[0], quatR[1], quatR[2], quatR[3]])
#updating the object dictonary
animData.setdefault(firstNode.name(), attrData)
# save it out
outFile = open((path+"test.json"), 'w')
outFile.write(json.dumps(animData))
outFile.close()
