import bpy
import random
import bmesh


class FirTree():

    def createFirTree(_self, _season) -> object:

        branchMaterialName = "firBranch"
        branchColor = (0.114 ,0.041 ,0.010 ,1)

        if(_season == "0"):
                leavesMaterialName = "firLeavesSpring"
                leavesColor = (0.112 ,0.127 ,0.024 ,1)
        elif(_season == "1"):
                leavesMaterialName = "firLeavesSummer"
                leavesColor = (0.195 ,0.347 ,0.018 ,1)
        elif(_season == "2"):
                leavesMaterialName = "firLeavesAutumn"
                leavesColor = (0.366 ,0.114 ,0.026 ,1)
        elif(_season == "3"):
                leavesMaterialName = "firLeavesWinter"
                leavesColor = (1,1,1,1)

        if bpy.context.mode == "EDIT_MESH":
            bpy.ops.object.mode_set(mode='OBJECT')

        bpy.ops.mesh.primitive_cylinder_add(vertices=12, enter_editmode=False, align='WORLD', location=(0, 0, .5), scale=(.3, .3, .85))
        tribe = bpy.context.object
        tribe.name = 'tribe'
        bpy.ops.object.editmode_toggle()
        branch = bpy.context.object
        branch_mesh = bpy.context.view_layer.objects.active.data

        bm = bmesh.from_edit_mesh(branch_mesh)

        for vert in bm.verts:
            for l in vert.link_edges:
                if vert.index % 2 == 1:
                    vert.co[0] = vert.co[0] * 0.85
                    vert.co[1] = vert.co[1] * 0.85

        bpy.ops.object.editmode_toggle()

        for edge in branch.data.edges:
            edge.select = False

        for poly in branch.data.polygons:
            if poly.index != 10:
                poly.select = False

        mat = bpy.data.materials.get(branchMaterialName)

        if mat is None:
            mat = bpy.data.materials.new(name=branchMaterialName)
            mat.use_nodes = True
            mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = branchColor


        mat.use_nodes = True

        if branch.data.materials:
            branch.data.materials[0] = mat
        else: 
            branch.data.materials.append(mat)

        bpy.ops.mesh.primitive_cylinder_add(vertices=12, enter_editmode=False, align='WORLD', location=(0, 0, 4.25), scale=(1.2, 1.2, 3))
        fir = bpy.context.object
        fir.name = 'fir'
        bpy.ops.object.editmode_toggle()
        leaves = bpy.context.object
        leaves_mesh = bpy.context.view_layer.objects.active.data

        bm = bmesh.from_edit_mesh(leaves_mesh)

        vl = []

        for vert in bm.verts:
            for l in vert.link_edges:
                if vert.index % 2 == 1:
                    print(vert.co)
                    vert.co[0] = vert.co[0] * 0.1
                    vert.co[1] = vert.co[1] * 0.1
                
                print(vert.index)


        mat_leaves = bpy.data.materials.get(leavesMaterialName)

        if mat_leaves is None:
            mat_leaves = bpy.data.materials.new(name=leavesMaterialName)
            mat_leaves.use_nodes = True
            mat_leaves.node_tree.nodes["Principled BSDF"].inputs[0].default_value = leavesColor


        mat_leaves.use_nodes = True

        if leaves.data.materials:
            leaves.data.materials[0] = mat_leaves
        else: 
            leaves.data.materials.append(mat_leaves)

        bpy.ops.object.editmode_toggle()

        fir.parent = tribe
        fir.matrix_parent_inverse = tribe.matrix_world.inverted()
        bpy.ops.object.select_more()
        bpy.ops.object.join()
        bpy.ops.object.origin_set(type='ORIGIN_CURSOR')

        return fir