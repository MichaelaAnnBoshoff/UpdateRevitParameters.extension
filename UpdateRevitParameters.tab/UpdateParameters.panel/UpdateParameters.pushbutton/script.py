# -*- coding: utf-8 -*-

__title__ = {
    "en_gb": "Update Parameters",
    "spanish": "Actualizar parametros"
} # Name of the button displyaed in Revit UI
__doc__ = """Version = 1.0
Date = 18 March 2025

--------------------------------------------------------------------
Description:

This tool will update all parameters that were updated in the Model Progress Tracker Application.
--------------------------------------------------------------------
How-to:

-> Click on the button
-> Update Parameters
--------------------------------------------------------------------
Last Update:
- [18 March 2025] - 1.0 RELEASE
-------------------------------------------------------------------
To-Do:

-> Test a script for updating parameters from Speckle.
-------------------------------------------------------------------
Author: Michaela Boshoff
""" # Button Description shown in Revit UI

__author__ = "Michaela Boshoff"
# __helpurl__ = ""
__highlight__ = "new"
__min_revit_ver__ = 2018
__max_revit_ver__ = 2024
# __context__ = ["Walls", "Floors", "Roofs"] # List of class names - users will need to select an element of one of these categories. DOES NOT NEED TO BE INCLUDED. This makes your button available only when certain categories are selected. 
# The context can also be set to a specific view type or Revit file


# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗╔═╗
# ║║║║╠═╝║ ║╠╦╝ ║ ╚═╗
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ ╚═╝ IMPORTS (sorted by category)
# =======================================================================================================

# Regular + Autodesk
import os, sys, math, datetime, time
from Autodesk.Revit.DB import * # Import everything from DB (Very good for beginners and development)
# from Autodesk.Revit.DB import Transaction, Element, ElementId, FilteredElementCollector

# pyRevit
from pyrevit import revit, forms

# Custom Imports
# from lib.Snippets._selection import get_selected_elements

# .NET Imports
import clr
clr.AddReference("System")
# from System.Collections.Generic import List # List<ElementType>() <_ it's a special type of list that Revit API often requires


# ╦  ╦╔═╗╦═╗╦╔═╗╔╗ ╦  ╔═╗╔═╗
# ╚╗╔╝╠═╣╠╦╝║╠═╣╠╩╗║  ║╣ ╚═╗
#  ╚╝ ╩ ╩╩╚═╩╩ ╩╚═╝╩═╝╚═╝╚═╝ VARIABLES
# =======================================================================================================

# from pyrevit.revit import uidoc, doc, app # Alternative
from Autodesk.Revit.UI import UIDocument
doc = __revit__.ActiveUIDocument.Document   ##type: Document
uidoc = __revit__.ActiveUIDocument          #type: UIDocument
app = __revit__.Application                 #Application
PATH_SCRIPT = os.path.dirname(__file__)




# ╔═╗╦ ╦╔╗╔╔═╗╔╦╗╦╔═╗╔╗╔╔═╗
# ╠╣ ║ ║║║║║   ║ ║║ ║║║║╚═╗
# ╚  ╚═╝╝╚╝╚═╝ ╩ ╩╚═╝╝╚╝╚═╝ FUNCTIONS
# =======================================================================================================

def get_selected_elements(uidoc):
    """This function will return elements that are currently selected in Revit UI
    :param uidoc:   uidoc where elements are selected.
    :return:        List of selected elements"""
    return [uidoc.Document.GetElement(elem_id) for elem_id in uidoc.Selection.GetElementIds()]



# ╔═╗╦  ╔═╗╔═╗╔═╗╔═╗╔═╗
# ║  ║  ╠═╣╚═╗╚═╗║╣ ╚═╗
# ╚═╝╩═╝╩ ╩╚═╝╚═╝╚═╝╚═╝ CLASSES
# =======================================================================================================



# ╔╦╗╔═╗╦╔╗╔
# ║║║╠═╣║║║║
# ╩ ╩╩ ╩╩╝╚╝ MAIN
# =======================================================================================================

# Get elements
# all_walls = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Walls).WhereElementIsElementType().ToElements()
all_elements = FilteredElementCollector(doc).WhereElementIsNotElementType().ToElementIds()
print("Number of elements: {}".format(len(all_elements)))

uidoc.Selection.SetElementIds(all_elements)


element_id = "1046970"
# print("Type {}".format(type(element_id)))
uniclass_param = "Classification.Uniclass.Ss.Description"
param_value = "NEW Concreate Wall Systems from pyRevit"

t = Transaction(doc,"Update Parameters") # Use Transaction to make changes to Revit project - control when you want to modify any elements
t.Start() # Put Transactions outside of loop - provide better peformance

# print("Type {}".format(type(str(all_elements[0]))))

for element in all_elements:
    if str(element) == element_id:
        correct_element = doc.GetElement(element)
    # revit_element = element.GetElementId(element_id)
        print("Revit Element {} found in the project.".format(element))
        param = correct_element.LookupParameter("Classification.Uniclass.Ss.Description")


            # Get instance parameters
        instance_parameters = {param.Definition.Name for param in correct_element.Parameters}

        # Get the type of the element
        elem_type = doc.GetElement(correct_element.GetTypeId()) if correct_element.GetTypeId() != ElementId.InvalidElementId else None

        # Get type parameters (if applicable)
        type_parameters = {param.Definition.Name for param in elem_type.Parameters} if elem_type else {}


        print("Instance parameters: {}".format(type(instance_parameters)))
        print("Type parameters: {}".format(type(type_parameters)))
        
        # for parameter in type_parameters:
        #     if str(parameter) == uniclass_param:
        #         print("Found specified parameter: {}".format(parameter))
        #         try:
        #             parameter.Set(param_value)
        #             print("Parameter successfully updated.")
        #         except Exception as e:
        #             print("Parameter could not be updated. See error below:")
        #             print(e)
        #     else:
        #         print("Could not find param?? {}".format(parameter))

        # Example: Update a type parameter (e.g., 'Type Name')
        if elem_type:

            # Get the type parameter and update it
            type_param = elem_type.LookupParameter(uniclass_param)
            if type_param and type_param.HasValue:
                type_param.Set(param_value)
                print("Updated type parameter '{}' to {}".format(uniclass_param, param_value))
            else:
                print("Type parameter '{}' not found or not valid".format(uniclass_param))
        else:
            print("This element has no associated type.")
    else:
        # print("Element {} could not be found".format(element))
        pass
    # if revit_element:
    #     param = revit_element.LookupParameter("Classification.Uniclass.Ss.Description")
    #     print("Parameter:")
    #     print(param)
    #     if param:
    #         try:
    #             param.Set(param_value)
    #             print("Parameter successfully updated.")
    #         except Exception as e:
    #             print("Parameter could not be updated. See error below:")
    #             print(e)

t.Commit() # Put Transactions outside of loop - provide better peformance

# Report Changes