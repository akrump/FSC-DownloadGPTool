# Download GP Tool FSC
#Goal**: Create a gp service that can accept the JSON/Feature collection of the Audit Polygon of Interest and allow user to download polygon as shapefile/KMZ.

import os
import arcpy
from os import path as p
import zipfile
arcpy.overwriteOutput = True

# Parameter 1, feature collection from application (user drawn poly)
feature_collection = arcpy.GetParameterAsText(0)

# Paramter 2, user names the output
file_name = arcpy.GetParameterAsText(1)

# Parameter 3, file type. Shapefile or KML. User selects from dropdown
file_type = arcpy.GetParameterAsText(2)



### Convert Input to Feature Class

# Feature Collection to Feature Class Store in memory
temp_fc = arcpy.conversion.FeatureClassToFeatureClass(feature_collection, "memory", file_name)
print(temp_fc)

arcpy.SetProgressorLabel("Temporary Feature Class Created")
arcpy.AddMessage("Temporary Feature Class Created in memory")

# set up scratch workspace.
scratch = arcpy.env.scratchFolder # where to put new folder
print(scratch)
arcpy.AddMessage(f'Scratch workspace -- {scratch} created')

# change current directory to this directory
os.chdir(scratch)
arcpy.AddMessage("Current directory changed to scratch")


# If statement to let user select which file type to download
if file_type == "Shapefile":
    arcpy.conversion.FeatureClassToShapefile(temp_fc, scratch)
    print(f"Shapefile -- {file_name} created ")
    arcpy.AddMessage(f"Shapefile -- {file_name} created")
    arcpy.SetProgressorLabel("Shapefile Created")

    # Zip shapefile. Zips all files in scratch folder
    def ZipShapes(path, out_path):
        # Path of folder to zip up contents
        arcpy.env.workspace = path
        print("environment set")
        shapes = arcpy.ListFeatureClasses()
        print("list of shapes created")
        # iterate through list of shapefiles
        for shape in shapes:
            name = p.splitext(shape)[0]
            print(name)
            zip_path = p.join(out_path, name + '.zip')
            print(zip_path)
            zip = zipfile.ZipFile(zip_path, 'w', compression=zipfile.ZIP_DEFLATED)
            print(zip)
            zip.write(p.join(path, shape), shape)
            print("A")
            for f in arcpy.ListFiles('%s*' % name):
                if not f.endswith('.shp'):
                    zip.write(p.join(path, f), f)
            #deletes files outside of the zipped folder
            for f in arcpy.ListFiles():
                if f.endswith('.cpg'):
                    os.remove(f)
                elif f.endswith('.dbf'):
                    os.remove(f)
                elif f.endswith('.prj'):
                    os.remove(f)
                elif f.endswith('.sbn'):
                    os.remove(f)
                elif f.endswith('.sbx'):
                    os.remove(f)
                elif f.endswith('.shp'):
                    os.remove(f)
                elif f.endswith('.shp'):
                    os.remove(f)
                elif f.endswith('.shx'):
                    os.remove(f)
            print('All files written to %s' %zip_path)
            zip.close()



    if __name__ == '__main__':
        path = scratch
        out_path = scratch

        ZipShapes(path, out_path)

        arcpy.AddMessage("Zipped Shapefile Created")
        arcpy.SetProgressorLabel("Zipped Shapefile Created")

elif file_type == "KML":
    # write an out kml file with a kmz extension by joining the out_folder location
    out_kmz_file = os.path.join(scratch, file_name + ".kmz")
    #arcpy.conversion.LayerToKML(file_name, out_kmz_file)
    zip = arcpy.conversion.LayerToKML(feature_collection,out_kmz_file)
    print(f"KML file created")
    arcpy.AddMessage(f"KML -- {file_name} created")
    arcpy.SetProgressorLabel("KML Created")

# Parameter 4, set ouput as a derived parameter. Output = file link
output = arcpy.SetParameter(3, zip)



