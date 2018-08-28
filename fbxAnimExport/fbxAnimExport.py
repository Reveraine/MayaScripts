'''
########################################################
Name: fbxExporter_Anim.py

Author: Sarah Slater

Date: August 6th, 2018

Summary: This UI is for exporting animated meshes for use in UE4
########################################################
'''

import pymel.core as pm
import maya.mel as mel
import os

#UIWindow Object

class ExportAnimUI(object):
	def __init__(self):
		#window UI
		exportWindow = pm.window('Animation Exporter')
		col = pm.columnLayout(adjustableColumn = True)
		
		pm.showWindow(exportWindow)

def selectExport():
	#selects all joints and meshes in order to bake
	bakeJoints = pm.ls(exactType = 'joint')
	bakeMesh = pm.ls(exactType = 'mesh')
	pm.select(bakeJoints, bakeMesh)
	
def bakeAnim():
	#bakes the selected mesh and joints to one frame intervals
	pm.bakeResults(simulation = True, preserveOutsideKeys = True, disableImplicitControl = True, removeBakedAttributeFromLayer = False, minimizeRotation = True, t=(1,60))


def deleteObjects(objects):
	constraints = pm.ls('*' + objects + '*')
	for j in constraints:
		pm.select(j, add = True)
	pm.delete()
	
def deselectAll():
	pm.select(clear = True)


def createMaterial():
	animShader = pm.shadingNode('lambert', n = 'animMaterial', asShader = True) 
	#create a file node w/2D placement texture
	animShaderGrp = pm.sets(renderable = True, noSurfaceShader = True, empty = True, n = 'animShaderGrp')
	#connect shader to shader group set
	pm.connectAttr('%s.outColor' %animShader, '%s.surfaceShader' %animShaderGrp)
	#get the script location, and image location
	scriptPath = os.path.join(os.path.dirname(__file__))
	#format the image location
	animImagePath = os.path.join(scriptPath + '/animTexFile' + '.tga')
	#assign file node to variable to connect
	animTexFile_1 = mel.eval('importImageFile("%s", false, false, true)' %animImagePath)
	#connect the file node to material node
	pm.connectAttr('%s.outColor' %animTexFile_1, '%s.color' %animShader)
	#collect meshes to apply
	meshMaterial = (pm.ls(exactType = 'mesh'))
	#add meshes to shader set to assign material
	pm.sets('animShaderGrp', forceElement = meshMaterial)
	
	
def exportAnim(bakeTimeEnd, bakeTimeStart, outFilePath, triangulateMesh = 'true'):
	#loads maya fbx plugin in order to correctly export file
	pm.loadPlugin("fbxmaya")
	mel.eval('FBXResetExport')
	#indicates the object to export is animated
	mel.eval('FBXExportBakeComplexAnimation -v true')
	#designates the final key frame to export
	mel.eval('FBXExportBakeComplexEnd -v  "%s" ' %bakeTimeEnd)
	#designates the first key frame to export
	mel.eval('FBXExportBakeComplexStart -v "%s" ' %bakeTimeStart)
	#excludes cameras
	mel.eval('FBXExportCameras -v false')
	#tells maya to export the texture with the fbx
	mel.eval('FBXExportEmbeddedTextures -v true')
	#tells maya to ignore any leftover constraints
	mel.eval('FBXExportConstraints -v false')
	#forces the use of fbx 2016, which is the current version that works with unreal
	mel.eval('FBXExportFileVersion -v FBX201600')
	#includes Input Connections
	mel.eval('FBXExportInputConnections -v true')
	#excludes lights 
	mel.eval('FBXExportLights -v false')
	#includes deformer shapes
	mel.eval('FBXExportShapes -v true')
	#includes skeleton
	mel.eval('FBXExportSkeletonDefinitions -v true')
	#includes skin
	mel.eval('FBXExportSkins -v true')
	#includes smoothing groups
	mel.eval('FBXExportSmoothingGroups -v true')
	#triangulate
	mel.eval('FBXExportTriangulate -v %s' %triangulateMesh)
	#exports the file with designated settings
	mel.eval('FBXExport -f "%s" -s' %outFilePath)
	
ExportAnimUI()
