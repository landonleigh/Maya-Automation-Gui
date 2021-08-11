import fileinput, os, sys, glob, re, math
import maya.OpenMayaUI as mui
import maya.cmds as cmds
import maya.mel as mel
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from shiboken2 import wrapInstance

ms_dir = os.path.expanduser("~/maya/scripts/magic-shade")
sys.path.append(ms_dir)
from CableMaker import *

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
    skeleton_dir = ms_dir + '/skelFiles'
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
        self.dialogs = list()
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
        self.tab4 = QWidget()
        self.tab5 = QWidget()
        self.tab6 = QWidget()
        self.tabWidget.addTab(self.tab1, 'Vehicle Tools')
        self.tabWidget.addTab(self.tab2, 'Site Tools')
        self.tabWidget.addTab(self.tab3, 'Point Cloud Tools')
        self.tabWidget.addTab(self.tab4, 'Virtual Crash Tools')
        self.tabWidget.addTab(self.tab5, 'Vehicle Rigging')
        self.tabWidget.addTab(self.tab6, 'Character Rigging')

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
        self.quick_rotate_button.setMinimumHeight(UI_ELEMENT_HEIGHT)
        self.hv_rotate_button = QPushButton("Quick HV Rotate")
        self.hv_rotate_button.setMinimumHeight(UI_ELEMENT_HEIGHT)

        ##### Scale Button #####
        self.autoScale_button = QPushButton("Auto Scale")
        self.autoScale_button.setMinimumHeight(UI_ELEMENT_HEIGHT)

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

        ##### Cable Creation Buttons #####
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

        ##################################################### VC Files ####################################################################################
        ##### VC Data Buttons #####
        self.choose_vcData_button = QPushButton(QIcon(self.icon_dir + "/open.png"), "")
        self.choose_vcData_button.setMinimumHeight(UI_ELEMENT_HEIGHT)

        self.choose_vcData_edit = QLineEdit()
        self.choose_vcData_edit.setPlaceholderText("Virtual Crash Data File")
        self.choose_vcData_edit.setMinimumHeight(UI_ELEMENT_HEIGHT)

        self.convert_vcData_button = QPushButton("Convert VC Data")
        self.convert_vcData_button.setMinimumHeight(UI_ELEMENT_HEIGHT)

        ##### File Management Buttons #####
        self.choose_rig_button = QPushButton(QIcon(self.icon_dir + "/open.png"), "")
        self.choose_rig_button.setMinimumHeight(UI_ELEMENT_HEIGHT)

        self.choose_rig_edit = QLineEdit()
        self.choose_rig_edit.setPlaceholderText("Rig File")
        self.choose_rig_edit.setMinimumHeight(UI_ELEMENT_HEIGHT)

        self.loadRig_button = QPushButton("Load Rig")
        self.loadRig_button.setMinimumHeight(UI_ELEMENT_HEIGHT)

        self.choose_mesh_button = QPushButton(QIcon(self.icon_dir + "/open.png"), "")
        self.choose_mesh_button.setMinimumHeight(UI_ELEMENT_HEIGHT)

        self.choose_mesh_edit = QLineEdit()
        self.choose_mesh_edit.setPlaceholderText("Ground Proxy File")
        self.choose_mesh_edit.setMinimumHeight(UI_ELEMENT_HEIGHT)

        self.loadMesh_button = QPushButton("Load Ground Proxy")
        self.loadMesh_button.setMinimumHeight(UI_ELEMENT_HEIGHT)

        ##### Vehicle Locator Buttons #####
        self.choose_vLocator_button = QPushButton(QIcon(self.icon_dir + "/open.png"), "")
        self.choose_vLocator_button.setMinimumHeight(UI_ELEMENT_HEIGHT)

        self.choose_vLocator_edit = QLineEdit()
        self.choose_vLocator_edit.setPlaceholderText("Vehicle Locator .MOV File")
        self.choose_vLocator_edit.setMinimumHeight(UI_ELEMENT_HEIGHT)

        self.create_vLocator_button = QPushButton("Create Vehicle Locator")
        self.create_vLocator_button.setMinimumHeight(UI_ELEMENT_HEIGHT)

        self.fps_edit = QComboBox(self)
        fps_list = ['24','30','100']
        for i in range(0,len(fps_list)):
            self.fps_edit.addItem(fps_list[i])
            if fps_list[i] == '100':
                hundredIndex = i
        self.fps_edit.setCurrentIndex(hundredIndex)
        self.fps_label = QLabel()
        self.fps_label.setText('FPS:')
        self.fps_label.setMaximumWidth(35)

        ##################################################### Vehicle Rigging ####################################################################################
        ##### Active Locator Drop Down #####
        self.LocatorLabel = QLabel()
        self.LocatorLabel.setText('Active Locator:')
        self.activeLocator_dropdown = QComboBox(self)
        locators = cmds.ls('*_Locator')
        for locator in locators:
            self.activeLocator_dropdown.addItem(locator)
        self.activeLocator_dropdown.setMinimumHeight(UI_ELEMENT_HEIGHT)

        ##### Active Rig Dropdown #####
        self.RigLabel = QLabel()
        self.RigLabel.setText('Active Rig:')
        self.activeRig_dropdown = QComboBox(self)
        rigs = cmds.ls('*_TopNode*')
        rigs.extend(cmds.ls('*:*_TopNode*'))
        for rig in rigs:
            self.activeRig_dropdown.addItem(rig)
        self.activeRig_dropdown.setMinimumHeight(UI_ELEMENT_HEIGHT)

        ##### Make Constraints #####
        self.pairRig2Locator_button = QPushButton('Pair Rig to Locator')
        self.pairRig2Locator_button.setMinimumHeight(UI_ELEMENT_HEIGHT)

        ##### Edit Constraint Rotation #####
        self.parentX = QLineEdit()
        self.parentX.setPlaceholderText("Rotate X")
        self.parentX.setMinimumHeight(UI_ELEMENT_HEIGHT)
        self.parentY = QLineEdit()
        self.parentY.setPlaceholderText("Rotate Y")
        self.parentY.setMinimumHeight(UI_ELEMENT_HEIGHT)
        self.parentZ = QLineEdit()
        self.parentZ.setPlaceholderText("Rotate Z")
        self.parentZ.setMinimumHeight(UI_ELEMENT_HEIGHT)
        self.rotateOnConst_button = QPushButton('Rotate on Constraint')
        self.rotateOnConst_button.setMinimumHeight(UI_ELEMENT_HEIGHT)

        ##### Edit Constraint Translation #####
        self.cgHeight_edit = QLineEdit()
        self.cgHeight_edit.setPlaceholderText('CoG Height')
        self.cgHeight_edit.setMinimumHeight(UI_ELEMENT_HEIGHT)
        self.cgXOffset_edit = QLineEdit()
        self.cgXOffset_edit.setPlaceholderText('CoG X Offset')
        self.cgXOffset_edit.setMinimumHeight(UI_ELEMENT_HEIGHT)
        self.cgYOffset_edit = QLineEdit()
        self.cgYOffset_edit.setPlaceholderText('CoG Y Offset')
        self.cgYOffset_edit.setMinimumHeight(UI_ELEMENT_HEIGHT)
        self.cgAdjust_button = QPushButton('Adjust CoG Offset')
        self.cgAdjust_button.setMinimumHeight(UI_ELEMENT_HEIGHT)

        ##### Light Rigging #####
        self.lightName_edit = QLineEdit()
        self.lightName_edit.setMinimumHeight(UI_ELEMENT_HEIGHT)
        self.lightName_edit.setPlaceholderText('Light Name')
        self.lightIntensity = QLineEdit()
        self.lightIntensity.setMinimumHeight(UI_ELEMENT_HEIGHT)
        self.lightIntensity.setPlaceholderText('Intensity')
        self.pairLight_button = QPushButton('Pair Light to Locator')
        self.pairLight_button.setMinimumHeight(UI_ELEMENT_HEIGHT)

        ##### Save Pre-Bake #####
        self.preBakeSave_button = QPushButton('Save Pre-Baked File')
        self.preBakeSave_button.setMinimumHeight(UI_ELEMENT_HEIGHT)

        ##### Wheel Constraint #####
        self.siteName_edit = QLineEdit()
        self.siteName_edit.setPlaceholderText('Site Name')
        self.siteName_edit.setMinimumHeight(UI_ELEMENT_HEIGHT)
        self.wheelConstr_button = QPushButton('Constrain wheels to mesh')
        self.wheelConstr_button.setMinimumHeight(UI_ELEMENT_HEIGHT)

        ##### Bake Button #####
        self.bakeButton = QPushButton('Bake Root Joint')
        self.bakeButton.setMinimumHeight(UI_ELEMENT_HEIGHT)

        ##### Bake Settings #####
        self.bakeStart_label = QLabel()
        self.bakeStart_label.setText('Start Frame:')
        self.bakeStart_edit = QLineEdit()
        self.bakeStart_edit.setMinimumHeight(UI_ELEMENT_HEIGHT)
        self.bakeStart_edit.setPlaceholderText('Ex:  0')
        self.bakeStop_label = QLabel()
        self.bakeStop_label.setMinimumHeight(UI_ELEMENT_HEIGHT)
        self.bakeStop_label.setText('Stop Frame:')
        self.bakeStop_edit = QLineEdit()
        self.bakeStop_edit.setMinimumHeight(UI_ELEMENT_HEIGHT)
        self.bakeStop_edit.setPlaceholderText('Ex:  2500')

        ##### Export FBX #####
        self.exportFBX_button = QPushButton('Export Selected Root Joint Animation')
        self.exportFBX_button.setMinimumHeight(UI_ELEMENT_HEIGHT)
        self.unrealExportSelection_button = QPushButton('Select Skeleton and Mesh for Unreal')
        self.unrealExportSelection_button.setMinimumHeight(UI_ELEMENT_HEIGHT)
        self.unrealExport_button = QPushButton('Bake and Export to Unreal')
        self.unrealExport_button.setMinimumHeight(UI_ELEMENT_HEIGHT)

        ##### Blend Shapes #####
        self.blendNode_edit = QLineEdit()
        self.blendNode_edit.setPlaceholderText('Blend Node Name - Ex: Initial Impact')
        self.blendNode_edit.setMinimumHeight(UI_ELEMENT_HEIGHT)
        self.blendGroupName_edit = QLineEdit()
        self.blendGroupName_edit.setPlaceholderText('Create Group Name')
        self.blendGroupName_edit.setMinimumHeight(UI_ELEMENT_HEIGHT)
        self.createBlendGroup_button = QPushButton('Group Shapes')
        self.createBlendGroup_button.setMinimumHeight(UI_ELEMENT_HEIGHT)

        ##################################################### Character Rigging ####################################################################################
        ##### File Load #####
        self.chooseCharacterData_edit = QLineEdit()
        self.chooseCharacterData_edit.setPlaceholderText("Character Data File")
        self.chooseCharacterData_edit.setMinimumHeight(UI_ELEMENT_HEIGHT)

        self.chooseCharacterData_button = QPushButton(QIcon(self.icon_dir + "/open.png"), "")
        self.chooseCharacterData_button.setMinimumHeight(UI_ELEMENT_HEIGHT)

        self.chooseCharacterData_edit.setText('C:/Users/DylanSteimel/Desktop/fallstraightdown.csv')

        ##### Import Character #####
        self.importCharacter_button = QPushButton('Import Character Locators')
        self.importCharacter_button.setMinimumHeight(UI_ELEMENT_HEIGHT)
        self.popUp_button = QPushButton('Pop-Up')

        ##### Skele Rig File #####
        self.chooseSkeleRig_edit = QLineEdit()
        self.chooseSkeleRig_edit.setPlaceholderText("Character File")
        self.chooseSkeleRig_edit.setMinimumHeight(UI_ELEMENT_HEIGHT)

        self.chooseSkeleRig_button = QPushButton(QIcon(self.icon_dir + "/open.png"), "")
        self.chooseSkeleRig_button.setMinimumHeight(UI_ELEMENT_HEIGHT)

        ##### Load Character #####
        self.loadCharacter_button = QPushButton('Load Character')
        self.loadCharacter_button.setMinimumHeight(UI_ELEMENT_HEIGHT)

        ##### Active Assets #####
        self.charLoc_label = QLabel()
        self.charLoc_label.setText('Active Locator Group: ')
        self.activeCharLocs_dropdown = QComboBox()
        charLocs = cmds.ls('*Character_Locators*')
        for cLoc in charLocs:
            self.activeCharLocs_dropdown.addItem(cLoc)
        self.activeCharLocs_dropdown.setMinimumHeight(UI_ELEMENT_HEIGHT)

        self.activeChar_label = QLabel()
        self.activeChar_label.setText('Active Character: ')
        self.activeCharacter_edit = QLineEdit()
        self.activeCharacter_edit.setMinimumHeight(UI_ELEMENT_HEIGHT)

        ##### Rig DropDown #####
        self.skeleRig_label = QLabel()
        self.skeleRig_label.setText('Character Rig Type: ')
        self.skeleRig_dropdown = QComboBox(self)
        skel_list = []
        self.skelePath_list = []
        for file in glob.glob(self.skeleton_dir + '/*'): #Finds all spellbooks and creates dropdown
            skel_match = re.search('skelFiles(.*).SKEL', file)
            skel_name = skel_match.group(1)
            skel_list.append(skel_name[1:])
            self.skelePath_list.append(file)
        for item in skel_list:
            self.skeleRig_dropdown.addItem(item)
        self.skeleRig_current = self.skelePath_list[self.skeleRig_dropdown.currentIndex()]

        ##### Alignment Confirmation #####
        self.alignment_checkbox = QCheckBox('Alignment Complete', self)

        ##### Pair to Locators #####
        self.charRig2Loc_button = QPushButton('Pair Character to Locators')
        self.charRig2Loc_button.setMinimumHeight(UI_ELEMENT_HEIGHT)

    def create_layout(self):
        main_layout = QVBoxLayout()
        vehicleTool_layout = QVBoxLayout()
        siteTool_layout = QVBoxLayout()
        vCrashTool_layout = QVBoxLayout()
        vehicleRigging_layout = QVBoxLayout()
        characterRigging_layout = QVBoxLayout()
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

        ##### Extra Tools GUI Section #####
        tools_group = QGroupBox("Extra Tools")
        tools_layout = QVBoxLayout()
        tools_layout.addWidget(self.autoScale_button)
        tools_layout.addWidget(self.remove_tires_button)
        tools_layout.addWidget(self.remove_license_plate_button)
        tools_layout.addWidget(self.make_windows_transparent_button)
        tools_group.setLayout(tools_layout)
        vehicleTool_layout.addWidget(tools_group)

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
        ######           VC Section             ######
        ##############################################

        ##### File Management #####
        files_group = QGroupBox("File Management")
        files_layout = QGridLayout()

        files_layout.addWidget(self.choose_vcData_button,0,0)
        files_layout.addWidget(self.choose_vcData_edit,0,1,1,4)
        files_layout.addWidget(self.convert_vcData_button,0,5,1,2)

        files_layout.addWidget(self.choose_mesh_button,1,0)
        files_layout.addWidget(self.choose_mesh_edit,1,1,1,4)
        files_layout.addWidget(self.loadMesh_button,1,5,1,2)

        files_layout.addWidget(self.choose_rig_button,2,0)
        files_layout.addWidget(self.choose_rig_edit,2,1,1,4)
        files_layout.addWidget(self.loadRig_button,2,5,1,2)

        files_layout.addWidget(self.choose_vLocator_button, 3, 0)
        files_layout.addWidget(self.choose_vLocator_edit, 3, 1, 1, 4)
        files_layout.addWidget(self.fps_label, 3, 5)
        files_layout.addWidget(self.fps_edit, 3, 6)
        files_layout.addWidget(self.create_vLocator_button, 4, 0, 1, 7)
        files_group.setLayout(files_layout)
        vCrashTool_layout.addWidget(files_group)

        ##############################################
        ######    Vehicle Rigging Section       ######
        ##############################################

        ##### Active Locator and Rig #####
        activeItems_group = QGroupBox("Active Locator and Rig")
        activeItems_Layout = QGridLayout()

        activeItems_Layout.addWidget(self.LocatorLabel,0,0)
        activeItems_Layout.addWidget(self.activeLocator_dropdown,0,1,1,2)
        activeItems_Layout.addWidget(self.RigLabel,1,0)
        activeItems_Layout.addWidget(self.activeRig_dropdown,1,1,1,2)

        activeItems_group.setLayout(activeItems_Layout)
        vehicleRigging_layout.addWidget(activeItems_group)

        ##### Vehicle Rigging #####
        vLocator_group = QGroupBox("Vehicle Rigging")
        vLocator_layout = QGridLayout()

        vLocator_layout.addWidget(self.pairRig2Locator_button,0,0,1,4)

        vLocator_layout.addWidget(self.parentX,1,0)
        vLocator_layout.addWidget(self.parentY,1,1)
        vLocator_layout.addWidget(self.parentZ,1,2)
        vLocator_layout.addWidget(self.rotateOnConst_button,1,3)

        vLocator_layout.addWidget(self.cgXOffset_edit,2,0)
        vLocator_layout.addWidget(self.cgYOffset_edit,2,1)
        vLocator_layout.addWidget(self.cgHeight_edit,2,2)
        vLocator_layout.addWidget(self.cgAdjust_button,2,3)

        vLocator_layout.addWidget(self.lightName_edit,3,0,1,2)
        vLocator_layout.addWidget(self.lightIntensity,3,2)
        vLocator_layout.addWidget(self.pairLight_button,3,3)

        vLocator_layout.addWidget(self.preBakeSave_button, 4,0,1,4)

        vLocator_layout.addWidget(self.siteName_edit, 5,0,1,2)
        vLocator_layout.addWidget(self.wheelConstr_button, 5,2,1,2)
        vLocator_group.setLayout(vLocator_layout)
        vehicleRigging_layout.addWidget(vLocator_group)

        ##### Blend Shapes #####
        blend_group = QGroupBox("Blend Shapes")
        blend_layout = QGridLayout()

        blend_layout.addWidget(self.blendNode_edit, 0,0)
        blend_layout.addWidget(self.blendGroupName_edit, 0,1)
        blend_layout.addWidget(self.createBlendGroup_button, 1,0,1,2)

        blend_group.setLayout(blend_layout)
        vehicleRigging_layout.addWidget(blend_group)

        ##### Bake Section #####
        bake_group = QGroupBox("Joint Bake")
        bake_layout = QGridLayout()

        bake_layout.addWidget(self.unrealExportSelection_button,0,0,1,2)
        bake_layout.addWidget(self.unrealExport_button,0,2,1,2)
        bake_layout.addWidget(self.bakeStart_label,1,0)
        bake_layout.addWidget(self.bakeStart_edit,1,1)
        bake_layout.addWidget(self.bakeStop_label,1,2)
        bake_layout.addWidget(self.bakeStop_edit,1,3)
        bake_layout.addWidget(self.bakeButton,2,0,1,4)
        bake_layout.addWidget(self.exportFBX_button,3,0,1,4)

        bake_group.setLayout(bake_layout)
        vehicleRigging_layout.addWidget(bake_group)

        ##############################################
        ######   Character Rigging Section      ######
        ##############################################

        ##### File Management #####
        joint_group = QGroupBox("File Management")
        joint_layout = QGridLayout()

        joint_layout.addWidget(self.chooseCharacterData_button, 0,0)
        joint_layout.addWidget(self.chooseCharacterData_edit, 0,1,1,3)
        joint_layout.addWidget(self.importCharacter_button, 1,0,1,4)
        joint_layout.addWidget(self.chooseSkeleRig_button, 2,0)
        joint_layout.addWidget(self.chooseSkeleRig_edit, 2,1,1,3)

        joint_layout.addWidget(self.loadCharacter_button, 4,0,1,4)
        joint_layout.addWidget(self.popUp_button, 5,0,1,4)

        joint_group.setLayout(joint_layout)
        characterRigging_layout.addWidget(joint_group)

        ##### Char Rigging #####
        charRig_group = QGroupBox("Character Rigging")
        charRig_layout = QGridLayout()

        charRig_layout.addWidget(self.charLoc_label, 0,0,1,1)
        charRig_layout.addWidget(self.activeCharLocs_dropdown, 0,1,1,3)

        charRig_layout.addWidget(self.activeChar_label, 1,0,1,1)
        charRig_layout.addWidget(self.activeCharacter_edit, 1,1,1,3)

        charRig_layout.addWidget(self.skeleRig_label, 2,0,1,1)
        charRig_layout.addWidget(self.skeleRig_dropdown, 2,1,1,3)

        charRig_layout.addWidget(self.alignment_checkbox, 3,0,1,1)
        charRig_layout.addWidget(self.charRig2Loc_button, 3,1,1,3)

        charRig_group.setLayout(charRig_layout)
        characterRigging_layout.addWidget(charRig_group)

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
        self.tab4.setLayout(vCrashTool_layout)
        self.tab5.setLayout(vehicleRigging_layout)
        self.tab6.setLayout(characterRigging_layout)
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
        self.autoScale_button.clicked.connect(self.autoScale)
        self.remove_tires_button.clicked.connect(self.remove_tires)
        self.remove_license_plate_button.clicked.connect(self.remove_license_plate)
        self.make_windows_transparent_button.clicked.connect(self.make_windows_transparent)
        ##### Save Group #####
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

        #--------------------------------------  VC Section  ------------------------------------------------#
        ##### File Management #####
        self.choose_rig_button.clicked.connect(self.choose_rig)
        self.loadRig_button.clicked.connect(self.load_rig)
        self.choose_mesh_button.clicked.connect(self.choose_mesh)
        self.loadMesh_button.clicked.connect(self.load_mesh)
        self.choose_vcData_button.clicked.connect(self.loadVCData)
        self.convert_vcData_button.clicked.connect(self.convertVCData)
        self.choose_vLocator_button.clicked.connect(self.loadvLocator)
        self.create_vLocator_button.clicked.connect(self.vehicleLocator)

        ##### Vehicle Rigging #####
        self.pairRig2Locator_button.clicked.connect(self.pairRig2Locator)
        self.rotateOnConst_button.clicked.connect(self.rotateOnConst)
        self.cgAdjust_button.clicked.connect(self.cgAdjustOffset)
        self.pairLight_button.clicked.connect(self.pairLight2Brakes)
        self.preBakeSave_button.clicked.connect(self.save)
        self.wheelConstr_button.clicked.connect(self.wheelConst)

        ##### Bake Joint #####
        self.bakeButton.clicked.connect(self.bake)
        self.exportFBX_button.clicked.connect(self.exportFBX)
        self.unrealExportSelection_button.clicked.connect(self.unrealExportSelection)
        self.unrealExport_button.clicked.connect(self.unrealExport)

        ##### Blend Shapes #####
        self.createBlendGroup_button.clicked.connect(self.createBlendGroup)

        ##### Charcater Import #####
        self.chooseCharacterData_button.clicked.connect(self.loadCharacterData)
        self.importCharacter_button.clicked.connect(self.charLocators)
        self.chooseSkeleRig_button.clicked.connect(self.loadCharRig)
        self.loadCharacter_button.clicked.connect(self.importCharRig)
        self.popUp_button.clicked.connect(self.popUp)

        ##### Character Rigging #####
        self.charRig2Loc_button.clicked.connect(self.charRig2Locs)
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

            cmds.file(vehiclespec_path, i=True)
            cmds.select(allDagObjects=True)
            new_all_objects = cmds.ls(selection=True)
            cmds.select(deselect=True)

            diff = [x for x in new_all_objects if x not in prev_all_objects]
            group = cmds.group(diff, name="Vehiclespecs")
            cmds.move(0,0,0,group,rpr=True)
            cmds.rotate(90,90,0)
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
        #Rotate in negative direction
        direction = self.xyz_selection.currentIndex()
        if direction == 0:
            cmds.select('Vehicle*')
            cmds.rotate(-90, 0, 0, relative=True, p=[0,0,0])
            cmds.select(deselect=True)
        if direction == 1:
            cmds.select('Vehicle*')
            cmds.rotate(0, -90, 0, relative=True, p=[0,0,0])
            cmds.select(deselect=True)
        if direction == 2:
            cmds.select('Vehicle*')
            cmds.rotate(0, 0, -90, relative=True, p=[0,0,0])
            cmds.select(deselect=True)

    def pos_rotation(self):
        #Rotate in positive direction
        direction = self.xyz_selection.currentIndex()
        if direction == 0:
            cmds.select('Vehicle*')
            cmds.rotate(90, 0, 0, relative=True, p=[0,0,0])
            cmds.select(deselect=True)
        if direction == 1:
            cmds.select('Vehicle*')
            cmds.rotate(0, 90, 0, relative=True, p=[0,0,0])
            cmds.select(deselect=True)
        if direction == 2:
            cmds.select('Vehicle*')
            cmds.rotate(0, 0, 90, relative=True, p=[0,0,0])
            cmds.select(deselect=True)

    def quick_rotate(self):
        #Rotates to a preset for Virtual Crash asset creation
        cmds.select('Vehicle*')
        cmds.rotate(90, 0, 90, a=True, p=[0,0,0])
        cmds.select(deselect=True)

    def hv_rotate(self):
        #Rotates for a preset for HV asset creation
        cmds.select('Vehicle*')
        cmds.rotate(-90, 0, -90, a=True, p=[0,0,0])
        cmds.select(deselect=True)

    def autoScale(self):
        #Scales vehicle to size of vehicle specs
        length = cmds.getAttr('curveShape4.maxValue')
        width = cmds.getAttr('curveShape1.maxValue')

        bumpers = cmds.ls('*bumper*', '*Bumper*','*Fender*','*fender*')
        bumper_group = cmds.group(bumpers)

        cmds.select(bumper_group)

        cmds.geomToBBox(n='tempBBox', single=True, keepOriginal=True)


        bbMinX = cmds.getAttr('tempBBox.boundingBoxMinX')
        bbMaxX = cmds.getAttr('tempBBox.boundingBoxMaxX')
        bbMinZ = cmds.getAttr('tempBBox.boundingBoxMinZ')
        bbMaxZ = cmds.getAttr('tempBBox.boundingBoxMaxZ')

        cmds.delete('tempBBox')

        bbLength = bbMaxZ - bbMinZ
        bbWidth = bbMaxX - bbMinX

        dxfArea = length*width

        bbArea = bbLength*bbWidth

        scaleZ = length/bbLength
        scaleX = width/bbWidth

        print('DXF Length x Width')
        print(f'{length} x {width}')
        print('Bounding Box Length x Width')
        print(f'{bbLength} x {bbWidth}')

        currentScale = cmds.getAttr('Vehicle.scale')
        vehicle = cmds.select('Vehicle')
        cmds.scale(scaleX*currentScale[0][0], 1*currentScale[0][1], scaleZ*currentScale[0][2], vehicle)

    def remove_tires(self):
        #removes tire objects
        cmds.select('Vehicle*', hierarchy=True)
        cmds.select('Vehicle*', deselect=True, hierarchy=False)
        items = cmds.ls(sl=True, g=True)
        cmds.select(deselect=True)
        coordinateList = []
        tireBB = []
        tires = []
        #Get Bounding Box Coordinates for each item
        for item in items:
            cmds.select(item)
            cmds.geomToBBox(n='tempBBox', single=True, keepOriginal=True)
            minY = cmds.getAttr('tempBBox.boundingBoxMinY')
            maxY = cmds.getAttr('tempBBox.boundingBoxMaxY')
            minX = cmds.getAttr('tempBBox.boundingBoxMinX')
            maxX = cmds.getAttr('tempBBox.boundingBoxMaxX')
            minZ = cmds.getAttr('tempBBox.boundingBoxMinZ')
            maxZ = cmds.getAttr('tempBBox.boundingBoxMaxZ')
            coords = (minX,maxX,minY,maxY,minZ,maxZ)
            coordinateList.append(coords)
            if -0.05 < minY and minY < 0.05:
                tireBB.append(coords)
                tires.append(item)
            cmds.delete('tempBBox')

        #See if BBox is inside tire, delete if True
        i = 0
        for coord in coordinateList:
            itemMinX = coord[0]
            itemMaxX = coord[1]
            itemMinY = coord[2]
            itemMaxY = coord[3]
            itemMinZ = coord[4]
            itemMaxZ = coord[5]
            for tire in tireBB:
                inY = False
                inX = False
                inZ = False
                tireMinX = tire[0]
                tireMaxX = tire[1]
                tireMinY = tire[2]
                tireMaxY = tire[3]
                tireMinZ = tire[4]
                tireMaxZ = tire[5]
                if itemMinX > tireMinX and itemMaxX < tireMaxX:
                    inX = True
                if itemMinY > tireMinY and itemMaxY < tireMaxY:
                    inY = True
                if itemMinZ > tireMinZ and itemMaxZ < tireMaxZ:
                    inZ = True
                if (inY and inX) or (inY and inZ) or (inX and inZ):
                    cmds.delete(items[i])
                    break
            i += 1
        for tire in tires:
            cmds.delete(tire)

    def choose_locator(self):
        # Set locator Path
        file_path = QFileDialog.getOpenFileName(None, "", self.desktop_dir, "Text Files (*.txt);;All Files (*.*)")[0]
        if file_path == "": # If they cancel the dialog
            return # Then just don't open anything
        self.choose_locator_edit.setText(file_path)

    def load_locator(self):
        #load xyz file
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
        #Make Load Bar appear
        progress_group = QGroupBox("Loading Bar")
        progressBox = QVBoxLayout()
        load_label = QLabel()
        self.progress = QProgressBar(self)

        progressBox.addWidget(load_label)
        progressBox.addWidget(self.progress)
        progress_group.setLayout(progressBox)
        self.pcTool_layout.addWidget(progress_group)

        #Does nothing but updates load bar
        load_label.setText('Reading File')
        load_value = 0
        for i in range(0,5):
            load_value += 1
            self.progress.setValue(load_value)
            progress_group.setVisible(True)

        #Load file and get data
        filename = self.choose_xyzfile_edit.text()
        intensity = self.choose_density_button.currentIndex()
        stepSize = intensity*intensity + 1

        try:
            assetMatch = re.search('/*([a-zA-Z0-9-_ ]*)\.xyz', filename)
            asset = assetMatch.group(1) + '_PointCloud'
            clouds = cmds.ls('*_PointCloud*')
            if asset in clouds:
                nameTaken=True
                i=1
                while nameTaken:
                    temp = asset+str(i)
                    if temp not in clouds:
                        asset = temp
                        nameTaken = False
                    else:
                        i += 1
        except:
            print("Couldn't retrieve asset name")
            asset = 'PointCloud'
            clouds = cmds.ls('*PointCloud*')
            if asset in clouds:
                nameTaken=True
                i=1
                while nameTaken:
                    temp = asset+str(i)
                    if temp not in clouds:
                        asset = temp
                        nameTaken = False
                    else:
                        i += 1


        f = open(filename, 'r')
        full = [line.rstrip().split(' ') for line in f.readlines()[::stepSize]]
        particleList, colorList = [(float(pos[0]), float(pos[1]), float(pos[2])) for pos in full], [(float(color[3])/255, float(color[4])/255, float(color[5])/255) for color in full]
        #xmin, ymin, zmin = min([float(x[0]) for x in particleList]), min([float(y[1]) for y in particleList]), min([float(z[2]) for z in particleList])
        f.close()

        #Disable Dynamics and create Point Cloud
        load_label.setText('Creating Point Cloud')
        load_value += 35
        self.progress.setValue(load_value)
        progress_group.setVisible(True)

        cmds.evaluator(n='dynamics', c='disablingNodes=dynamics')
        cmds.evaluator(n='dynamics', c='handledNodes=none')
        cmds.evaluator(n='dynamics', c='action=none')

        pointCloud, pointCloudShape = cmds.particle(n=asset)
        cmds.emit(object=pointCloud, pos=particleList)

        #Apply Colors
        load_label.setText('Applying Colors')
        load_value += 35
        self.progress.setValue(load_value)
        progress_group.setVisible(True)
        cmds.select(pointCloudShape)
        cmds.addAttr(ln='rgbPP', dt='vectorArray')

        cmds.setAttr(pointCloudShape+'.rgbPP', len(colorList), *colorList, type='vectorArray')
        cmds.setAttr(pointCloudShape+'.isDynamic', 0)
        cmds.setAttr(pointCloudShape+'.forcesInWorld',0)
        cmds.setAttr(pointCloudShape+'.emissionInWorld', 0)
        mel.eval('createRenderNodeCB -asUtility "" "particleSamplerInfo" ""')
        shader = cmds.shadingNode('lambert', asShader=True)
        cmds.connectAttr('particleSamplerInfo1.rgbPP', shader + '.color')
        cmds.connectAttr(shader + '.outColor','initialParticleSE.surfaceShader', f=True)

        load_value += 20
        self.progress.setValue(load_value)
        self.progress.setVisible(True)

        #rotate for Maya
        cmds.select(pointCloud)
        cmds.rotate(-90,0, 0, r=True, p=[0,0,0])
        cmds.select(deselect=True)
        load_value += 4
        self.progress.setValue(load_value)
        self.progress.setVisible(True)
        progress_group.setVisible(False)

    def auto_vc(self):
        #Do everything
        self.remove_tires()
        self.quick_rotate()
        self.auto_apply_spellbook()
        self.remove_license_plate()

    def export(self):
        cmds.select(all=True)
        cmds.file(self.desktop_dir + '\\' + self.asset + '_OBJ', type='OBJexport', es=True, sh=True, force=True)

    def exportFBX(self):
        #Exports root joint for Unreal Engine
        rigName = self.activeRig_dropdown.currentText()

        cmds.select(rigName, hierarchy=True)
        groupList = cmds.ls(sl=True)
        cmds.select(deselect=True)
        for item in groupList:
            if item.endswith('root_jt'):
                root = item

        colonIndex = 0
        for i in range(0,len(root)):
            if root[i] == ':':
                colonIndex = i + 1

        cmds.select(root)
        cmds.file(self.desktop_dir + '\\' + root[colonIndex:] + '_FBX', type='FBX export', es=True, pr=True, force=True)

    def cable_gui(self):
        #Opens GUI for easy cable creation
        if cmds.window("Cable Maker", exists =True):
            cmds.deleteUI("Cable Maker")
        cmds.workspaceControl("Cable Maker", retain=False, floating=True)
        createCustomWorkspaceControlCable()

    def choose_rig(self):
        # Set Rig Path
        file_path = QFileDialog.getOpenFileName(None, "", self.desktop_dir, "Maya Files (*.mb *.ma);;All Files (*.*)")[0]
        if file_path == "": # If they cancel the dialog
            return # Then just don't open anything
        self.choose_rig_edit.setText(file_path)

    def load_rig(self):
        filename = self.choose_rig_edit.text()
        cmds.file(filename, i=True)
        try:
            assetMatch = re.search('/*([a-zA-Z0-9-_ ]*)\.m[ab]', filename)
            asset = assetMatch.group(1)
        except:
            print("Couldn't retrieve asset name")
            asset = 'asset'
        dc = cmds.ls('*drive_ctrl', r=True)
        dc = cmds.rename(dc, asset + '_driveControl')
        rig = cmds.ls('*:*_TopNode')
        rigName = cmds.rename(rig, asset + '_TopNode')
        self.activeRig_dropdown.addItem(rigName)

    def choose_mesh(self):
        # Set Mesh Path
        file_path = QFileDialog.getOpenFileName(None, "", self.desktop_dir, "OBJ Files (*.obj, *.fbx);;All Files (*.*)")[0]
        if file_path == "": # If they cancel the dialog
            return # Then just don't open anything
        self.choose_mesh_edit.setText(file_path)

    def load_mesh(self):
        #Import mesh from set path
        filename = self.choose_mesh_edit.text()
        cmds.file(filename, i=True)

    def loadVCData(self):
        #Set path for VC data
        file_path = QFileDialog.getOpenFileName(None, "", self.desktop_dir, "CSV Files (*.csv);;All Files (*.*)")[0]
        if file_path == "":  # If they cancel the dialog
            return  # Then just don't open anything
        self.choose_vcData_edit.setText(file_path)

    def loadvLocator(self):
        #Load in MOV file
        file_path = QFileDialog.getOpenFileName(None, "", self.desktop_dir, "MOV Files (*.mov);;All Files (*.*)")[0]
        if file_path == "":  # If they cancel the dialog
            return  # Then just don't open anything
        self.choose_vLocator_edit.setText(file_path)

    def convertVCData(self):
        #Convert VC Data to individual MOV files
        #Get File Path
        filename = self.choose_vcData_edit.text()
        f = open(filename, "r")
        lines = f.readlines()
        f.close()

        #Clean CSV
        lines = [line.split(',') for line in lines]
        for i in range(0,len(lines)):
            lines[i] = [item.strip() for item in lines[i] if item != '' and item != '\n']

        #Get Vehicle List
        vehicles = []
        vehicleIndices = []
        for i in range(0,len(lines)-1):
            if 'time [ s]' in lines[i+1]:
                vehicles.append(lines[i][0])
                vehicleIndices.append(i)

        frameTotal = vehicleIndices[1] - vehicleIndices[0]

        #Create MOV Files
        for i in range(0,len(vehicles)):
            name = str(vehicles[i])
            f = open(self.desktop_dir + '/' + name + '.mov', 'w')
            for j in range(2, frameTotal):
                for k in range(0,len(lines[vehicleIndices[i] + j])):
                    f.write(lines[vehicleIndices[i] + j][k] + ' ')
                f.write('\n')

            f.close()

    def createBlendGroup(self):
        #Connect blend shape to root joint for Unreal export
        blendNode = self.blendNode_edit.text()
        groupName = self.blendGroupName_edit.text()
        rigName = self.activeRig_dropdown.currentText()

        cmds.select(rigName, hierarchy=True)
        groupList = cmds.ls(sl=True)
        cmds.select(deselect=True)
        for item in groupList:
            if item.endswith('root_jt'):
                rootJoint = item

        attrs = cmds.listAttr(blendNode, m=True)
        presets = ['message', 'caching', 'frozen', 'isHistoricallyInteresting', 'nodeState', 'binMembership', 'input', 'output', 'originalGeometry', 'envelopeWeightsList', 'envelope', 'function', 'fchild', 'map64BitIndices', 'topologyCheck', 'origin', 'baseOrigin', 'baseOriginX', 'baseOriginY', 'baseOriginZ', 'targetOrigin', 'targetOriginX', 'targetOriginY', 'targetOriginZ', 'parallelBlender', 'useTargetCompWeights', 'supportNegativeWeights', 'paintWeights', 'offsetDeformer', 'offsetX', 'offsetY', 'offsetZ', 'localVertexFrame', 'midLayerId', 'midLayerParent', 'nextNode', 'parentDirectory', 'targetDirectory', 'deformationOrder', 'attributeAliasList']

        cmds.select(rootJoint)
        cmds.addAttr(ln=groupName, dv=0, minValue=0, maxValue=1, k=True)

        for attr in attrs:
            is_preset = False
            for preset in presets:
                if preset in attr:
                    is_preset = True
            if not is_preset:
                shape = attr
                cmds.expression(s=f'{blendNode}.{shape} = {rootJoint}.{groupName}')

    def vehicleLocator(self):
        #Create vehicle locator with MOV data
        filename = self.choose_vLocator_edit.text()

        f = open(filename, 'r')
        lines = f.readlines()
        f.close()
        frameTotal = len(lines) - 1
        #Init Scene
        fps = self.fps_edit.currentText()
        cmds.playbackOptions(min='0sec', max=frameTotal)
        cmds.playbackOptions(ast='0sec')
        cmds.playbackOptions(aet=str(frameTotal/int(fps))+'sec')
        cmds.currentUnit(time=fps+'fps')
        cmds.currentTime(0)

        #Get Asset Name for Locator
        try:
            assetMatch = re.search('/*([a-zA-Z0-9-_ ]*)\.mov', filename)
            asset = assetMatch.group(1) + '_Locator'
        except:
            print("Couldn't retrieve asset name")
            asset = 'vehicleLocator'

        #Set up locator with vehicle attributes
        locator = cmds.spaceLocator(p=(0,0,0), n=asset)
        cmds.addAttr(ln='Time', at='float')
        cmds.setAttr(locator[0]+'.Time', k=True)
        cmds.addAttr(ln='Distance', at='float')
        cmds.setAttr(locator[0]+'.Distance', k=True)
        cmds.addAttr(ln='Velocity', at='float')
        cmds.setAttr(locator[0]+'.Velocity', k=True)
        cmds.addAttr(ln='Xrot', at='float')
        cmds.setAttr(locator[0]+'.Xrot', k=True)
        cmds.addAttr(ln='Yrot', at='float')
        cmds.setAttr(locator[0]+'.Yrot', k=True)
        cmds.addAttr(ln='Zrot', at='float')
        cmds.setAttr(locator[0]+'.Zrot', k=True)
        cmds.addAttr(ln='vni', at='float')
        cmds.setAttr(locator[0]+'.vni', k=True)
        cmds.addAttr(ln='vnz', at='float')
        cmds.setAttr(locator[0]+'.vnz', k=True)
        cmds.addAttr(ln='steer', at='float')
        cmds.setAttr(locator[0]+'.steer', k=True)
        cmds.addAttr(ln='CGx', at='float')
        cmds.setAttr(locator[0]+'.CGx', k=True)
        cmds.addAttr(ln='CGy', at='float')
        cmds.setAttr(locator[0]+'.CGy', k=True)
        cmds.addAttr(ln='CGz', at='float')
        cmds.setAttr(locator[0]+'.CGz', k=True)
        cmds.addAttr(ln='Xrad', at='float')
        cmds.setAttr(locator[0]+'.Xrad', k=True)
        cmds.addAttr(ln='Yrad', at='float')
        cmds.setAttr(locator[0]+'.Yrad', k=True)
        cmds.addAttr(ln='Zrad', at='float')
        cmds.setAttr(locator[0]+'.Zrad', k=True)
        cmds.addAttr(ln='lastV', at='float')
        cmds.setAttr(locator[0]+'.lastV', k=True)
        cmds.addAttr(ln='brake', at='float')
        cmds.setAttr(locator[0]+'.brake', k=True)

        #Connect Attr to expressions
        locName = locator[0]

        cmds.expression(s=locator[0]+".translateX="+locator[0]+".CGx", o=locator[0], ae=True, n='translateX')
        cmds.expression(s=locator[0]+".translateY="+locator[0]+".CGy", o=locator[0], ae=True, n='translateY')
        cmds.expression(s=locator[0]+".translateZ="+locator[0]+".CGz", o=locator[0], ae=True, n='translateZ')

        cmds.expression(s=locator[0]+".rotateX="+locator[0]+".Xrot", o=locator[0], ae=True, n='rotX', uc='angularOnly')
        cmds.expression(s=locator[0]+".rotateY="+locator[0]+".Yrot", o=locator[0], ae=True, n='rotY', uc='angularOnly')
        cmds.expression(s=locator[0]+".rotateZ="+locator[0]+".Zrot", o=locator[0], ae=True, n='rotZ', uc='angularOnly')

        cmds.expression(s=locator[0]+f""".lastV=`getAttr -time (frame-1)  {locName}.Velocity`;
        float $diff =  {locName}.Velocity-{locName}.lastV ;
        if ($diff < 0)""" +'{'+f'{locName}.brake=1;'+
        '}'+f'else {locName}.brake = 0;', o=locator[0], ae=True, n='brakeAndVel')

        #Load Attr from MOV file
        cmds.movIn(locName + '.Time', locName + '.Distance', locName + '.Velocity', locName + '.Xrot', locName + '.Yrot', locName + '.Zrot', locName + '.vni', locName + '.vnz', locName + '.steer', locName + '.CGx', locName + '.CGy', locName + '.CGz', locName + ".Xrad", locName + '.Yrad', locName + '.Zrad', locName + '.lastV', locName + '.brake', f=filename)

        #Add to group
        grp = cmds.group(locName, n=locName+'_group')
        cmds.rotate('-90deg',0,0,grp,pivot=(0,0,0))
        self.activeLocator_dropdown.addItem(locName)

    def pairRig2Locator(self):
        #Constrain rig to vehicle locator
        locName = self.activeLocator_dropdown.currentText()
        rigName = self.activeRig_dropdown.currentText()

        cmds.select(rigName, hierarchy=True)
        groupList = cmds.ls(sl=True)
        cmds.select(deselect=True)
        for item in groupList:
            if item.endswith('root_ctrl'):
                root = item
            if item.endswith('driveControl'):
                dc = item
        rootconst = cmds.parentConstraint(locName, root)

        cmds.delete(rootconst)
        cmds.select(root)
        cmds.rotate(0,0,0)
        cmds.select(deselect=True)
        constraint = cmds.parentConstraint(locName, dc)
        self.parentX.setText('90')
        self.parentY.setText('0')
        self.parentZ.setText('90')

        cmds.connectAttr(locName+'.steer',dc+'.steer')

        cmds.select(rigName, hierarchy=True)
        groupList = cmds.ls(sl=True)
        cmds.select(deselect=True)
        for item in groupList:
            if item.endswith('root_jt'):
                rootJoint = item

        cmds.select(rootJoint)
        cmds.addAttr(ln='brake', at='float', k=True)
        cmds.connectAttr(f'{locName}.brake',f'{rootJoint}.brake')
        cmds.select(deselect=True)

        self.rotateOnConst()

    def pairLight2Brakes(self):
        #Pair lights to MOV data
        rigName = self.activeRig_dropdown.currentText()
        locName = self.activeLocator_dropdown.currentText()

        cmds.select(rigName, hierarchy=True)
        groupList = cmds.ls(sl=True)
        cmds.select(deselect=True)
        for item in groupList:
            if item.endswith('root_jt'):
                root = item

        light = self.lightName_edit.text()
        intensity = self.lightIntensity.text()

        cmds.expression(s=f'{light}.intensity = {root}.brake * {intensity};')

    def rotateOnConst(self):
        #Rotate rig on parent constraint
        rigName = self.activeRig_dropdown.currentText()

        cmds.select(rigName, hierarchy=True)
        groupList = cmds.ls(sl=True)
        cmds.select(deselect=True)
        for item in groupList:
            if item.endswith('driveControl'):
                dc = item

        cmds.select(dc, hierarchy=True)
        groupList = cmds.ls(sl=True)
        cmds.select(deselect=True)
        for item in groupList:
            if 'parentConstraint' in item:
                const = item

        rotX = self.parentX.text()
        rotY = self.parentY.text()
        rotZ = self.parentZ.text()

        if rotX == '':
            rotX = 0
            self.parentX.setText('0')
        if rotY == '':
            rotY = 0
            self.parentY.setText('0')
        if rotZ == '':
            rotZ = 0
            self.parentZ.setText('0')

        rotX = float(rotX)
        rotY = float(rotY)
        rotZ = float(rotZ)

        if self.parentX.text() != '':
            cmds.setAttr(const + '.target[0].targetOffsetRotateX', rotX)
        if self.parentY.text() != '':
            cmds.setAttr(const + '.target[0].targetOffsetRotateY', rotY)
        if self.parentZ.text() != '':
            cmds.setAttr(const + '.target[0].targetOffsetRotateZ', rotZ)

    def cgAdjustOffset(self):
        #Adjust CoG offset
        rigName = self.activeRig_dropdown.currentText()

        cmds.select(rigName, hierarchy=True)
        groupList = cmds.ls(sl=True)
        cmds.select(deselect=True)
        for item in groupList:
            if item.endswith('driveControl'):
                dc = item

        cmds.select(dc, hierarchy=True)
        groupList = cmds.ls(sl=True)
        cmds.select(deselect=True)
        for item in groupList:
            if 'parentConstraint' in item:
                const = item

        xOffset = self.cgXOffset_edit.text()
        yOffset = self.cgYOffset_edit.text()
        height = self.cgHeight_edit.text()

        if xOffset == '':
            xOffset = 0
            self.cgXOffset_edit.setText('0')
        if yOffset == '':
            yOffset = 0
            self.cgYOffset_edit.setText('0')
        if height == '':
            height = 0
            self.cgHeight_edit.setText('0')

        xOffset = float(xOffset)
        yOffset = float(yOffset)
        height = float(height)

        cmds.setAttr(const + '.target[0].targetOffsetTranslateX', -xOffset)
        cmds.setAttr(const + '.target[0].targetOffsetTranslateY', -yOffset)
        cmds.setAttr(const + '.target[0].targetOffsetTranslateZ', -height)

    def wheelConst(self):
        #constrain wheels to mesh
        site = self.siteName_edit.text()

        mesh = cmds.ls(site, r=True)
        wheelCtrls = cmds.ls('*wheel_ctrl', r=True)

        for ctrl in wheelCtrls:
            cmds.geometryConstraint(mesh[0],ctrl)

    def bake(self):
        #Bake animation
        start = self.bakeStart_edit.text()
        stop = self.bakeStop_edit.text()
        rigName = self.activeRig_dropdown.currentText()

        cmds.select(rigName, hierarchy=True)
        groupList = cmds.ls(sl=True)
        cmds.select(deselect=True)
        for item in groupList:
            if item.endswith('root_jt'):
                root = item

        cmds.bakeResults(root, hi='below', shape=True, sm=True, time=(start,stop))

    def loadCharacterData(self):
        #Set path to character data
        file_path = QFileDialog.getOpenFileName(None, "", self.desktop_dir, "CSV Files (*.csv);;All Files (*.*)")[0]
        if file_path == "":  # If they cancel the dialog
            return  # Then just don't open anything
        self.chooseCharacterData_edit.setText(file_path)

    def loadCharRig(self):
        #Set path to character data
        file_path = QFileDialog.getOpenFileName(None, "", self.desktop_dir, "Char Files (*.ma *.mb);;All Files (*.*)")[0]
        if file_path == "":  # If they cancel the dialog
            return  # Then just don't open anything
        self.chooseSkeleRig_edit.setText(file_path)

    def importCharRig(self):
        filename = self.chooseSkeleRig_edit.text()

        #prevItems = cmds.ls()
        cmds.file(filename, i=True)
        #allItems = cmds.ls()
        #newItems = [item for item in allItems if item not in prevItems]
        #grp = cmds.group(newItems, n='Character_Group')
        #self.activeCharacter_edit.addItem(grp)

    def unrealExportSelection(self):
        #Exports root joint for Unreal Engine
        rigName = self.activeRig_dropdown.currentText()

        cmds.select(rigName, hierarchy=True)
        groupList = cmds.ls(sl=True)
        cmds.select(deselect=True)
        for item in groupList:
            if item.endswith('root_jt'):
                root = item

        cmds.select(rigName, hierarchy=True)
        groupList = cmds.ls(sl=True)
        cmds.select(deselect=True)
        for item in groupList:
            if item.endswith('_Render'):
                renderGroup = item

        cmds.select([renderGroup, root], hierarchy=True)
        renderGroupList = cmds.ls(sl=True)
        for item in renderGroupList:
            if item.endswith('_Chassis'):
                chassisGroup = item
            if item.endswith('_ParentYourMeshHere'):
                parentGroup = item

        cmds.select(root, deselect=True, hierarchy=True)
        cmds.select(renderGroup, deselect=True, hierarchy=False)
        cmds.select([chassisGroup,parentGroup], deselect=True, hierarchy=True)
        exportItems = cmds.ls(sl=True)
        cmds.parent(exportItems, world=True)
        cmds.parent(root, world=True)
        cmds.select(root, hierarchy=True)
        cmds.select(exportItems, add=True)

    def charLocators(self):
        #Load data from set character path
        filename = self.chooseCharacterData_edit.text()
        f = open(filename, "r")
        lines = f.readlines()
        f.close()

        #Clean CSV
        lines = [line.split(',') for line in lines]
        for i in range(0,len(lines)):
            lines[i] = [item.strip() for item in lines[i] if item != '' and item != '\n']

        #Get joint list
        parts = []
        partIndices = []
        partStrings = ['femur', 'foot', 'head', 'hip', 'arm', 'leg', 'neck', 'torso']
        for i in range(0,len(lines)):
            print(lines[i])
            for part in partStrings:
                if len(lines[i]) == 1:
                    if part in lines[i][0]:
                        parts.append(lines[i][0])
                        partIndices.append(i)

        frameTotal = partIndices[1] - partIndices[0]

        for i in range(0,len(parts)):
            print(parts[i])
            print(partIndices[i])

        #Create MOV Files
        jointFiles = []
        for i in range(0,len(parts)):
            name = str(parts[i])
            name = name.split(' ')
            new_name = ''
            for n in range(0,len(name)):
                new_name += name[n]
            name = new_name
            f = open(self.desktop_dir + '/' + name + '.mov', 'w')
            jointFiles.append(self.desktop_dir + '/' + name + '.mov')
            for j in range(2, frameTotal):
                for k in range(0,len(lines[partIndices[i] + j])):
                    f.write(lines[partIndices[i] + j][k] + ' ')
                f.write('\n')

        f.close()

        charList = cmds.ls('Character_Locators*')
        charNum = len(charList)

        locators = []
        colors = [(1,1,0),(1,1,0),(.2,1,.6),(.2,1,.6),(1,0,0),(1,.502,0),(1,.6,.6),(1,0,.498),(.502,1,0),(.502,1,0),(.498,0,1),(1,.6,.6),(1,0,.498),(0,0,1)]
        i = 0
        cmds.currentTime(0)

        for joint in jointFiles:
            locator = cmds.spaceLocator(p=(0,0,0), n=str(charNum)+parts[i])
            locName = locator[0]
            locators.append(locName)
            cmds.addAttr(ln='Time', at='float')
            cmds.setAttr(locator[0]+'.Time', k=True)
            cmds.addAttr(ln='Distance', at='float')
            cmds.setAttr(locator[0]+'.Distance', k=True)
            cmds.addAttr(ln='Velocity', at='float')
            cmds.setAttr(locator[0]+'.Velocity', k=True)
            cmds.addAttr(ln='Xrot', at='float')
            cmds.setAttr(locator[0]+'.Xrot', k=True)
            cmds.addAttr(ln='Yrot', at='float')
            cmds.setAttr(locator[0]+'.Yrot', k=True)
            cmds.addAttr(ln='Zrot', at='float')
            cmds.setAttr(locator[0]+'.Zrot', k=True)
            cmds.addAttr(ln='vni', at='float')
            cmds.setAttr(locator[0]+'.vni', k=True)
            cmds.addAttr(ln='vnz', at='float')
            cmds.setAttr(locator[0]+'.vnz', k=True)
            cmds.addAttr(ln='steer', at='float')
            cmds.setAttr(locator[0]+'.steer', k=True)
            cmds.addAttr(ln='CGx', at='float')
            cmds.setAttr(locator[0]+'.CGx', k=True)
            cmds.addAttr(ln='CGy', at='float')
            cmds.setAttr(locator[0]+'.CGy', k=True)
            cmds.addAttr(ln='CGz', at='float')
            cmds.setAttr(locator[0]+'.CGz', k=True)
            cmds.addAttr(ln='Xrad', at='float')
            cmds.setAttr(locator[0]+'.Xrad', k=True)
            cmds.addAttr(ln='Yrad', at='float')
            cmds.setAttr(locator[0]+'.Yrad', k=True)
            cmds.addAttr(ln='Zrad', at='float')
            cmds.setAttr(locator[0]+'.Zrad', k=True)
            cmds.addAttr(ln='lastV', at='float')
            cmds.setAttr(locator[0]+'.lastV', k=True)
            cmds.addAttr(ln='brake', at='float')
            cmds.setAttr(locator[0]+'.brake', k=True)

            cmds.movIn(locName + '.Time', locName + '.Distance', locName + '.Velocity', locName + '.rotateX', locName + '.rotateY', locName + '.rotateZ', locName + '.vni', locName + '.vnz', locName + '.translateX', locName + '.translateY', locName + '.translateZ', locName + ".Xrad", locName + '.Yrad', locName + '.Zrad', f=joint)
            cmds.setAttr(f'{locName}Shape.overrideEnabled', 1)
            cmds.setAttr(f'{locName}Shape.overrideRGBColors', 1)
            cmds.setAttr(f'{locName}Shape.overrideColorR',colors[i][0])
            cmds.setAttr(f'{locName}Shape.overrideColorG',colors[i][1])
            cmds.setAttr(f'{locName}Shape.overrideColorB',colors[i][2])
            cmds.setAttr(f'{locName}.scaleX', .2)
            cmds.setAttr(f'{locName}.scaleY', .2)
            cmds.setAttr(f'{locName}.scaleZ', .2)
            i += 1

        #Add to group
        grp = cmds.group(locators, n='Character_Locators')
        self.activeCharLocs_dropdown.addItem(grp)
        cmds.rotate('-90deg',0,0,grp,pivot=(0,0,0))

    def charRig2Locs(self):
        if self.alignment_checkbox.checkState():
            #Get Active Assets
            actLocs = self.activeCharLocs_dropdown.currentText()
            cmds.select(actLocs, hi=True)
            locs = cmds.ls(sl=True)
            locs = [x for x in locs if ('Character' not in x) and 'Shape' not in x]
            cmds.select(deselect=True)

            skelSelection = self.skeleRig_dropdown.currentText()
            for file in glob.glob(self.skeleton_dir + '/*'):
                if skelSelection in file:
                    f = open(file, 'r')
                    skelJoints = f.readlines()
                    f.close()

            for i in range(0,len(skelJoints)):
                skelJoints[i] = skelJoints[i].strip()

            actChar = self.activeCharacter_edit.text()
            cmds.select(actChar, hi=True)
            charItems = cmds.ls(sl=True)
            cmds.select(deselect=True)
            charJoints = []
            indexOrder = []
            for joint in charItems:
                for skel in skelJoints:
                    if joint.endswith(skel):
                        charJoints.append(joint)
                        indexOrder.append(skelJoints.index(skel))

            #Pair Elements
            for i in range(0,len(charJoints)):
                joint = charJoints[i]
                loc = locs[indexOrder[i]]
                const = cmds.parentConstraint(loc, joint, mo=True)
                #const = const[0]
                #cmds.setAttr(const + '.target[0].targetOffsetRotateX', 90)
                #cmds.setAttr(const + '.target[0].targetOffsetRotateY', 0)
                #cmds.setAttr(const + '.target[0].targetOffsetRotateZ', 90)
        else:
            warning_box = QMessageBox(QMessageBox.Warning, "Check Alignment", "Please confirm Joint and Locator alignment before pairing.")
            warning_box.exec_()

    def unrealExport(self):
        mel.eval('ExportSelection;')

    def popUp(self):
        dialog = skelePopUp(self)
        self.dialogs.append(dialog)
        dialog.show()

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
        cmds.delete('LicPlate*')

    def make_windows_transparent(self):
        selection = cmds.ls(selection=True)

        cmds.select(deselect=True)
        cmds.hyperShade(objects='*Window*')
        windows = cmds.ls(selection=True)
        cmds.select(deselect=True)

        for window in windows:
            cmds.setAttr(window + '.aiOpaque', False)

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


class skelePopUp(QDialog):
    # Set up file references
    ms_dir = os.path.expanduser("~/maya/scripts/magic-shade")
    skeleton_dir = ms_dir + '/skelFiles'
    icon_dir = os.path.expanduser("~/maya/scripts/magic-shade/resources/icons")
    spellbook_dir = os.path.expanduser("~/maya/scripts/magic-shade/spellbooks")
    studio_dir = os.path.expanduser("~/maya/scripts/magic-shade/studios")
    pref_path = os.path.expanduser("~/maya/scripts/magic-shade/prefs")
    save_path = os.path.expanduser("~/maya/projects/default/scenes/")
    user_profile = os.environ['USERPROFILE']
    desktop_dir = user_profile + '\\Desktop'

    #--------------------------------------------------------------------------------------------------------------
    #                                            Create GUI Window
    #--------------------------------------------------------------------------------------------------------------
    def __init__(self, parent=maya_main_window()):
        super(skelePopUp, self).__init__(parent)

        # Set up the window
        # self.setWindowFlags(Qt.Tool)
        self.setFixedWidth(600)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.resize(250, -1)
        self.setWindowTitle('SKEL File Creator')
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)

        self.create_controls()  # Initializes controls
        self.create_layout()  # Initializes the internal window layout
        self.make_connections()

    #--------------------------------------------------------------------------------------------------------------
    #                                             Create Widgets
    #--------------------------------------------------------------------------------------------------------------
    def create_controls(self):
        UI_ELEMENT_HEIGHT = 30
        ##### ADV Options #####
        self.advOption_checkbox = QCheckBox('Advanced Options')
        ##### New File Name Line #####
        self.newFileName = QLineEdit()
        self.newFileName.setPlaceholderText('Rig Name')
        self.newFileName.setMinimumHeight(UI_ELEMENT_HEIGHT)
        ##### Joint Labels and Edits #####
        self.headLabel = QLabel()
        self.headLabel.setText('Head Joint: ')
        self.head_edit = QLineEdit()
        self.head_edit.setMinimumHeight(UI_ELEMENT_HEIGHT)
        self.neckLabel = QLabel()
        self.neckLabel.setText('Neck Joint: ')
        self.neck_edit = QLineEdit()
        self.neck_edit.setMinimumHeight(UI_ELEMENT_HEIGHT)
        self.torsoJointLabel = QLabel()
        self.torsoJointLabel.setText('Torso Joint: ')
        self.torsoJoint_edit = QLineEdit()
        self.torsoJoint_edit.setMinimumHeight(UI_ELEMENT_HEIGHT)
        self.rightUpperArmLabel = QLabel()
        self.rightUpperArmLabel.setText('Right Upper Arm Joint: ')
        self.rightUpperArm_edit = QLineEdit()
        self.rightUpperArm_edit.setMinimumHeight(UI_ELEMENT_HEIGHT)
        self.rightLowerArmLabel = QLabel()
        self.rightLowerArmLabel.setText('Right Lower Arm Joint: ')
        self.rightLowerArm_edit = QLineEdit()
        self.rightLowerArm_edit.setMinimumHeight(UI_ELEMENT_HEIGHT)
        self.leftUpperArmLabel = QLabel()
        self.leftUpperArmLabel.setText('Left Upper Arm Joint: ')
        self.leftUpperArm_edit = QLineEdit()
        self.leftUpperArm_edit.setMinimumHeight(UI_ELEMENT_HEIGHT)
        self.leftLowerArmLabel = QLabel()
        self.leftLowerArmLabel.setText('Left Lower Arm Joint: ')
        self.leftLowerArm_edit = QLineEdit()
        self.leftLowerArm_edit.setMinimumHeight(UI_ELEMENT_HEIGHT)
        self.hipLabel = QLabel()
        self.hipLabel.setText('Hip Joint: ')
        self.hip_edit = QLineEdit()
        self.hip_edit.setMinimumHeight(UI_ELEMENT_HEIGHT)
        self.rightFemurLabel = QLabel()
        self.rightFemurLabel.setText('Right Femur Joint: ')
        self.rightFemur_edit = QLineEdit()
        self.rightFemur_edit.setMinimumHeight(UI_ELEMENT_HEIGHT)
        self.rightLowerLegLabel = QLabel()
        self.rightLowerLegLabel.setText('Right Lower Leg Joint: ')
        self.rightLowerLeg_edit = QLineEdit()
        self.rightLowerLeg_edit.setMinimumHeight(UI_ELEMENT_HEIGHT)
        self.rightFootLabel = QLabel()
        self.rightFootLabel.setText('Right Foot Joint: ')
        self.rightFoot_edit = QLineEdit()
        self.rightFoot_edit.setMinimumHeight(UI_ELEMENT_HEIGHT)
        self.LeftFemurLabel = QLabel()
        self.LeftFemurLabel.setText('Left Femur Joint: ')
        self.LeftFemur_edit = QLineEdit()
        self.LeftFemur_edit.setMinimumHeight(UI_ELEMENT_HEIGHT)
        self.leftLowerLegLabel = QLabel()
        self.leftLowerLegLabel.setText('Left Lower Leg Joint: ')
        self.leftLowerLeg_edit = QLineEdit()
        self.leftLowerLeg_edit.setMinimumHeight(UI_ELEMENT_HEIGHT)
        self.leftFootLabel = QLabel()
        self.leftFootLabel.setText('Left Foot Joint: ')
        self.leftFoot_edit = QLineEdit()
        self.leftFoot_edit.setMinimumHeight(UI_ELEMENT_HEIGHT)

        self.all_edits = [self.LeftFemur_edit, self.rightFemur_edit, self.leftFoot_edit, self.rightFoot_edit,
        self.head_edit, self.hip_edit, self.leftLowerArm_edit, self.leftUpperArm_edit, self.leftLowerLeg_edit,
        self.rightLowerLeg_edit, self.neck_edit,  self.rightLowerArm_edit, self.rightUpperArm_edit, self.torsoJoint_edit, self.newFileName]

        ##### Create SKEL File #####
        self.createSkel_button = QPushButton('Create SKEL File')

    #--------------------------------------------------------------------------------------------------------------
    #                                              Make Layout
    #--------------------------------------------------------------------------------------------------------------
    def create_layout(self, layout='simple'):
        layout1 = QVBoxLayout()

        simple_group = QGroupBox()
        simpleLayout = QGridLayout()

        #simpleLayout.addWidget(self.advOption_checkbox, 0,0)
        simpleLayout.addWidget(self.headLabel, 1,0)
        simpleLayout.addWidget(self.head_edit, 1,1,1,3)
        simpleLayout.addWidget(self.neckLabel, 2,0)
        simpleLayout.addWidget(self.neck_edit, 2,1,1,3)
        simpleLayout.addWidget(self.torsoJointLabel, 3,0)
        simpleLayout.addWidget(self.torsoJoint_edit, 3,1,1,3)
        simpleLayout.addWidget(self.rightUpperArmLabel, 4,0)
        simpleLayout.addWidget(self.rightUpperArm_edit, 4,1,1,3)
        simpleLayout.addWidget(self.rightLowerArmLabel, 5,0)
        simpleLayout.addWidget(self.rightLowerArm_edit, 5,1,1,3)
        simpleLayout.addWidget(self.leftUpperArmLabel, 6,0)
        simpleLayout.addWidget(self.leftUpperArm_edit, 6,1,1,3)
        simpleLayout.addWidget(self.leftLowerArmLabel, 7,0)
        simpleLayout.addWidget(self.leftLowerArm_edit, 7,1,1,3)
        simpleLayout.addWidget(self.hipLabel, 8,0)
        simpleLayout.addWidget(self.hip_edit, 8,1,1,3)
        simpleLayout.addWidget(self.rightFemurLabel, 9,0)
        simpleLayout.addWidget(self.rightFemur_edit, 9,1,1,3)
        simpleLayout.addWidget(self.rightLowerLegLabel, 10,0)
        simpleLayout.addWidget(self.rightLowerLeg_edit, 10,1,1,3)
        simpleLayout.addWidget(self.rightFootLabel, 11,0)
        simpleLayout.addWidget(self.rightFoot_edit, 11,1,1,3)
        simpleLayout.addWidget(self.LeftFemurLabel, 12,0)
        simpleLayout.addWidget(self.LeftFemur_edit, 12,1,1,3)
        simpleLayout.addWidget(self.leftLowerLegLabel, 13,0)
        simpleLayout.addWidget(self.leftLowerLeg_edit, 13,1,1,3)
        simpleLayout.addWidget(self.leftFootLabel, 14,0)
        simpleLayout.addWidget(self.leftFoot_edit, 14,1,1,3)
        simpleLayout.addWidget(self.newFileName, 15,0,1,2)
        simpleLayout.addWidget(self.createSkel_button, 15,2,1,2)


        simple_group.setLayout(simpleLayout)
        layout1.addWidget(simple_group)
        self.setLayout(layout1)

    #--------------------------------------------------------------------------------------------------------------
    #                                             Make Connections
    #--------------------------------------------------------------------------------------------------------------
    def make_connections(self):
        self.createSkel_button.clicked.connect(self.createFile)
        #self.advOption_checkbox.stateChanged.connect(self.setOptions)

    #--------------------------------------------------------------------------------------------------------------
    #                                                 Functions
    #--------------------------------------------------------------------------------------------------------------
    def createFile(self):
        #Get Variables
        joints = [self.LeftFemur_edit.text(), self.rightFemur_edit.text(), self.leftFoot_edit.text(), self.rightFoot_edit.text(),
        self.head_edit.text(), self.hip_edit.text(), self.leftLowerArm_edit.text(), self.leftUpperArm_edit.text(), self.leftLowerLeg_edit.text(),
        self.rightLowerLeg_edit.text(), self.neck_edit.text(),  self.rightLowerArm_edit.text(), self.rightUpperArm_edit.text(), self.torsoJoint_edit.text()]

        newFile = f'{self.skeleton_dir}/{self.newFileName.text()}'

        #Create File
        f = open(f'{newFile}.SKEL', 'w')
        for joint in joints:
            f.write(f'{joint}\n')
        f.close()

        for edit in self.all_edits:
            edit.setText('')

# Dev code to automatically close old windows when running
try:
    ui.close()
except:
    pass

# Show a new instance of the UI
ui = MainUI()
ui.show()
