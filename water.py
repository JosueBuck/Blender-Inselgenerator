import random
import bpy

from .sky import Sky

class Water():
    def createWater(_self, _season, _islandSize):
        waterScaleFactor = 4.5
        bpy.ops.mesh.primitive_plane_add(size= waterScaleFactor * _islandSize)
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
        node_mapping.inputs[1].keyframe_insert("default_value", frame=250)
        node_tex_coord = nodes_water.new("ShaderNodeTexCoord")
        mat_water.node_tree.links.new(node_tex_coord.outputs[0], node_mapping.inputs[0])
        mat_water.node_tree.links.new(node_mapping.outputs[0], node_tex.inputs[0])
        mat_water.node_tree.links.new(node_tex.outputs[0], node_bump.inputs[2])
        mat_water.node_tree.links.new(node_bump.outputs[0], node_BSDF.inputs[20])
        bpy.context.object.data.materials.append(bpy.data.materials.get("Water Material"))

        for c_curve in mat_water.node_tree.animation_data.action.fcurves:
            for c_keyframe in c_curve.keyframe_points:
                c_keyframe.interpolation = "LINEAR"
        
        if(_season == "3"):
            _self.createWinterObjects()

    def createWinterObjects(_self):
        iceShellObject = _self.createIceShell(1)
        bpy.context.view_layer.objects.active = bpy.data.objects.get("Plane")
        bpy.ops.object.particle_system_add()
        bpy.data.particles["ParticleSettings"].count = 100
        bpy.data.particles["ParticleSettings"].type = 'HAIR'
        bpy.data.particles["ParticleSettings"].render_type = 'OBJECT'
        bpy.data.particles["ParticleSettings"].instance_object = iceShellObject
        bpy.data.particles["ParticleSettings"].particle_size = 0.07
        bpy.data.particles["ParticleSettings"].hair_length = 2
        bpy.data.particles["ParticleSettings"].rotation_mode = 'OB_Y'
        bpy.data.particles["ParticleSettings"].size_random = 0.308219
        sky = Sky()
        sky.createSky()

    def createIceShell(_self, _number) -> object:
        iceCollection = bpy.context.blend_data.collections.new(name='ice_collection')

        bpy.ops.mesh.primitive_uv_sphere_add(segments=30, ring_count=30, align='WORLD', scale=(1,1,0.5))
        tex = bpy.data.textures.new(name = "cloud" + str(_number), type="CLOUDS")
        tex.noise_scale = random.uniform(1.5,2)
        tex.noise_depth = 1
        iceShellObject = bpy.context.object
        iceShellObject.modifiers.new(name="DisplaceShells", type='DISPLACE')
        iceShellObject.modifiers['DisplaceShells'].texture = tex
        iceShellObject.name = "Ice Shell"

        iceCollection.objects.link(iceShellObject)
        bpy.data.collections["Collection"].objects.unlink(iceShellObject)

        return iceShellObject