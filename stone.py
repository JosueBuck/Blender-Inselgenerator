import bpy
import random
import bmesh


class OneStone():

    DECIMATE_FACTOR = random.uniform(0.35, 0.55)
    """ MATERIAL_NAME = "stone_material" """

    def createStone(_self)-> object:


        stoneMaterialName = "stoneMaterial"
        stoneColor = (0.127 ,0.127 ,0.127 ,1)


        """ match season:
            case "SPRING":
                
                stoneMaterialName = ""
                stoneColor = (0,0,0,1)
                return

            case "SUMMER":

                stoneMaterialName = ""
                stoneColor = (0,0,0,1)
                return

            case "AUTUMN":

                stoneMaterialName = ""
                stoneColor = (0,0,0,1)
                return
            
            case "WINTER":

                stoneMaterialName = ""
                stoneColor = (0,0,0,1)
                return """

        bpy.ops.mesh.primitive_ico_sphere_add(
            radius=1, enter_editmode=False, align='WORLD', location=(0, 0, 8), scale=(1, 1, 1))


        stone = bpy.context.object
        stone.name = 'Stone'
        decimate_modifier: bpy.types.DecimateModifier = stone.modifiers.new(
            "decimate", type="DECIMATE")

        decimate_modifier.ratio = _self.DECIMATE_FACTOR

        bpy.ops.object.editmode_toggle()

        stone_mesh = bpy.context.view_layer.objects.active.data

        bm = bmesh.from_edit_mesh(stone_mesh)

        bpy.context.scene.tool_settings.use_proportional_edit = True
        #print(bpy.data.scenes["Scene"])


        vl = []


        for vert in bm.verts:

            for l in vert.link_edges:
                selected_vert = random.randint(0, 2)
                selected_vert2 = random.randint(0, 2)
                vert_value = random.uniform(0.7, 1)
                #print(selected_vert)
                if selected_vert == selected_vert2:
                    vert.co[selected_vert] = vert.co[selected_vert] * vert_value
                vl.append(vert.co)


        bpy.ops.object.editmode_toggle()

        mat = bpy.data.materials.get(stoneMaterialName)

        if mat is None:
            mat = bpy.data.materials.new(name=stoneMaterialName)
            mat.use_nodes = True
            mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = stoneColor


        mat.use_nodes = True

        if stone.data.materials:
            stone.data.materials[0] = mat
        else:
            stone.data.materials.append(mat)
        
        return stone
