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

from bpy.utils import register_class, unregister_class
import bpy
from .ground import Ground
from .water import Water
from .simpleTree import SimpleTree

from .stone import OneStone
from .firTree import FirTree
from .mushroom import OneMushroom

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

    ISLAND_SIZE: bpy.props.IntProperty(name="Island Size", min=1, max=5, default=3)
    ISLAND_HEIGHT: bpy.props.IntProperty(name="Island Height", min=1, max=5, default=3)


    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        bpy.ops.object.select_all(action='SELECT') # selektiert alle Objekte
        bpy.ops.object.delete(use_global=False, confirm=False) # löscht selektierte objekte
        bpy.ops.outliner.orphans_purge() # löscht überbleibende Meshdaten etc.
        try:
            if(bpy.data.collections['new_collection']):
                bpy.data.collections.remove(bpy.data.collections['new_collection'])
        except:
            print("nicht vorhanden")

        stone = OneStone()
        stone.createStone()

        fir = FirTree()
        fir.createFirTree()

        mushroom = OneMushroom()
        mushroom.createMushroom()

        simpleTree = SimpleTree()
        simpleTree.create_leaf_material()
        simpleTree.create_tribe_material()
        for i in range(10):
            for j in range(1):
                simpleTree.normalTree([i,j,0], (i+1)*(j+1), self.TREE_HEIGHT_MIN, self.TREE_HEIGHT_MAX, self.BRANCH_LENGTH_MIN, self.BRANCH_LENGTH_MAX)

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

        collection.objects.link(bpy.data.objects["Stone"])
        bpy.data.collections["Collection"].objects.unlink(bpy.data.collections["Collection"].objects["Stone"])

        collection.objects.link(bpy.data.objects["fir"])
        bpy.data.collections["Collection"].objects.unlink(bpy.data.collections["Collection"].objects["fir"])

        collection.objects.link(bpy.data.objects["mushroom"])
        bpy.data.collections["Collection"].objects.unlink(bpy.data.collections["Collection"].objects["mushroom"])


        ground = Ground()
        ground.createGround(self.ISLAND_SIZE, self.ISLAND_HEIGHT)

        water = Water() 
        water.createWater()
        
        return {"FINISHED"}

def register():
    register_class(OT_Generate_Island)
 
def unregister():
    unregister_class(OT_Generate_Island)
 
if __name__ == '__main__':
    register()
#register, unregister = bpy.utils.register_classes_factory({OT_Generate_Island})