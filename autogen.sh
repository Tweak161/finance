# Script creates .py files from .ui (Qt Designer file format) files and .rcc (Resource XML file) files
pyuic5 view/MainWindow.ui -o view/MainWindow.py
pyrcc5 content/resources.qrc -o resources_rc.py
