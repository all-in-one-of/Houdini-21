"""Helper python scrips for solaris
"""
import hou
from pxr import Usd

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

def get_hou_node(_type):
    return {
        "prim": "prim",
        "reference": "reference",
        "merge": "mergeoverlay",
        "insert": "mergeinsert",
        "variant_add": "addvariant",
        "variant_set": "setvaraint",
        "save": "rop_usd",
        "layer_properties": "layerproperties",
        "layer_load": "loadlayer",
        "layer_break": "layerbreak",
        "file": "file"
    }.get(_type, None)


def create_variant_set(prim_name, variant_set_name,
                       variant_dict, default_variant=None,
                       execute=False):
    stage_context = hou.node("/stage")
    prim = stage_context.createNode("prim", node_name=prim_name)

    add_variant = stage_context.createNode("addvariant")
    set_variant = stage_context.createNode("setvariant")
    rop_usd = stage_context.createNode("rop_usd")

    add_variant.setInput(0,prim)

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


def run(usd_file_path):
    stage = Usd.Stage.Open(usd_file_path)
    convert_to_nodes(stage)
