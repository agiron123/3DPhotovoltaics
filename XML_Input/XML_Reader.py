import xml.etree.ElementTree as ET
import sys


def map_validate_xml(input_el, valid_el, errors):
    """
    Simultaneously parse the XML onto a results dictionary as well as verify
    the contents of the XML.

    Essentially we perform a DFS of the XML tree. Recursively mapping the tags which are descendants of this element.
    A tag name is mapped to a dictionary. This dictionary maps child tag names to their dictionaries.
    The base case is when a tag has no children. In this case the tag name is mapped directly to the tag's value

    An important note is that the use of dictionary keys means the tag names for a nodes children
    must be distinct. To account for this we must call map_validate_xml on each simulation tag instead
    of just calling it on the root.

    The errors list passed in will be appended with all errors found during the parsing.
    After finding one error we continue searching for all possible errors.
    The following are checked for:

    -Missing or misspelled tags (treated as the same)
    -Extra tags
    -Invalid data in a tag (invalid data type or value)

    Each error will result in an entry to the errors list, which will describe the error

    Additionally all data undergoes the proper type conversions into live python data types
    """

    valid_children = list(valid_el)
    input_children = list(input_el)
    valid_children_tags = set([el.tag for el in valid_children])
    input_children_tags = set([el.tag for el in input_children])
    result = {}

    #use of dictionaries for the tree requires a node have children with unique tag names
    #if there are duplicate tag name this is an error, we could possibly continue the recursion
    #but in this case we terminate it
    if len(input_children) > len(input_children_tags):
        error = "The tag " + input_el.tag + " has multiple children with the same tag name. Duplicate tags are not allowed"
        errors.append(error)
        for child in input_children:
            result[child.tag] = None
        return result

    #base case, no children just a value
    elif len(valid_children) == 0:
        #should just be a value, but contains children
        if len(input_children) > 0:
            error = "The tag " + input_el.tag + " should have 0 children and should just contain a value."
            error += "The tag has the following extra children " + str(input_children_tags)
            errors.append(error)
            for child in input_children:
                result[child.tag] = None
            return result
        #perform data type conversions and check ranges
        else:
            #convert the raw text into live python data types
            #for number data types we check ranges, for strings we check against valid_set
            #if range or valid_set is absent than any value is acceptable
            try:
                #match to the proper datatype
                if valid_el.attrib['datatype'] == 'float':
                    val = float(input_el.text)
                    if 'range' in valid_el.attrib:
                        bounds = valid_el.attrib['range'].split('-')
                        if val < float(bounds[0].strip()) or val > float(bounds[1].strip()):
                            error = "The data in tag " + input_el.tag + " is out of the valid range."
                            errors.append(error)
                            return None
                    return val
                elif valid_el.attrib['datatype'] == 'int':
                    val = int(input_el.text)
                    if 'range' in valid_el.attrib:
                        bounds = valid_el.attrib['range'].split('-')
                        #int function doesn't handle inf like float does
                        if bounds[1].strip() == 'inf':
                            upper = sys.maxint
                        else:
                            upper = int(bounds[1].strip())
                        if val < int(bounds[0].strip()) or val > upper:
                            error = "The data in tag " + input_el.tag + " is out of the valid range."
                            errors.append(error)
                            return None
                    return val
                elif valid_el.attrib['datatype'] == 'bool':
                    if input_el.text == "false" or input_el.text == "False":
                        val = False
                    elif input_el.text == "true" or input_el.text == "True":
                        val = True
                    else:
                        error = "The data in tag " + input_el.tag + " is not valid. "
                        error += "Please specify 'True', 'true', 'False', or 'false'"
                        errors.append(error)
                        val = None
                    return val
                elif valid_el.attrib['datatype'] == 'str':
                    val = input_el.text.strip()
                    if 'valid_set' in valid_el.attrib:
                        valid_set = [el.strip() for el in valid_el.attrib['valid_set'].split(',')]
                         #if we are allowed a list e.g. graph settings
                        if 'list' in valid_el.attrib:
                            val = [el.strip() for el in val.split()]
                            for v in val:
                                if v not in valid_set:
                                    error = "Some data in tag " + input_el.tag + " is not in the valid set of values."
                                    errors.append(error)
                                    return None
                        #no list, single value
                        elif val not in valid_set:
                            error = "The data in tag " + input_el.tag + " is not in the valid set of values."
                            errors.append(error)
                            return None
                    return val
                else:
                    error = "The data type for tag " + valid_el.tag + " is NA. There should be no value."
                    errors.append(error)
                    return None
            except Exception as e:
                error = "The data in tag " + input_el.tag + " is of the wrong type."
                error += " The expected type is " + valid_el.attrib['datatype'] + "."
                errors.append(error)
                return None


    #child_set case means we should only have one child, which should be from the child_set
    elif 'child_set' in valid_el.attrib:
        #if more than one child this is an error
        if len(input_children) > 1:
            error = "The tag " + input_el.tag + " should only have one child."
            error += " This child should be from the child_set { " + valid_el.attrib['child_set'] + " }"
            errors.append(error)
            #can't continue finding errors from here, end recursion and return
            for child in input_children:
                result[child.tag] = None
            return result
        else:
            name = input_children[0].tag
            #if one child but wrong child
            if name not in valid_el.attrib['child_set']:
                error = "The tag " + input_el.tag + " does not have a valid child."
                error += " This tag should have one child from the child_set { " + valid_el.attrib['child_set'] + " }."
                errors.append(error)
                #can't continue finding errors from here, end recursion and return
                for child in input_children:
                    result[child.tag] = None
                return result
            #correct case, continue the recursion
            else:
                next = input_children[0]
                for child in valid_children:
                    if child.tag == name:
                        next = child
                result[name] = map_validate_xml(input_children[0], next, errors)
                return result

    #majority case, multiple children tags
    else:
        #Too many children on the input
        if len(input_children) > len(valid_children):
            error = "The tag " + input_el.tag + " has the following unneeded descendants: "
            #add errors for all the incorrect children
            for child in input_children:
                if child.tag not in valid_children_tags:
                    error += key_list(child)
                    result[child.tag] = None
                else:
                    #find the matching valid child and continue the recursion for valid children
                    #we may find more errors
                    for next in valid_children:
                        if next.tag == child.tag:
                            result[child.tag] = map_validate_xml(child, next, errors)
            errors.append(error)
            return result

        #Too few children on the input or the right number
        else:
            #initialize error
            error = "The tag " + input_el.tag + " is missing the following descendants: "
            for child in valid_children:
                if child.tag in input_children_tags:
                    #find the matching valid child and continue the recursion for valid children
                    #we may find more errors
                    for next in input_children:
                        if next.tag == child.tag:
                            result[child.tag] = map_validate_xml(next, child, errors)
                else:
                    error += key_list(child) + ", "
                    result[child.tag] = None
            #only add error if lengths didn't actually match
            if len(valid_children) != len(input_children):
                errors.append(error[:-2]) #trim off extra ', '
            return result


def key_list(el):
    """
    Utility function which generates a comma separated list of tag names
     for this element and all of its descendants of
    this xml element. Essentially just a string of the DFS traversal order
    """
    children = list(el)
    if len(children) == 0:
        return el.tag
    result = el.tag
    for child in children:
        result += ", " + key_list(child)
    return result


def test():
    """
    Simple method for just testing while we are writing
    """
    #note, you will have to set up errors like this so you have a reference
    errors = []
    print(map_validate_xml(ET.parse('test2.xml')._root, ET.parse('validation.xml')._root, errors))
    for err in errors:
        print(err)