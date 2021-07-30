import fileinput
import os
import sys
import glob
import re

import maya.OpenMayaUI as mui
import maya.cmds as cmds
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from shiboken2 import wrapInstance
import math

SCRIPT_NAME = "Redline Forensic Studio - Maya Tools"

# ----------------------------------------------------------------------------------------------------------------------
# Returns an instance of Maya's main window
# ----------------------------------------------------------------------------------------------------------------------
def maya_main_window():
    main_window_ptr = mui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window_ptr), QWidget)

class MainUI(QDialog):
    # Set up file references
    ms_dir = os.path.expanduser("~/maya/scripts/magic-shade")
    icon_dir = os.path.expanduser("~/maya/scripts/magic-shade/resources/icons")
    spellbook_dir = os.path.expanduser("~/maya/scripts/magic-shade/spellbooks")
    studio_dir = os.path.expanduser("~/maya/scripts/magic-shade/studios")
    pref_path = os.path.expanduser("~/maya/scripts/magic-shade/prefs")
    arnold_studio_path = os.path.expanduser("~/maya/scripts/magic-shade/Arnold_Studio_V3.mb")
    thumbs_dir = os.path.expanduser("~/maya/projects/default/scenes/.mayaSwatches")
    save_path = os.path.expanduser("~/maya/projects/default/scenes/")
    user_profile = os.environ['USERPROFILE']
    desktop_dir = user_profile + '\\Desktop'
    last_file_pref = "last_vehicular_spellbook"
    vehicle_library_dir = user_profile + "/deltav/Jason Young - Asset Library/3D Vehicle Library/"
    vehiclespec_library_dir = user_profile + "/deltav/Jason Young - Asset Library/3D Vehicle Library/"

    # --------------------------------------------------------------------------------------------------------------
    # Initializes variables, window, and UI elements
    # --------------------------------------------------------------------------------------------------------------
    def __init__(self, parent=maya_main_window()):
        super(MainUI, self).__init__(parent)

        # Set up the window
        # self.setWindowFlags(Qt.Tool)
        self.setFixedWidth(600)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.resize(250, -1)
        self.setWindowTitle(SCRIPT_NAME)
        self.setWindowIcon(QIcon(self.icon_dir + "/RedlineLogo.png"))
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)

        self.create_controls()  # Initializes controls
        self.create_layout()  # Initializes the internal window layout
        self.make_connections()
        self.dont_shrink = False
        self.asset = None

        # If we have a last-opened file saved in preferences, automatically open that file. Otherwise, just open
        # a new, empty file
        # region Open Last File
        found_last_file_path = False
        if os.path.isfile(self.pref_path):  # If the prefs file exists
            with open(self.pref_path) as f:
                data = f.read().splitlines()  # Read the prefs file
                found_last_file_path = False
                for line in data:
                    if line.startswith(self.last_file_pref + "="):  # If we find the last-opened file line in prefs
                        last_file_path = line[len(self.last_file_pref) + 1:]  # Get the last-opened file path
                        # print(last_file_path)
                        if os.path.isfile(last_file_path):  # If the path we get exists
                            # print("found last file: " + last_file_path)
                            #self.choose_spellbook_edit.setText(last_file_path)  # Open the last-opened file
                            found_last_file_path = True
                            break
                f.close()

        if not found_last_file_path:
            # print("no path in prefs")
            self.current_file = None
        pass  # I hate PyCharm
        # endregion

    #--------------------------------------------------------------------------------------------------------------
    #                                   Make the Buttons
    #--------------------------------------------------------------------------------------------------------------
    def create_controls(self):
        UI_ELEMENT_HEIGHT = 30
        UI_ELEMENT_WIDTH = 150

        ##### Banner #####
        self.banner = QLabel()
        self.pixmap = QPixmap(self.icon_dir + '/banner.jpg')
        self.pixmap = self.pixmap.scaled(600, 1000, Qt.KeepAspectRatio, Qt.FastTransformation)
        self.banner.setPixmap(self.pixmap)
        self.banner.resize(self.pixmap.width(), self.pixmap.height())
        ##### Tab Bar #####
        self.tabWidget = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()
        self.tabWidget.addTab(self.tab1, 'Vehicle Tools')
        self.tabWidget.addTab(self.tab2, 'Site Tools')
        self.tabWidget.addTab(self.tab3, 'Point Cloud Tools')

        ################################################## VEHICLE TOOL BUTTONS ########################################################################
        ##### Studio Dropdown #####
        self.choose_studio_button = QComboBox(self)
        studio_list = []
        self.studio_paths = []
        for file in glob.glob(self.studio_dir + '/*'): #finds all studios and creates dropdown
            studio_match = re.search('/studios(.*).mb', file)
            studio_name = studio_match.group(1)
            studio_list.append(studio_name[1:])
            self.studio_paths.append(file)
        for item in studio_list:
            self.choose_studio_button.addItem(item)
        self.studio_current = self.studio_paths[self.choose_studio_button.currentIndex()]

        ##### Studio Load Button #####
        self.load_studio_button = QPushButton(QIcon(self.icon_dir + "/template.png"), "Load Studio")
        self.load_studio_button.setMinimumHeight(UI_ELEMENT_HEIGHT)
        self.load_studio_button.setMinimumWidth(UI_ELEMENT_WIDTH)

        ##### Vehicle Text Bar #####
        self.choose_vehicle_edit = QLineEdit()
        self.choose_vehicle_edit.setPlaceholderText("Vehicle File")
        self.choose_vehicle_edit.setMinimumHeight(UI_ELEMENT_HEIGHT)
        self.choose_vehicle_edit.setMinimumWidth(UI_ELEMENT_WIDTH)

        ##### Vehicle Folder Button #####
        self.choose_vehicle_button = QPushButton(QIcon(self.icon_dir + "/open.png"), "")
        self.choose_vehicle_button.setMinimumHeight(UI_ELEMENT_HEIGHT)

        ##### Load Vehicle Button #####
        self.load_vehicle_button = QPushButton(QIcon(self.icon_dir + "/load.png"), "Load Vehicle")
        self.load_vehicle_button.setMinimumHeight(UI_ELEMENT_HEIGHT)
        self.load_vehicle_button.setMinimumWidth(UI_ELEMENT_WIDTH)

        ##### Vehicle Specs Image #####
        self.specs_icon = QLabel()
        self.specsmap = QPixmap(self.icon_dir + '/dxf.png')
        self.specsmap = self.specsmap.scaled(70, 90, Qt.KeepAspectRatio, Qt.FastTransformation)
        self.specs_icon.setPixmap(self.specsmap)

        ##### Vehicle Specs Text Bar #####
        self.choose_vehiclespec_edit = QLineEdit()
        self.choose_vehiclespec_edit.setPlaceholderText("Vehicle Specs")
        self.choose_vehiclespec_edit.setMinimumHeight(UI_ELEMENT_HEIGHT)
        self.choose_vehiclespec_edit.setMinimumWidth(UI_ELEMENT_WIDTH)

        ##### Vehicle Specs Folder Button #####
        self.choose_vehiclespec_button = QPushButton(QIcon(self.icon_dir + "/open.png"), "")
        self.choose_vehiclespec_button.setMinimumHeight(UI_ELEMENT_HEIGHT)
        #self.choose_vehiclespec_button.setMinimumWidth(UI_ELEMENT_WIDTH)

        ##### Do Everything Button #####
        self.do_everything_button = QPushButton(QIcon(self.icon_dir + "/wizzardHat.png"),"Magic VC Button")
        self.do_everything_button.setMinimumHeight(UI_ELEMENT_HEIGHT)

        ##### Load Specs Button #####
        self.load_vehiclespec_button = QPushButton(QIcon(self.icon_dir + "/load.png"), "Load Vehicle Specs")
        self.load_vehiclespec_button.setMinimumHeight(UI_ELEMENT_HEIGHT)
        self.load_vehiclespec_button.setMinimumWidth(UI_ELEMENT_WIDTH)

        ##### Don't Scale Switch #####
        self.post_arnold_button = QCheckBox('No Scaling', self)

        ##### Spellbook Dropdown #####
        self.choose_spellbook_button = QComboBox(self)
        spellbook_list = []
        self.path_list = []
        for file in glob.glob(self.spellbook_dir + '/*'): #Finds all spellbooks and creates dropdown
            spell_match = re.search('/spellbooks(.*).spb', file)
            spell_name = spell_match.group(1)
            spellbook_list.append(spell_name[1:])
            self.path_list.append(file)
        for item in spellbook_list:
            self.choose_spellbook_button.addItem(item)
        self.spellbook_current = self.path_list[self.choose_spellbook_button.currentIndex()]

        ##### Apply Spellbook Button #####
        self.apply_spellbook_button = QPushButton(QIcon(self.icon_dir + "/cast_all.png"), "Apply Spellbook")
        self.apply_spellbook_button.setMinimumHeight(UI_ELEMENT_HEIGHT)

        ##### Rotation Buttons #####
        self.xyz_selection = QComboBox(self)
        direction_list = ['X','Y','Z']
        for dir in direction_list:
            self.xyz_selection.addItem(dir)
        self.left_arrow_button = QPushButton(QIcon(self.icon_dir + "/left"), "Rotate -90")
        self.left_arrow_button.setMinimumHeight(UI_ELEMENT_HEIGHT)
        self.right_arrow_button = QPushButton(QIcon(self.icon_dir + "/right"), "Rotate +90")
        self.right_arrow_button.setMinimumHeight(UI_ELEMENT_HEIGHT)
        self.quick_rotate_button = QPushButton("Quick VC Rotate")
        self.hv_rotate_button = QPushButton("Quick HV Rotate")

        ##### Remove Tires Button #####
        self.remove_tires_button = QPushButton(QIcon(self.icon_dir + "/tire.png"), "Remove Tires")
        self.remove_tires_button.setMinimumHeight(UI_ELEMENT_HEIGHT)

        ##### Remove License Plate Button #####
        self.remove_license_plate_button = QPushButton(QIcon(self.icon_dir + "/license_plate.png"), "Remove License Plates")
        self.remove_license_plate_button.setMinimumHeight(UI_ELEMENT_HEIGHT)

        ##### Make Windows Transparent Button #####
        self.make_windows_transparent_button = QPushButton(QIcon(self.icon_dir + "/window.png"), "Transparent Windows (Arnold Only)")
        self.make_windows_transparent_button.setMinimumHeight(UI_ELEMENT_HEIGHT)

        ##### Save Button #####
        self.save_button = QPushButton(QIcon(self.icon_dir + "/save_as.png"), "Save As...")
        self.save_button.setMinimumHeight(UI_ELEMENT_HEIGHT)

        ##### Export Button #####
        self.export_obj = QPushButton(QIcon(self.icon_dir + "/export.png"),"Export OBJ")
        self.export_obj.setMinimumHeight(UI_ELEMENT_HEIGHT)

        ##### Thumbnail Capture #####
        self.thumb_button = QPushButton('Capture Thumbnail')
        self.thumb_button.setMinimumHeight(UI_ELEMENT_HEIGHT)

        ################################################### SITE TOOL BUTTONS #######################################################################################
        ##### XYZ Text Bar #####
        self.choose_locator_edit = QLineEdit()
        self.choose_locator_edit.setPlaceholderText("Locator File")
        self.choose_locator_edit.setMinimumHeight(UI_ELEMENT_HEIGHT)

        ##### XYZ Folder Button #####
        self.choose_locator_button = QPushButton(QIcon(self.icon_dir + "/open.png"), "")
        self.choose_locator_button.setMinimumHeight(UI_ELEMENT_HEIGHT)

        ##### Load XYZ Button #####
        self.load_locator_button = QPushButton(QIcon(self.icon_dir + "/load.png"), "Load Locators")
        self.load_locator_button.setMinimumHeight(UI_ELEMENT_HEIGHT)

        self.open_cable_button = QPushButton("Open Cable Creator")
        self.open_cable_button.setMinimumHeight(UI_ELEMENT_HEIGHT)

        ##################################################### Point Cloud Buttons ####################################################################################
        ##### Point CLoud Text Bar #####
        self.choose_xyzfile_edit = QLineEdit()
        self.choose_xyzfile_edit.setPlaceholderText("XYZ File")
        self.choose_xyzfile_edit.setMinimumHeight(UI_ELEMENT_HEIGHT)

        ##### Point CLoud Folder Button #####
        self.choose_xyzfile_button = QPushButton(QIcon(self.icon_dir + "/open.png"), "")
        self.choose_xyzfile_button.setMinimumHeight(UI_ELEMENT_HEIGHT)

        ##### Load Point CLoud Button #####
        self.load_xyzfile_button = QPushButton(QIcon(self.icon_dir + "/load.png"), "Load Point Cloud")
        self.load_xyzfile_button.setMinimumHeight(UI_ELEMENT_HEIGHT)

        ##### Density Dropdown #####
        self.choose_density_button = QComboBox(self)
        self.density_list = ['Entire File','High','Medium','Low','Very Low']
        for item in self.density_list:
            self.choose_density_button.addItem(item)
        self.density_label = QLabel()
        self.density_label.setText('Density Settings:')
        self.density_label.setAlignment(Qt.AlignCenter)
        self.density_current = self.density_list[self.choose_density_button.currentIndex()]

    def create_layout(self):
        main_layout = QVBoxLayout()
        vehicleTool_layout = QVBoxLayout()
        siteTool_layout = QVBoxLayout()
        self.pcTool_layout = QVBoxLayout()

        self.setStyleSheet("""QTabWidget {background-color: rgb(100,102,117);}
                            QPushButton {background-color: rgb(87,87,87);}
                            QGroupBox {background-color: rgb(72,71,76);}
                            QComboBox {background-color: rgb(87,87,87); }
                            QComboBox QAbstractItemView {background-color: rgb(72,71,76); selection-background-color : rgb(100,102,117)}
                            """)

        ##############################################
        ######       Vehicle Section            ######
        ##############################################

        ##### Studio GUI Section #####
        studio_group = QGroupBox("Studio")
        studio_layout = QVBoxLayout()
        studio_layout.addWidget(self.choose_studio_button)
        studio_layout.addWidget(self.load_studio_button)
        studio_group.setLayout(studio_layout)
        vehicleTool_layout.addWidget(studio_group)
        #vehicleTool_layout.insertSpacing(-1, 10)

        ##### Vehicle GUI Section #####
        load_group = QGroupBox("Vehicle")
        load_vehicle_layout = QGridLayout()
        load_vehicle_layout.addWidget(self.choose_vehicle_button, 0, 0)
        load_vehicle_layout.addWidget(self.choose_vehicle_edit, 0, 1, 1, 3)
        load_vehicle_layout.addWidget(self.post_arnold_button, 0, 4)
        load_vehicle_layout.addWidget(self.load_vehicle_button, 0, 5, 1, 3)
        load_vehicle_layout.addWidget(self.choose_vehiclespec_edit, 1, 1, 1, 3)
        load_vehicle_layout.addWidget(self.choose_vehiclespec_button, 1, 0)
        load_vehicle_layout.addWidget(self.specs_icon, 1, 4)
        load_vehicle_layout.addWidget(self.load_vehiclespec_button, 1, 5, 1, 3)
        load_vehicle_layout.addWidget(self.do_everything_button, 2, 0, 1, 8)
        load_group.setLayout(load_vehicle_layout)
        vehicleTool_layout.addWidget(load_group)

        ##### Spellbook GUI Section #####
        spell_group = QGroupBox("Spellbook")
        spell_layout = QVBoxLayout()
        spell_layout.addWidget(self.choose_spellbook_button)
        spell_layout.addWidget(self.apply_spellbook_button)
        spell_group.setLayout(spell_layout)
        vehicleTool_layout.addWidget(spell_group)

        ##### Rotation GUI Section #####
        rotation_group = QGroupBox("Rotation")
        rotation_layout = QGridLayout()
        rotation_layout.addWidget(self.xyz_selection, 2, 0)
        rotation_layout.addWidget(self.left_arrow_button, 2, 1)
        rotation_layout.addWidget(self.right_arrow_button, 2, 2)
        rotation_layout.addWidget(self.quick_rotate_button, 0, 0, 1, 3)
        rotation_layout.addWidget(self.hv_rotate_button, 1, 0, 1, 3)
        rotation_group.setLayout(rotation_layout)
        vehicleTool_layout.addWidget(rotation_group)
        #vehicleTool_layout.insertSpacing(-1, 10)

        ##### Extra Tools GUI Section #####
        tools_group = QGroupBox("Extra Tools")
        tools_layout = QVBoxLayout()
        tools_layout.addWidget(self.remove_tires_button)
        tools_layout.addWidget(self.remove_license_plate_button)
        tools_layout.addWidget(self.make_windows_transparent_button)
        tools_group.setLayout(tools_layout)
        vehicleTool_layout.addWidget(tools_group)
        #vehicleTool_layout.insertSpacing(-1, 10)

        ##############################################
        ######          Site Section            ######
        ##############################################

        ##### XYZ Locator Section #####
        locator_group = QGroupBox("Locators")
        locator_layout = QGridLayout()
        locator_layout.addWidget(self.choose_locator_button, 0, 0)
        locator_layout.addWidget(self.choose_locator_edit, 0, 1, 1, 2)
        locator_layout.addWidget(self.load_locator_button, 1, 0, 1, 3)
        locator_group.setLayout(locator_layout)
        siteTool_layout.addWidget(locator_group)

        ##### Cable GUI #####
        cable_group = QGroupBox("Cable GUI")
        cable_layout = QVBoxLayout()
        cable_layout.addWidget(self.open_cable_button)
        cable_group.setLayout(cable_layout)
        siteTool_layout.addWidget(cable_group)

        ##############################################
        ######      Point Cloud Section         ######
        ##############################################

        ##### Load Section #####
        pcload_group = QGroupBox("Load Point Cloud")
        pcload_layout = QGridLayout()
        pcload_layout.addWidget(self.choose_xyzfile_button, 0, 0)
        pcload_layout.addWidget(self.choose_xyzfile_edit, 0, 1, 1, 2)
        pcload_layout.addWidget(self.density_label, 1, 0)
        pcload_layout.addWidget(self.choose_density_button, 1, 1, 1, 2)
        pcload_layout.addWidget(self.load_xyzfile_button, 2, 0, 1, 3)
        pcload_group.setLayout(pcload_layout)
        self.pcTool_layout.addWidget(pcload_group)

        ##############################################
        ######          Save Section            ######
        ##############################################

        ##### Save Section #####
        save_group = QGroupBox("File Management")
        save_layout = QVBoxLayout()
        save_layout.addWidget(self.save_button)
        save_layout.addWidget(self.export_obj)
        save_group.setLayout(save_layout)

        ##### Set Main Layout #####
        self.tab1.setLayout(vehicleTool_layout)
        self.tab2.setLayout(siteTool_layout)
        self.tab3.setLayout(self.pcTool_layout)
        main_layout.addWidget(self.banner)
        main_layout.addWidget(self.tabWidget)
        main_layout.addWidget(save_group)
        self.setLayout(main_layout)

    #---------------------------------------------------------------------------------------------------------------
    # Connect button to button functions
    #---------------------------------------------------------------------------------------------------------------
    def make_connections(self):
        #--------------------------------- Vehicle Section -------------------------------------------------#
        ##### Studio Group #####
        self.load_studio_button.clicked.connect(self.load_studio)
        ##### Vehicle Group #####
        self.choose_vehicle_button.clicked.connect(self.choose_vehicle)
        self.load_vehicle_button.clicked.connect(self.load_vehicle)
        self.choose_vehiclespec_button.clicked.connect(self.choose_vehiclespec)
        self.load_vehiclespec_button.clicked.connect(self.load_vehiclespec)
        self.post_arnold_button.stateChanged.connect(self.dont_shrink_bool)
        self.do_everything_button.clicked.connect(self.auto_vc)
        ##### Spellbook Group #####
        self.apply_spellbook_button.clicked.connect(self.apply_spellbook)
        ##### Rotation Group #####
        self.left_arrow_button.clicked.connect(self.neg_rotation)
        self.right_arrow_button.clicked.connect(self.pos_rotation)
        self.quick_rotate_button.clicked.connect(self.quick_rotate)
        self.hv_rotate_button.clicked.connect(self.hv_rotate)
        ##### Extra Tools #####
        self.remove_tires_button.clicked.connect(self.remove_tires)
        self.remove_license_plate_button.clicked.connect(self.remove_license_plate)
        self.make_windows_transparent_button.clicked.connect(self.make_windows_transparent)
        ##### Save Group #####
        self.thumb_button.clicked.connect(self.get_thumb)
        self.save_button.clicked.connect(self.save)
        self.export_obj.clicked.connect(self.export)

        #-------------------------------------- Site Section ------------------------------------------------#
        ##### Locator Group #####
        self.choose_locator_button.clicked.connect(self.choose_locator)
        self.load_locator_button.clicked.connect(self.load_locator)

        ##### Cable Group #####
        self.open_cable_button.clicked.connect(self.cable_gui)

        #------------------------------------- Point Cloud Section ------------------------------------------#
        ##### Load Group #####
        self.choose_xyzfile_button.clicked.connect(self.choose_xyzfile)
        self.load_xyzfile_button.clicked.connect(self.load_xyzfile)

    #---------------------------------------------------------------------------------------------------------------
    # Button Functions
    #---------------------------------------------------------------------------------------------------------------
    def dont_shrink_bool(self, state):
        # If project already scaled click to prevent scaling again
        if state == Qt.Checked:
            self.dont_shrink = True
        else:
            self.dont_shrink = False

    def load_studio(self):
        #Choose which studio to work in
        cmds.file(new=True, force=True)
        studio_path = self.studio_paths[self.choose_studio_button.currentIndex()]
        cmds.file(studio_path, open=True)

    def choose_vehicle(self):
        #Sets vehicle path
        file_path = QFileDialog.getOpenFileName(None, "", self.vehicle_library_dir, "Vehicles (*.mb *.obj *.fbx);;All Files (*.*)")[0]
        if file_path == "":  # If they cancel the dialog
            return  # Then just don't open anything
        self.choose_vehicle_edit.setText(file_path)

    def load_vehicle(self):
        # Loads choosen vehicle
        vehicle_path = self.choose_vehicle_edit.text()
        if os.path.isfile(vehicle_path):
            cmds.select(allDagObjects=True)
            prev_all_objects = cmds.ls(selection=True)
            cmds.select(deselect=True)
            # print(str(prev_all_objects))
            cmds.file(vehicle_path, i=True)
            cmds.select(allDagObjects=True)
            new_all_objects = cmds.ls(selection=True)
            cmds.select(deselect=True)
            # print(str(new_all_objects))
            diff = [x for x in new_all_objects if x not in prev_all_objects]
            # print(str(diff))
            cmds.group(diff, name="Vehicle")
            if self.dont_shrink == False:
                #print('shrink!')
                cmds.scale(0.0328, 0.0328, 0.0328, absolute=True, pivot=(0, 0, 0))
            cmds.select(deselect=True)
            asset_match = re.search('.*/([a-zA-Z_0-9\(\)]*).*\.m[ab]', vehicle_path)
            if asset_match != None:
                self.asset = asset_match.group(1)
                cmds.file(rename=self.asset)
        else:
            warning_box = QMessageBox(QMessageBox.Warning, "No Vehicle Found", "No vehicle file found at the specified path.")
            warning_box.exec_()

    def choose_vehiclespec(self):
        # Set Spec Path
        file_path = QFileDialog.getOpenFileName(None, "", self.vehiclespec_library_dir, "Vehicles (*.mb *.obj *.fbx *.ma *dxf);;All Files (*.*)")[0]
        if file_path == "": # If they cancel the dialog
            return # Then just don't open anything
        self.choose_vehiclespec_edit.setText(file_path)

    def load_vehiclespec(self):
        #Load Specs From Choosen Path
        vehiclespec_path = self.choose_vehiclespec_edit.text()
        if os.path.isfile(vehiclespec_path):
            cmds.select(allDagObjects=True)
            prev_all_objects = cmds.ls(selection=True)
            cmds.select(deselect=True)
            # print(str(prev_all_objects))

            cmds.file(vehiclespec_path, i=True)
            cmds.select(allDagObjects=True)
            new_all_objects = cmds.ls(selection=True)
            cmds.select(deselect=True)
            # print(str(new_all_objects))
            diff = [x for x in new_all_objects if x not in prev_all_objects]
            # print(str(diff))
            cmds.group(diff, name="Vehiclespecs")
            cmds.xform (absolute=True, scale=(1, 1, 1),rotation=(90,90,0),translation=(-10.583,-4.333,0),)
            cmds.makeIdentity(apply=True, t=1, r=1, s=1, n=0)
            cmds.select(deselect=True)

        else:
            warning_box = QMessageBox(QMessageBox.Warning, "No Vehiclespecs Found", "No vehicle specs file found at the specified path.")
            warning_box.exec_()

    def choose_spellbook(self):
        # Sets spellbook path
        file_path = self.path_list[self.choose_spellbook_button.currentIndex()]
        #if file_path == "":
        #    return
        self.save_last_file(self.spellbook_current)

    def neg_rotation(self):
        direction = self.xyz_selection.currentIndex()
        if direction == 0:
            cmds.select(all=True)
            cmds.rotate(-90, 0, 0, relative=True, p=[0,0,0])
            cmds.select(deselect=True)
            print('rotate')
        if direction == 1:
            cmds.select(all=True)
            cmds.rotate(0, -90, 0, relative=True, p=[0,0,0])
            cmds.select(deselect=True)
            print('rotate')
        if direction == 2:
            cmds.select(all=True)
            cmds.rotate(0, 0, -90, relative=True, p=[0,0,0])
            cmds.select(deselect=True)
            print('rotate')

    def pos_rotation(self):
        direction = self.xyz_selection.currentIndex()
        if direction == 0:
            cmds.select(all=True)
            cmds.rotate(90, 0, 0, relative=True, p=[0,0,0])
            cmds.select(deselect=True)
            print('rotate')
        if direction == 1:
            cmds.select(all=True)
            cmds.rotate(0, 90, 0, relative=True, p=[0,0,0])
            cmds.select(deselect=True)
            print('rotate')
        if direction == 2:
            cmds.select(all=True)
            cmds.rotate(0, 0, 90, relative=True, p=[0,0,0])
            cmds.select(deselect=True)
            print('rotate')

    def quick_rotate(self):
        cmds.select(all=True)
        cmds.rotate(90, 0, 90, a=True, p=[0,0,0])
        cmds.select(deselect=True)

    def hv_rotate(self):
        cmds.select(all=True)
        cmds.rotate(-90, 0, -90, a=True, p=[0,0,0])
        cmds.select(deselect=True)

    def remove_tires(self):
        try:
            tires = cmds.ls('*Tire*', '*tire*')
            for tire in tires:
                try:
                    print(tire)
                    cmds.delete(tire)
                except Exception as e:
                    print(e)

            rims = cmds.ls('*Rim*', '*rim*')
            for rim in rims:
                if (rim == 'rimShader') or (rim == 'rimSG') or (rim == 'Rims') or ('primary' in rim) or ('Primary' in rim):
                    continue
                else:
                    try:
                        print(rim)
                        cmds.delete(rim)
                    except Exception as e:
                        print(e)

            brakes = cmds.ls('*Brake*', '*brake*')
            for brake in brakes:
                if (brake == 'brakeShader') or (brake == 'brakeSG'):
                    continue
                else:
                    try:
                        print(brake)
                        cmds.delete(brake)
                    except Exception as e:
                        print(e)

            bolts = cmds.ls('*Bolt*', '*bolt*', '*Nuts*', '*nuts*')
            for bolt in bolts:
                try:
                    print(bolt)
                    cmds.delete(bolt)
                except Exception as e:
                    print(e)

            logos = cmds.ls('*Logo*')
            for logo in logos:
                try:
                    print(logo)
                    cmds.delete(logo)
                except Exception as e:
                    print(e)

            wheels = cmds.ls('*Wheel*', '*wheel*')
            for wheel in wheels:
                try:
                    print(wheel)
                    cmds.delete(wheel)
                except Exception as e:
                    print(e)

            axis = cmds.ls('*Axis*', '*axis*', '*axel*', '*Axel*')
            for axel in axis:
                try:
                    print(axel)
                    cmds.delete(axel)
                except Exception as e:
                    print(e)
        except Exception as e:
            print(e)

        try:
            tires = cmds.ls('*Tire*', '*tire*', s=True)
            for tire in tires:
                try:
                    print(tire)
                    cmds.delete(tire)
                except Exception as e:
                    print(e)

            rims = cmds.ls('*Rim*', '*rim*', s=True)
            for rim in rims:
                if (rim == 'rimShader') or (rim == 'rimSG') or (rim == 'Rims') or ('primary' in rim) or ('Primary' in rim):
                    continue
                else:
                    try:
                        print(rim)
                        cmds.delete(rim)
                    except Exception as e:
                        print(e)

            brakes = cmds.ls('*Brake*', '*brake*', s=True)
            for brake in brakes:
                if (brake == 'brakeShader') or (brake == 'brakeSG'):
                    continue
                else:
                    try:
                        print(brake)
                        cmds.delete(brake)
                    except Exception as e:
                        print(e)

            bolts = cmds.ls('*Bolt*', '*bolt*', '*Nuts*', '*nuts*', s=True)
            for bolt in bolts:
                try:
                    print(bolt)
                    cmds.delete(bolt)
                except Exception as e:
                    print(e)

            logos = cmds.ls('*Logo*')
            for logo in logos:
                try:
                    print(logo)
                    cmds.delete(logo)
                except Exception as e:
                    print(e)

            wheels = cmds.ls('*Wheel*', '*wheel*', s=True)
            for wheel in wheels:
                try:
                    print(wheel)
                    cmds.delete(wheel)
                except Exception as e:
                    print(e)

            axis = cmds.ls('*Axis*', '*axis*', '*axel*', '*Axel*', s=True)
            for axel in axis:
                try:
                    print(axel)
                    cmds.delete(axel)
                except Exception as e:
                    print(e)
        except Exception as e:
            print(e)

    def choose_locator(self):
        # Set locator Path
        file_path = QFileDialog.getOpenFileName(None, "", self.desktop_dir, "Text Files (*.txt);;All Files (*.*)")[0]
        if file_path == "": # If they cancel the dialog
            return # Then just don't open anything
        self.choose_locator_edit.setText(file_path)

    def load_locator(self):
        filename = self.choose_locator_edit.text()
        f = open(filename, 'r')
        full = f.readlines()
        for i in range(0,len(full)):
            full[i] = full[i].rstrip()
            #print(full)
            if i == 0:
                headers = full[i].split('\t')
                #print(headers)
                for i in range(0, len(headers)):
                    headers[i] = headers[i].lower()
                #print(headers)
                x_loc = headers.index('x')
                y_loc = headers.index('y')
                z_loc = headers.index('z')
                #print(str(x_loc) + ' ' + str(y_loc) + ' ' + str(z_loc))

            else:
                xyz = full[i].split('\t')
                #print(xyz)
                x = xyz[x_loc]
                y = xyz[y_loc]
                z = xyz[z_loc]
                #print(z)
                cmds.spaceLocator(p=[x,y,z])

        f.close()

    def choose_xyzfile(self):
        # Set locator Path
        file_path = QFileDialog.getOpenFileName(None, "", self.desktop_dir, "XYZ Files (*.xyz);;Text Files (*.txt);;All Files (*.*)")[0]
        if file_path == "": # If they cancel the dialog
            return # Then just don't open anything
        self.choose_xyzfile_edit.setText(file_path)

    def load_xyzfile(self):
        progress_group = QGroupBox("Loading Bar")
        progressBox = QVBoxLayout()
        load_label = QLabel()
        self.progress = QProgressBar(self)

        progressBox.addWidget(load_label)
        progressBox.addWidget(self.progress)
        progress_group.setLayout(progressBox)
        self.pcTool_layout.addWidget(progress_group)

        load_label.setText('Reading File')
        load_value = 0
        for i in range(0,5):
            load_value += 1
            self.progress.setValue(load_value)
            progress_group.setVisible(True)

        filename = self.choose_xyzfile_edit.text()
        intensity = self.choose_density_button.currentIndex()
        stepSize = intensity + 1

        f = open(filename, 'r')
        full = [line.rstrip().split(' ') for line in f.readlines()[::stepSize]]
        particleList, colorList = [(float(pos[0]), float(pos[1]), float(pos[2])) for pos in full], [(float(color[3])/255, float(color[4])/255, float(color[5])/255) for color in full]
        xmin, ymin, zmin = min([float(x[0]) for x in full]), min([float(y[1]) for y in full]), min([float(z[0]) for z in full])
        f.close()

        load_label.setText('Creating Point Cloud')
        load_value += 35
        self.progress.setValue(load_value)
        progress_group.setVisible(True)

        cmds.evaluator(n='dynamics', c='disablingNodes=dynamics')
        cmds.evaluator(n='dynamics', c='handledNodes=none')
        cmds.evaluator(n='dynamics', c='action=none')

        pointCloud, pointCloudShape = cmds.nParticle(p=particleList)

        load_label.setText('Applying Colors')
        load_value += 35
        self.progress.setValue(load_value)
        progress_group.setVisible(True)
        cmds.select(pointCloudShape)
        cmds.addAttr(ln='rgbPP', dt='vectorArray')
        cmds.setAttr(pointCloudShape+'.rgbPP', len(colorList), *colorList, type='vectorArray')

        cmds.select(pointCloud)
        cmds.xform(cp=True)
        load_label.setText('Moving to origin')
        load_value += 20
        self.progress.setValue(load_value)
        self.progress.setVisible(True)
        cmds.move(-xmin, -ymin, -zmin, rpr=True)
        cmds.select(deselect=True)

        cmds.select(pointCloud)
        cmds.rotate(-90,0, 0, r=True, p=[0,0,0])
        cmds.select(deselect=True)
        load_value += 4
        self.progress.setValue(load_value)
        self.progress.setVisible(True)
        progress_group.setVisible(False)

    def get_thumb(self):
        filename, file_extension = os.path.splitext(self.choose_vehicle_edit.text())
        cmds.SaveSceneAsOptions()
        print(window)
        #cmds.thumbnailCaptureComponent(capture=True)
        #cmds.thumbnailCaptureComponent(save=self.thumbs_dir + '_Done')
        #cmds.thumbnailCaptureComponent(delete=True)
        #cmds.thumbnailCaptureComponent(q=True, previewPath=True)

    def auto_vc(self):
        self.quick_rotate()
        self.auto_apply_spellbook()
        self.remove_tires()
        self.remove_license_plate()

    def export(self):
        cmds.select(all=True)
        cmds.file(self.desktop_dir + '\\' + self.asset + '_OBJ', type='OBJexport', es=True, sh=True, force=True)

    def cable_gui(self):
        exec(open(self.ms_dir + '/CableMaker.py').read())

    # --------------------------------------------------------------------------------------------------------------
    # Writes the current file path to preferences
    # --------------------------------------------------------------------------------------------------------------
    def save_last_file(self, last_file_path):
        line_found = False
        if os.path.isfile(self.pref_path):  # If the prefs file exists
            for line in fileinput.input(self.pref_path, inplace=True):
                if line.startswith(self.last_file_pref):
                    line_found = True
                    line = self.last_file_pref + "=" + last_file_path + "\n"
                sys.stdout.write(line)

        if not line_found:
            with open(self.pref_path, "a") as f:
                f.write(self.last_file_pref + "=%s\n" % last_file_path)
                f.close()

    def apply_spellbook(self):
        # Applies choosen spellbook
        spellbook_path = self.path_list[self.choose_spellbook_button.currentIndex()]
        if os.path.isfile(spellbook_path):
            selection = cmds.ls(selection=True)
            cmds.select(deselect=True)
            with open(spellbook_path) as f:
                data = f.read().splitlines()
                for spell in data:
                    spell_split = spell.split(":")
                    original = spell_split[0]
                    replacement = spell_split[1]
                    spell_type = spell_split[2]

                    # print("Replacing " + original + " " + spell_type + " with " + replacement)
                    if spell_type == "Shader":
                        cmds.hyperShade(objects=original)
                    elif spell_type == "Object":
                        cmds.select(original, replace=True)
                    else:
                        raise ValueError(
                            "Spell type invalid. Should be one of the following: " + str(self.types_model.stringList()))
                    cmds.hyperShade(assign=replacement)
                    cmds.select(deselect=True)
            cmds.select(selection)
        else:
            warning_box = QMessageBox(QMessageBox.Warning, "No Spellbook Found",
                                      "No spellbook file (*.spb) found at the specified path.")
            warning_box.exec_()

    def remove_license_plate(self):
        cmds.delete("LicPlate*")

    def make_windows_transparent(self):
        selection = cmds.ls(selection=True)

        cmds.select(deselect=True)
        cmds.hyperShade(objects="*Window*")
        windows = cmds.ls(selection=True)
        cmds.select(deselect=True)

        for window in windows:
            cmds.setAttr(window + ".aiOpaque", False)

        cmds.select(selection)

    def save(self):
        cmds.SaveSceneAs(o=True)

    def auto_apply_spellbook(self):
        # Applies choosen spellbook
        is_arnold = False
        arnold_list = cmds.ls('*Arnold*')
        if len(arnold_list) > 0:
            is_arnold = True

        if is_arnold:
            spellbook_path = self.spellbook_dir + '\\' + 'Arn2Blinn.spb'
            cmds.select(all=True)
            cmds.rotate(0, 0, -90, r=True, p=[0,0,0])
            cmds.select(deselect=True)
            cmds.delete('*aiSkyDomeLight*')

        else:
            spellbook_path = self.spellbook_dir + '\\' + 'Hum2Blinn.spb'
            cmds.select(deselect=True)

        #spellbook_path =
        if os.path.isfile(spellbook_path):
            selection = cmds.ls(selection=True)
            cmds.select(deselect=True)
            with open(spellbook_path) as f:
                data = f.read().splitlines()
                for spell in data:
                    spell_split = spell.split(":")
                    original = spell_split[0]
                    replacement = spell_split[1]
                    spell_type = spell_split[2]

                    # print("Replacing " + original + " " + spell_type + " with " + replacement)
                    if spell_type == "Shader":
                        cmds.hyperShade(objects=original)
                    elif spell_type == "Object":
                        cmds.select(original, replace=True)
                    else:
                        print('Error applying spellbook')
                    cmds.hyperShade(assign=replacement)
                    cmds.select(deselect=True)
            cmds.select(selection)

# Dev code to automatically close old windows when running
try:
    ui.close()
except:
    pass

# Show a new instance of the UI
ui = MainUI()
ui.show()
