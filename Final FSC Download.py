# Final FSC Download
# no KML due to bug and allows user entry file name
# -*- coding: utf-8 -*-
import arcpy
import os
import shutil


class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "Audit Polygon Download"
        self.alias = "AuditPolygonDownload"

        # List of tool classes associated with this toolbox
        self.tools = [AuditPolygonDownload]


class AuditPolygonDownload(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "FSC Audit Polygon Download"
        self.description = "Allows user to download the polygon drawn in the application as a KML or shapefile"
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        feature_collection = arcpy.Parameter(
            name = "feature_collection",
            displayName = "Input Audit Polygon",
            datatype = "GPFeatureLayer",
            parameterType = "Required",
            direction = "Input")

        out_name = arcpy.Parameter(
            name = "out_name",
            displayName = "File Name",
            datatype = "GPString",
            parameterType = "Required",
            direction = "Input")

        output_file = arcpy.Parameter(
            name="output_file",
            displayName="Output File",
            datatype="DEFile",
            parameterType="Derived",
            direction="Output")

        return [feature_collection, out_name, output_file]

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


    def unpackParameters(self, parameters):
        """
        Unpack a list of Arcpy Parameters to a dictionary
        :param parameters: list of arcpy Parameter objects
        :return: dictionary of parameters using the parameter name as the key
        """
        params = {p.name: p for p in parameters}
        return params

    def execute(self, parameters, messages):
        # Bring imports and set overwrite
        arcpy.overwriteOutput = True

        feature_collection = parameters[0].value
        file_name = parameters[1].valueAsText 
      
        """The source code of the tool."""
        params = self.unpackParameters(parameters)
        arcpy.AddMessage(params)

        # turn feature collection to temp feature class in memory
        temp_fc = arcpy.conversion.FeatureClassToFeatureClass(feature_collection, "memory", file_name)
        arcpy.AddMessage("Temporary Feature Class Created")

        # set scratch directory
        # Where I am going to put the new folder
        directory = arcpy.env.scratchFolder
        arcpy.AddMessage(f"Scratch Directory: {directory}")

        # change current directory to the scratch directory
        os.chdir(directory)
        arcpy.AddMessage("Scratch set as current directory")

    
        # create a subfolder within the scratch to place the individual shapefiles and then zip the folder
        new_folder = file_name
        # make the folder
        os.makedirs(new_folder)
        subfolder = os.path.abspath(new_folder)
        arcpy.AddMessage("New subfolder created")

        # convert fc to shapefile
        arcpy.conversion.FeatureClassToShapefile(temp_fc, subfolder)
        arcpy.AddMessage(f"Shapefile -- {file_name} created")

        # zip shapefile
        zipped_folder = shutil.make_archive(file_name, 'zip', subfolder)
        arcpy.AddMessage("Folder zipped")
        arcpy.AddMessage(zipped_folder)

        #set ouput parameter
        arcpy.SetParameter(2, zipped_folder)

    
        return
