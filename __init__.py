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
from .boat import Boat

from .stone import OneStone
from .firTree import FirTree
from .mushroom import OneMushroom

class MainPanel(bpy.types.Panel):
    bl_label = "Generate Island"
    bl_idname = "VIEW3D_PT_Main_Panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'

    def draw(self, context):
        col = self.layout.column()
        for (prop_name, _) in props:
            row = col.row()
            row.prop(context.scene, prop_name)
            
            # insert operator
        row = self.layout.row()
        row.operator("mesh.island_generator", text="Generate Island")
class OT_Generate_Island(bpy.types.Operator):

    bl_idname = "mesh.island_generator"
    bl_label = "Generate_Island"
    bl_description = "Generate an island"

    
    amount_objects = 60 #should be between 0 - 60 (danach siehts affig aus)
    amount_trees = 1
    amount_stones = 5

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

        

        fir = FirTree()
        fir.createFirTree()

        mushroom = OneMushroom()
        mushroom.createMushroom()

        simpleTree = SimpleTree()
        simpleTree.create_leaf_material()
        simpleTree.create_tribe_material()
        
        newCollection = bpy.context.blend_data.collections.new(name='new_collection')

        scene = context.scene
        for i in range(self.amount_trees):
            for j in range(1):
                tree = simpleTree.normalTree([i,j,0], (i+1)*(j+1), scene.Tree_Height_Min, scene.Tree_Height_Max, scene.Branch_Length_Min, scene.Branch_Length_Max)
                newCollection.objects.link(tree)
                bpy.data.collections["Collection"].objects.unlink(tree)
                
        stone = OneStone()
        for i in range(self.amount_stones):
            stoneObject = stone.createStone()
            newCollection.objects.link(stoneObject)
            bpy.data.collections["Collection"].objects.unlink(stoneObject)

        collection.objects.link(bpy.data.objects["fir"])
        bpy.data.collections["Collection"].objects.unlink(bpy.data.collections["Collection"].objects["fir"])

        collection.objects.link(bpy.data.objects["mushroom"])
        bpy.data.collections["Collection"].objects.unlink(bpy.data.collections["Collection"].objects["mushroom"])


        ground = Ground()
        ground.createGround(scene.Island_Size, scene.Island_Height, scene.Season, self.amount_objects)

        water = Water() 
        water.createWater(scene.Season)

        boat = Boat()
        boat.createBoat(scene.Island_Size)
        
        return {"FINISHED"}

classes = [MainPanel, OT_Generate_Island] 

props = [
    ("Branch_Length_Min", bpy.props.IntProperty(name="Max Branch Length", min=2, max=4, default=2)),
    ("Branch_Length_Max", bpy.props.IntProperty(name="Max Branch Length", min=2, max=4, default=4)),
    ("Tree_Height_Min", bpy.props.IntProperty(name="Tree Height Min", min=5, max=8, default=5)),
    ("Tree_Height_Max", bpy.props.IntProperty(name="Tree Height Max", min=5, max=8, default=8)),
    ("Island_Size", bpy.props.IntProperty(name="Island Size", min=1, max=5, default=3)),
    ("Island_Height", bpy.props.IntProperty(name="Island Height", min=1, max=5, default=3)),
    ("Season", bpy.props.EnumProperty(items=[
        ("0", "Spring", ""),
        ("1", "Summer", ""),
        ("2", "Autumn", ""),
        ("3", "Winter", "")
    ]))
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    
    for (prop_name, prop_value) in props:
        setattr(bpy.types.Scene, prop_name, prop_value)
 
def unregister():
    for cls in classes:
        bpy.utils.register_class(cls)

    for (prop_name, prop_value) in props:
        delattr(bpy.types.Scene, prop_name)
 
if __name__ == '__main__':
    register()
#register, unregister = bpy.utils.register_classes_factory({OT_Generate_Island})