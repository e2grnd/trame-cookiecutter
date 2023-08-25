import os
from paraview import simple # type: ignore # noqa 
from paraview import make_name_valid # type: ignore # noqa 

class RenderView:
    def __init__(self, fileData):
        # -----------------------------------------------------------------------------
        # ParaView pipeline
        # -----------------------------------------------------------------------------

        # Rendering setup
        view = simple.GetRenderView()
        view.UseColorPaletteForBackground = 0
        view.Background = [0.8, 0.8, 0.8]
        view.OrientationAxesVisibility = 0
        view = simple.Render() 
        self.flag2D = '2D'
        if 'flag2D' in fileData.keys():
            flag2D = fileData["flag2D"][0] 
            self.flag2D = flag2D
        dataType = fileData["dataType"] 
        fields =  fileData["fields"] 
        reader_props = fileData["reader_properties"] 
        FileNames=fileData['FileNames']
        reader = simple.OpenDataFile(FileNames)
        if reader:
            print("Success")
        else:
            print("Failed")
        
        split_tup      = os.path.splitext(FileNames[0])
        file_extension = split_tup[-1]
        # print('splitext = ', file_extension)
        if file_extension =='.ex2':
            for key, value in reader_props.items():  
                print('keys =',key,value)
                if len(value) >0:
                    reader.GetProperty(key).SetData(value)

            reader.UpdatePipeline() 
            for k in range(len(fields)):  
                arrayField = fields[k] 
                fields[k]["value"] = int(arrayField.get("value"))
                #print('arrayField =',arrayField)
                #print('reader.PointData.keys()         ',reader.PointData.keys())
                vtk_dataS  = reader.PointData[arrayField.get("text")]
                numofComponents = vtk_dataS.GetNumberOfComponents()
                # print('numofComponents         ',arrayField.get("text"),numofComponents)
                if numofComponents==1: 
                    componentNames = []
                    adjustIndex    = 0
                else: # 
                    if arrayField.get("range"):
                        dataRange = arrayField.get("range")
                    else:
                        dataRange = vtk_dataS.GetRange(-1)
                    #
                    componentNames = [{ "text": "Magnitude", "value": 0, "range":dataRange}]
                    adjustIndex    = 1
                #
                for j in range(numofComponents):
                    arrayFieldComponent = arrayField.get("components")[j+adjustIndex]
                    
                    if arrayFieldComponent.get("range"):
                        dataRange = arrayFieldComponent.get("range")
                    elif arrayField.get("range"):
                        dataRange = arrayField.get("range")
                    else:
                        dataRange = vtk_dataS.GetRange(j)
                    #  
                    componentNames.append({ "text": vtk_dataS.GetComponentName(j), "value": j+adjustIndex, "range":dataRange})#arrayField.get("range")})#
                    #
                fields[k].update({'components':componentNames})
        elif file_extension =='.vtk':
            reader.UpdatePipeline()
            vtk_data = simple.servermanager.Fetch(reader)
            for k in range(len(fields)):  
                arrayField = fields[k] 
                vtk_dataS  = vtk_data.GetPointData().GetArray(arrayField.get("text")) 
                numofComponents = vtk_dataS.GetNumberOfComponents()
                if numofComponents==1:
                    componentNames = []
                    adjustIndex    = 0
                else: # 
                    componentNames = [{ "text": "Magnitude", "value": 0, "range":vtk_dataS.GetRange(-1)}]
                    adjustIndex    = 1
                #
                for j in range(numofComponents):
                        # print('Component ',arrayField.get("text"),vtk_dataS.GetComponentName(j),vtk_dataS.GetRange(j))
                        componentNames.append({ "text": vtk_dataS.GetComponentName(j), "value": j+adjustIndex, "range":vtk_dataS.GetRange(j)})
                        #
                fields[k].update({'components':componentNames})

        self.representation = simple.GetDisplayProperties(reader, view=view)
        self.view = view
        self.fields = fields
        self.components = fields[0]['components']
        self.dataType = dataType 
 

class getColorBarActors:  
    def __init__(
        self,
        fields  
    ):  
        self.listColorBarActors  = []
        for k in range(len(fields)):
            arrayField      = fields[k] 
            fieldName       = make_name_valid(arrayField.get("text"))
            componentsArrays = arrayField['components']
            componentColorBarActors  = []
            numofComponents =  len(componentsArrays)
            #
            for j in range(numofComponents):
                componentsArray = componentsArrays[j] 
                componentName   = make_name_valid(componentsArray.get("text")) 
                colorBarName    = fieldName+'-'+componentName
                if componentName == '':
                    _min, _max = arrayField.get("range")
                else  :
                    _min, _max = componentsArray.get("range")
                lut             = simple.GetColorTransferFunction(colorBarName)
                lut.RescaleTransferFunction(_min, _max)
                lut.ApplyPreset('Jet', True)
                componentColorBarActors.append(lut) 
            self.listColorBarActors.append(componentColorBarActors)
