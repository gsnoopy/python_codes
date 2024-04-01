import arcpy
import pandas as pd
import os.path

class Toolbox(object):
    def __init__(self):

        self.label = "ExcelTool"
        self.alias = "ExcelTool"
        self.tools = [Tool]

class Tool(object):
    def __init__(self):
        self.label = "ExcelTool"
        self.description = ""
        self.canRunInBackground = False

    def getParameterInfo(self):

        param_excel_file = arcpy.Parameter(
            name="excel_file", 
            displayName="Arquivo XLSX", 
            direction="Input", 
            parameterType="Required", 
            datatype="DEFile"
        )

        param_choices = arcpy.Parameter(
            displayName="list_names disponíveis",
            name="listname",
            datatype="GPString",
            parameterType="Required",
            direction="Input",
            multiValue=True
        )

        param_output_folder = arcpy.Parameter(
            name="output_folder", 
            displayName="Pasta em que a saída será salva", 
            direction="Input", 
            parameterType="Required", 
            datatype="DEFolder"
        )

        param_filename = arcpy.Parameter(
            name="filename",
            displayName="Nome do arquivo de saída", 
            direction="Output", 
            parameterType="Required", 
            datatype="GPString"
        )

        param_choices.filter.list =  []
        param_excel_file.filter.list = ['xlsx']
        params = [param_excel_file, param_choices, param_output_folder, param_filename]

        return params

    def isLicensed(self):
        return True

    def updateParameters(self, parameters):
        
        parameters = ParametersWrapper(parameters)
        
        if changed(parameters.excel_file):
            excel_filepath = parameters.excel_file.valueAsText
            if os.path.exists(excel_filepath) == False:
                parameters.listname.filter.list =  []
            else:
                xlsx = pd.ExcelFile(excel_filepath)
                df = pd.read_excel(xlsx, 'choices', index_col='list_name').dropna(how='all')
                choices = df.index.unique().to_list()
                parameters.listname.filter.list =  choices
        return

    def updateMessages(self, parameters):

        parameters = ParametersWrapper(parameters)

        if parameters.excel_file.hasError():
            parameters.excel_file.clearMessage()
            parameters.excel_file.setErrorMessage("Arquivo inexistente!")
            
        return

    def execute(self, parameters, messages):

        parameters = ParametersWrapper(parameters)

        excel_filepath = parameters.excel_file.valueAsText
        excel_filename = parameters.filename.valueAsText
        output_path = parameters.output_folder.valueAsText

        xlsx = pd.ExcelFile(excel_filepath)
        df = pd.read_excel(xlsx, 'choices', index_col='list_name').dropna(how='all')

        df.fillna('', inplace=True)
        df = df.loc[:, df.ne('').any()]

        #choices = df.index.unique().to_list()
        select = parameters.listname.valueAsText
        choices = select.split(";")
        d = {}

        with pd.ExcelWriter(output_path+'/'+excel_filename+'.xlsx') as writer:
            for name in choices:
                d[name] = pd.DataFrame(df.loc[name]).fillna('')
                d[name] = d[name].loc[:, d[name].ne('').any()]
                d[name].to_excel(writer, sheet_name=name, index=False)

        return

class ParametersWrapper(object):
    def __init__(self, parameters):
        for p in parameters:
            self.__dict__[p.name] = p

last_values = {}
def changed(parameter):
    global last_values
    if parameter.name not in last_values:
        last_values[parameter.name] = parameter.valueAsText
        return True
    last_value = last_values[parameter.name]
    current_value = parameter.valueAsText
    ans = (last_value != current_value)
    last_values[parameter.name] = current_value
    return ans
