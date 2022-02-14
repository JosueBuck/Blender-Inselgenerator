import bpy
class Sky():
    def createSky(_self):
        bpy.ops.mesh.primitive_plane_add(size=20, location=(0,0,10))
        bpy.context.object.name = "sky"
        bpy.ops.object.particle_system_add()
        bpy.data.particles["ParticleSettings.001"].count = 2000
        bpy.data.particles["ParticleSettings.001"].force_field_1.type = 'WIND'
        bpy.data.particles["ParticleSettings.001"].mass = 0.01
        bpy.data.particles["ParticleSettings.001"].lifetime = 38