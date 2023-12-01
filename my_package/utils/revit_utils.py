# -*- coding: utf-8 -*-
import clr
clr.AddReference('System.Core')
clr.AddReference('RevitAPI') 
clr.AddReference('RevitAPIUI')
from Autodesk.Revit import DB
from Autodesk.Revit.DB import Element, ElementId, ElementType, Family, FamilySymbol, FamilyInstance, BuiltInCategory, BuiltInParameter, Transaction
from System.Collections.Generic import List, IList
from System import Enum, Action, Func, Uri, Guid, DateTime

def get_element_name(element):
    return Element.Name.GetValue(element)

def get_element_id(element):
    return element.Id

def get_element_type_by_elment(doc,element):
    return doc.GetElement(element.GetTypeId())

def get_element_type_by_built_in_param(doc,element, built_in_param):
    return doc.GetElement(element.get_Parameter(built_in_param).AsElementId())

def get_parameter_value_as_string(element, parameter_name):
    return element.LookupParameter(parameter_name).AsString()

def get_parameter_value_as_double(element, parameter_name):
    return element.LookupParameter(parameter_name).AsDouble()

def get_parameter_value_as_bool(element, parameter_name):
    return element.LookupParameter(parameter_name).AsInteger()

def get_parameter_value_as_element_id(element, parameter_name):
    return element.LookupParameter(parameter_name).AsElementId()

def set_parameter_value(element, parameter_name, value):
    element.LookupParameter(parameter_name).Set(value)

def set_builtin_parameter_value(element, parameter, value):
    element.get_Parameter(parameter).Set(value)

def get_builtin_parameter_value(element, parameter):
    return element.get_Parameter(parameter).AsValueString()

def get_parameter_value_as_int(element, parameter_name):
    return element.LookupParameter(parameter_name).AsInteger()



