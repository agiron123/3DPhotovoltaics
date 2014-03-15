from xml.etree import ElementTree
import xml.etree.ElementTree as ET

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

    def parseRecur(self, root):
        resultDict = {}
        dataTypeDict = {}
        children = list(root)
        if(len(children) == 0):
            resultDict[root.tag] = root.text
            print "Attrib: " + str(root.attrib)
            dataTypeDict[root.tag] = root.attrib
            return resultDict[root.tag]

        for child_of_root in children:
            resultDict[child_of_root.tag] = self.parseRecur(child_of_root)
        return resultDict

    def compareDict(self, validDict, parsed):
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
        return missingkeylist

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