import arcpy
arcpy.env.overwriteOutput = True

#Set feature classes
sde = r"C:\Users\djacosta\AppData\Roaming\ESRI\Desktop10.2\ArcCatalog\Connection to cno-sqlcst01.sde"
nola_parcels = r"C:\Users\djacosta\Desktop\temp\hdlc_sandbox\data.gdb\nola_parcels_v1"
hdlc_parcels = r"C:\Users\djacosta\Desktop\temp\hdlc_sandbox\data.gdb\hdlc_parcels_v1"
hdlc_features = r"C:\Users\djacosta\Desktop\temp\hdlc_sandbox\data.gdb\hdlc_features"
hdlc_features_buffer = r"C:\Users\djacosta\Desktop\temp\hdlc_sandbox\data.gdb\hdlc_features_buffer"
points = r"C:\Users\djacosta\Desktop\temp\hdlc_sandbox\data.gdb\points"

#Fetch points from AGO
baseURL = "http://services.arcgis.com/VhMjCzR3cIjEkh7L/arcgis/rest/services/historic_landmarks_v1/FeatureServer/0/query"
where = '1=1'
fields ='*'
token = ''
query = "?where={}&outFields={}&returnGeometry=true&f=json&token={}".format(where, fields, token)

fsURL = baseURL + query
 
fs = arcpy.FeatureSet()
fs.load(fsURL)
 
arcpy.CopyFeatures_management(fs, points)

#Create feature layers from feature classes
arcpy.MakeFeatureLayer_management(hdlc_parcels, "hdlc_parcels")
arcpy.MakeFeatureLayer_management(nola_parcels, "nola_parcels")

#Join all HDLC features to parcels
arcpy.SpatialJoin_analysis(points, nola_parcels, hdlc_features,"JOIN_ONE_TO_MANY","KEEP_ALL", "#", "INTERSECT")

#Select those that do not intersect
arcpy.SelectLayerByAttribute_management('hdlc_features', "NEW_SELECTION", " \"Join_Count\" = 0 ")

#Copy those that do not intersect to a new feature layer
arcpy.CopyFeatures_management('hdlc_features', hdlc_features_buffer)

#arcpy.SpatialJoin_analysis(points, footprints, hdlc_features_buffer,"JOIN_ONE_TO_MANY","KEEP_ALL", "#", "INTERSECT", 10)

arcpy.SelectLayerByLocation_management("nola_parcels", "CONTAINS", hdlc_features)
arcpy.SelectLayerByLocation_management("nola_parcels", "WITHIN_A_DISTANCE", hdlc_features_buffer, 20, "ADD_TO_SELECTION")
arcpy.CopyFeatures_management('nola_parcels', hdlc_parcels)






