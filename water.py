import bpy

class Water():
    #def createWater(): 
        #    bpy.ops.mesh.primitive_plane_add(size=15, enter_editmode=True)
        #    bpy.ops.mesh.subdivide(number_cuts=50)
        #    bpy.ops.object.editmode_toggle()
        #    tex = bpy.data.textures.new(name = "cloud", type="CLOUDS")
        #    tex.noise_scale = 0.4
        #    bpy.context.object.modifiers.new(name="Displace", type='DISPLACE')
        #    bpy.data.objects["Plane"].modifiers["Displace"].strength = 0.5
        #    bpy.context.object.modifiers['Displace'].texture = tex
        #    bpy.ops.object.shade_smooth()

    def createWater(_self):
        bpy.ops.mesh.primitive_plane_add(size=10)
        mat_water: bpy.types.Material = bpy.data.materials.new("Water Material")
        mat_water.use_nodes = True
        nodes_water = mat_water.node_tree.nodes
        node_BSDF = nodes_water["Principled BSDF"]
        node_BSDF.inputs[0].default_value = [0.010519, 0.09228, 0.8, 1]
        node_BSDF.inputs[4].default_value = 0.8
        node_BSDF.inputs[7].default_value = 0.086
        node_bump = nodes_water.new("ShaderNodeBump")
        node_bump.inputs[0].default_value = 0.1
        node_tex = nodes_water.new("ShaderNodeTexMusgrave")
        node_tex.inputs[2].default_value = 21.8
        node_tex.inputs[3].default_value = 16
        node_tex.inputs[4].default_value = 1.2
        node_tex.inputs[5].default_value = 1.9
        node_mapping = nodes_water.new("ShaderNodeMapping")
        node_mapping.inputs[1].default_value = (0, 0, 0)
        node_mapping.inputs[1].keyframe_insert("default_value", frame=0)
        node_mapping.inputs[1].default_value = (0, 0, 1)
        node_mapping.inputs[1].keyframe_insert("default_value", frame=240)
        node_tex_coord = nodes_water.new("ShaderNodeTexCoord")
        mat_water.node_tree.links.new(node_tex_coord.outputs[0], node_mapping.inputs[0])
        mat_water.node_tree.links.new(node_mapping.outputs[0], node_tex.inputs[0])
        mat_water.node_tree.links.new(node_tex.outputs[0], node_bump.inputs[2])
        mat_water.node_tree.links.new(node_bump.outputs[0], node_BSDF.inputs[20])
        bpy.context.object.data.materials.append(bpy.data.materials.get("Water Material"))
        #fcurves = bpy.data.objects["Plane"].animation_data.action.fcurves[0].keyframe_points[0]
        #fcurves.interpolation = "LINEAR"