# AUTOGENERATED! DO NOT EDIT! File to edit: ../manuscriptFiles.ipynb.

# %% auto 0
__all__ = ['createManuscriptDirectory', 'dictToList', 'directoryNameClean', 'saveImages', 'currentManuscripts']

# %% ../manuscriptFiles.ipynb 3
import os
import io
import cv2
import numpy as np

# %% ../manuscriptFiles.ipynb 5
def createManuscriptDirectory(metadata:dict):
    # This function creates a directory and metadata file for a new manuscript and returns the new manuscript root directory
    
    # Establishing the baseDirectory the web app is running in
    baseDirectory = os.getcwd()
    os.chdir('manuscripts')
    allManuscriptsDirectory = os.getcwd()

    # Creating the root directory for a new manuscript
    title = directoryNameClean(metadata['Work'])
    manuscriptDirectory = os.path.join(allManuscriptsDirectory,title)
    os.mkdir(manuscriptDirectory)
    
    # Creating directories
    imagesDirectory = os.path.join(manuscriptDirectory,'images')
    os.mkdir(imagesDirectory)
    statesDirectory = os.path.join(manuscriptDirectory,'states')
    os.mkdir(statesDirectory)
    exportTranscriptDirectory = os.path.join(manuscriptDirectory,'exportTranscripts')
    os.mkdir(exportTranscriptDirectory)
    importTranscriptDirectory = os.path.join(manuscriptDirectory,'importTranscripts')
    os.mkdir(importTranscriptDirectory)
    
    # Creating metadata file as config file
    os.chdir(manuscriptDirectory)
    f = open(title + '.cfg', 'w')
    
    # Writes relevant metadata to file
    printable = dictToList(metadata)
    for data in printable:
        f.write(data + '\n')
    
    os.chdir(baseDirectory)
    
    return manuscriptDirectory

# %% ../manuscriptFiles.ipynb 8
def dictToList(thisdict:dict):
    # This function turns a dictionary into a list of printable strings
    keys = []
    for key in thisdict.keys():
        keys.append(key)

    values = []
    for value in thisdict.values():
        values.append(value)
    
    printable = []
    for i in range(len(keys)):
        printable.append(str(keys[i]) + ':' + str(values[i]))
    
    return printable

# %% ../manuscriptFiles.ipynb 11
def directoryNameClean(string):
    # This function removes any of the illegal characters for directories
    illegalChars = ['\\','#','%','&','{','}','<','>','*','?','/',' ','$','!',"'",'"',':','@','+','`','|','=']
    
    for char in illegalChars:
        for i in range(len(string)):
            if string[i] == char:
                string = string[:i] + string[i+1:]
                break
    
    if len(string) > 26:
        string = string[0:26]
    
    return string.lower()

# %% ../manuscriptFiles.ipynb 14
def saveImages(files:dict, targetDirectory):
    # This function saves content from memory into storage using the keys in the passed files dict (from a FileUpload widget)
    # This 
    baseDirectory = os.getcwd()
    os.chdir(os.path.join(targetDirectory, 'images'))
    
    # Not sure what exactly this does, this is what I borrowed
    for i in range(len(files)):
        # I think this takes the content from the memory marker and reads it into Python readable code
        img_stream = io.BytesIO(files[i]['content'])
        # I have no clue why Numpy is needed here (probably some ungodly matrices and formats), but this turns the data into a cv2 readable image
        img = cv2.imdecode(np.frombuffer(img_stream.read(), np.uint8), 1)
        # This writes an image to some target directory
        cv2.imwrite(files[i]['name'], img)
        
    os.chdir(baseDirectory)

# %% ../manuscriptFiles.ipynb 19
def currentManuscripts():
    # If this is run on any computer, it will have a unique file structure. This implementation works with that file structure.
    baseDirectory = os.getcwd()
    manuscriptDirectory = os.path.join(baseDirectory,'manuscripts')
    
    # This is necessary to keep directories accessible. Without os.path.join, we can't keep a full directory name and access files inside specific directories
    directories = []
    for path in os.listdir(manuscriptDirectory):
        directories.append(os.path.join(manuscriptDirectory,path))
    
    # This is necessary to store metadata from .cfg files
    manuscriptMetadata = []
    
    # This is necessary to search each directory in the manuscripts folder
    for directory in directories:
        # This looks through each file in a given directory
        for file in os.listdir(directory):
            # This opens config files and reads metadata from them
            if file.endswith('.cfg'):
                fileDirectory = os.path.join(directory,file)
                f = open(fileDirectory, 'r')
                metadata = {}

                for line in f:
                    key, value = line.split(':')
                    metadata[key] = value[:-1]

                manuscriptMetadata.append([directory, metadata])
    
    os.chdir(baseDirectory)
    return manuscriptMetadata