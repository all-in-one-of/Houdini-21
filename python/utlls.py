import os, os.path
import hou


sel = hou.selectedNodes()


def create_null_node():
    readValues = hou.ui.readInput("Enter the Null Name:")
    nullName = readValues[1]
    parent = sel[0].parent()
    nullNode = parent.createNode("null")
    nullNode.setName(nullName)
    nullNode.setInput(0, sel[0])
    nullNode.moveToGoodPosition()


def mergeAll():
    parent = sel[0].parent()
    mergeN = parent.createNode("merge")
    for i, obj in enumerate(sel):
        mergeN.setInput(i, obj)
    mergeN.moveToGoodPosition()


def import_alembic_caches(importPath):
    #create a node for the import
    geoNode = hou.node('/obj').createNode('geo')
    geoNode.setName('ImportBalls_Geo')
    geoNode.node('file1').destroy()
    #create a merge node to merge all the nodes for viewing
    mergeN = geoNode.createNode('merge')
    connectionNo = 0
    xpos = 0
    ypos = 6
    for root, dirs, files in os.walk(importPath):
        for file in files:
            if os.path.isfile(os.path.join(importPath, file)):
                alembicN = geoNode.createNode('alembic')
                alembicN.parm('fileName').set(os.path.join(importPath, file))
                alembicN.moveToGoodPosition()
                mergeN.setInput(connectionNo, nds)
                connectionNo += 1

    mergeN.moveToGoodPosition()


def apply_mat_to_group_geos():
    sel = hou.selectedNodes()
    geo = sel[0].geometry()
    grps = geo.primGroups()
    parentPath = sel[0].parent()
    mergeN = parentPath.createNode("merge")
    shopNetwork = parentPath.createNode("shopnet")

    #iterate through the groups
    for i, grp in enumerate(grps):
        #create a delete node and connect it to the previous node
        delNode = parentPath.createNode("delete")
        matNode = parentPath.createNode('material')
        vopMat = shopNetwork.createNode('vopmaterial')
        #sets its Name
        delNode.setName(grp+"_delete")
        matNode.setName(grp+'_mat')
        vopMat.setName(grp+"_vopMat")
        #connect the selected node
        delNode.setInput(0, sel[0])
        matNode.setInput(0, delNode)
        #set the group name in the group field
        delNode.parm('group').set(grp)
        #set the parm to delete unselected
        delNode.parm('negate').set(1)
        #arrange the node in the network editor automaticaly
        delNode.moveToGoodPosition()
        mergeN.setInput(i, matNode)


def print_params():

    print(
        [p.name() for p in sel[0].parms()]
    )


def set_centroid_expression():
    sel[0].parm("px").setExpression("$CEX")
    sel[0].parm("py").setExpression("$CEY")
    sel[0].parm("pz").setExpression("$CEZ")


def create_shader(matName='my_mat'):
    matShaderN = hou.node('/shop').createNode('mantrasurface')
    matShaderN.setName('shade1')
    matShaderN.parm('shop_materialpath1').set(matName)


def rename_nodes(searchString, replaceString):
    for nds in sel:
        origString = nds.name()
        newString = origString.replace(searchString, replaceString)
        nds.setName(newString)


lastNodes = []
def Bp_findLastNodes(parent, level):
    child = parent.children()
    lastNodes

    if child:
        for node in child:
            print("-"*level+">traversing node :"+node.name())
            level += 1
            Bp_findLastNodes(node, level)
    else:
        print("------->reached last node "+parent.name())
        lastNodes.append(parent)

    return lastNodes


def apply_mat_to_alembic():
    parent = hou.node('/obj/alembicarchive1')
    finalNodes = Bp_findLastNodes(parent, 0)
    matName = '/shop/my_mat'
    #apply a material node
    for node in finalNodes:
        parentNode = node.parent()
        matN = parentNode.createNode('material')
        matN.setName('shade1')
        matN.parm('shop_materialpath1').set(matName)
        matN.setInput(0, node)
        matN.moveToGoodPosition()
