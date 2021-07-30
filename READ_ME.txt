--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Installation Instructions:

-Download Zip
-Extract to desktop
-Copy/Cut and paste entire folder to
	documents/maya/scripts
-Copy the following scripts to your Maya Shelf
	-Vehicle_GUI (A pop up window with tools for preparing vehicles for rendering)
	-magic_shade (A tool to help you create your own spellbooks top be used in the Vehicle_GUI script)
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
GUI Notes:

-Load Studio with name of shaders you are changing to (i.e. if you want your end product to be in blinn shaders load blinn studio)
-Choose and load desired vehicle
-Choose and apply appropiate spellbook (i.e. if you load a Hum3d file and want to change to blinn choose the Hum2Blinn spellbook)
-Apply Spellbook 
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Spellbook Notes:

- Start Magic Shade from your shelf button
- Add a shader replacement ("spell") by clicking the green "+" button on the right
- Select the shader to replace from the drop-down box on the left
	-You can select objects from this box by choosing "Object" from the Type drop-down box
- Select the shader to apply from the drop-down box on the right
	-Both drop-down boxes can be edited manually. Add a "*" as a wildcard
- Apply all spells by clicking Cast - Cast All Spells
- Save your spells to a spellbook file for future use by clicking the save button
- If new shaders are added to your scene, click File - Refresh Shaders to make them show up in the drop-down boxes
- Save a studio with your new shaders in your documents/maya/magic-shade/studios folder
	-This studio will be what you load whenever you want to apply your new shaders so save it with no objects other than those you want loaded in every use
		(i.e. Don't save your studio with vehicles or you will have to delete them every time you load the studio)
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Contributors

Jake Cheek - [@jgchk](https://github.com/jgchk)
Dylan Steimel - [@steimel60](https://github.com/steimel60)