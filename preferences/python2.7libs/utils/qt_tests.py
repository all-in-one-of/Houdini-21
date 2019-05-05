from PySide2 import QtGui,QtWidgets,Qtcore
import time 
app = QtWidgets.QApplication.instance()

Gl_drawables = [widget for widget in app.allWidgets() if widget.objectName()=="RE_GLDrawable"]

Gl_drawables[2].hide();time.sleep(2);Gl_drawables[2].show()

# RE_GLDrawableWrapper
# RE_GLDrawable
# RE_Window
# for widget in app.allWidgets():
#     if widget.objectName()!="RE_GLDrawable":
#         continue
#     try:
#         print(widget.objectName())
#         print(widget.__dict__)
#         print(widget.__repr__())
#         print(widget.children())
#         c = raw_input("hide for 2 secs")
#         if c=="b":
#             break
#         widget.hide()
#         time.sleep(2)
#         widget.show() 
#         widget_ = QtWidgets.QLabel("Am Here!!!!!!!!!!")
#         widget_.setParent(widget)
#         widget_.show()
#         time.sleep(3)
#         widget_.setParent(None)
#     except:
#         pass