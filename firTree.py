import bpy
import random
import bmesh


class FirTree():

    def createFirTree(_self) -> object:

        branchMaterialName = "firBranch"
        leavesMaterialName = "firLeaves"
        branchColor = (0.114 ,0.041 ,0.010 ,1)
        leavesColor = (0.112 ,0.127 ,0.024 ,1)

        """ match season:
            case "SPRING":
                
                leavesMaterialName = "firLeavesSpring"
                leavesColor = (0.112 ,0.127 ,0.024 ,1)
                return

            case "SUMMER":

                leavesMaterialName = "firLeavesSummer"
                leavesColor = (0.184 ,0.212 ,0.038 ,1)
                return

            case "AUTUMN":

                leavesMaterialName = "firLeavesAutumn"
                leavesColor = (0.107 ,0.127 ,0.011 ,1)
                return
            
            case "WINTER":

                leavesMaterialName = "firLeavesWinter"
                leavesColor = (0.047 ,0.054 ,0.006 ,1)
                return """

        if bpy.context.mode == "EDIT_MESH":
            bpy.ops.object.mode_set(mode='OBJECT')

        bpy.ops.mesh.primitive_cylinder_add(vertices=12, enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(.5, .5, .5))
        tribe = bpy.context.object
        tribe.name = 'tribe'
        bpy.ops.object.editmode_toggle()
        branch = bpy.context.object
        branch_mesh = bpy.context.view_layer.objects.active.data

        bm = bmesh.from_edit_mesh(branch_mesh)

        vl = []

        for vert in bm.verts:
            for l in vert.link_edges:
                if vert.index % 2 == 1:
                    print(vert.co)
                    vert.co[0] = vert.co[0] * 0.85
                    vert.co[1] = vert.co[1] * 0.85
                
                print(vert.index)
                
        #for e in bm.select_history:
        #    if isinstance(e, bmesh.types.BMFace) and e.select:
        #        print(repr(e))

        print(branch.data.polygons[1])

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

            

        bpy.ops.object.editmode_toggle()
        bpy.ops.mesh.extrude_faces_move(MESH_OT_extrude_faces_indiv={"mirror":False}, TRANSFORM_OT_shrink_fatten={"value":2, "use_even_offset":True, "mirror":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "release_confirm":False})
        bpy.ops.transform.resize(value=(0.8, 0.8, 0.8), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', mirror=True, use_proportional_edit=True, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
        bpy.ops.object.editmode_toggle()

        bpy.ops.mesh.primitive_cylinder_add(vertices=12, enter_editmode=False, align='WORLD', location=(0, 0, 6), scale=(2, 2, 4.5))
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
            
            
            
        

        """ def view3d_find( return_area = False ):
            # returns first 3d view, normally we get from context
            for area in bpy.context.window.screen.areas:
                if area.type == 'VIEW_3D':
                    v3d = area.spaces[0]
                    rv3d = v3d.region_3d
                    for region in area.regions:
                        if region.type == 'WINDOW':
                            if return_area: return region, rv3d, v3d, area
                            return region, rv3d, v3d
            return None, None

        region, rv3d, v3d, area = view3d_find(True) 

        override = {
            'scene'  : bpy.context.scene,
            'region' : region,
            'area'   : area,
            'space'  : v3d
        }

        bpy.ops.mesh.loopcut_slide(
            override, 
            MESH_OT_loopcut = {
                "number_cuts"           : 2,
                "smoothness"            : 0,     
                "falloff"               : 'SMOOTH',  # Was 'INVERSE_SQUARE' that does not exist
                "edge_index"            : 2,
                "mesh_select_mode_init" : (True, False, False),
                "object_index"          : 0
            },
            TRANSFORM_OT_edge_slide={"value":-0.00106458, "single_side":False, "use_even":False, "flipped":False, "use_clamp":True, "mirror":True, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "correct_uv":True, "release_confirm":False, "use_accurate":False})
 """








        bpy.ops.object.editmode_toggle()

        fir.parent = tribe
        fir.matrix_parent_inverse = tribe.matrix_world.inverted()
        bpy.ops.object.select_more()
        bpy.ops.object.join()
        bpy.ops.object.origin_set(type='ORIGIN_CURSOR')

        return fir