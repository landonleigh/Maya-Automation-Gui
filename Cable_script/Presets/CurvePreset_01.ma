//Maya ASCII 2018ff09 scene
//Name: CurvePreset_01.ma
//Last modified: Fri, Mar 20, 2020 08:50:05 AM
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
createNode transform -n "CurvePreset_01";
	rename -uid "3AE41F51-4333-A255-54D3-ADB498DA5789";
createNode nurbsCurve -n "CurvePreset_0Shape1" -p "CurvePreset_01";
	rename -uid "DCCF0AEB-4C51-075A-8A79-A591A3AB50AE";
	setAttr -k off ".v";
	setAttr ".cc" -type "nurbsCurve" 
		1 95 0 no 3
		96 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27
		 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54
		 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81
		 82 83 84 85 86 87 88 89 90 91 92 93 94 95
		96
		-23.626491359369766 -10.22343282904194 -22.899796747159485
		-25.732525986555402 -13.414651681090163 -18.241344535927567
		-25.666559325880598 -15.968037304888185 -13.466902501426432
		-24.53355626990674 -18.40329875271118 -8.7807503575384658
		-23.182312733991921 -20.500795969074261 -4.1280597322989934
		-21.830929240522664 -22.185138484633626 0.58849819029813943
		-20.500772642815036 -23.413779202830483 5.378592144641118
		-19.101523665716059 -23.980140773262974 10.34067060717183
		-17.530220201652241 -23.780467995548861 15.429364003982073
		-15.842005527085576 -22.833981707168732 20.331167413053265
		-14.543992514388492 -21.074435332339363 24.257373362414057
		-13.564756158261844 -18.787342282183999 27.043018547859504
		-12.588645520851742 -16.26381427000706 29.087308567263563
		-11.376986319264233 -13.65015359274912 30.80629057755516
		-9.4627868467424605 -11.121773718683471 32.363971506317057
		-7.0007468534968211 -8.6463911052446747 33.699959668794406
		-4.4100392151726737 -6.2413604891876275 34.852930002539722
		-2.0692024641001581 -3.9404582936581392 35.930929739605858
		-0.14912477429061255 -1.6459008405977329 36.849144601982402
		1.6049166033964184 0.66451846863583341 37.386628263675391
		3.5251342507605159 2.9846415016463652 37.377554348893739
		5.5158438530606873 5.3504840024511395 36.666290057063975
		7.2924183970176273 7.7762283365705116 35.255261319130284
		8.5839000571727411 10.241907226232343 33.293196362978847
		9.3232491649332587 12.709638826693208 30.953502598601233
		9.7833829515210482 15.216558542406347 28.41380948888235
		10.466049249720299 17.788231953322338 25.710132777839704
		11.598772390585168 20.255217113493018 22.569625213028985
		12.96382507187468 22.240934896350154 18.577149361625345
		14.18416164183941 23.21410642511637 13.636810972556077
		15.083342276807684 22.90937217651117 7.9446439271190457
		15.908438712941916 22.342823996006246 1.8846101128802957
		16.934467544780546 22.317258416055665 -4.112547770011588
		18.221703825783152 22.890897779320767 -9.9174972780945154
		19.185731460990382 23.661970599428514 -15.393674827591667
		18.939126250009735 23.331297550727868 -20.389133166864099
		17.415455006984644 21.862676279128664 -24.776091048678268
		14.873732512725837 19.611412362919054 -28.43818542961975
		11.580951128648962 16.85592803046211 -31.339902080241131
		7.7631889577453421 13.72983609376206 -33.462078478709202
		3.6807670513339872 10.338944464000178 -34.791348678571808
		-0.53606075988909652 6.7886878322115081 -35.272662708403118
		-4.8003808345966945 3.2003627456069808 -34.844345939198774
		-9.0077381846339222 -0.30566729896827383 -33.481707525724005
		-13.066833831966505 -3.6163165974994627 -31.208097053316578
		-16.891780490666406 -6.7019141484388456 -28.093026774031273
		-20.377703299915424 -9.5969828152224181 -24.255845492444564
		-23.316158808585897 -12.361984261383441 -19.848092250661637
		-25.497677210150414 -15.003076619317653 -15.081872722485798
		-26.983046735768085 -17.456999074403939 -10.132390439857659
		-27.907326425505175 -19.549084598660556 -5.0532957986582687
		-28.463191179352179 -21.293328947534064 0.10902693493409288
		-28.709096602560521 -22.85488203530349 5.1844593534580667
		-28.418777982066217 -24.166004405602507 9.9384325956175417
		-27.310314150643194 -24.978131441689129 14.289666311652581
		-25.217202270987286 -25.102600360133238 18.163411504345277
		-22.428547998120621 -24.661454148435496 21.69288443929446
		-19.456082803713343 -23.975102301301831 25.154384655288084
		-16.451940549477172 -23.178837121389279 28.384045182297825
		-13.327154883285516 -22.136993085895028 31.036194187035505
		-10.002743091897855 -20.722861955503959 32.954242492305298
		-6.6284597585996607 -18.927673056802178 34.357923458629159
		-3.4466647152195264 -16.876641748524435 35.614135815057125
		-0.52780326417530432 -14.627430543113405 36.851780469258301
		2.2792787533635419 -12.08860050498015 37.836941695190944
		5.1487818401972163 -9.1694591388268236 38.270810114056019
		8.0550471113389222 -5.8679537338543923 38.038667183704149
		10.887041573573811 -2.2521969665731376 37.269530443099939
		13.542129686955377 1.5869320576466635 36.19936832908428
		15.925373577033042 5.5716169385177636 34.971707313768775
		18.128305484431849 9.6798376874703536 33.533480157749239
		20.388993209309547 13.910288033995585 31.676103452343284
		22.917932913593177 18.072812314083421 29.026706946176944
		25.699775918808768 21.621762675363243 25.146640337273936
		28.366667119284216 24.059450054130593 20.000634321907114
		30.474381237123453 25.102600360133238 13.982179564476269
		31.880208219282622 24.908339274525133 7.507229916873996
		32.596277720482476 24.121777818389091 0.87235543702769291
		32.265464714227505 22.830249505715983 -5.7827545725695018
		30.875079715578522 21.357709422591597 -12.195154856452064
		28.987518830924728 19.655638950132015 -18.057568603775508
		26.83725761652579 17.53126988331087 -23.320847386660773
		24.304912278416623 15.250894795770364 -27.887674052231318
		21.08276280683026 12.769540660007806 -31.673654195140159
		17.130781341187458 10.023013611037186 -34.562844644636243
		12.602081446081115 7.0152324603845955 -36.537645738244635
		7.7470471864628507 3.8869012028130783 -37.761632867755225
		2.7887709041619928 0.84851600024921936 -38.270810114056133
		-2.1290576448963066 -2.0124030232432233 -37.974963170160095
		-6.8553776069179548 -4.6630124948819685 -36.786851827112628
		-11.33033380110669 -7.1057383456104617 -34.730922004428294
		-15.570207956299782 -9.375103438865608 -31.984616554919171
		-20.024590389981086 -11.259118732139086 -28.780008430160024
		-25.204699396120986 -12.662613088390572 -25.035665659706808
		-29.611169693654574 -14.402752015666465 -20.441010767055275
		-32.59627772048259 -17.420236890096021 -15.077277449447308
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
// End of CurvePreset_01.ma
