bl_info = {
    "name" : "island_generator",
    "author" : "SexyPeople",
    "description" : "",
    "blender" : (2, 80, 0),
    "version" : (0, 0, 1),
    "location" : "",
    "warning" : "",
    "category" : "Generic"
}

from bmesh.types import BMVert
from bpy.utils import register_class, unregister_class
import bpy
import bmesh
import random
import typing

from mathutils import Vector

class OT_Generate_Island(bpy.types.Operator):

    bl_idname = "mesh.island_generator"
    bl_label = "Generate_Island"
    bl_description = "Generate an island"
    bl_options = {"REGISTER", "UNDO"}

    ####normal Tree start
    BRANCH_LENGTH_MIN: bpy.props.IntProperty(name="Max Branch Length", min=2, max=4, default=2)
    BRANCH_LENGTH_MAX: bpy.props.IntProperty(name="Max Branch Length", min=2, max=4, default=4)

    TREE_HEIGHT_MIN: bpy.props.IntProperty(name="Tree Height Min", min=5, max=8, default=5)
    TREE_HEIGHT_MAX: bpy.props.IntProperty(name="Tree Height Max", min=5, max=8, default=8)

    def getCoordNextStepTribe(_self, _lastVert) -> float():
        xPos = random.uniform(-0.3,0.3)
        yPos = random.uniform(-0.3,0.3)
        zPos = random.uniform(0.5, 0.9)
        newPos = [_lastVert[0] + xPos, _lastVert[1] + yPos, _lastVert[2] + zPos]
        return newPos

    def getCoordNextStepBranchEast(_self, _lastVert) -> float():
        xPos = random.uniform(0.5, 0.8)
        yPos = random.uniform(-0.3,0.3)
        zPos = random.uniform(0.1, 0.3)
        newPos = [_lastVert[0] + xPos, _lastVert[1] + yPos, _lastVert[2] + zPos]
        return newPos

    def getCoordNextStepBranchWest(_self, _lastVert) -> float():
        xPos = random.uniform(-0.8,-0.5)
        yPos = random.uniform(-0.3,0.3)
        zPos = random.uniform(0.3, 0.5)
        newPos = [_lastVert[0] + xPos, _lastVert[1] + yPos, _lastVert[2] + zPos]
        return newPos

    def getCoordNextStepBranchNorth(_self, _lastVert) -> float():
        xPos = random.uniform(-0.3,0.3)
        yPos = random.uniform(0.5,0.8)
        zPos = random.uniform(0.3, 0.5)
        newPos = [_lastVert[0] + xPos, _lastVert[1] + yPos, _lastVert[2] + zPos]
        return newPos

    def getCoordNextStepBranchSouth(_self, _lastVert) -> float():
        xPos = random.uniform(-0.3,0.3)
        yPos = random.uniform(-0.8,-0.5)
        zPos = random.uniform(0.3, 0.5)
        newPos = [_lastVert[0] + xPos, _lastVert[1] + yPos, _lastVert[2] + zPos]
        return newPos

    def createBranch(_self, _branchVert, _endpointsOfTree, _direction, _bm, _edges):
        print("ast")
        branchLength = int(random.uniform(_self.BRANCH_LENGTH_MIN, _self.BRANCH_LENGTH_MAX))
        lastVertBranch = _branchVert
        for i in range(branchLength):
            if(i == branchLength - 1):
                if(_direction == "west"):
                    endOfBranchCoord = _self.getCoordNextStepBranchWest(lastVertBranch.co)
                if(_direction == "east"):
                    endOfBranchCoord = _self.getCoordNextStepBranchEast(lastVertBranch.co)
                if(_direction == "south"):
                    endOfBranchCoord = _self.getCoordNextStepBranchSouth(lastVertBranch.co)
                if(_direction == "north"):
                    endOfBranchCoord = _self.getCoordNextStepBranchNorth(lastVertBranch.co)

                _endpointsOfTree.append((endOfBranchCoord[0], endOfBranchCoord[1], endOfBranchCoord[2]))
                newVert = _bm.verts.new((endOfBranchCoord[0], endOfBranchCoord[1], endOfBranchCoord[2]))
                _edges.append([lastVertBranch, newVert])
                print(lastVertBranch.co)
                print("ast Ende")
            else:
                if(_direction == "west"):
                    newVert = _bm.verts.new(_self.getCoordNextStepBranchWest(lastVertBranch.co))
                if(_direction == "east"):
                    newVert = _bm.verts.new(_self.getCoordNextStepBranchEast(lastVertBranch.co))
                if(_direction == "south"):
                    newVert = _bm.verts.new(_self.getCoordNextStepBranchSouth(lastVertBranch.co))
                if(_direction == "north"):
                    newVert = _bm.verts.new(_self.getCoordNextStepBranchNorth(lastVertBranch.co))
                _edges.append([lastVertBranch, newVert])
                lastVertBranch = newVert

    def create_leaf_material(self) -> bpy.types.Material:
        mat_roof: bpy.types.Material = bpy.data.materials.new("Leaf Material")
        mat_roof.use_nodes = True
        nodes_roof: typing.List[bpy.types.Node] = mat_roof.node_tree.nodes
        nodes_roof["Principled BSDF"].inputs[0].default_value = [0, 1, 0, 1.000000]
        return mat_roof

    def create_tribe_material(self) -> bpy.types.Material:
        mat_roof: bpy.types.Material = bpy.data.materials.new("Tribe Material")
        mat_roof.use_nodes = True
        nodes_roof: typing.List[bpy.types.Node] = mat_roof.node_tree.nodes
        nodes_roof["Principled BSDF"].inputs[0].default_value = [0.8, 0.4, 0.1, 1.000000]
        return mat_roof

    def normalTree(_self, _root, _number):
        # Mesh und Objekt erstellen
        tree_mesh = bpy.data.meshes.new("tree_mesh")
        tree_object = bpy.data.objects.new("tree" + str(_number), tree_mesh)
        tree_object.location = (_root[0], _root[1], _root[2])

        # Mesh in aktuelle Collection der Szene verlinken
        bpy.context.collection.objects.link(tree_object)

        # 
        bm = bmesh.new()
        bm.from_mesh(tree_mesh)

        bpy.data.meshes.new(name="treeMesh")
        bm = bmesh.new()

        edges = []
        endpointsOfTree = []

        treeHight = int(random.uniform(_self.BRANCH_LENGTH_MIN, _self.BRANCH_LENGTH_MAX))
        vert_1 = bm.verts.new((0, 0, 0))
        lastVert = vert_1

        for i in range(treeHight):
            if(i == treeHight - 1): 
                endOfTribCoord = _self.getCoordNextStepTribe(lastVert.co)
                endpointsOfTree.append((endOfTribCoord[0], endOfTribCoord[1], endOfTribCoord[2]))
                newVert = bm.verts.new((endOfTribCoord[0], endOfTribCoord[1], endOfTribCoord[2]))
                edges.append([lastVert, newVert])
            else:
                newVert = bm.verts.new(_self.getCoordNextStepTribe(lastVert.co))
                newBranch = random.uniform(0,100)
                if(newBranch > 80 and newBranch < 85):
                    _self.createBranch(newVert, endpointsOfTree, "west", bm, edges)
                if(newBranch >= 85 and newBranch < 90):
                    _self.createBranch(newVert, endpointsOfTree, "east", bm, edges)
                if(newBranch >= 90 and newBranch < 95):
                    _self.createBranch(newVert, endpointsOfTree, "south", bm, edges)
                if(newBranch >= 95 and newBranch <= 100):
                    _self.createBranch(newVert, endpointsOfTree, "north", bm, edges)
                edges.append([lastVert, newVert])
                lastVert = newVert

        for i in edges:
            bm.edges.new(i)

        bm.to_mesh(tree_mesh)
        bm.free()

        #Attach Modifiers
        tree_skin_modifier = tree_object.modifiers.new(name="Skin", type='SKIN')
        tree_skin_modifier.branch_smoothing = 1
        tree_object.modifiers.new(name="Subdivision", type='SUBSURF')
        tree_object.data.materials.append(bpy.data.materials.get("Tribe Material"))
        bpy.context.view_layer.objects.active = tree_object
        tree_object.select_set(True)
        bpy.ops.object.modifier_apply(modifier="Skin")


        for i in endpointsOfTree:
            leaf_object = bpy.ops.mesh.primitive_cube_add(location=(i)) 
            bpy.context.object.modifiers.new(name="Subdivision", type='SUBSURF')
            bpy.context.object.parent = tree_object
            bpy.context.object.data.materials.append(bpy.data.materials.get("Leaf Material"))
            bpy.context.view_layer.objects.active = tree_object
            bpy.data.objects["tree" + str(_number)].select_set(True)
            bpy.ops.object.join()


    ####normal Tree End


    def createGround(self):
        #bpy.ops.mesh.primitive_plane_add(size=10, enter_editmode=True)
        #bpy.ops.mesh.primitive_cube_add(enter_editmode=True, align='WORLD', location=(0, 0, 0), scale=(10, 10, 1))
        bpy.ops.mesh.primitive_uv_sphere_add(enter_editmode=True, align='WORLD', scale=(3, 3, 3))
        #bpy.ops.mesh.subdivide(number_cuts=50)
        bpy.ops.object.editmode_toggle()
        tex = bpy.data.textures.new(name = "cloud", type="CLOUDS")
        tex.noise_scale = 0.88
        #tex.noise_type = "HARD_NOISE"
        tex.noise_depth = 2
        bpy.context.object.modifiers.new(name="Displace", type='DISPLACE')
        bpy.context.object.modifiers['Displace'].texture = tex
        #bpy.ops.object.shade_smooth()
        bpy.ops.object.particle_system_add()
        bpy.data.particles["ParticleSettings"].type = 'HAIR'
        bpy.data.particles["ParticleSettings"].render_type = 'COLLECTION'
        bpy.data.particles["ParticleSettings"].instance_collection = bpy.data.collections["new_collection"]
        bpy.data.particles["ParticleSettings"].use_advanced_hair = True
        bpy.data.particles["ParticleSettings"].use_rotations = True
        bpy.data.particles["ParticleSettings"].rotation_mode = 'GLOB_Y'
        bpy.data.particles["ParticleSettings"].count = 30
        bpy.ops.transform.resize(value=(1, 1, 0.1), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)


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

    ####fir tree
    def firTree(_root, _number):
        bpy.ops.mesh.primitive_cylinder_add(vertices=11, location=_root)


    def createWater(self):
        plane = bpy.ops.mesh.primitive_plane_add(size=10)
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

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        bpy.ops.object.select_all(action='SELECT') # selektiert alle Objekte
        bpy.ops.object.delete(use_global=False, confirm=False) # löscht selektierte objekte
        bpy.ops.outliner.orphans_purge() # löscht überbleibende Meshdaten etc.
        self.create_leaf_material()
        self.create_tribe_material()
        for i in range(10):
            for j in range(1):
                self.normalTree([i,j,0], (i+1)*(j+1))

        collection = bpy.context.blend_data.collections.new(name='new_collection')

        for i in range(10):
            for j in range(1):
                num = (i+1)*(j+1)
                bpy.data.objects["tree" + str(num)].select_set(True)

        counter = 1
        for tree in bpy.context.selected_objects:
            collection.objects.link(tree)
            bpy.data.collections["Collection"].objects.unlink(bpy.data.collections["Collection"].all_objects["tree" + str(counter)])
            counter += 1
        self.createGround()
        self.createWater()
        
        
        return {"FINISHED"}

def register():
    register_class(OT_Generate_Island)
 
 
def unregister():
    unregister_class(OT_Generate_Island)
 
 
if __name__ == '__main__':
    register()
#register, unregister = bpy.utils.register_classes_factory({OT_Generate_Island})