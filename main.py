import DTD2_5
import utils

#process DTD2_5 files, only porocess pgb20020430.xml for testing purpose
utils.processFiles("D:\\patent\\pgb\\", DTD2_5.processXMLDoc, filesToProcess=['pgb20020430.xml'])