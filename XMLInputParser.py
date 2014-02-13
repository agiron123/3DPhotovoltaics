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
        #Need to loop through multiple Simulation tags
        for valid in validTree.findall("Simulation"):
            validSim.append(self.parseRecur(valid))

        diff = list()
        #TODO: Find the difference between the two dictionaries, and do type checking.
        #This is not done, need to do a deep compare of the two dictionaries.
        #This should be a list full of Simulations dicts
        for i in range(0, len(simulations)):
            diff.append(set(validSim[0].keys()) - set(simulations[i].keys()))

        print("Parameters that need to be re entered: \n")
        print (diff)

        #If everything was succesful, return the dictionary that was parsed.
        return simulations

    def parseRecur(self, root):
        resultDict = {}
        children = list(root)
        if(len(children) == 0):
            resultDict[root.tag] = root.text
            return resultDict[root.tag]

        for child_of_root in children:
            resultDict[child_of_root.tag] = self.parseRecur(child_of_root)
        return resultDict
