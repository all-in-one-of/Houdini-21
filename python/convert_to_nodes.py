"""Helper python scrips for solaris,
- import Kitchen_Set as solaris nodes.
"""
import hou
import os
from pxr import Usd, Kind, UsdGeom
import logging


logging.basicConfig(
    format="%(asctime)s %(message)s",
    level=logging.DEBUG
)
_log = logging.getLogger("UsdToHip")


# *****************************Extra**************************************
#'addvariant','attribsop','attribvop','attribwrangle','bakeskinning','begincontextoptionsblock',
#'cache','camera','capsule','collection','cone','createxform','cube','cylinder',
#'duplicate','edit','editcontextoptions','editmaterial','editproperties','fetch','file','foreach',
#'geosubsetvop','instancer','layerbreak','layerproperties','lightpanel','loadlayer','loadmasks',
# 'mantradomelight','mantralight','material','materiallibrary','mergeinsert','mergeoverlay',
# 'null','output','prim','primproperties','prune','pythonscript','reference','rop_usd','rop_usdhydra',
# 'sceneimport','scope','setvariant','sphere','stagemanager','sublayer','switch','timeshift',
# 'xform',
def get_primitives():
    return (
        'capsule',
        'cone',
        'cylinder',
        'cube',
        'sphere'
    )


def create_variant_set(prim_name, variant_set_name,
                       variant_dict, default_variant=None,
                       execute=False):
    stage_context = hou.node("/stage")
    prim = stage_context.createNode("prim", node_name=prim_name)

    add_variant = stage_context.createNode("addvariant")
    set_variant = stage_context.createNode("setvariant")
    rop_usd = stage_context.createNode("rop_usd")

    add_variant.setInput(0, prim)

    add_variant.parm("variantset").set(variant_set_name)

    for index, data in enumerate(
        variant_dict.iteritems(), start=1
        ):
        name, node = data
        add_variant.setInput(index, node)

    set_variant.setInput(0, add_variant)
    set_variant.parm("variantset1").set(variant_set_name)
    default_variant and set_variant.parm("variantname1").set(default_variant)

    rop_usd.setInput(0, set_variant)

    execute and rop_usd.parm("execute").pressButton()


def generate_all_references(stage):
    it = iter(
        Usd.PrimRange.Stage(
            stage,
            Usd.PrimIsLoaded & ~Usd.PrimIsAbstract
        )
    )
    for prim in it:
        if prim.GetMetadata("references"):
            #if the prim is a reference then no need to iterate further
            it.PruneChildren()
            # finding the added references
            created_node = create_reference_node(prim)
            print("Created Node %s" % created_node.name())
# *******************************************************************

def add_transform_to_node(prim, parent_node):

    stage_context = hou.node("/stage")
    # set it and return the transform node.
    xform_node = stage_context.createNode("xform")
    usd_xform = UsdGeom.Xform(prim)
    usd_xform_api = UsdGeom.XformCommonAPI(usd_xform)
    translate, rotate, scale, pivot, rotateorder = \
        usd_xform_api.GetXformVectors(Usd.TimeCode.Default())
    xform_node.parm('rOrd').set(rotateorder.value)
    xform_order = []
    # get the ops
    for xform_type in usd_xform.GetXformOpOrderAttr().Get():
        if xform_type.startswith("xformOp:translate"):
            xform_node.parmTuple('t').set(translate)
            xform_order.append("t")
        if xform_type.startswith("xformOp:rotate"):
            xform_node.parmTuple('r').set(rotate)
            xform_order.append("r")
        if xform_type.startswith("xformOp:scale"):
            xform_node.parmTuple('s').set(scale)
            xform_order.append("s")

    # somehow this seems to not work.
    # if len(xform_order) == 3:
    #     xform_node.parm('xOrd').set("".join(xform_order))
    # elif len(xform_order) == 2:
    #     xform_order.append(
    #         list(
    #             set(xform_order).symmetric_difference(set(["r", "s", "t"]))
    #         )[0]
    #     )
    #     xform_node.parm('xOrd').set(
    #         "".join(xform_order)
    #     )

    xform_node.setInput(0, parent_node)
    _log.debug("Added xform for %s ", prim.GetName())
    return xform_node


def create_reference_node(prim):
    stage_context = hou.node("/stage")
    added_references = prim.GetMetadata("references").addedItems
    # finding the prepended references
    #prepend_references = prim.GetMetadata("references").prependedItems
    # payload = prim.GetMetadata("payload")
    #references.extend(added_references+prepend_references)
    prim_name = prim.GetName()
    ref_node = stage_context.createNode(
        "reference",
        prim_name
    )
    ref_node.parm("num_files").set(
        len(
            added_references
        )
    )
    for index, reference in enumerate(
                                added_references,
                                start=1):
        ref_node.parm(
            "filepath%s" % index
        ).set("$HIP%s" % reference.assetPath[1:])
    return_node = ref_node
    if prim.HasVariantSets():
        node = stage_context.createNode(
            "setvariant",
            "%s_set_variant" % prim_name
        )
        node.setInput(0, ref_node)
        node.parm("num_variants").set(
            len(
                prim.GetVariantSets().GetNames()
            )
        )
        for index, variant_set_name in enumerate(
                                          prim.GetVariantSets().GetNames(),
                                          start=1):
            variant_name = prim.GetVariantSets().GetVariantSelection(
                variant_set_name
            )
            node.parm("variantset%s" % index).set(variant_set_name)
            node.parm("variantname%s" % index).set(variant_name)
        return_node = node
    _log.debug("Created Reference for %s", prim.GetName())
    return add_transform_to_node(prim, return_node)


def create_merge_insert(prim, parent_node):
    stage_context = hou.node("/stage")
    merge_insert = stage_context.createNode("mergeinsert", prim.GetName())
    merge_insert.parm("destpath").set("/$OS")
    # set it as the parent.
    if  Usd.ModelAPI(prim.GetParent()).GetKind() == Kind.Tokens.assembly:
        merge_insert.setInput(0, parent_node)
    else:
        # dont set the first input.
        parent_node.setInput(
            len(parent_node.inputs())+1,
            merge_insert
        )
    _log.debug("Created Merge for %s", prim.GetName())
    return merge_insert


def run(usd_file_path="D:\Resources\Kitchen_set\Kitchen_set.usd"):
    hou.hipFile.clear(suppress_save_prompt=False)
    _log.info("Starting Conversion ..")
    usd_stage = Usd.Stage.Open(usd_file_path)
    stage_context = hou.node("/stage")
    # get the default prim and create it a prim node.
    default_node = stage_context.createNode("prim", usd_stage.GetDefaultPrim().GetName())
    # set the kind type.
    default_node.parm("primkind").set(Usd.ModelAPI(usd_stage.GetDefaultPrim()).GetKind())
    # merge overlay to collect all the groups.
    merge_overlay = stage_context.createNode("mergeoverlay")
    # create the rop node to save the usda file.
    rop_usd = stage_context.createNode("rop_usd")
    rop_usd.setInput(0, merge_overlay)

    # Group to keep track of created groups.
    groups = {}
    # set the iterator for traversing the stage.
    it = iter(
        Usd.PrimRange.Stage(
            usd_stage,
            Usd.PrimIsLoaded & ~Usd.PrimIsAbstract
        )
    )
    prim_no = 0
    with hou.InterruptableOperation(
            "UsdToHip", "Traversing Prims..",
            open_interrupt_dialog=True) as operation:

        for prim in it:
            # find the group prim and create node with connections
            if Usd.ModelAPI(prim).GetKind() == Kind.Tokens.group:
                # find the parent node
                parent_node = groups.get(
                    prim.GetParent().GetName(),
                    default_node
                )
                # create a group(merge_insert and connect them)
                merge_node = create_merge_insert(
                    prim,
                    parent_node
                )
                # this logic is not clear to me yet, basically we need
                # to combine groups to view them.
                if parent_node == default_node:
                    merge_overlay.setNextInput(merge_node)
                groups[prim.GetName()] = merge_node
            if prim.GetMetadata("references"):
                #if the prim is a reference then no need to iterate further
                it.PruneChildren()
                # finding the added references
                created_node = create_reference_node(prim)
                # find and parent to group node.
                group_node = groups[prim.GetParent().GetName()]
                # dont set the first input as that meant for the group parent.
                group_node. setInput(
                    len(group_node.inputs())+1,
                    created_node
                )
            prim_no += 1
            percent = float(prim_no) / float(452)
            operation.updateProgress(percent)
    print prim_no
    # create the merge overlay to combine everything.
    _log.info("Finished Conversion ..")
    # Save current scene as file
    kitchen_set_hip = os.path.join(
        os.path.dirname(usd_file_path),
        "Kitchen_set.hipnc"
    )
    hou.hipFile.save(kitchen_set_hip)
    _log.info("Saved Hip File: %s", kitchen_set_hip)
    #generate_all_references(stage)


run()
