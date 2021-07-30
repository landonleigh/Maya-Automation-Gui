import os
import re

user_profile = os.environ['USERPROFILE']
desktop_dir = user_profile + '\\Desktop'
folder = 'C:\\Users\\DylanSteimel\\deltav\\Jason Young - Asset Library\\3D Vehicle Library'


def search_folder(path):
    asset_match = re.search('.*/([a-zA-Z_0-9\(\)]*)', path)
    if asset_match != None:
        asset = asset_match.group(1)
        cmds.file(rename=asset)
        #print('\nGoing in to ' + asset)
    for file in os.listdir(path):
        #print('\n' + path + '\\' + file)
        run = True
        folder = True
        Render = False
        Smooth = False
        Unsmooth = False
        VC = False
        parent = False

        extensions = ['.mayaswatches', '.ma', '.mb','.ico', '.png', '.zip', '.vc4', '.mtl', '.obj', '.vc5', '.mel', '.jpg', '.rar', '.txt', '.fbx']

        if not os.path.isdir(path + '\\' + file):
            folder = False
            continue

        for sub in os.listdir(path + '\\' + file):
            if '.mayaswatches' in sub.lower():
                continue
            if not os.path.isdir(path + '\\' + file + '\\' + sub):
                folder = False
                continue
            if 'render' in sub.lower():
                print('Render folder found: ' + file)
                renderFolder = path + '\\' + file + '\\' + sub
                Render = True
                run = False
            if 'smooth' in sub.lower() and 'unsmooth' not in sub.lower():
                print('Smooth folder found: ' + file)
                smoothFolder = path + '\\' + file + '\\'  + sub
                Smooth = True
                run = False
            if 'unsmooth' in sub.lower():
                print('Unsmooth folder found: ' + file)
                unsmoothFolder = path + '\\' + file + '\\' + sub
                unsmoothSubName = sub
                Unsmooth = True
                run = False
            if 'vc' in sub.lower():
                print('VC folder found: ' + file)
                vcFolder = path + '\\' + file + '\\' + sub
                VC = True
                run = False
            if 'virtualcrash' in sub.lower():
                print('VC folder found: ' + file)
                vcFolder = path + '\\' + file + '\\' + sub
                VC = True
                run = False
        if run == True:
            dir = os.listdir(path + '\\' + file)
            if len(dir) != 0:
                file_count = 0
                for item in dir:
                    for ext in extensions:
                        if ext in item:
                            file_count += 1
                folders_in_folder = len(dir) - file_count
                if folders_in_folder == 0:
                    print('Unsorted files found in ' + file)
                    savePath = desktop_dir
                    fileName = 'sortByHand' + '.txt'
                    completeName = os.path.join(savePath, fileName)
                    f = open(completeName, 'a+')
                    f.write('Unsorted files found in ' + file + '\n')
                    f.close()
                else:
                    print('Searching folder: ' + file + '\\' + sub)
                    parent = True
                    search_folder(path + '\\' + file)
            else:
                print('Empty folder: ' + file)

        if not parent:
            print('For file ' + file)
            contains = [Render, Smooth, Unsmooth, VC]
            contains_str = ['Render', 'Smooth', 'Unsmooth', 'VirtualCrash']
            for i in range(0,len(contains)):
                if not contains[i]:
                    print('Missing folder: ' + contains_str[i])
                    print('Creating missing folder in ' + file)
                    os.mkdir(path + '\\' + file + '\\' + contains_str[i])
            if contains[3]:
                vc_exists = False
                for vcFile in os.listdir(vcFolder):
                    if '.obj' in vcFile:
                        vc_exists = True
                if vc_exists:
                    print('VC assest already exists for ' + file)
                else:
                    print('No .obj file for ' + file)
            if contains[2] and not vc_exists:
                #print('Creating VC asset for ' + file)
                #os.mkdir(path + '\\' + file + '\\' + 'VirtualCrash')
                unsmooth_exists = False
                for mFile in os.listdir(unsmoothFolder):
                    if'.mb' in mFile:
                        vehicle_file = mFile
                        unsmooth_exists = True
                        break
                if unsmooth_exists:
                    print('Found unsmooth asset: ' + unsmoothFolder)
                    savePath = desktop_dir
                    fileName = 'readyAssets' + '.txt'
                    completeName = os.path.join(savePath, fileName)
                    f = open(completeName, 'a+')
                    f.write('Asset ready to create: ' + file + '\n')
                else:
                    print('No unsmooth asset: ' + unsmoothFolder)

        else:
            print(file + ' is a parent folder')
            pass

        print('Next, leaving folder: ' + file + '\n')

search_folder(folder)
