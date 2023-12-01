# -*- coding: utf-8 -*-
import Rhino
import scriptcontext as sc
import Rhino.Geometry as rg
import System
import clr
clr.AddReference("Grasshopper")
import Grasshopper
import Grasshopper.DataTree as DataTree

def offset_plane(plane, offset):
    return rg.Plane(plane.Origin + plane.Normal * offset, plane.Normal)

def get_angle_from_plane(plane):
    return rg.Vector3d.VectorAngle(plane.XAxis, rg.Vector3d.XAxis, plane.Normal)

def copy_geometry_at_plane(geometry, plane):
    new_geometry = geometry.Duplicate()
    transform = rg.Transform.PlaneToPlane(rg.Plane.WorldXY, plane)
    new_geometry.Transform(transform)
    return new_geometry

def preview_block_instance(block_name, plane):
    # ブロック定義を名前で取得
    block_definition = Rhino.RhinoDoc.ActiveDoc.InstanceDefinitions.Find(block_name)
    if not block_definition:
        print("Block definition not found.")
        return None

    # ブロックのジオメトリを取得して平面に変換
    transformed_geometries = []
    for obj in block_definition.GetObjects():
        geom = obj.Geometry
        if geom:  # ジオメトリが存在する場合

            transformed_geom = copy_geometry_at_plane(geom, plane)
            transformed_geometries.append(transformed_geom)

    return transformed_geometries