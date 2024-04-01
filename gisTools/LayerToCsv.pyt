# -*- coding: utf-8 -*-

import arcpy
import pandas as pd


class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "Toolbox"
        self.alias = "toolbox"

        # List of tool classes associated with this toolbox
        self.tools = [Tool]


class Tool(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "LayerToCsv"
        self.description = "Layer to csv"
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        
        param_input = arcpy.Parameter(
            name="in_features",
            displayName="Input Features",
            direction="Input",
            parameterType="Required",
            datatype="GPFeatureLayer"
        )

        param_output = arcpy.Parameter(
            name="output", 
            displayName="Output Features", 
            direction="Output", 
            parameterType="Derived", 
            datatype="DEFile"
        )

        params = [param_input, param_output]

        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""

        parameters = ParametersWrapper(parameters)
        
        field_names = []
        input_feature = parameters.in_features.valueAsText
        arcpy.AddMessage(input_feature)
        output = parameters.output.valueAsText

        fields = arcpy.ListFields(input_feature)
        fields_name = []
        for field in fields:
            fields_name += [field.name]
        fields_len = len(fields_name)

        df = pd.DataFrame()
        for field in fields:
            df.insert (0, field.name, 0, allow_duplicates = False)
        df = df.loc[:,::-1]

        cont = 1
        i = 0
        for fields in fields_name:
            content = [row[0] for row in arcpy.da.SearchCursor(input_feature, fields_name[i])]
            df[fields_name[i]] = content
            i += 1
            if i == fields_len:
                break
        
        output = df.to_csv(arcpy.env.scratchFolder+'/out.csv', index=False)
        arcpy.SetParameter(1, arcpy.env.scratchFolder+'/out.csv')

        return

class ParametersWrapper(object):
    def __init__(self, parameters):
        for p in parameters:
            self.__dict__[p.name] = p