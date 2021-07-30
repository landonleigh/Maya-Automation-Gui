import maya.cmds as mc
import maya.cmds as cmds
import maya.mel as mel
import os, sys

#____________________________________________________________________________________________INIT
#_________________SUPP ERROR MESSAGE

#mc.warning()
#print('', end=' ')

if mc.window("Cable Maker", exists =True):
    mc.deleteUI("Cable Maker")

if mc.workspaceControl("Cable Maker", exists =True):
    mc.deleteUI("Cable Maker")

# SET correct brush -------------------------------------------------------------------------
version = mc.about(v=True)
# command to get Maya version you are now running
OS = mc.about(os=True)

str1 = os.getcwd()


#if OS == 'win64':
#    mel.eval('string $maya = `getenv maya_location`;')
#    mel.eval('$s="/Examples/Paint_Effects/Trees/birchLimb.mel";')
#    total = mel.eval('$total= $maya+$s;')
#    mel.eval('visorPanelBrushPressCallback files1VisorEd $total;')
#    mel.eval('setToolTo $gMove;')

#if OS == 'mac':
  #  mel.eval('string $maya = `getenv maya_location`;')
   # mel.eval('$s="/Examples/Paint_Effects/Trees/birchLimb.mel";')
  #  total = mel.eval('$total= $maya+$s;')
  #  mel.eval('visorPanelBrushPressCallback files1VisorEd $total;')
   # mel.eval('setToolTo $gMove;')

#elif OS == 'mac':
 #   if version == '2018':
 #       mel.eval('visorPanelBrushPressCallback files1VisorEd "/Applications/Autodesk/maya2018/Maya.app/Contents/Examples/Paint_Effects/Trees/birchLimb.mel";')
  #      mel.eval('setToolTo $gMove;')



#elif OS == 'linux64':
#        print ("For Linux User you should Config your Path directly onto the Script. If your not at ease with Maya Scripting just ask me on the Discord")





# SET default setting for the tube --------------------------------------------------------------

#mc.setAttr("birchLimb.globalScale", 10)
#mc.setAttr("birchLimb.brushWidth", 0.1)
#mc.setAttr("birchLimb.forwardTwist", 0)
#mc.setAttr(("birchLimb.color1"), 0, 0.149078, 0.228, type='double3')
#mc.setAttr(("birchLimb.specularColor"), 0, 0, 0, type='double3')
#mc.setAttr(("birchLimb.tubeSections"), 8)

#___________________________________________________________________________________________________________
#___________________________________________________________________________________________________________________________________________UI
#___________________________________________________________________________________________________________

def createCustomWorkspaceControlCable(*args):
    mc.columnLayout(adj = True, w=300, h=415)


    #_________________________________________________________________________________________________________________CREATE

    cH1 = mc.columnLayout(adj =True)
    frameCreate = mc.frameLayout(l = "CREATE", cll =1, cl =0, bgc= [0.15, 0.15, 0.15], font= 'boldLabelFont' )


    mc.rowColumnLayout ( numberOfRows = 1 )
    mc.separator (w = 18, style = 'none')
    toolCV = mc.symbolButton( image='curveEP.png', c= mc.EPCurveTool, ann= "EP Curve")
    mc.separator (w = 40, style = 'none')
    toolBezier = mc.symbolButton( image='curveBezier.png', c= mc.CreateBezierCurveTool, ann= "Bezier Curve")
    mc.separator (w = 40, style = 'none')
    toolPen = mc.symbolButton( image='pencil.png', c= mc.PencilCurveTool, ann= "Pencil Curve")
    mc.separator (w = 40, style = 'none')
    toolEdge = mc.symbolButton( image='polyEdgeToCurves.png', c= "edgeC()" , ann= "Create Curve from Edge")
    mc.separator (w = 40, style = 'none')
    mc.setParent( '..' )


    mc.rowColumnLayout ( numberOfRows = 1 )
    mc.separator (w = 2, style = 'none')
    buttonCreate = mc.button('buttonCreate', w= 290, l= " - CREATE Cables - ", c= "Attach_Cable()", ann= "Create cables", bgc= [0.22, 0.22, 0.22])
    mc.setParent( '..' )



    #_________________________________________________________________________________________________________________EDIT

    mc.setParent(cH1)
    cH2 = mc.columnLayout(adj =True)

    frameEdit = mc.frameLayout(l = "EDIT", cll =1, cl =0, bgc= [0.15, 0.15, 0.15])



    mc.separator(h= 1, style = 'none')
    reference = mc.checkBoxGrp('Check_Manip', l= "Manipulation", onc="Manip_on()", ofc="Manip_off()",adj =0, cat= [1, "left", 1], cw= [1, 80], v1= 0, ann= "Easier to manipulate curves")
    mc.separator (w = 1, style = 'in')
    slideScale = mc.floatSliderGrp('Slider_Scale', l = "Scale",min =0.1, max =100,po =True, field =True, cc="Scale_Val()", dc="Scale_Val()", v= 1, adj =0, cat= [1, "left", 3], cw= [1, 60], ann= "Configure to scene set in cm")
    slideWidth = mc.floatSliderGrp('Slider_Width', l = "Width",min =0.001, max =2,po =True, field =True, cc="Width_Val()", dc="Width_Val()", v= 0.1, pre= 3, adj =0, cat= [1, "left", 3], cw= [1, 60])
    slideDensity = mc.floatSliderGrp('Slider_Density', l = "Density",min =0.1, max =10,po =True, field =True, cc="Density_Val()", dc="Density_Val()", v= 1, adj =0, cat= [1, "left", 3], cw= [1, 60])
    slideSection = mc.intSliderGrp('Slider_Section', l = "Section",min =3, max =12,po =True, field =True, cc="Section_Val()", dc="Section_Val()", adj =0, cat= [1, "left", 3], cw= [1, 60])
    slideSmoothing = mc.floatSliderGrp('Slider_Smoothing', l = "Smoothing",min =0, max =100,po =True, field =True, cc="Smoothing_Val()", dc="Smoothing_Val()", v= 0, adj =0, cat= [1, "left", 3], cw= [1, 60])

    cH2b = mc.columnLayout(adj =True)
    frameEdit = mc.frameLayout(l = "Advance Parameters", cll =1, cl =1, bgc= [0.15, 0.15, 0.15])
    mc.separator(h= 1, style = 'none')
    checkboxLearn = mc.checkBox('Check_Twist', l= "Twist", onc="twist_on()", ofc="twist_off()")
    slideTwist = mc.floatSliderGrp('Slider_Twist', l = "Twist Rate",min =0, max =300,po =True, field =True, cc="Twist_Val()", dc="Twist_Val()", v= 0, adj =0, cat= [1, "left", 3], cw= [1, 60])
    mc.separator (w = 1, style = 'in')
    slideFlat = mc.floatSliderGrp('Slider_Flat', l = "Flatness",min =0, max =1,po =True, field =True, cc="Flat_Val()", dc="Flat_Val()", pre= 3, v= 0, adj =0, cat= [1, "left", 3], cw= [1, 60])
    mc.separator (w = 1, style = 'in')
    slidePstart = mc.floatSliderGrp('Slider_Pstart', l = "Pressure A",min =0, max =1,po =True, field =True, cc="Pstart_Val()", dc="Pstart_Val()", pre= 3, v= 1, adj =0, cat= [1, "left", 3], cw= [1, 60])
    slidePend = mc.floatSliderGrp('Slider_Pend', l = "Pressure B",min =0, max =1,po =True, field =True, cc="Pend_Val()", dc="Pend_Val()", pre= 3, v= 1, adj =0, cat= [1, "left", 3], cw= [1, 60])
    mc.separator(h= 1, style = 'none')

    mc.setParent(cH2)


    #_________________________________________________________________________________________________________________DYNAMIQUE
    cH4 = mc.columnLayout(adj =True)
    frameConvert = mc.frameLayout(l = "DYNAMICS", cll =1, cl =1, bgc= [0.15, 0.15, 0.15])
    slideRebuild = mc.intSliderGrp('Slider_Rebuild', l = "Rebuild Span",min =1, max =100,po =True, field =True, cc="Rebuild_Val()", dc="Rebuild_Val()", v= 25, adj =0, cat= [1, "left", 3], cw= [1, 80])
    buttonDyn = mc.button('buttonDyn', w= 290, l= " - Make Dynamique - ", c= "Dyn()", ann= "Create Dynamique on Cable", bgc= [0.22, 0.22, 0.22])
    buttonCollide = mc.button('buttonCollide', w= 290, l= " - Make Collide - ", c= "Collide()", ann= "Make Mesh Collider", bgc= [0.22, 0.22, 0.22])

    mc.separator (w = 1, style = 'in')
    mc.text(" - Properties (Affect All) - ")


    cH5 = mc.rowColumnLayout( numberOfColumns=2, columnWidth=[(1, 100), (2, 250)] )
    checkBoxOffset = mc.checkBoxGrp('CB_Offset', l = "Offset Preview", onc="offset_on()", ofc="offset_off()",adj =0, cat= [1, "left", 3], cw= [1, 80])
    slideOffset = mc.floatSliderGrp('Slider_Offset', min =0, max =10,po =True, field =True, cc="Offset()", dc="Offset()", v= 1, adj =0, cat= [1, "left", 3], cw= [1, 80], ann= "Control the radius of collider")
    mc.setParent( '..' )

    cH6 = mc.columnLayout(adj =True)
    slideFriction = mc.floatSliderGrp('Slider_Friction', l = "Friction",min =0, max =1,po =True, field =True, cc="Friction()", dc="Friction()", v= 0.5, adj =0, cat= [1, "left", 3], cw= [1, 80], ann= "Friction Parameter")
    slideStretch = mc.floatSliderGrp('Slider_Stretch', l = "Stretch",min =0, max =100,po =True, field =True, cc="Stretch()", dc="Stretch()", v= 10, adj =0, cat= [1, "left", 3], cw= [1, 80], ann= "Stretch Parameter")
    slideStartCurve = mc.floatSliderGrp('Slider_StartCurve', l = "Start Curve",min =0, max =1,po =True, field =True, cc="StartCurve()", dc="StartCurve()", v= 0, adj =0, cat= [1, "left", 3], cw= [1, 80], ann= "Start Curve Parameter")
    slideMotionDrag = mc.floatSliderGrp('Slider_MotionDrag', l = "Motion Drag",min =0, max =1,po =True, field =True, cc="MotionDrag()", dc="MotionDrag()", v= 0, adj =0, cat= [1, "left", 3], cw= [1, 80], ann= "Motion Drag Parameter")


    mc.separator (w = 1, style = 'in')
    mc.setParent( '..' )
    cH6 = mc.rowColumnLayout( numberOfColumns=4, columnWidth=[(1, 70), (2, 70), (3, 70), (4, 70)] )
    buttonPlNo = mc.button('buttonPlNo', w= 70, l= "No Attach", c= "PlNo()", ann= "Point Lock No Attach", bgc= [0.22, 0.22, 0.22])
    buttonPlBase = mc.button('buttonPlBase', w= 70, l= "Base", c= "PlBase()", ann= "Point Lock Base", bgc= [0.22, 0.22, 0.22])
    buttonPlTip = mc.button('buttonPlTip', w= 70, l= "Tip", c= "PlTip()", ann= "Point Lock Tip", bgc= [0.22, 0.22, 0.22])
    buttonPlBoth = mc.button('buttonPlBoth', w= 70, l= "Both", c= "PlBoth()", ann= "Point Lock Both", bgc= [0.22, 0.22, 0.22])
    mc.setParent( '..' )
    cH7 = mc.columnLayout(adj =True)
    #slideFollicleSample = mc.floatSliderGrp('Slider_FSample', l = "Sample Density",min =0, max =3,po =True, field =True, cc="FSample()", dc="FSample()", v= 1, adj =0, cat= [1, "left", 3], cw= [1, 80], ann= "Sample Density of Dyn Curve")
    mc.setParent( '..' )

    mc.setParent(cH4)

    #_________________________________________________________________________________________________________________CONVERT

    cH3 = mc.columnLayout(adj =True)
    frameConvert = mc.frameLayout(l = "CONVERT", cll =1, cl =1, bgc= [0.15, 0.15, 0.15])

    mc.rowColumnLayout ( numberOfRows = 1 )
    buttonBakeHistory = mc.button('buttonBakeHistory', w=95, l= "Bake + History", c= "B_History()", ann= "Convert to Mesh and keep history to manipulate with Curve", bgc= [0.22, 0.22, 0.22])
    mc.separator (w = 4, style = 'none')
    buttonBake = mc.button('buttonBake', w=95, l= "BAKE", c= "B_Bake()", ann= "Convert to Mesh, delete history and remove extra node", bgc= [0.22, 0.22, 0.22])
    mc.separator (w = 4, style = 'none')
    buttonBakeCurve = mc.button('buttonBakeCurve', w=95, l= "Bake + Curve", c= "B_BakeC()", ann= "Convert to Mesh, delete history but keep the original curve", bgc= [0.22, 0.22, 0.22])
    mc.setParent( '..' )

    mc.rowColumnLayout ( numberOfRows = 1 )
    buttonCleanDyn = mc.button('buttonCleanDyn', w=290, l= "Clean Dynamique Nodes", c= "B_Dyn()", ann= "Be sure to Bake your Cables first", bgc= [0.22, 0.22, 0.22])
    mc.setParent( '..' )

    buttonBackToC = mc.button('buttonBackToCurve', w=290, l= "Back to Curve", c= "B_BtoC()", ann= "Rebuild curve based on Geo", bgc= [0.22, 0.22, 0.22])

    mc.setParent(cH3)
    mc.setParent( '..' )




#mc.workspaceControl("Cable Maker", retain=False, floating=True, uiScript="createCustomWorkspaceControlCable()");




def UpdateInfo():
    selection = mc.ls(sl = True, fl = True, dag = True, type= 'stroke')
    nbrItem = len(selection)

    if nbrItem == 1:
        ScaleValue = GetScale_Val()
        WidthValue = GetWidth_Val()
        DensityValue = GetDensity_Val()
        SmoothValue = GetSmoothing_Val()
        TwistValue = GetTwist_Val()
        GSectionValue = GetSection_Val()
        TwistOnValue = GetTwistOn_Val()
        FlatValue = GetFlat_Val()
        PstartValue = GetPstart_Val()
        PendValue = GetPend_Val()

        mc.floatSliderGrp( "Slider_Scale",e=True, value = ScaleValue)
        mc.floatSliderGrp( "Slider_Width",e=True, value = WidthValue)
        mc.floatSliderGrp( "Slider_Density",e=True, value = DensityValue)
        mc.floatSliderGrp( "Slider_Smoothing",e=True, value = SmoothValue)
        mc.floatSliderGrp( "Slider_Twist",e=True, value = TwistValue)
        mc.intSliderGrp( "Slider_Section",e=True, value = GSectionValue)
        mc.checkBox( "Check_Twist",e=True, value = TwistOnValue)
        mc.floatSliderGrp( "Slider_Flat",e=True, value = FlatValue)
        mc.floatSliderGrp( "Slider_Pstart",e=True, value = PstartValue)
        mc.floatSliderGrp( "Slider_Pend",e=True, value = PendValue)

    else:
        return



mc.scriptJob( runOnce=False, e = ["SelectionChanged", UpdateInfo])


###____________________________________________________________________________
###____________________________________________________________________________________________________________CREATE
###____________________________________________________________________________


def Attach_Cable():
    import maya.mel as mel
    mel.eval('AttachBrushToCurves')
    mel.eval('convertCurvesToStrokes')
    mel.eval('setToolTo $gMove;')

def edgeC():
    mc.polyToCurve(form= 3, degree= 1, conformToSmoothMeshPreview= 1)

#PRESET__________________
PresetFile_01 = mc.internalVar(upd = True)+"scripts/Cable_script/Presets/CurvePreset_01.ma"
PresetFile_02 = mc.internalVar(upd = True)+"scripts/Cable_script/Presets/CurvePreset_02.ma"
PresetFile_03 = mc.internalVar(upd = True)+"scripts/Cable_script/Presets/CurvePreset_03.ma"
PresetFile_04 = mc.internalVar(upd = True)+"scripts/Cable_script/Presets/CurvePreset_04.ma"
PresetFile_05 = mc.internalVar(upd = True)+"scripts/Cable_script/Presets/CurvePreset_05.ma"
PresetFile_06 = mc.internalVar(upd = True)+"scripts/Cable_script/Presets/CurvePreset_06.ma"

def Preset01():
    mc.file(PresetFile_01, i = True)

def Preset02():
    mc.file(PresetFile_02, i = True)

def Preset03():
    mc.file(PresetFile_03, i = True)

def Preset04():
    mc.file(PresetFile_04, i = True)

def Preset05():
    mc.file(PresetFile_05, i = True)

def Preset06():
    mc.file(PresetFile_06, i = True)

###____________________________________________________________________________
###____________________________________________________________________________________________________________EDIT
###____________________________________________________________________________


##___________________________________________________PaintEffectControl
#SCALE__________________
def GetScale_Val():
    selection = mc.ls(sl = True, fl = True, dag = True, type= 'stroke')
    brush = mc.listConnections(selection, d = True, scn=True, type= 'brush')

    getValue = mc.getAttr(brush[0] + ".globalScale")
    return getValue



def Scale_Val():

    myValueWidght = mc.floatSliderGrp("Slider_Scale", q= True, value=True)

    selection = mc.ls(sl = True, fl = True, dag = True, type= 'stroke')

    buffer = mc.listConnections(selection, d = True, scn=True, type= 'brush')

    for each in buffer:
        mc.setAttr(each + ".globalScale", myValueWidght)

#WIDTH__________________
def GetWidth_Val():
    selection = mc.ls(sl = True, fl = True, dag = True, type= 'stroke')
    brush = mc.listConnections(selection, d = True, scn=True, type= 'brush')

    getValue = mc.getAttr(brush[0] + ".brushWidth")
    return getValue


def Width_Val():

    myValueWidght = mc.floatSliderGrp("Slider_Width", q= True, value=True)

    selection = mc.ls(sl = True, fl = True, dag = True, type= 'stroke')

    buffer = mc.listConnections(selection, d = True, scn=True, type= 'brush')

    for each in buffer:
        mc.setAttr(each + ".brushWidth", myValueWidght)

#SECTION__________________
def GetSection_Val():
    selection = mc.ls(sl = True, fl = True, dag = True, type= 'stroke')
    brush = mc.listConnections(selection, d = True, scn=True, type= 'brush')

    getValue = mc.getAttr(brush[0] + ".tubeSections")
    return getValue


def Section_Val():

    myValueWidght = mc.intSliderGrp("Slider_Section", q= True, value=True)

    selection = mc.ls(sl = True, fl = True, dag = True, type= 'stroke')

    buffer = mc.listConnections(selection, d = True, scn=True, type= 'brush')

    for each in buffer:
        mc.setAttr(each + ".tubeSections", myValueWidght)


#TWIST__________________
def GetTwistOn_Val():
    selection = mc.ls(sl = True, fl = True, dag = True, type= 'stroke')
    brush = mc.listConnections(selection, d = True, scn=True, type= 'brush')

    getValue = mc.getAttr(brush[0] + ".forwardTwist")
    return -1+getValue


def twist_on():
    myValueWidght = 0
    selection = mc.ls(sl = True, fl = True, dag = True, type= 'stroke')

    buffer = mc.listConnections(selection, d = True, scn=True, type= 'brush')

    for each in buffer:
        mc.setAttr(each + ".forwardTwist", myValueWidght)

def twist_off():
    myValueWidght = 1
    selection = mc.ls(sl = True, fl = True, dag = True, type= 'stroke')

    buffer = mc.listConnections(selection, d = True, scn=True, type= 'brush')

    for each in buffer:
        mc.setAttr(each + ".forwardTwist", myValueWidght)

#MANIP__________________
def Manip_on():

    selection = mc.ls(typ='stroke', ni=True, o=True, r=True)

    for each in selection:
        mc.setAttr(each + ".overrideEnabled", 1)
        mc.setAttr(each + ".overrideDisplayType", 2)
        mc.select(d= True)

def Manip_off():

    selection = mc.ls(typ='stroke', ni=True, o=True, r=True)

    for each in selection:
        mc.setAttr(each + ".overrideEnabled", 0)

#TWIST RATE__________________
def GetTwist_Val():
    selection = mc.ls(sl = True, fl = True, dag = True, type= 'stroke')
    brush = mc.listConnections(selection, d = True, scn=True, type= 'brush')

    getValue = mc.getAttr(brush[0] + ".twistRate")
    return getValue

def Twist_Val():

    myValueWidght = mc.floatSliderGrp("Slider_Twist", q= True, value=True)

    selection = mc.ls(sl = True, fl = True, dag = True, type= 'stroke')

    buffer = mc.listConnections(selection, d = True, scn=True, type= 'brush')

    for each in buffer:
        mc.setAttr(each + ".twistRate", myValueWidght)



##___________________________________________________Stroke
#DENSITY__________________
def GetDensity_Val():
    selection = mc.ls(sl = True, fl = True, dag = True, type= 'stroke')

    getValue = mc.getAttr(selection[0] + ".sampleDensity")
    return getValue


def Density_Val():

    myValueWidght = mc.floatSliderGrp("Slider_Density", q= True, value=True)

    selection = mc.ls(sl = True, fl = True, dag = True, type= 'stroke')


    for each in selection:
        mc.setAttr(each + ".sampleDensity", myValueWidght)


#SMOOTHING__________________
def GetSmoothing_Val():
    selection = mc.ls(sl = True, fl = True, dag = True, type= 'stroke')

    getValue = mc.getAttr(selection[0] + ".smoothing")
    return getValue


def Smoothing_Val():

    myValueWidght = mc.floatSliderGrp("Slider_Smoothing", q= True, value=True)

    selection = mc.ls(sl = True, fl = True, dag = True, type= 'stroke')


    for each in selection:
        mc.setAttr(each + ".smoothing", myValueWidght)


#FLATNESS__________________
def GetFlat_Val():
    selection = mc.ls(sl = True, fl = True, dag = True, type= 'stroke')
    brush = mc.listConnections(selection, d = True, scn=True, type= 'brush')

    getValue = mc.getAttr(brush[0] + ".flatness1")
    return getValue


def Flat_Val():

    myValueWidght = mc.floatSliderGrp("Slider_Flat", q= True, value=True)

    selection = mc.ls(sl = True, fl = True, dag = True, type= 'stroke')

    buffer = mc.listConnections(selection, d = True, scn=True, type= 'brush')

    for each in buffer:
        mc.setAttr(each + ".flatness1", myValueWidght)


#PRESSURE_START__________________
def GetPstart_Val():
    selection = mc.ls(sl = True, fl = True, dag = True, type= 'stroke')

    getValue = mc.getAttr(selection[0] + ".pressureScale[0].pressureScale_FloatValue")
    return getValue


def Pstart_Val():
    myValueWidght = mc.floatSliderGrp("Slider_Pstart", q= True, value=True)
    selection = mc.ls(sl = True, fl = True, dag = True, type= 'stroke')

    for each in selection:
        mc.setAttr(each + ".pressureScale[0].pressureScale_FloatValue", myValueWidght)


#PRESSURE_END__________________
def GetPend_Val():
    selection = mc.ls(sl = True, fl = True, dag = True, type= 'stroke')

    getValue = mc.getAttr(selection[0] + ".pressureScale[1].pressureScale_FloatValue")
    return getValue


def Pend_Val():
    myValueWidght = mc.floatSliderGrp("Slider_Pend", q= True, value=True)
    selection = mc.ls(sl = True, fl = True, dag = True, type= 'stroke')

    for each in selection:
        mc.setAttr(each + ".pressureScale[1].pressureScale_FloatValue", myValueWidght)
        mc.setAttr(each + ".pressureScale[1].pressureScale_Position", 1)

###________________________________________BAKE_______________________________###

def B_History():

    selection = mc.ls(sl = True, fl = True, dag = True, type= 'stroke')

    for each in selection:
        mc.select(each)
        import maya.mel as mel
        mel.eval('doPaintEffectsToPoly(1,0,1,1,100000);')
        mel.eval('polyMultiLayoutUV -lm 1 -sc 1 -rbf 0 -fr 1 -ps 0.05 -l 2 -gu 1 -gv 1 -psc 1 -su 1 -sv 1 -ou 0 -ov 0;')
        mc.CenterPivot()
        mc.hyperShade( a= "lambert1")
        selected_objects = mc.ls("birchLimb*MeshGroup")
        newname = "Cable_Hist_"
        for number, object in enumerate(selected_objects):
            print('Old Name:', object)
            print('New Name:', '%s%02d' % (newname, number))
            mc.rename(object, ('%s%02d' % (newname, number)))

    print("Done")



def B_Bake():

    selection = mc.ls(sl = True, fl = True, dag = True, type= 'stroke')


    for each in selection:
        sel1 = mc.ls(sl= True, fl = True, dag = True)
        sel2 = mc.listConnections(sel1)
        selAll = sel1 + sel2
        import maya.mel as mel
        mel.eval('doPaintEffectsToPoly(1,0,1,1,100000);')
        mel.eval('polyMultiLayoutUV -lm 1 -sc 1 -rbf 0 -fr 1 -ps 0.05 -l 2 -gu 1 -gv 1 -psc 1 -su 1 -sv 1 -ou 0 -ov 0;')
        mc.delete(ch= True)
        mc.parent(w= True)
        sel4 = mc.ls("birchLimb*MeshGroup")
        mc.delete(selAll)
        mc.delete(sel4)
        mc.CenterPivot()
        mc.hyperShade( a= "lambert1")
        selected_objects = mc.ls(selection=True)
        newname = "Cable_"
        for number, object in enumerate(selected_objects):
            print('Old Name:', object)
            print('New Name:', '%s%02d' % (newname, number))
            mc.rename(object, ('%s%02d' % (newname, number)))


def B_BakeC():

    selection = mc.ls(sl = True, fl = True, dag = True, type= 'stroke')


    for each in selection:
        sel1 = mc.ls(sl= True, fl = True, dag = True)
        sel2 = mc.listConnections(sel1)
        sel2 = mc.listConnections(sel1, type= 'stroke')
        sel3 = mc.listConnections(sel1, type= 'transform')
        import maya.mel as mel
        mel.eval('doPaintEffectsToPoly(1,0,1,1,100000);')
        mel.eval('polyMultiLayoutUV -lm 1 -sc 1 -rbf 0 -fr 1 -ps 0.05 -l 2 -gu 1 -gv 1 -psc 1 -su 1 -sv 1 -ou 0 -ov 0;')
        mc.delete(ch= True)
        mc.parent(w= True)
        sel4 = mc.ls("birchLimb*MeshGroup")
        mc.delete(sel1)
        mc.delete(sel2)
        mc.delete(sel3)
        mc.delete(sel4)
        mc.CenterPivot()
        mc.hyperShade( a= "lambert1")
        selected_objects = mc.ls(selection=True)
        newname = "Cable_"
        for number, object in enumerate(selected_objects):
            print('Old Name:', object)
            print('New Name:', '%s%02d' % (newname, number))
            mc.rename(object, ('%s%02d' % (newname, number)))

    print("Done")


def B_BtoC():

    getSelect=mc.ls(sl=True)

    for each in getSelect:
        #mc.select(each)
        #mc.ConvertSelectionToEdgePerimeter()
        #sel = mc.ls(sl= True)
        #selA = mc.select(sel[1])
        #mc.SelectEdgeLoopSp()
        #mc.CreateCluster()
        #mc.rename("ClusterTps")
        #selClu = mc.ls(sl= True)
        mc.select(each)
        mc.ConvertSelectionToEdgePerimeter()
        mc.ConvertSelectionToFaces()
        mc.ConvertSelectionToContainedEdges()
        sel = mc.ls(sl= True)
        selO = mc.ls(os= True)
        selA = mc.select(selO[1])
        mc.SelectEdgeLoopSp()
        mc.polyToCurve(form= 2,degree= 1,conformToSmoothMeshPreview= 0)
        mc.CenterPivot()
        mc.DeleteHistory()
        mc.rename("Curve_0")
        selCurv = mc.ls(sl= True)
        posX = mc.getAttr(selCurv[0]+".controlPoints[0].xValue")
        posY = mc.getAttr(selCurv[0]+".controlPoints[0].yValue")
        posZ = mc.getAttr(selCurv[0]+".controlPoints[0].zValue")
        mc.move(posX, posY, posZ, selCurv[0] + ".scalePivot", selCurv[0] + ".rotatePivot", absolute=True)
        #selAll = mc.ls(selClu + selCurv)
        #mc.matchTransform(selCurv, selClu)
        #mc.delete("ClusterTps")


def B_Dyn():
    mc.select("hairSystem1", "nucleus1", "hairSystem1Follicles", "hairSystem1OutputCurves", "nRigid*")
    mc.DeleteHistory()
    mc.delete()




###____________________________________________________________________________
###____________________________________________________________________________________________________________DYNAMIQUE
###____________________________________________________________________________


##___________________________MAKE COLLIDE
def Collide():
    selection = mc.ls(sl = True, fl = True, dag = True, type= "mesh")
    for each in selection:
        mel.eval("makeCollideNCloth;")

##____REBUILD ALL
def Dyn():

    mc.playbackOptions(ps = 1)
    version = mc.about(v=True)
    if version == 2018 :
        print("Ok")
    else :
        mc.evaluationManager(mode = "off");


    ##___________________________CONFORM
    mc.sets(n= "Settemps")
    ##____CONVERT BEZIER_don't affect CV
    mc.bezierCurveToNurbs()

    selection = mc.ls(sl = True, fl = True, dag = True)
    Rvalue =  mc.intSliderGrp("Slider_Rebuild", q=True, v=True)
    for each in selection:
        mc.select(each)
        mc.rebuildCurve(ch= 0, rpo= 1, rt= 0, end= 1, kr= 0, kcp= 0, kep= 1, kt= 0, s= Rvalue, d= 3, tol= 0.01)

    ##___________________________MAKE DYNAMIQUE
    if mc.objExists('hairSystem1'):
        mc.select("Settemps", "hairSystem1")
        mc.delete("Settemps")
        DynCreate = mel.eval('makeCurvesDynamic 2 { "1", "0", "1", "1", "0"};')

    else:
        mc.select("Settemps")
        mc.delete("Settemps")
        DynCreate = mel.eval('makeCurvesDynamic 2 { "1", "0", "1", "1", "0"};')
        mc.setAttr ("nucleus1.spaceScale", 0.01)
        mc.setAttr ("hairSystem1.collideWidthOffset", 1)

        mc.setAttr("hairSystem1Follicles.visibility", 0, l= True)


##___________________________POINT LOCK
def PlNo():

    sel1 = mc.ls(type= "follicle")
    for each in sel1:
        mc.setAttr (each+".pointLock", 0)

def PlBase():
    sel1 = mc.ls(type= "follicle")
    for each in sel1:
        mc.setAttr (each+".pointLock", 1)

def PlTip():
    sel1 = mc.ls(type= "follicle")
    for each in sel1:
        mc.setAttr (each+".pointLock", 2)

def PlBoth():
    sel1 = mc.ls(type= "follicle")
    for each in sel1:
        mc.setAttr (each+".pointLock", 3)


##___________________________________________________EDIT
##___________________________FSAMPLE DENSITY
def FSample():

    myValueWidght = mc.floatSliderGrp("Slider_FSample", q= True, value=True)
    selection = mc.ls(sl = True, fl = True, dag = True, type= 'nurbsCurve')
    buffer = mc.listConnections(selection, d = True, scn=True, type= 'follicle')
    for each in buffer:
        mc.setAttr(each + ".sampleDensity", myValueWidght)

##___________________________OFFSET
def Offset():

    myValueWidght = mc.floatSliderGrp("Slider_Offset", q= True, value=True)
    selection = mc.ls("hairSystem1")
    for each in selection:
        mc.setAttr("hairSystem1.collideWidthOffset", myValueWidght)


##___________________________Friction
def Friction():

    myValueWidght = mc.floatSliderGrp("Slider_Friction", q= True, value=True)
    selection = mc.ls("hairSystem1")
    for each in selection:
        mc.setAttr("hairSystem1.friction", myValueWidght)

##___________________________Stretch
def Stretch():

    myValueWidght = mc.floatSliderGrp("Slider_Stretch", q= True, value=True)
    selection = mc.ls("hairSystem1")
    for each in selection:
        mc.setAttr("hairSystem1.stretchResistance", myValueWidght)

##___________________________StartCurve
def StartCurve():

    myValueWidght = mc.floatSliderGrp("Slider_StartCurve", q= True, value=True)
    selection = mc.ls("hairSystem1")
    for each in selection:
        mc.setAttr("hairSystem1.startCurveAttract", myValueWidght)

##___________________________MotionDrag
def MotionDrag():

    myValueWidght = mc.floatSliderGrp("Slider_MotionDrag", q= True, value=True)
    selection = mc.ls("hairSystem1")
    for each in selection:
        mc.setAttr("hairSystem1.motionDrag", myValueWidght)

##___________________________Offset_ON OFF
def offset_on():
    mc.setAttr("hairSystem1.solverDisplay", 1)

def offset_off():
    mc.setAttr("hairSystem1.solverDisplay", 0)




###____________________________________________________________________________
###____________________________________________________________________________________________________________MATERIALS
###____________________________________________________________________________

###_________DISPLACE
def Disp():

    mc.toggleDisplacement()

###_________Plastic SIMPLE
def PShiny():

    PShinyPath = mc.internalVar(upd = True)+"scripts/Cable_script/Shaders/Plastic_Shiny_1.ma"
    selection = mc.ls(sl = True, fl = True, dag = True)

    if mc.objExists('Plastic_Shiny_1'):
      print("Plastic_Shiny_1_EXIST")
      for each in selection:
        mc.hyperShade( a= "Plastic_Shiny_1")
        mc.select("Plastic_Shiny_1")
        print("Done")


    else:
      mc.sets(n= "Settemps")
      mc.file(PShinyPath, i = True)
      mc.binMembership("Plastic_Shiny_1", addToBin= "Viewport_Shaders")
      mc.select("Settemps")
      mc.ls(selection= True)
      mc.delete("Settemps")
      for each in selection:
        mc.hyperShade( a= "Plastic_Shiny_1")
        mc.select("Plastic_Shiny_1")
        print("Done")


def cn_PShiny():

    PShinyPath = mc.internalVar(upd = True)+"scripts/Cable_script/Shaders/Plastic_Shiny_1.ma"
    selection = mc.ls(sl = True, fl = True, dag = True)

    mc.sets(n= "Settemps")
    mc.file(PShinyPath, i = True)
    mc.select("Plastic_Shiny_1_Plastic_Shiny_1")
    mc.rename("Plastic_Shiny_New")
    mc.binMembership("Plastic_Shiny_New", addToBin= "Viewport_Shaders")
    mc.select("Settemps")
    mc.ls(selection= True)
    mc.delete("Settemps")
    mc.hyperShade( a= "Plastic_Shiny_New")
    mc.select("Plastic_Shiny_New")
    mc.rename("Plastic_Shiny_2")
    mc.select("Plastic_Shiny_2")
    print("Done")

###________TRESSE
def Tresse():

    TressePath = mc.internalVar(upd = True)+"scripts/Cable_script/Shaders/Tresse.ma"
    selection = mc.ls(sl = True, fl = True, dag = True)

    if mc.objExists('Tresse'):
      print("Tresse_EXIST")
      for each in selection:
        mc.hyperShade( a= "Tresse")
        mc.select("Tresse")
        print("Done")


    else:
      mc.sets(n= "Settemps")
      mc.file(TressePath, i = True)
      mc.binMembership("Tresse", addToBin= "Viewport_Shaders")
      mc.select("Settemps")
      mc.ls(selection= True)
      mc.delete("Settemps")
      for each in selection:
        mc.hyperShade( a= "Tresse")
        mc.select("Tresse")
        print("Done")


###_________CABLE
def Cable():

    CablePath = mc.internalVar(upd = True)+"scripts/Cable_script/Shaders/Cable.ma"
    selection = mc.ls(sl = True, fl = True, dag = True)

    if mc.objExists('Cable'):
      print("Cable_EXIST")
      for each in selection:
        mc.hyperShade( a= "Cable")
        mc.select("Cable")
        print("Done")

    else:
      mc.sets(n= "Settemps")
      mc.file(CablePath, i = True)
      mc.binMembership("Cable", addToBin= "Viewport_Shaders")
      mc.select("Settemps")
      mc.ls(selection= True)
      mc.delete("Settemps")
      for each in selection:
        mc.hyperShade( a= "Cable")
        mc.select("Cable")
        print("Done")


###_________VELCRO
def Velcro():

    VelcroPath = mc.internalVar(upd = True)+"scripts/Cable_script/Shaders/Velcro.ma"
    selection = mc.ls(sl = True, fl = True, dag = True)

    if mc.objExists('Velcro'):
      print("Velcro_EXIST")
      for each in selection:
        mc.hyperShade( a= "Velcro")
        mc.select("Velcro")
        print("Done")

    else:
      mc.sets(n= "Settemps")
      mc.file(VelcroPath, i = True)
      mc.binMembership("Velcro", addToBin= "Viewport_Shaders")
      mc.select("Settemps")
      mc.ls(selection= True)
      mc.delete("Settemps")
      for each in selection:
        mc.hyperShade( a= "Velcro")
        mc.select("Velcro")
        print("Done")

###_________Plastic SIMPLE
def StripeA():

    StripeAPath = mc.internalVar(upd = True)+"scripts/Cable_script/Shaders/Cable_StripeA_shd.ma"
    selection = mc.ls(sl = True, fl = True, dag = True, type= 'mesh')

    if mc.objExists('Cable_StripeA_shd'):
      print("Cable_StripeA_shd1_EXIST")
      for each in selection:
        mc.setAttr(each + ".aiSubdivType", 1)
        mc.setAttr(each + ".aiSubdivIterations", 3)
        mc.hyperShade( a= "Cable_StripeA_shd")
        mc.select("Cable_StripeA_shd")
        print("Done")


    else:
      mc.sets(n= "Settemps")
      mc.file(StripeAPath, i = True)
      mc.binMembership("Cable_StripeA_shd", addToBin= "Viewport_Shaders")
      mc.select("Settemps")
      mc.ls(selection= True)
      mc.delete("Settemps")
      for each in selection:
        mc.hyperShade( a= "Cable_StripeA_shd")
        mc.select("Cable_StripeA_shd")
        print("Done")


def cn_PShiny():

    PShinyPath = mc.internalVar(upd = True)+"scripts/Cable_script/Shaders/Plastic_Shiny_1.ma"
    selection = mc.ls(sl = True, fl = True, dag = True)

    mc.sets(n= "Settemps")
    mc.file(PShinyPath, i = True)
    mc.select("Plastic_Shiny_1_Plastic_Shiny_1")
    mc.rename("Plastic_Shiny_New")
    mc.binMembership("Plastic_Shiny_New", addToBin= "Viewport_Shaders")
    mc.select("Settemps")
    mc.ls(selection= True)
    mc.delete("Settemps")
    mc.hyperShade( a= "Plastic_Shiny_New")
    mc.select("Plastic_Shiny_New")
    mc.rename("Plastic_Shiny_2")
    mc.select("Plastic_Shiny_2")
    print("Done")



def DiscordLink():
    mc.showHelp("https://discord.gg/2mkvw9r", absolute=True)

def WzxStoreLink():
    mc.showHelp("http://www.wzxstore.com/", absolute=True)
