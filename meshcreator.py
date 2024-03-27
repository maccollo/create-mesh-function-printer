import maya.cmds as cmds
import maya.api.OpenMaya as om

def print_function_to_recreate_selected_mesh():
    selected = cmds.ls(selection=True, long=True)
    mesh_name = cmds.ls(selection=True, long=False)[0]
    meshShape = None
    if selected:
        for obj in selected:
            if cmds.nodeType(obj) == "mesh":
                meshShape = obj
                break
            else:
                children = cmds.listRelatives(obj, children=True, shapes=True, fullPath=True) or []
                for child in children:
                    if cmds.nodeType(child) == "mesh":
                        meshShape = child
                        break
            if meshShape:
                break

    if meshShape:
        mesh = meshShape
        new_mesh = cmds.duplicate(mesh)[0]
        cmds.setAttr(new_mesh + '.tx', lock=False)
        cmds.setAttr(new_mesh + '.ty', lock=False)
        cmds.setAttr(new_mesh + '.tz', lock=False)
        cmds.setAttr(new_mesh + '.rx', lock=False)
        cmds.setAttr(new_mesh + '.ry', lock=False)
        cmds.setAttr(new_mesh + '.rz', lock=False)
        cmds.setAttr(new_mesh + '.sx', lock=False)
        cmds.setAttr(new_mesh + '.sy', lock=False)
        cmds.setAttr(new_mesh + '.sz', lock=False)
        cmds.setAttr(new_mesh+'.translate', 0, 0, 0)
        cmds.setAttr(new_mesh+'.rotate', 0, 0, 0)
        cmds.setAttr(new_mesh+'.scale', 1, 1, 1)
        vertexCount = cmds.polyEvaluate(new_mesh, vertex=True)
        vertices = [cmds.pointPosition(f"{new_mesh}.vtx[{i}]", world=True) for i in range(vertexCount)]
        faces = cmds.polyInfo(mesh, faceToVertex=True)
        cmds.delete(new_mesh)
        
        face_connectivity = []
        for face_info in faces:
            _, face_desc = face_info.split(":")
            indices = [int(i) for i in face_desc.split() if i.isdigit()]
            face_connectivity.append(indices)

        print("def recreate_" + mesh_name + "_mesh():")
        print("    import maya.api.OpenMaya as om")
        print("    import maya.cmds as cmds")
        print(f"    vertexArray = om.MFloatPointArray({vertices})")
        print(f"    faceCounts = {[len(face) for face in face_connectivity]}")
        print(f"    faceConnects = {[v for face in face_connectivity for v in face]}")
        print("    meshFn = om.MFnMesh()")
        print("    mesh = meshFn.create(vertexArray, faceCounts, faceConnects)")
        print("    newMeshDagPath = om.MDagPath.getAPathTo(mesh)")
        print("    newMeshNode = newMeshDagPath.fullPathName()")
        print("    cmds.sets(newMeshNode, edit=True, forceElement='initialShadingGroup')")
        print("    cmds.select(newMeshNode, r = True)")
        print("    cmds.hyperShade(assign='lambert1')")
        print(f"    cmds.rename(newMeshNode, '{mesh_name}')")
        print("    print('New mesh created:', newMeshNode)")

print_function_to_recreate_selected_mesh()
