# Project M Raw Manager
# 3/25/22
# v.01
#
# Configure multiple versions of Dolphin
# Define multiple SD.raw files for each version
# Press play to start your desired version of Project M/+

import os
import json
import sys
# import subprocess

# DEV
from tkinter import Frame, Tk, StringVar, Label, Entry, Button, Listbox, PhotoImage, filedialog
from tkinter.ttk import Combobox
from PIL import Image as PILImage

# For Md5 hashes, if I ever use them
# import hashlib

global sdRawFiles

if getattr(sys, 'frozen', False):
        # The application is frozen
        scriptPath = os.path.dirname(sys.executable)
        configPath = scriptPath + '/config.json'
else :
    # The application is not frozen
    scriptPath = os.path.dirname(__file__)
    configPath = scriptPath + '/config.json'

def initConfig() :

    if os.path.exists(configPath) :

        with open(configPath, 'r') as f:
            config = json.loads(f.read())

            sdRawFiles = []
            for i in config['sdRawFiles'] :
                sdRawFiles.append(config['sdRawFiles'][i]['name'])

            return config
    
    else :

        with open(configPath, 'w') as f:
            config = {"firstTime": "True","imgs": {"icon_dolphin_default": "/assets/icon_dolphin_default_32x32.png","icon_dolphin_pplus": "/assets/icon_dolphin_pplus_32x32.png"},"dolphins": {},"sdRawFiles": {}}
            json.dump(config, f, indent = 4)

        with open(configPath, 'r') as f:
            config = json.loads(f.read())

            sdRawFiles = []
            for i in config['sdRawFiles'] :
                sdRawFiles.append(config['sdRawFiles'][i]['name'])

            return config

def saveConfig() :
    with open(configPath, 'w') as f:
        json.dump(config, f, indent = 4)
    
    sdRawFiles = []
    for i in config['sdRawFiles'] :
        sdRawFiles.append(config['sdRawFiles'][i]['name'])

    print('Saved config.')

#################
# MD5 Functions #
#################

# def getMD5(filepath) :

#     with open(filepath, 'rb') as f :
#         data = f.read()
#         md5_returned = hashlib.md5(data).hexdigest()
#         return md5_returned

#################


def browseForDolphinExe() :
    selectedFile = filedialog.askopenfile(filetypes=[("Applications", "*.exe")], title = 'Select a Dolphin EXE File')
    # stringVar.set(selectedFile)
    return selectedFile.name

def browseForImage() :
    selectedFile = filedialog.askopenfile(filetypes=[("Images", "*.png")], title = "Select an Image File")
    return selectedFile.name

def browseForSDRaw() :
    selectedFile = filedialog.askopenfile(filetypes=[("RAW", "*.raw")], title = "Select an SD.raw file")
    return selectedFile.name

def browseForFolder(initialDir = '') :
    selectedDir = filedialog.askdirectory(initialdir = initialDir)
    return selectedDir

def addDolphinDialogue(firstTime = False) :

    def setDolphinPath() :
        # Browse for Dolphin Exe
        path = browseForDolphinExe()
        addTabDolphinEntry.delete(0, 'end')
        addTabDolphinEntry.insert(0, path)
        dolphinPath.set(path)
        
        # Automatically set the sd.raw path
        userWii = os.path.dirname(dolphinPath.get())
        userWii = userWii + '/User/Wii'

        addSDRawFolderEntry.delete(0, 'end')
        addSDRawFolderEntry.insert(0, userWii)
        sdRawPath.set(userWii)

        # Fill in list of sd.raw files
        populateSDRawList()

    def setSDRawPath() :

        # Manually browse for sd.raw folder
        userWii = os.path.dirname(dolphinPath.get())
        userWii = userWii + '/User/Wii'

        path = browseForFolder(userWii)
        addSDRawFolderEntry.delete(0, 'end')
        addSDRawFolderEntry.insert(0, path)
        sdRawPath.set(path)

        # Fill in list of sd.raw files
        populateSDRawList()

    def populateSDRawList() :

        sdRawListBox.delete(0, 'end')

        global sdRawList
        sdRawList = []
        for file in os.listdir(sdRawPath.get()) :
            if file.endswith('.raw') and file != 'sd.raw' and file != 'OLDsd.raw' :
                # fileMD5 = getMD5(sdRawPath.get() + '/' + file) ## MD5 hash checking, too slow
                sdRawList.append(file)
        
        for i in sdRawList :
            sdRawListBox.insert('end', i)

    def setIconPath() :
        # Browse for custom icon file
        # This file will be resized and saved to assets folder upon clicking "Submit"
        path = browseForImage()
        addTabIconEntry.delete(0, 'end')
        addTabIconEntry.insert(0, path)
        newIconPath.set(path)

    def submit() :
        if not dolphinPath.get().__contains__('Dolphin.exe') :
            print('No Dolphin.exe selected.')
        elif addSDRawFolderEntry.get() == '' :
            print('sd.raw folder cannot be left blank.')
        elif sdRawList == [] :
            print('No sd.raw files detected.')

        else :
            newDolphin = dolphinPath.get()
            newName = addTabNameEntry.get()
            newIcon = addTabIconEntry.get()
            newSDRawPath = addSDRawFolderEntry.get()

            if newIcon == '' :
                # If icon is left blank, use the default
                newIconPath = config['imgs']['icon_dolphin_default']
            else :
                # If custom icon was selected, resize and save the image
                newIconPath = newIcon.split('/')
                newIconPath = newIconPath[len(newIconPath)-1]
                newIconPath = '/assets/' + newIconPath

                newIconImg = PILImage.open(newIcon)
                newIconResized = newIconImg.resize((32,32), resample=0) 
                newIconResized.save(scriptPath + newIconPath)
            
            # Add sd.raw files to the config file
            for i in sdRawList :
                newSdRawFile = {
                    i: {
                        "name": i,
                        "path": newSDRawPath + '/' + i,
                        "dolphin": newDolphin,
                        "active": "False"
                    }
                }
                config['sdRawFiles'].update(newSdRawFile)

            # Add Dolphin version to the config file
            newDolphinJSON = {
                newName: {
                    "name": newName,
                    "path": newDolphin,
                    "icon": newIconPath,
                    "defaultSD": sdRawList[0],
                    "userWiiPath": newSDRawPath,
                    "currentSDRaw": ""
                }
            }
            config['dolphins'].update(newDolphinJSON)
            
            saveConfig()

        addTabRoot.destroy()

        if firstTime == False :
            root.destroy()
        else :
            config['firstTime'] = "False"
            saveConfig()

        initMainGUI()

    addTabRoot = Tk()
    addTabRoot.title('Add a Dolphin version to the launcher')

    dolphinPath = StringVar()
    newIconPath = StringVar()
    newTabName = StringVar()
    sdRawPath = StringVar()
    newTabName.set('Dolphin')

    warningLabel = Label(addTabRoot, fg = 'red', text = 'WARNING:\nPlease make sure you RENAME your current sd.raw file so it is not lost.\nExample: Rename "sd.raw" to "pplus2.29.raw" or something similar.\nThis program WILL overwrite the sd.raw file.\n\nRead the README.txt for more information.')
    warningLabel.pack(padx = 16, pady = 16, side = 'top')

    addNameLabel = Label(addTabRoot, text = 'Dolphin Name')
    addNameLabel.pack(padx = 8, pady = 4, side = 'top')

    addTabNameEntry = Entry(addTabRoot, width = 58)
    addTabNameEntry.pack(padx = 8, pady = 4, ipady = 4)
    addTabNameEntry.insert(0, newTabName.get())

    ###############
    addIconFrame = Frame(addTabRoot)

    addIconLabel = Label(addIconFrame, text = 'Path to Icon Image (Optional - Uses the Dolphin logo if left blank)')
    addIconLabel.pack(pady = 4, side = 'top')

    addTabIconEntry = Entry(addIconFrame, width = 40, text = 'Icon (Can be left blank)', textvariable = newIconPath)
    addTabIconEntry.pack(side = 'left', padx = 4, pady = 4, ipady = 4)

    addTabIconBrowse = Button(addIconFrame, width = 12, text = "Browse", command = setIconPath)
    addTabIconBrowse.pack(padx = 4, side = 'right')
    addIconFrame.pack(padx = 8, pady = 8)
    ###############

    ###############
    addDolphinFrame = Frame(addTabRoot)

    addDolphinLabel = Label(addDolphinFrame, text = 'Path to Dolphin.exe')
    addDolphinLabel.pack(pady = 4, side = 'top')

    addTabDolphinEntry = Entry(addDolphinFrame, width = 40, textvariable = dolphinPath)
    addTabDolphinEntry.pack(side = 'left', padx = 4, pady = 4, ipady = 4)

    addTabDolphin = Button(addDolphinFrame, width = 12, text = "Browse", command = setDolphinPath)
    addTabDolphin.pack(padx = 4, side = 'right')
    addDolphinFrame.pack(padx = 8, pady = 8)
    ###############

    ###############
    addSDRawFolderFrame = Frame(addTabRoot)

    addSDRawFolderLabel = Label(addSDRawFolderFrame, text = 'SD.raw Folder (Usually Dolphin/User/Wii)')
    addSDRawFolderLabel.pack(pady = 4, side = 'top')

    addSDRawFolderEntry = Entry(addSDRawFolderFrame, width = 40, textvariable = sdRawPath)
    addSDRawFolderEntry.pack(padx = 4, side = 'left', pady = 4, ipady = 4)

    addTabSDRawFolder = Button(addSDRawFolderFrame, width = 12, text = "Browse", command = setSDRawPath)
    addTabSDRawFolder.pack(padx = 4, side = 'right')
    addSDRawFolderFrame.pack(padx = 8, pady = 8)
    ###############

    ###############
    sdRawListFrame = Frame(addTabRoot)

    sdRawListLabel = Label(sdRawListFrame, text = 'Detected ".raw" files (You can add more after the initial setup)')
    sdRawListLabel.pack(pady = 4, side = 'top')

    sdRawListBox = Listbox(sdRawListFrame, width = 58)
    # sdRawListBox['columns'] = ('SD.raw File')
    sdRawListBox.pack(pady = 8)

    sdRawListFrame.pack(padx = 8, pady = 8)
    ###############

    addTabSubmit = Button(addTabRoot, width = 12, text = "Submit", command = submit)
    addTabSubmit.pack(padx = 8, pady = 8, side = 'bottom')

    addTabRoot.mainloop()

def addSDRawDialogue() :

    def setSDRawPath() :
        path = browseForSDRaw()
        addSDRawPathEntry.delete(0, 'end')
        addSDRawPathEntry.insert(0, path)
        sdRawPath.set(path)

    def submit() :
        if not sdRawPath.get().__contains__('.raw') :
            print('.raw file not selected!')
        
        else :
            newName = sdRawPath.get()
            newName = os.path.basename(newName)
            newSdRaw = sdRawPath.get()
            newDolphin = config['dolphins'][addSDDolphinComboBox.get()]['path']

            newSdRawFile = {
                newName: {
                    "name": newName,
                    "path": newSdRaw,
                    "dolphin": newDolphin,
                    "active": "False"
                }
            }

            config['sdRawFiles'].update(newSdRawFile)
            
            saveConfig()

        addSDRawRoot.destroy()
        root.destroy()
        initMainGUI()

    addSDRawRoot = Tk()
    addSDRawRoot.title('Add a .raw file to an existing version of Dolphin')

    sdRawPath = StringVar()
    newTabName = StringVar()
    newTabName.set('New SD.raw')

    infoLabel = Label(addSDRawRoot, fg = 'red', text = 'It is highly recommended to have already copied your new .raw file\nto the correct directory with its unique name.')
    infoLabel.pack(padx = 16, pady = 16, side = 'top')

    addNameLabel = Label(addSDRawRoot, text = 'Dolphin Version')
    addNameLabel.pack(padx = 8, pady = 8, side = 'top')

    # addSDRawNameEntry = Entry(addSDRawRoot, width = 30, textvariable = newTabName)
    # addSDRawNameEntry.pack(padx = 8, pady = 4)
    # addSDRawNameEntry.insert(0, newTabName.get())

    dolphinList = []
    for i in config['dolphins'] :
        dolphinList.append(config['dolphins'][i]['name'])

    addSDDolphinComboBox = Combobox(addSDRawRoot, values = dolphinList, state = 'readonly') ##
    addSDDolphinComboBox.current(0)
    addSDDolphinComboBox.pack(padx = 8, pady = 4)

    ###############
    addSDRawFrame = Frame(addSDRawRoot)

    addSDRawLabel = Label(addSDRawFrame, text = 'Path to SD.raw')
    addSDRawLabel.pack(padx = 8, pady = 4, side = 'top')

    addSDRawPathEntry = Entry(addSDRawFrame, width = 30, textvariable = sdRawPath)
    addSDRawPathEntry.pack(padx = 8, side = 'left')

    addSDRawButton = Button(addSDRawFrame, width = 12, text = "Browse", command = setSDRawPath)
    addSDRawButton.pack(padx = 8, side = 'right')
    addSDRawFrame.pack(padx = 8, pady = 4)
    ###############

    addSDRawSubmit = Button(addSDRawRoot, width = 12, text = "Submit", command = submit)
    addSDRawSubmit.pack(padx = 8, pady = 8, side = 'bottom')

    addSDRawRoot.mainloop()

def renameSdRawFile(currentSD, newSD, sdPath, dolphin) :

    if config['dolphins'][dolphin]['currentSDRaw'] == "" :
        if os.path.exists(sdPath + '/sd.raw') :
            os.rename(sdPath + '/sd.raw', sdPath + '/OLDsd.raw')

    if 'sd.raw' in os.listdir(sdPath) :
        for i in config['sdRawFiles'] :
            if i == currentSD :
                originalSdName = config['sdRawFiles'][i]['path']
                os.rename(sdPath + '/sd.raw', originalSdName)
                config['sdRawFiles'][i]['active'] = 'False'
                saveConfig()

    newSdPath = config['sdRawFiles'][newSD]['path']
    os.rename(newSdPath, sdPath + '/sd.raw')
    config['sdRawFiles'][newSD]['active'] = 'True'
    config['dolphins'][dolphin]['currentSDRaw'] = newSD
    saveConfig()

    with open(sdPath + '/currentSDRaw.txt', 'w') as f:
        f.write(newSD)

class tabGUI () :

    def __init__(self, masterFrame, name, path, icon, defaultSD) :

        def launchDolphin() :
            
            launchSD = self.sdraw.get()
            if launchSD != config['dolphins'][self.name]['currentSDRaw'] :

                renameSdRawFile(config['dolphins'][self.name]['currentSDRaw'], launchSD, config['dolphins'][self.name]['userWiiPath'], self.name)
            
            # root.destroy()

            os.chdir(os.path.dirname(config['dolphins'][self.name]['path']))
            dolphinExe = config['dolphins'][self.name]['path'].split('/')
            dolphinExe = dolphinExe[len(dolphinExe)-1]
            # os.system(dolphinExe)
            os.system(dolphinExe)

            # subprocess.run(config['dolphins'][self.name]['path'])
            # subprocess.call([config['dolphins'][self.name]['path']])

        def setDefaultSD() :
            self.defaultSD = self.sdraw.get()
            config['dolphins'][self.name]['defaultSD'] = self.defaultSD
            saveConfig()

        self.name = name
        self.path = path
        self.icon = icon

        try:
            self.icon = PhotoImage(file = scriptPath + self.icon)
        except:
            print('No icon path specified for ' + self.name)
            self.icon = PhotoImage(file = scriptPath + config['imgs']['icon_dolphin_default'])

        self.frame = Frame(masterFrame, bg = '#dddddd') # This frame gets packed by the main script

        self.button = Button(self.frame, text = self.name, image = self.icon, width = 256, compound = 'left', command = launchDolphin)
        self.button.pack(side = 'left', padx = 8, pady = 4)

        self.sdRawFiles = []
        for i in config['sdRawFiles'] :
            if config['sdRawFiles'][i]['dolphin'] == config['dolphins'][self.name]['path'] :
                self.sdRawFiles.append(i)

        self.sdraw = Combobox(self.frame, values = self.sdRawFiles, state = 'readonly') ##

        self.defaultSD = defaultSD
        self.sdraw.current(self.sdRawFiles.index(self.defaultSD))

        self.setDefaultSDButton = Button(self.frame, text = 'Set As Default', width = 16, command = setDefaultSD)
        self.setDefaultSDButton.pack(side = 'right', padx = 8, pady = 4)

        self.sdraw.pack(side = 'right', padx = 8, pady = 4) ##

def initMainGUI() :

    initConfig()

    global root
    root = Tk()
    root.title("Project M Raw Manager")

    rootFrame = Frame(root)
    rootFrame.pack(padx = 16, pady = 16)

    global tabFrame
    tabFrame = Frame(rootFrame)
    tabFrame.pack(side = 'top')

    tabs = []
    for i in config['dolphins'] :

        tabs.append(tabGUI(
            name = config['dolphins'][i]['name'], 
            path = config['dolphins'][i]['path'], 
            icon = config['dolphins'][i]['icon'], 
            defaultSD = config['dolphins'][i]['defaultSD'], 
            masterFrame = tabFrame))

    for i in tabs :
        i.frame.pack(padx = 4, pady = 4, ipadx = 4, ipady = 4)

    ################

    footerFrame = Frame(rootFrame)
    footerFrame.pack(pady = 8)

    addTabButton = Button(footerFrame, width = 24, text = 'Add Dolphin', command = addDolphinDialogue)
    addTabButton.pack(padx = 8, side = 'left')

    addSDRawButton = Button(footerFrame, width = 24, text = 'Add SD Raw File', command = addSDRawDialogue)
    addSDRawButton.pack(padx = 8, side = 'right')

    root.mainloop()

if __name__ == '__main__' :

    config = initConfig()

    if config['firstTime'] == 'True' :
        # firstTimeDialogue()
        addDolphinDialogue(firstTime = True)

    else :
        initMainGUI()

