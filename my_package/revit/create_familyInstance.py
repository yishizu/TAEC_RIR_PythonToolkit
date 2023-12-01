# -*- coding: utf-8 -*-
from utils.rhinoinside_utils import get_active_doc, convert_rhino_to_revit_geometry
from repository.data_processor import find_row_by_name
from Autodesk.Revit.DB.Structure import StructuralType
from Autodesk.Revit.DB import BuiltInCategory,FilteredElementCollector,FamilySymbol,BuiltInParameter,XYZ,Transaction
from geometry.geometry import get_angle_from_plane, copy_geometry_at_plane
import Rhino.Geometry as rg

def get_built_in_category(category_name):
    try:
        # 文字列からBuiltInCategoryを取得
        category = getattr(BuiltInCategory, category_name)
        return category
    except Exception as e:
        # カテゴリが見つからない場合はNoneを返す
        return None
        
def query_family_symbol(doc, category, type_name):
    # 指定されたカテゴリとタイプ名に基づいてFamily Typeを取得
    collector = FilteredElementCollector(doc).OfClass(FamilySymbol).OfCategory(category)
    for elem in collector:
        if elem.get_Parameter(BuiltInParameter.ALL_MODEL_TYPE_NAME).AsString() == type_name:
            return elem
    return None
    
def place_family_instance(doc, family_symbol, position):
    # FamilyInstanceを配置するためのトランザクションを開始
    transaction = Transaction(doc, "Place Family Instance")
    transaction.Start()

    try:
        # FamilyInstanceを配置
        instance = doc.Create.NewFamilyInstance(position, family_symbol, StructuralType.NonStructural)
        transaction.Commit()
        return instance
    except Exception as e:
        print(e)
        transaction.RollBack()
        return None
    

def place_family_instance_by_name_and_point(_blockname, _point):
    doc = get_active_doc()
    type_name = find_row_by_name(_blockname,'BlockName')[0]['FamilyType']
    category_name = find_row_by_name(_blockname,'BlockName')[0]['BuiltInCategory']
    # カテゴリ名からBuiltInCategoryを取得
    category = get_built_in_category(category_name)
    if category is None:
        return None

    # Family Typeを取得
    family_symbol = query_family_symbol(doc, category, type_name)
    if family_symbol is None:
        return None

    position = convert_rhino_to_revit_geometry(_point)
    # FamilyInstanceを配置
    return place_family_instance(doc, family_symbol, position)

def place_family_instance_by_name_and_plane(_blockname, plane):
    plane_origin = plane.Origin
    instance = place_family_instance_by_name_and_point(_blockname, plane_origin)
    rotate_family_instance_by_plane(instance, plane)
    
    return instance


def rotate_family_instance_by_plane(instance, plane):
    angle = get_angle_from_plane(plane)
    print(angle)
    rotate_family_instance(instance, angle,plane)

def rotate_family_instance(instance, angle, plane):
    # FamilyInstanceを回転するためのトランザクションを開始
    transaction = Transaction(instance.Document, "Rotate Family Instance")
    transaction.Start()

    try:
        # FamilyInstanceを回転
        start_point = plane.Origin
        end_point = plane.Origin + plane.XAxis 
        line = rg.Line(start_point, end_point)
        rv_line = convert_rhino_to_revit_geometry(line)
        instance.Location.Rotate(rv_line, angle)
        transaction.Commit()
    except Exception as e:
        print(e)
        transaction.RollBack()