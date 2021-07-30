//Maya ASCII 2018ff09 scene
//Name: CurvePreset_03.ma
//Last modified: Fri, Mar 20, 2020 08:50:18 AM
//Codeset: 1252
requires maya "2018ff09";
requires "mtoa" "4.0.2";
requires "stereoCamera" "10.0";
currentUnit -l centimeter -a degree -t film;
fileInfo "application" "maya";
fileInfo "product" "Maya 2018";
fileInfo "version" "2018";
fileInfo "cutIdentifier" "201811122215-49253d42f6";
fileInfo "osv" "Microsoft Windows 8 Home Premium Edition, 64-bit  (Build 9200)\n";
createNode transform -n "CurvePreset_03";
	rename -uid "56A50768-4714-C509-B26A-C2B25679651F";
createNode transform -n "CurvePreset_03_1" -p "CurvePreset_03";
	rename -uid "3C1AAF6E-4616-9B3E-D44C-9FA79EBD2310";
	setAttr ".rp" -type "double3" -4.4522697951459271 2.0930403818698284 1.3279923278353891 ;
	setAttr ".sp" -type "double3" -4.4522697951459271 2.0930403818698284 1.3279923278353891 ;
createNode nurbsCurve -n "CurvePreset_03_Shape1" -p "CurvePreset_03_1";
	rename -uid "5E21539F-41A2-FB1D-CDBC-1B891369A578";
	setAttr -k off ".v";
	setAttr ".cc" -type "nurbsCurve" 
		3 8 0 no 3
		13 0 0 0 0.125 0.25 0.375 0.5 0.625 0.75 0.875 1 1 1
		11
		137.96602950059531 5.13056370229185 7.782960686531986
		124.64809956001534 9.7600007830817681 1.6838348420017937
		104.74892819144497 -5.8650007373188728 -16.282422143682464
		68.432256340467717 2.7162576180747791 21.707143522567279
		34.728144911144568 8.000608408365629 -18.981224968233629
		-7.8307039110825372e-06 -9.3850248483151137 19.414533668514164
		-34.728171356719621 17.954041367391007 -12.664583000531181
		-68.432266349317956 -16.61190244629265 9.44112603447895
		-104.74894740728537 21.415785447074576 1.0304542973535078
		-124.64808462253262 -1.4933972999012184 -5.4577616387560717
		-137.96602950059531 -5.0409045024769661 1.3279921406049269
		;
createNode transform -n "CurvePreset_03_2" -p "CurvePreset_03";
	rename -uid "A9B2C80C-4FE4-4F65-41FD-04AD60E24B2E";
	setAttr ".rp" -type "double3" -4.4522697951459271 2.0930403818698284 1.3279923278353891 ;
	setAttr ".sp" -type "double3" -4.4522697951459271 2.0930403818698284 1.3279923278353891 ;
createNode nurbsCurve -n "CurvePreset_03_Shape2" -p "CurvePreset_03_2";
	rename -uid "EA0CC5C0-45B0-6C6B-683E-C998219D745F";
	setAttr -k off ".v";
	setAttr ".cc" -type "nurbsCurve" 
		3 8 0 no 3
		13 0 0 0 0.125 0.25 0.375 0.5 0.625 0.75 0.875 1 1 1
		11
		-130.96671734564794 7.8780708571331308 2.368918274906239
		-119.13600066611551 4.011229927161553 7.3539645156773243
		-101.45896980100429 -13.619511052180929 -1.2500848107315505
		-69.197780762661267 18.444970132095676 -2.5218871149820501
		-39.257407518863417 -12.810534675659284 10.360573647331242
		-8.4073476578005373 14.039753786308392 -11.663957885956425
		22.442721783161893 -5.6607681472886924 16.935119733420834
		52.383080425723762 4.561140766150876 -15.288728223796529
		84.644277642912542 5.9768363839393821 16.769715283682697
		102.32127816860223 -4.0723069388163733 -0.079254290750892409
		114.1520081175486 0.57171897144714734 -4.3496558744674161
		;
createNode transform -n "CurvePreset_03_3" -p "CurvePreset_03";
	rename -uid "E4873072-4765-6B52-288B-7C9050E2FFA7";
	setAttr ".rp" -type "double3" -4.4522697951459271 2.0930403818698284 1.3279923278353891 ;
	setAttr ".sp" -type "double3" -4.4522697951459271 2.0930403818698284 1.3279923278353891 ;
createNode nurbsCurve -n "CurvePreset_03_Shape3" -p "CurvePreset_03_3";
	rename -uid "7276470D-4CE1-44C8-E451-56939341E3CF";
	setAttr -k off ".v";
	setAttr ".cc" -type "nurbsCurve" 
		3 8 0 no 3
		13 0 0 0 0.125 0.25 0.375 0.5 0.625 0.75 0.875 1 1 1
		11
		121.26028520045705 9.418344313838233 -13.839284070261186
		100.90062732827305 4.6938296173320735 -10.286011633356896
		82.385680128948337 -12.857621164468988 13.572780428907997
		56.485285301223257 14.308626866720164 -2.9242941312897912
		18.329366248755065 -22.534039653577285 17.880673131494522
		-0.91178389713737218 22.534039653577285 7.7338106104998356
		-30.455906132463767 -9.1163082083107732 -12.307597850177423
		-55.840101150461919 18.761090080626325 11.531041855261982
		-93.260864852015317 -4.1589660158532844 -3.170287371491213
		-102.26401226766303 1.2841662162716077 10.265407052184258
		-132.2243294372916 5.3152075104026473 8.7112485134779849
		;
createNode transform -n "CurvePreset_03_4" -p "CurvePreset_03";
	rename -uid "7B01293D-485A-5773-BD12-878F31235A56";
	setAttr ".rp" -type "double3" -4.5258125522502102 1.567324489988196 -0.67588481387751287 ;
	setAttr ".sp" -type "double3" -4.5258125522502102 1.567324489988196 -0.67588481387751287 ;
createNode nurbsCurve -n "CurvePreset_03_Shape4" -p "CurvePreset_03_4";
	rename -uid "588EA8A7-4849-CB37-FE52-17A874FD74D2";
	setAttr -k off ".v";
	setAttr ".cc" -type "nurbsCurve" 
		3 8 0 no 3
		13 0 0 0 0.125 0.25 0.375 0.5 0.625 0.75 0.875 1 1 1
		11
		121.43435445135145 -12.829082707953916 -4.435222889961647
		101.08261922294601 -7.7781087625245711 -1.31160508423946
		82.153988506238818 21.302598024855165 2.7031283997090281
		56.203710375246857 -7.0619704867333155 -11.545495093261287
		15.690331018080158 18.113111407567015 14.51008072032888
		-1.7296960376878001 -3.0448213290002695 -21.707143522567275
		-28.462435356397481 -19.77256415415934 20.601559926400334
		-56.649054612060596 1.0819461649351982 -18.15636984369625
		-92.929235361404764 -0.89339258443112612 10.507512135666309
		-102.5475841032561 7.8431613255881079 -0.5542341002640363
		-132.52245938959237 3.909824326654924 -2.0777232549930531
		;
select -ne :time1;
	setAttr -av -k on ".cch";
	setAttr -av -cb on ".ihi";
	setAttr -av -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr ".o" 1;
	setAttr -av ".unw" 1;
	setAttr -k on ".etw";
	setAttr -k on ".tps";
	setAttr -k on ".tms";
select -ne :hardwareRenderingGlobals;
	setAttr ".otfna" -type "stringArray" 22 "NURBS Curves" "NURBS Surfaces" "Polygons" "Subdiv Surface" "Particles" "Particle Instance" "Fluids" "Strokes" "Image Planes" "UI" "Lights" "Cameras" "Locators" "Joints" "IK Handles" "Deformers" "Motion Trails" "Components" "Hair Systems" "Follicles" "Misc. UI" "Ornaments"  ;
	setAttr ".otfva" -type "Int32Array" 22 0 1 1 1 1 1
		 1 1 1 0 0 0 0 0 0 0 0 0
		 0 0 0 0 ;
	setAttr ".msaa" yes;
	setAttr ".aasc" 16;
	setAttr ".laa" yes;
	setAttr ".fprt" yes;
select -ne :renderPartition;
	setAttr -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -s 2 ".st";
	setAttr -cb on ".an";
	setAttr -cb on ".pt";
select -ne :renderGlobalsList1;
	setAttr -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -k on ".nds";
	setAttr -cb on ".bnm";
select -ne :defaultShaderList1;
	setAttr -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -s 4 ".s";
select -ne :postProcessList1;
	setAttr -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -s 2 ".p";
select -ne :defaultRenderingList1;
select -ne :initialShadingGroup;
	setAttr -av -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -av -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -k on ".mwc";
	setAttr -cb on ".an";
	setAttr -cb on ".il";
	setAttr -cb on ".vo";
	setAttr -cb on ".eo";
	setAttr -cb on ".fo";
	setAttr -cb on ".epo";
	setAttr ".ro" yes;
select -ne :initialParticleSE;
	setAttr -av -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -av -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -k on ".mwc";
	setAttr -cb on ".an";
	setAttr -cb on ".il";
	setAttr -cb on ".vo";
	setAttr -cb on ".eo";
	setAttr -cb on ".fo";
	setAttr -cb on ".epo";
	setAttr ".ro" yes;
select -ne :defaultRenderGlobals;
	setAttr -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -k on ".macc";
	setAttr -k on ".macd";
	setAttr -k on ".macq";
	setAttr -k on ".mcfr";
	setAttr -cb on ".ifg";
	setAttr -k on ".clip";
	setAttr -k on ".edm";
	setAttr -k on ".edl";
	setAttr ".ren" -type "string" "arnold";
	setAttr -av -k on ".esr";
	setAttr -k on ".ors";
	setAttr -cb on ".sdf";
	setAttr -av ".outf" 51;
	setAttr ".imfkey" -type "string" "exr";
	setAttr -k on ".gama";
	setAttr -k on ".an";
	setAttr -cb on ".ar";
	setAttr -av ".bfs";
	setAttr -cb on ".me";
	setAttr -cb on ".se";
	setAttr -k on ".be";
	setAttr -k on ".ep";
	setAttr -k on ".fec";
	setAttr -av -k on ".ofc";
	setAttr -cb on ".ofe";
	setAttr -cb on ".efe";
	setAttr -cb on ".oft";
	setAttr -cb on ".umfn";
	setAttr -cb on ".ufe";
	setAttr -k on ".pff";
	setAttr -cb on ".peie";
	setAttr -cb on ".ifp";
	setAttr -k on ".comp";
	setAttr -k on ".cth";
	setAttr -k on ".soll";
	setAttr -cb on ".sosl";
	setAttr -k on ".rd";
	setAttr -k on ".lp";
	setAttr -av -k on ".sp";
	setAttr -k on ".shs";
	setAttr -av -k on ".lpr";
	setAttr -cb on ".gv";
	setAttr -cb on ".sv";
	setAttr -k on ".mm";
	setAttr -k on ".npu";
	setAttr -k on ".itf";
	setAttr -k on ".shp";
	setAttr -cb on ".isp";
	setAttr -k on ".uf";
	setAttr -k on ".oi";
	setAttr -k on ".rut";
	setAttr -k on ".mb";
	setAttr -av -k on ".mbf";
	setAttr -k on ".afp";
	setAttr -k on ".pfb";
	setAttr -k on ".prlm";
	setAttr -k on ".polm";
	setAttr -cb on ".prm";
	setAttr -cb on ".pom";
	setAttr -cb on ".pfrm";
	setAttr -cb on ".pfom";
	setAttr -av -k on ".bll";
	setAttr -av -k on ".bls";
	setAttr -av -k on ".smv";
	setAttr -k on ".ubc";
	setAttr -k on ".mbc";
	setAttr -cb on ".mbt";
	setAttr -k on ".udbx";
	setAttr -k on ".smc";
	setAttr -k on ".kmv";
	setAttr -cb on ".isl";
	setAttr -cb on ".ism";
	setAttr -cb on ".imb";
	setAttr -k on ".rlen";
	setAttr -av -k on ".frts";
	setAttr -k on ".tlwd";
	setAttr -k on ".tlht";
	setAttr -k on ".jfc";
	setAttr -cb on ".rsb";
	setAttr -k on ".ope";
	setAttr -k on ".oppf";
	setAttr -cb on ".hbl";
select -ne :defaultResolution;
	setAttr -av -k on ".cch";
	setAttr -k on ".ihi";
	setAttr -av -k on ".nds";
	setAttr -k on ".bnm";
	setAttr -av ".w" 2048;
	setAttr -av ".h" 2048;
	setAttr -av ".pa" 1;
	setAttr -av -k on ".al" yes;
	setAttr -av ".dar" 1;
	setAttr -av -k on ".ldar";
	setAttr -k on ".dpi";
	setAttr -av -k on ".off";
	setAttr -av -k on ".fld";
	setAttr -av -k on ".zsl";
	setAttr -k on ".isu";
	setAttr -k on ".pdu";
select -ne :hardwareRenderGlobals;
	setAttr -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr ".ctrs" 256;
	setAttr -av ".btrs" 512;
	setAttr -k off ".fbfm";
	setAttr -k off -cb on ".ehql";
	setAttr -k off -cb on ".eams";
	setAttr -k off ".eeaa";
	setAttr -k off ".engm";
	setAttr -k off ".mes";
	setAttr -k off ".emb";
	setAttr -av -k off ".mbbf";
	setAttr -k off ".mbs";
	setAttr -k off ".trm";
	setAttr -k off -cb on ".tshc";
	setAttr -k off ".enpt";
	setAttr -k off ".clmt";
	setAttr -k off -cb on ".tcov";
	setAttr -k off -cb on ".lith";
	setAttr -k off -cb on ".sobc";
	setAttr -k off -cb on ".cuth";
	setAttr -k off -cb on ".hgcd";
	setAttr -k off -cb on ".hgci";
	setAttr -k off -cb on ".mgcs";
	setAttr -k off ".twa";
	setAttr -k off ".twz";
	setAttr -cb on ".hwcc";
	setAttr -cb on ".hwdp";
	setAttr -cb on ".hwql";
	setAttr -k on ".hwfr";
	setAttr -k on ".soll";
	setAttr -k on ".sosl";
	setAttr -k on ".bswa";
	setAttr -k on ".shml";
	setAttr -k on ".hwel";
// End of CurvePreset_03.ma
