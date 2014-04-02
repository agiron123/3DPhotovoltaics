from xml.etree import ElementTree
import xml.etree.ElementTree as ET
import codecs
import StringIO

dataTypeDict = {}


class XMLInputParser(object):


    def __int__(self, filename):
        self.fileName = filename

    def parse_file(self, file):
        """Parse the XML file containing the users input specifications into a dictionary"""
        """Make sure that the user entered a valid xml file"""

        tokens = {}
        with open(file, 'rt') as f:
            tree = ET.parse(f)

        print("Testing out the recursive parse function: ")
        simulations = list()

        #Need to loop through multiple Simulation tags
        for sim in tree.findall("Simulation"):
            simulations.append(self.parseRecur(sim))

        #added filepath for XML validator here:
        with open("xml_validator.xml", 'rt') as f:
            validTree = ET.parse(f)

        validSim = list()
        missingkeylist = list()
        #Need to loop through multiple Simulation tags
        for valid in validTree.findall("Simulation"):
            validSim.append(self.parseRecur(valid))

        for i in range(0, len(validSim)):
            missingkeylist = self.compareDict(validSim[i], simulations[i]) #just going to print out the missing simulation tags.
            if len(missingkeylist) > 0:
                print "Keys Missing in Simulation Tag " + str(i+1) + ": \n"
                print missingkeylist
                print "\n"

        print str(missingkeylist)

        #If everything was successful, return the dictionary that was parsed.
        #Should we just return null here if there is a missing key?
        if len(missingkeylist) > 0:
            return None #return none because the parsing was not completely successful
        return simulations

    #recursively parse the xml tree.
    def parseRecur(self, root):
        resultDict = {}
        global dataTypeDict
        children = list(root)
        if(len(children) == 0):
            resultDict[root.tag] = root.text
            print "Attrib: " + str(root.attrib)
            dataTypeDict[root.tag] = root.attrib
            print dataTypeDict
            return resultDict[root.tag]

        for child_of_root in children:
            resultDict[child_of_root.tag] = self.parseRecur(child_of_root)
        return resultDict

    #compare the parsed xml file to a valid xml file
    def compareDict(self, validDict, parsed):
        global dataTypeDict #using a global dictionary to hold the datatypes that we need. Probably not one of my best ideas.
        missingkeylist = set()    #using set. As long as all the tags have different names, we're golden.
        for k,v in validDict.iteritems():
            if isinstance(v,dict):
                try:
                    missingkeylist.update(self.compareDictHelper(v,parsed[k], missingkeylist))
                except KeyError:
                    missingkeylist.add(k)
            elif not parsed.has_key(k):
                if k not in missingkeylist:
                    missingkeylist.add(k)
            elif parsed.has_key(k):    #do the type validation right here.
                print str(parsed[k].encode('utf-8')) #IMPORTANT LINE HERE. Make sure we encode to unicode, or we won't be able to print it out.
                #Need to do this for when you are printint out or writing to disk. see farmdev.com/talks/unicode for more information.
                #print "Parsed[k]: " + str(parsed[k]) + " dataTypeDict[k]: " + str(dataTypeDict)
                #check if not str(type(parsed[k])) == dataTypeDict[k]:
                    #print ("Datatype Mismatch")
        return missingkeylist

    #Essentially just has the base cases for the compareDict method.
    def compareDictHelper(self, validDict, parsed, missingkeylist):
        if isinstance(validDict, dict) and not isinstance(validDict, dict):
            if validDict not in missingkeylist:
                missingkeylist.add(validDict.keys())
        elif not isinstance(validDict, dict) and isinstance(parsed, dict):
            if validDict not in missingkeylist:
                missingkeylist.add(validDict)
        elif parsed == None:
            if validDict not in missingkeylist:
                missingkeylist.add(validDict)
        elif isinstance(parsed, dict) and isinstance(validDict, dict):
            missingkeylist.update(self.compareDict(validDict, parsed))
        return missingkeylist

    '''TODO:
    -Make sure that the datatypes are the proper datatypes for python to be using

    -Make sure that each xml element is validated against the parsed datatypes
    -Going to need to check that the input file has the right datatype specified, and that it matches the acceptable datatypes for that element in the validator.


    Some kind of switch, ifelse, etc to check the datatype (see below)

    def checkParsedValue(parsedValue, parsedType)
        if parsedType == "int"
            return type(parsedValue) == int
        elif parsedType == "string"
            return type(parsedType)n == str
        etc. for the rest of the datatypes that we need...

    -Make sure that each xml element is within an acceptable range.
        -This range is probably going to have to be specified in the xml_validator file

    -Add documentation so that it works with Sphinx. Did not get around to putting in the docstrings needed for that.

    '''