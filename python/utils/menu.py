import hou
import xml.etree.ElementTree as ET
import xml.dom.minidom as dom
import os

# https://github.com/shotgunsoftware/tk-houdini/blob/master/python/tk_houdini/ui_generation.py

# checking for the menu in custom locations


def get_houdini_menus():
    menus = {
        "main": (
            "MainMenuCommon.xml",
            "MainMenuMaster.xml",
            "MainMenuEscape.xml",
            "MainMenuMPlay.xml ",
        ),
        "context": (
            "CHGmenu.xml",
            "ChannelListMenu.xml",
            "KeyframesMenu.xml",
            "OPmenu.xml",
            "PaneTabTypeMenu.xml",
            "PARMmenu.xml",
            "ParmGearMenuenu.xml",
            "PlaybarMenu.xml",
            "ShelfToolMenu.xml",
            "ShelfMenu.xml",
            "ShelfSetMenu.xml",
            "ShelfSetPlusMenu.xml",
            "VOPFXmenu.xml",
        )
    }
    return menus


def is_menu_created(menu_id="Bp_Menu", menu_type="main"):

    custom_menu_paths = hou.getenv("HOUDINI_MENU_PATH")
    delimiter = ":" if ":" in custom_menu_paths else ";"
    menu_paths = filter(lambda x: x != "&",
                        custom_menu_paths.split(delimiter)
                        )
    for _path in menu_paths:
        for root, dirs, files in os.walk(_path, topdown=True):
            # dont recurse
            del dirs
            houdini_menus = set(get_houdini_menus()["main"])
            _files = set(files)
            found_menus = houdini_menus.intersection(_files)
            for _menu in found_menus:
                xml_path = os.path.join(root, _menu)
                if check_xml_for_menu_id(xml_path, menu_id):
                    return True
    return False


def check_xml_for_menu_id(xml_path, menu_id):
    xml_parser = ET.parse(xml_path)
    for child in xml_parser.iter("subMenu"):
        if child.attrib["id"] == menu_id:
            return True
    return False


class HoudiniMenu(object):
    def __init__(self, file_path):
        self._file_path = file_path
        self._xml_root = None

    def save(self):
        xml = ET.tostring(self._xml_root, encoding="UTF-8")
        formatted_xml = dom.parseString(xml).toprettyxml(
            indent="  ", encoding="UTF-8")
        with open(self._file_path, "w") as _file:
            _file.write(formatted_xml)

    def create_separator(self, parent):
        ET.SubElement(parent, "separatorItem")

    def create_title_item(self, parent, text):
        title = ET.SubElement(parent, "titleItem")
        label = ET.SubElement(title, "label")
        label.text = text
        return title

    def create_script_item(self, parent, script_id, script_data):
        item = ET.SubElement(parent, "scriptItem")
        label = ET.SubElement(item, "label")
        label.text = script_data["label"]
        script_path = ET.SubElement(item, "scriptPath")
        script_path.text = script_data["path"]
        if script_data.get("args"):
            script_args = ET.SubElement(item, "scriptArgs")
            script_args.text = script_data["args"]
        return item

    def create_submenu(self, parent, text, _id):
        menu = ET.SubElement(parent, "subMenu")
        menu.set("id", _id)
        label = ET.SubElement(menu, "label")
        label.text = text
        return menu

    def create_main_menu(self):
        self._xml_root = ET.Element("mainMenu")
        self._menu_bar = ET.SubElement(self._xml_root, "menuBar")

    def create_context_menu(self):
        self._xml_root = ET.Element("menuDocument")
        self._menu = ET.SubElement(self._xml_root, "menu")


def create_menu():
    python_lib_path = os.path.dirname(os.path.dirname(__file__))
    menu_path = os.path.join(
        os.path.dirname(python_lib_path),
        "menus",
        "MainMenuCommon.xml"
    )
    houdini_menu = HoudiniMenu(menu_path)
    houdini_menu.create_main_menu()
    menu_ = houdini_menu.create_submenu(
        houdini_menu._menu_bar, "Bp Menu", "bp_menu")
    houdini_menu.create_title_item(menu_, "First Iteration")
    houdini_menu.create_separator(menu_)
    houdini_menu.save()
