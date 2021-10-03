from osgeo import ogr, osr



def getCoordConverter(src='', targ=''):
    srcproj = osr.SpatialReference()
    srcproj.ImportFromEPSG(src)
    targproj = osr.SpatialReference()
    if isinstance(targ, str):
        targproj.ImportFromProj4(targ)
    else:
        targproj.ImportFromEPSG(targ)
    transform = osr.CoordinateTransformation(srcproj, targproj)

    def convertCoords(xy):
        pt = ogr.Geometry(ogr.wkbPoint)
        pt.AddPoint(xy[0], xy[1])
        pt.Transform(transform)
        return  [pt.GetX(), pt.GetY()]

    return convertCoords

latlongToAlbers = getCoordConverter(4326,5070)
albersToLatlong = getCoordConverter(5070,4326)

