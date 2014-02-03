import xml.dom.minidom
from xml.dom.minidom import parseString
from xml.dom.minidom import Node
#might want to use this xml parser instead, much less code
def main():
    #open the xml file for reading:
    file = open("walker_test.xml",'r')
    #convert to string:
    data = file.read()
    #close file because we dont need it anymore:
    file.close()
    #parse the xml you got from the file
    dom = parseString(data)
    #use simulation tag as root and recursively parse the data
    d=recur_map(dom.getElementsByTagName("Simulation")[0])
    #these dictionaries should be able to be passed directly to the underlying __dict__ field of the class
    #right now this parser does not check tag names for spelling at all
    #TODO: implement something which checks tags spelling
    #check a few tags to make sure it mapped correctly
    print(d['Material_Profile'])
    print(d['Orbital_Properties']['TLE']['line1'])
    print(d['Tower'])
    print(d['OutputSettings'])

def recur_map(element):
    """map each tag name to a dictionary, the dictionary maps child nodes to their dictionaires
        the base case is a tag with no children, which just gets mapped to its value"""
    #base case, child node is just the text node
    if len(element.childNodes)==1:
        return str(element.childNodes[0].nodeValue)
    d={}
    #recursively map the child nodes
    for el in element.childNodes:
        #avoid weird nodes
        if el.nodeName!="#text":
            d[str(el.nodeName)]=recur_map(el)
    return d


main()
