import arcpy
arcpy.env.overwriteOutput = True

sde = r"C:\Users\djacosta\AppData\Roaming\ESRI\Desktop10.2\ArcCatalog\Connection to cno-sqldev05.sde\CNOGIS.CNOGISOWNER.Economic_Development"
nola_parcels = r"C:\Users\djacosta\Desktop\temp\hdlc_sandbox\data.gdb\nola_parcels"
hdlc_parcels = r"C:\Users\djacosta\Desktop\temp\hdlc_sandbox\data.gdb\hdlc_parcels_v1"
hdlc_features = r"C:\Users\djacosta\Desktop\temp\hdlc_sandbox\data.gdb\hdlc_features"
hdlc_features_buffer = r"C:\Users\djacosta\Desktop\temp\hdlc_sandbox\data.gdb\hdlc_features_buffer"
points = r"C:\Users\djacosta\Desktop\temp\hdlc_sandbox\data.gdb\points"

#Fetch points from AGO
baseURL = "http://services.arcgis.com/VhMjCzR3cIjEkh7L/arcgis/rest/services/historic_landmarks_v3/FeatureServer/0/query"
where = '1=1'
fields ='*'
token = ''
query = "?where={}&outFields={}&returnGeometry=true&f=json&token={}".format(where, fields, token)

fsURL = baseURL + query
 
fs = arcpy.FeatureSet()
fs.load(fsURL)
 
arcpy.CopyFeatures_management(fs, points)

#Create feature layers from feature classes
arcpy.MakeFeatureLayer_management(hdlc_parcels, "hdlc_parcels_layer")
arcpy.MakeFeatureLayer_management(nola_parcels, "nola_parcels_layer")

#Join all HDLC features to parcels
arcpy.SpatialJoin_analysis("nola_parcels_layer", points,"nola_parcels_layer_join","JOIN_ONE_TO_MANY","KEEP_ALL", "#", "INTERSECT")

#Select those that intersect
arcpy.SelectLayerByAttribute_management('nola_parcels_layer_join', "NEW_SELECTION", ' "Join_Count" > 0 ')

#arcpy.SpatialJoin_analysis(points, footprints, hdlc_features_buffer,"JOIN_ONE_TO_MANY","KEEP_ALL", "#", "INTERSECT", 10)


arcpy.CopyFeatures_management('nola_parcels_layer_join', hdlc_parcels)

arcpy.FeatureClassToFeatureClass_conversion (hdlc_parcels, sde, "hdlc_parcels_djacosta_test_v1")




