# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/05_classes.ipynb.

# %% auto 0
__all__ = ['BBox', 'Line']

# %% ../nbs/05_classes.ipynb 3
from fastcore.utils import *
import csv
import os

# %% ../nbs/05_classes.ipynb 9
class BBox:
    type = "rect"
    line = dict(color="grey")
    opacity = 0.6

# %% ../nbs/05_classes.ipynb 11
@patch
def __init__(self: BBox, points: dict, lineNo=-1, index=-1):
    self.x0 = points["x0"]
    self.y0 = points["y0"]
    self.x1 = points["x1"]
    self.y1 = points["y1"]
    self.midpoint = (self.x0 + self.x1) / 2
    self.lineNo = lineNo
    self.index = index

# %% ../nbs/05_classes.ipynb 14
@patch
def isLine(self: BBox, line):
    y = line.midpoint
    y0 = self.y0
    y1 = self.y1
    dif = abs(y0-y1)
    
    if dif <= abs(y-y0) or dif <= abs(y-y1):
        return False
    
    self.lineNo = line.index
    
    return True

# %% ../nbs/05_classes.ipynb 16
@patch
def __gt__(self:BBox, other:BBox):
    return self.midpoint > other.midpoint

@patch
def __lt__(self:BBox, other:BBox):
    return self.midpoint < other.midpoint

@patch
def __eq__(self:BBox, other:BBox):
    return self.midpoint == other.midpoint

# %% ../nbs/05_classes.ipynb 18
@patch_to(BBox, cls_method=True)
def sortBBoxes(bboxList):
    size = len(bboxList)
    
    for i in range(size):
        minimum = i
        minValueI = bboxList[minimum]
        
        for j in range(j+1, size):
            if bboxList[j] < bboxList[minimum]:
                minimum = j
                minValueJ = bboxList[minimum]
        
        if minimum != i:
            bboxList[i] = minValueJ
            bboxList[minimum] = minValueI
        
    index = 1
    for bbox in bboxList:
        bbox.index = index
        index = index + 1
        
    return bboxList

# %% ../nbs/05_classes.ipynb 20
@patch_to(BBox, cls_method=True)
def bboxesToCSV(targetDirectory, bboxes, fileName):
    baseDirectory = os.getcwd()
    os.chdir(targetDirectory)
    
    # Prevents an already written csv file from having unwanted data
    if os.path.exists(fileName):
        os.remove(fileName)

    f = open(fileName, "w", newline="")
    writer = csv.writer(f)
    for bbox in bboxes:
        writer.writerow([bbox.x0, bbox.y0, bbox.x1, bbox.y1, bbox.lineNo, bbox.index])

    os.chdir(baseDirectory)

# %% ../nbs/05_classes.ipynb 22
@patch_to(BBox, cls_method=True)
def csvToLines(targetFile):
    csvReader = csv.reader(targetFile, delimiter=",")

    bboxes = []
    for row in csvReader:
        bbox = Line(
            x0=row[0], y0=row[1], x1=row[2], y1=row[3], lineNo=row[4], index=row[5]
        )
        bboxes.append(bbox)

    return bbox

# %% ../nbs/05_classes.ipynb 24
class Line:
    type = "line"
    line = dict(color="grey")
    opacity = 0.6

# %% ../nbs/05_classes.ipynb 26
@patch
def __init__(self: Line, x0, y0, x1, y1, index=-1):
    self.x0 = x0
    self.y0 = y0
    self.x1 = x1
    self.y1 = y1
    self.midpoint = (self.y0 + self.y1) / 2
    self.index = index

# %% ../nbs/05_classes.ipynb 28
@patch
def __gt__(self:Line, other:Line):
    return self.midpoint > other.midpoint

@patch
def __lt__(self:Line, other:Line):
    return self.midpoint < other.midpoint

@patch
def __eq__(self:Line, other:Line):
    return self.midpoint == other.midpoint

# %% ../nbs/05_classes.ipynb 30
@patch_to(Line, cls_method=True)
def sortLines(lineList):
    size = len(lineList)
    
    for i in range(size):
        minimum = i
        minValueI = lineList[minimum]
        
        for j in range(j+1, size):
            if lineList[j] < lineList[minimum]:
                minimum = j
                minValueJ = lineList[minimum]
        
        if minimum != i:
            lineList[i] = minValueJ
            lineList[minimum] = minValueI
        
    index = 1
    for line in lineList:
        line.index = index
        index = index + 1
        
    return lineList

# %% ../nbs/05_classes.ipynb 32
@patch_to(Line, cls_method=True)
def linesToCSV(targetDirectory, lines, fileName):
    baseDirectory = os.getcwd()
    os.chdir(targetDirectory)
    
    # Prevents an already written csv file from having unwanted data
    if os.path.exists(fileName):
        os.remove(fileName)

    f = open(fileName, "w", newline="")
    writer = csv.writer(f)
    for line in lines:
        writer.writerow([line.x0, line.y0, line.x1, line.y1, line.index])

    os.chdir(baseDirectory)

# %% ../nbs/05_classes.ipynb 34
@patch_to(Line, cls_method=True)
def csvToLines(targetFile):
    csvReader = csv.reader(targetFile, delimiter=",")

    lines = []
    for row in csvReader:
        line = Line(x0=row[0], y0=row[1], x1=row[2], y1=row[3], index=row[4])
        lines.append(line)
        
    return lines