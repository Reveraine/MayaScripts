Version 1.0 of Animation Exporter
Built by Sarah Slater
sacslater@gmail.com
https://github.com/Reveraine/MayaScripts

*****

To use:
Place all files (fbxExporter_Anim.py, fbxAnimExportConfig.txt, animTexFile.tga) in the Maya scripts folder:
Documents -> maya -> scripts

Open the Maya script editor.
Type or copy and paste the following and execute:
import fbxExporter_Anim


**Note**
This exporter operates on the assumption that constraints contain the string "Constraint" and Nurbs-based controls are "ctrls"
If this is not the case with the rigs you are working with, it can be edited simply in the code itself in lines 211-212

Lines 211-212, Example:

self.deleteObjects('Constraint')
self.deleteObjects('ctrl')

If your Nurbs curves are instead named "handle", replace 'ctrl' with 'handle', ensuring the '' stay where they are. Capitalization is important:

self.deleteObjects('Constraint')
self.deleteObjects('handle')

Now it should work for your rigs. 

****

fbxAnimExportConfig.txt

This is a text-based config file that saves a default path. If you like, you can manually enter the path here instead of using the provided dialog boxes. 
Maya will only read the first line.

****

animTexFile.tga

This is a tiny placeholder texture to ensure the animated object has a material already. 


****







