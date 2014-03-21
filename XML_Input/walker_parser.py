import xml.dom.minidom
from xml.dom.minidom import parseString
from xml.dom.minidom import Node


def main():
    file = open("validation.xml",'r')
    data = file.read()
    file.close()
    dom = parseString(data)
    valid = recur_map(dom.getElementsByTagName("Simulation")[0])
    file = open("test_input.xml",'r')
    data = file.read()
    file.close()
    dom = parseString(data)
    test = recur_map(dom.getElementsByTagName("Simulation")[0])
    #these dictionaries should be able to be passed directly to the underlying __dict__ field of the class
    #right now this parser does not check tag names for spelling at all
    #TODO: implement something which checks tags spelling
    #check a few tags to make sure it mapped correctly
    print(test['Material_Profile'])
    print(test['Orbital_Properties']['TLE']['line1'])
    print(test['Tower'])
    print(test['OutputSettings'])
    validate(valid, test)

def recur_map(element):
    """map each tag name to a dictionary, the dictionary maps child nodes to their dictionaires
        the base case is a tag with no children, which just gets mapped to its value"""
    #base case, child node is just the text node
    if len(element.childNodes) == 1:
        return str(element.childNodes[0].nodeValue)
    d={}
    #recursively map the child nodes
    for el in element.childNodes:
        #avoid weird nodes
        if el.nodeName != "#text":
            d[str(el.nodeName)] = recur_map(el)
    return d


def validate(valid, test):
    try:
        recur_validate(valid,test)
    except Exception as e:
        print(e)
        return False
    print("XMl was Valid")
    return True

def etree_to_dict(t):
    return {t.tag : map(etree_to_dict, t.iterchildren()) or t.text}


def recur_validate(valid, test):
    """Recursively validate whether the tag names and data types on the test dictionary are valid
    Raise an exception when we reach a problem to stop execution immediately. Exception contains details on why the XML
    was invalid """
    for key in valid.keys():
        if key in test:
            if type(valid[key]) is dict:
                if type(test[key]) is dict:
                    recur_validate(valid[key], test[key])
                else:
                    raise Exception("Tags are not properly nested")
            else:
                typematch = False
                types = valid[key].split(",")
                for t in types:
                    try:
                        #this is a little hacky here, we are using eval
                        #possible security risk, but its their simulation
                        #try catch around the eval for errors in formatting
                        if t == 'str':
                            typematch = typematch or eval("type('"+test[key]+"') is "+t)
                        else:
                            typematch = typematch or eval("type("+test[key]+") is "+t)
                    except Exception:
                        raise Exception("Improper data type in tag "+key)
                if not typematch:
                    raise Exception("Improper data type in tag "+key)

        else:
            raise Exception("Tag names do not match for tag "+key)
main()
