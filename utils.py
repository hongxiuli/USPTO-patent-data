import os
                    
def processFiles(folder, xmlHandler, filesToProcess=[]):
    """process XML files inside folder
    NOTE: each XML file in the folder contains lots of XML snippets. Each XML snippet represent one patent.
    
    @param folder: the path to the folder to be processed 
    @param xmlHandler: the function to process specific xml accoding to the corresponding dtds
    @param filesToProcess: if length>0, a list of files to be processed instead of files inside @folder
    """
    if(len(filesToProcess)==0):
        filesToProcess = os.listdir(folder)
        
    for fileName in filesToProcess:
        if(fileName.endswith('.xml')):
            print('process ', folder+fileName)
            content = ''
            with open(folder+fileName, encoding='ISO-8859-1') as f:
                for line in f:
                    if(line.startswith('<?xml')):
                        if(len(content)>0):
                            xmlHandler(content)
                            content = ''
                    content += line