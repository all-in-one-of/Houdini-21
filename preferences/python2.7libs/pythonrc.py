print("Running pythonrc")

import hou
# initializing custom scripts that we want.
for file_ in hou.findFiles("scripts/custom123.py"):
	execfile(file_)

# Checking for custom menu, otherwise generating one.
import utils.menu as menu

#menu.create_menu()

#import utils.shelf

#utils.shelf.run_shelf_creation()


