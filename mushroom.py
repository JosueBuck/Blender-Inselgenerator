import bpy
import random
import bmesh

class OneMushroom():
    def createMushroom(_self, _season)-> object:
        tribeMaterialName = "mushroomTribe"
        tribeColor = (0.584, 0.423, 0.423, 1)

        if(_season == "0"):
            mushroomHatColor = (0.917, 0.493, 0.600, 1)
            mushroomMaterialName = "mushroomHatSpring"
        elif(_season == "1"):
            mushroomHatColor = (0.855, 0, 0, 1)
            mushroomMaterialName = "mushroomHatSummer"
        elif(_season == "2"):
            mushroomHatColor = (0.127, 0.050, 0.026, 1)
            mushroomMaterialName = "mushroomHatAutumn"
        elif(_season == "3"):
            mushroomHatColor = (0.031, 0.038, 0.072, 1)
            mushroomMaterialName = "mushroomHatWinter"

        if bpy.context.mode == "EDIT_MESH":
            bpy.ops.object.mode_set(mode='OBJECT')  

        bpy.ops.mesh.primitive_cylinder_add(vertices=12, enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(.09, .09, .3))
        tribe = bpy.context.object
        tribe.name = 'tribe'
        bpy.ops.object.editmode_toggle()
        tribe_mesh = bpy.context.view_layer.objects.active.data

        bm = bmesh.from_edit_mesh(tribe_mesh)

        for vert in bm.verts:
            for l in vert.link_edges:
                if vert.index % 2 == 1:
                    vert.co[0] = vert.co[0] * 0.85
                    vert.co[1] = vert.co[1] * 0.85

        bpy.ops.object.editmode_toggle()

        for edge in tribe.data.edges:
            edge.select = False

        for poly in tribe.data.polygons:
            if poly.index != 10:
                poly.select = False

        mat = bpy.data.materials.get(tribeMaterialName)

        if mat is None:
            mat = bpy.data.materials.new(name=tribeMaterialName)
            mat.use_nodes = True
            mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = tribeColor

        mat.use_nodes = True

        if tribe.data.materials:
            tribe.data.materials[0] = mat
        else: 
            tribe.data.materials.append(mat)

        DECIMATE_FACTOR = random.uniform(0.95, 1)

        bpy.ops.mesh.primitive_ico_sphere_add(radius=1, enter_editmode=False, align='WORLD', location=(0, 0, .3), scale=(0.4, 0.4, 0.1))
        mushroom = bpy.context.object
        mushroom.name = 'mushroom'
        decimate_modifier: bpy.types.DecimateModifier = mushroom.modifiers.new("decimate", type="DECIMATE")

        decimate_modifier.ratio = DECIMATE_FACTOR

        bpy.ops.object.editmode_toggle()

        mushroom_mesh = bpy.context.view_layer.objects.active.data

        bm = bmesh.from_edit_mesh(mushroom_mesh)

        bpy.context.scene.tool_settings.use_proportional_edit = True

        vl=[]

        for vert in bm.verts:
            for l in vert.link_edges:
                selected_vert = random.randint(0, 2)
                selected_vert2 = random.randint(0, 2)
                vert_value = random.uniform(0.7, 1)
                if selected_vert == selected_vert2:
                    vert.co[selected_vert] =  vert.co[selected_vert] * vert_value
                vl.append(vert.co)

        bpy.ops.object.editmode_toggle()

        mat = bpy.data.materials.get(mushroomMaterialName)

        if mat is None:
            mat = bpy.data.materials.new(name=mushroomMaterialName)
            mat.use_nodes = True
            mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = mushroomHatColor
            
        mat.use_nodes = True

        if mushroom.data.materials:
            mushroom.data.materials[0] = mat
        else: 
            mushroom.data.materials.append(mat)

        mushroom.parent = tribe
        mushroom.matrix_parent_inverse = tribe.matrix_world.inverted()
        bpy.ops.object.select_more()
        bpy.ops.object.join()
        bpy.ops.object.origin_set(type='ORIGIN_CURSOR')

        return mushroom