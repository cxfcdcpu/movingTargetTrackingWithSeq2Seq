import rotatingCalipers as rc


  
  



convexHullPts = [[0,0],[3,0],[2,2],[1,2]]
'''
iniR = rc.initialRectangle(convexHullPts)
print (iniR.area)
iniL = iniR.lines
print ( iniL[0].getAngleToPoint(iniR.supportPoints[3]))

iniR.printRect()
nextRec, edge = rc.rotateMinAngle(convexHullPts,iniR)
nextRec.printRect()
print(edge)
'''

finalRect = rc.findMinAreaRect(convexHullPts)
finalRect.printRect()
