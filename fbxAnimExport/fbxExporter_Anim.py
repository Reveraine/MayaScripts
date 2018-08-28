'''
########################################################
Name: fbxExporter_Anim.py

Author: Sarah Slater

Date: August 20th, 2018

Summary: This UI is for exporting animated meshes + skeletons in an .fbx format
########################################################
'''

import pymel.core as pm
import maya.mel as mel
import maya.cmds as cmds
import os

#UIWindow Object

class ExportAnimUI(object):
	def __init__(self):
		#delets current window if exists
		if pm.window("Animation_Exporter", exists = True):
			pm.deleteUI("Animation_Exporter", window = True)
			
		#window UI
		exportWindow = pm.window("Animation_Exporter", title = "Animation Exporter")
		col = pm.columnLayout(adjustableColumn = True)
		#call function to set default variable for file name to name of scene 
		self.getFileName()
		#location of the script and related files
		self.scriptPath = os.path.join(os.path.dirname(__file__))

		#opens config file to read/write default exported file path
		configFilePath = os.path.join(self.scriptPath + '/fbxAnimExportConfig.txt')
		with open(configFilePath, 'r+') as self.configFile:   
			self.first_char = self.configFile.read(1)
			#if the file is not empty, use the file to pick the default file path
			if self.first_char:
				self.configFile.seek(0)
				self.filePath =	 self.configFile.readline()
			#if the file is empty, prompt the user to provide a path using Maya dialogs
			else:
				#dialog message to inform users of the reason for the file viewer
				result = pm.confirmDialog(title = 'Setting Error', 
				icon = 'warning',
				message = 'No default path found.\nPlease choose an export path.',
				button = ['OK'],
				defaultButton = 'OK',
				dismissString = 'OK')

				#opens a dialog box to set default export path
				self.fileDir = pm.fileDialog2(fileMode = 3, returnFilter = False)
				dir(self.fileDir)
				#sets the file path to a variable
				self.dirToWrite = str(self.fileDir)
				self.filePath = self.dirToWrite[3:-2]
				self.configFile.write('%s' %self.filePath)
				
		pm.separator(height = 8, style = 'none')
		#UI title
		pm.text('Animation Export Tool')
		pm.separator(height = 15)
		#text field and button groupd to edit export file path
		self.filePathField = pm.textFieldButtonGrp('File_Path', 
													buttonLabel = 'Change File Path', 
													adjustableColumn = True, 
													pht = 'Please select a file path', 
													buttonCommand = self.filePathButton, 
													textChangedCommand = self.fileNameEditChange, 
													ann = 'Locate a temporary file path for this session')
		#sets the file path text field to the current self.filePath variable
		self.filePathField.setText(self.filePath)
		#set the UI to place a new button to the right of text group button
		row = pm.rowLayout(numberOfColumns = 2)
		#text field and button to edit exported scene name
		self.fileNameField = pm.textFieldButtonGrp('File_Name', 
													buttonLabel = 'Locate File', 
													adjustableColumn = True, 
													pht = 'Untitled', 
													textChangedCommand = self.fileNameEditChange, 
													width = 500, 
													ann = 'Locate a file to change the name of the exported file to')
		#sets the file name field to the current self.fileName variable
		self.fileNameField.setText(self.fileName)
		#button to load a file name in, if user has opened a file after the script
		self.refreshFile = pm.button(label = 'Refresh File Name', command = self.refreshFileName, ann = 'Use the name of the currently open file')
		
		pm.setParent(col)
		#sets the final file path and name based on initial default inputs
		self.finalFilePath = os.path.join(self.filePath + '/' + self.fileName)
				
		pm.separator(height = 10, style = 'none')		
		
		row2 = pm.rowLayout(numberOfColumns = 2)
		#runs the full export function
		pm.button(label = 'Clean-up, Bake, and Export', 
					command = self.exportButton, 
					width = 300, 
					ann = 'Save, bake, delete Constraints and ctrls, create material, and export')
		#runs only the select and export functions
		pm.button(label = 'Export Only', 
					command = self.onlyExport, 
					width = 300, 
					ann = 'Export the file with no changes')
		pm.setParent(col)
		pm.separator(height = 20)
		pm.rowLayout(numberOfColumns = 4)
		pm.separator(width = 15, style = 'single', horizontal = False)
		pm.button(label = 'Change Default Path', 
					command = self.changeDefaultPath, 
					width = 150, 
					height = 20, 
					ann = 'Change the file path that appears when the tool is opened')
		pm.separator(width = 15, style = 'single', horizontal = False)
		pm.text('Remember to import any referenced files, and clean up namespaces if necessary.')
		pm.setParent(col)
		pm.separator(height = 10, style = 'none')		
		
		pm.showWindow(exportWindow)
		
		
	def getFileName(self, *args):
		#gets the name of the file to set as the export file name (minus .ext)
		self.fileNameGet = str(cmds.file(q = True, sn = True, shortName = True))
		self.fileName = self.fileNameGet[:-3]
		

	def filePathButton(self, *args):
		#overwrites defualt file path in current session only
		self.fileDirTemp = pm.fileDialog2(fileMode = 3, returnFilter = False)
		dir(self.fileDirTemp)
		self.tempDir = str(self.fileDirTemp)
		self.filePathField.setText(self.tempDir[3:-2])

		
	def fileNameEditChange(self, *args):
		#updates the file path for final export
		dirPath = self.filePathField.getText()
		filePath = self.fileNameField.getText()
		self.finalFilePath = os.path.join(dirPath + '/' + filePath)
		return self.finalFilePath
		
	def changeDefaultPath(self, *args):
		#overwrites default path in config file
		with open(os.path.join(self.scriptPath + '/fbxAnimExportConfig.txt'), 'r+') as self.configFile: 
			#empties text file to ensure there is no cross-contamination
			self.configFile.truncate(0)
			#opens a folder dialog box
			self.fileDir_2 = pm.fileDialog2(fileMode = 3, returnFilter = False)
			dir(self.fileDir_2)
			#sets the file path to a variable
			self.dirToWrite_2 = str(self.fileDir_2)
			#subtracts the Maya annotation from the string
			self.filePath_2 = self.dirToWrite_2[3:-2]
			#write the file path to the config file
			self.configFile.write('%s' %self.filePath_2)
		#replaces current file path
		self.filePathField.setText(self.filePath_2)
		
		
	def refreshFileName(self, *args):
		#refresh the current file name and set it as export name
		self.getFileName()
		self.fileNameField.setText(self.fileName)
		
		
	def onlyExport(self, *args):
		#exports the current file with no changes
		self.selectExport()
		self.exportAnim(self.finalFilePath)
		
	def exportButton(self, *args):
		#Incrememnt and save the current file before executing changes
		mel.eval('IncrementAndSave')
		#Selects the joints and meshes
		self.selectExport()
		#bakes selected
		self.bakeAnim()
		#deselects the joints and meshes
		self.deselectAll()
		#selects and deletes controls and constraints
		self.deleteExtras()
		#clear selection
		self.deselectAll()
		#creates a material and assigns it to meshes
		self.createMaterial()
		#selects the joints and meshes
		self.selectExport()
		#exports all joints and meshes
		self.exportAnim(self.finalFilePath)

	def selectExport(self, *args):
		#selects all joints and meshes in order to bake
		self.bakeJoints = pm.ls(exactType = 'joint')
		self.bakeMesh = pm.ls(exactType = 'mesh')
		pm.select(self.bakeJoints, self.bakeMesh)
		
	def bakeAnim(self, *args):
		#bakes the selected mesh and joints to one frame intervals
		pm.bakeResults(simulation = True, 
						preserveOutsideKeys = True, 
						disableImplicitControl = True, 
						removeBakedAttributeFromLayer = False, 
						minimizeRotation = True, 
						t=(1,60))

	def deleteExtras(self, *args):
		#executes delete on specific objects
		#to edit, only change the words within the '' symbols
		#removes all constraints 
		self.deleteObjects('Constraint')
		#removes all nurbs controls
		self.deleteObjects('ctrl')
		
	def deleteObjects(self, objects, *args):
		#lists all objects by name, this is useful for deleting rig controls and constraints
		self.constraints = pm.ls('*:*' + objects + '*')
		#selects every object in list
		for j in self.constraints:
			pm.select(j, add = True)
		#deletes the objects
		pm.delete()
		
	def deselectAll(self, *args):
		#deselect all items
		pm.select(clear = True)


	def createMaterial(self, *args):
		#creates a shader node if one does not exist
		if pm.objExists('animMaterial'):
			self.animShader = 'animMaterial'
		else:
			self.animShader = pm.shadingNode('lambert', n = 'animMaterial', asShader = True)
		
		#creates and connects a shader group to shader if it does not already exist
		if pm.objExists('animShaderGrp'):
			self.animShaderGrp = pm.sets('animShaderGrp', clear = 'animShaderGrp')
			
		else:
			self.animShaderGrp = pm.sets(renderable = True, noSurfaceShader = True, empty = True, n = 'animShaderGrp')
			#connect shader to shader group set
			pm.connectAttr('%s.outColor' %self.animShader, '%s.surfaceShader' %self.animShaderGrp)

			#format the image location
			self.animImagePath = os.path.join(self.scriptPath + '/animTexFile' + '.tga')
			#assign file node to variable to connect
			self.animTexFile_1 = mel.eval('importImageFile("%s", false, false, true)' %self.animImagePath)
			#connect the file node to material node
			pm.connectAttr('%s.outColor' %self.animTexFile_1, '%s.color' %self.animShader)
			
		#collect meshes to apply
		self.meshMaterial = (pm.ls(exactType = 'mesh'))
		#add meshes to shader set to assign material
		pm.sets('animShaderGrp', forceElement = self.meshMaterial)
		
		
	def exportAnim(self, outFilePath, *args):
		#loads maya fbx plugin in order to correctly export file
		pm.loadPlugin("fbxmaya")
		mel.eval('FBXResetExport')
		#indicates the object to export is animated
		mel.eval('FBXExportBakeComplexAnimation -v true')
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
		mel.eval('FBXExportTriangulate -v true')
		#exports selected with above settings
		pm.exportSelected(outFilePath, force = True, shader = True, type = 'FBX export')
		
ExportAnimUI()
