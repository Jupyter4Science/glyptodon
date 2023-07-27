# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/07_app.ipynb.

# %% auto 0
__all__ = ['app', 'selectionKey', 'manuscriptSelect', 'selectionInfo', 'finalizeSelection', 'metadata', 'inputObjects',
           'centuries', 'centuriesSlider', 'uploadImages', 'uploadeManuscripts', 'informationInfo', 'saveNContinue',
           'annotationTextArea', 'pageSelector', 'exportInfo', 'exportName', 'directoryOptions', 'exportButton',
           'exportDownload', 'newManuscript', 'selectedManuscript', 'figureList', 'selectManuscript', 'renderContent',
           'createFigureList', 'method']

# %% ../nbs/07_app.ipynb 4
from dash import Dash, Input, Output, callback, dcc, html
from .annotation import *
from .classes import *
from .export import *
from .information import *
from .manuscriptFiles import *
from .selection import *

# %% ../nbs/07_app.ipynb 6
app = Dash(__name__)
app.layout = html.Div(
    [
        dcc.Tabs(
            id="tabs-object",
            value="selection",
            children=[
                dcc.Tab(label="Selection", value="selection"),
                dcc.Tab(label="Information", value="information"),
                dcc.Tab(label="Annotation", value="annotation"),
                dcc.Tab(label="Export", value="export"),
            ],
        ),
        html.Div(id="current-tab"),
    ]
)

# %% ../nbs/07_app.ipynb 8
#################
### SELECTION ###
#################
selectionKey, manuscriptSelect = createManuscriptSelect()
selectionInfo = createSelectionInfo()
finalizeSelection = createFinalizeSelection()


###################
### INFORMATION ###
###################
# the ids for objects in inputObjects are: "work", "author", "language", "country", "city", "institution"
metadata, inputObjects = createInputObjects()
centuries, centuriesSlider = createCenturiesSlider()
uploadImages, uploadeManuscripts = createUploadObjects()
informationInfo = createInformationInfo()
# the id for saveNContinue is "save-and-continue"
saveNContinue = createSaveNContinue()


##################
### ANNOTATION ###
##################
annotationTextArea = createAnnotationTextArea()
pageSelector = createPageSelector()


##############
### EXPORT ###
##############
exportInfo = createExportInfo()
exportName = createExportName()
directoryOptions = createDirectoryOptions()
exportButton = createExportButton()
exportDownload = createExportDownload()

# %% ../nbs/07_app.ipynb 10
newManuscript = False
selectedManuscript = selectionKey[
    "Stavronikita Monastery Greek handwritten document Collection no.53"
]


@callback(
    Output("work", "placeholder"),
    Output("author", "placeholder"),
    Output("language", "placeholder"),
    Output("country", "placeholder"),
    Output("city", "placeholder"),
    Output("institution", "placeholder"),
    Output("centuries-slider", "value"),
    Input("manuscript-select", "value"),
    allow_duplicate=True,
    prevent_initial_call=True,  # This is here to avoid tripping callbacks from the output widgets at the very beginning
    suppress_callback_exceptions=True,
)
def selectManuscript(work):
    if work == "Create New Manuscript":
        newManuscript = True
        selectedManuscript = None
        return "", "", "", "", "", "", [1, 20]
    else:
        selectedManuscript = selectionKey[work]
        work = selectedManuscript[1]["Work"]
        author = selectedManuscript[1]["Author"]
        language = selectedManuscript[1]["Language"]
        country = selectedManuscript[1]["Country"]
        city = selectedManuscript[1]["City"]
        institution = selectedManuscript[1]["Institution"]

        ### Converts the string containing centuries into list containing the centuries as integers
        # This stores the string as a list of words. There are strings with two words and four words
        centuriesAsList = selectedManuscript[1]["Centuries"].split()

        # This picks out the relevant words and strips them of everything but the integer values
        if len(centuriesAsList) == 2:
            centuriesValue = [
                int(re.sub("[^0-9]", "", centuriesAsList[0])),
                int(re.sub("[^0-9]", "", centuriesAsList[0])),
            ]
        else:
            centuriesValue = [
                int(re.sub("[^0-9]", "", centuriesAsList[0])),
                int(re.sub("[^0-9]", "", centuriesAsList[2])),
            ]
        return work, author, language, country, city, institution, centuriesValue

# %% ../nbs/07_app.ipynb 12
@callback(Output("current-tab", "children"), Input("tabs-object", "value"))
def renderContent(tab):
    if tab == "selection":
        return html.Div(
            [
                selectionInfo,
                html.Br(),
                manuscriptSelect,
                html.Br(),
                finalizeSelection,
            ]
        )
    elif tab == "information":
        if newManuscript:
            return html.Div(
                [
                    informationInfo,
                    html.Br(),
                    html.Div(inputObjects),
                    html.Br(),
                    html.Div(
                        [
                            uploadImages,
                            uploadManuscripts,
                        ]
                    ),
                    html.Br(),
                    saveNContinue,
                ]
            )
        else:
            return html.Div(
                [
                    informationInfo,
                    html.Br(),
                    html.Div(inputObjects),
                    html.Br(),
                    saveNContinue,
                ]
            )
    elif tab == "annotation":
        return html.Div(
            [
                dcc.Graph(
                    id="annotation-figure",
                    config={
                        "modeBarButtonsToAdd": ["drawline", "drawrect", "eraseshape"]
                    },
                    style={
                        "height": 900,
                        "width": 800,
                    },
                ),
                pageSelector,
                annotationTextArea,
            ]
        )
    elif tab == "export":
        return html.Div(
            [
                exportInfo,
                exportName,
                directoryOptions,
                exportButton,
                exportDownload,
            ]
        )

# %% ../nbs/07_app.ipynb 14
def createFigureList(targetDirectory):
    imagePaths = manuscriptImages(targetDirectory)
    
    figureList=[]
    for path in imagePaths:
        figureList.append(createAnnotationFigure(path))
        
    return figureList

# %% ../nbs/07_app.ipynb 17
figureList = []


@callback(
    Output("annotation-figure", "figure"),
    Output("page-selector", "options"),
    Input("finalize-selection", "n_clicks"),
    prevent_initial_call=True,
)
def method():
    pass

# %% ../nbs/07_app.ipynb 19
if __name__ == "__main__":
    app.run(debug=True)