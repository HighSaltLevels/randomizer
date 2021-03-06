""" Check box controllers """

def handler(*elements):
    """ Toggle the state of the ui elements """
    for element in elements:
        element.setDisabled(element.isEnabled())
        
