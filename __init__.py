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

from unicodedata import name
from bpy.utils import register_class, unregister_class
import bpy
from .ground import Ground
from .water import Water
from .simpleTree import SimpleTree
from .boat import Boat

from .stone import OneStone
from .firTree import FirTree
from .mushroom import OneMushroom

class MySettings(bpy.types.PropertyGroup):
    Island_Size: bpy.props.IntProperty(name="Island Size", min=1, max=5, default=3)
    Island_Height: bpy.props.IntProperty(name="Island Height", min=1, max=5, default=3)
    Season: bpy.props.EnumProperty(items=[
        ("0", "Spring", ""),
        ("1", "Summer", ""),
        ("2", "Autumn", ""),
        ("3", "Winter", "")
    ])
    Amount_Objects: bpy.props.IntProperty(name="Amount of Objects", min=1, max=60, default=60)
    Simple_Tree: bpy.props.BoolProperty(name="Simple Tree", default=True)
    Simple_Tree_Amount: bpy.props.IntProperty(name="Simple Tree Amount", min=1, max=10, default=1)
    Branch_Length_Min: bpy.props.IntProperty(name="Max Branch Length", min=2, max=4, default=2)
    Branch_Length_Max: bpy.props.IntProperty(name="Max Branch Length", min=2, max=4, default=4)
    Tree_Height_Min: bpy.props.IntProperty(name="Tree Height Min", min=5, max=8, default=5)
    Tree_Height_Max: bpy.props.IntProperty(name="Tree Height Max", min=5, max=8, default=8)

    Fir: bpy.props.BoolProperty(name="Fir", default=True)
    Fir_Amount: bpy.props.IntProperty(name="Fir Amount", min=1, max=10, default=2)

    Stone: bpy.props.BoolProperty(name="Stone", default=True)
    Stone_Amount: bpy.props.IntProperty(name="Stone Amount", min=1, max=10, default=5)
    
    Mushroom: bpy.props.BoolProperty(name="Mushroom", default=True)
    Mushroom_Amount: bpy.props.IntProperty(name="Mushroom Amount", min=1, max=10, default=5)
class MainPanel(bpy.types.Panel):
    bl_label = "Generate Island"
    bl_idname = "VIEW3D_PT_Main_Panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Generate Island'

    def draw(self, context):
        col = self.layout.column()
        myprop = context.scene.my_props

        row = col.row()
        row.prop(myprop, "Island_Size")

        row = col.row()
        row.prop(myprop, "Island_Height")

        row = col.row()
        row.prop(myprop, "Season")

        row = col.row()
        row.prop(myprop, "Amount_Objects")
        
        row = col.row()
        row.prop(myprop, "Simple_Tree")

        if myprop.Simple_Tree == True:
            row = col.row()
            row.prop(myprop, "Simple_Tree_Amount")
            row = col.row()
            row.prop(myprop, "Branch_Length_Min")
            row = col.row()
            row.prop(myprop, "Branch_Length_Max")
            row = col.row()
            row.prop(myprop, "Tree_Height_Min")
            row = col.row()
            row.prop(myprop, "Tree_Height_Max")
        
        row = col.row()
        row.prop(myprop, "Fir")

        if myprop.Fir == True:
            row = col.row()
            row.prop(myprop, "Fir_Amount")

        row = col.row()
        row.prop(myprop, "Stone")

        if myprop.Stone == True:
            row = col.row()
            row.prop(myprop, "Stone_Amount")

        row = col.row()
        row.prop(myprop, "Mushroom")

        if myprop.Mushroom == True:
            row = col.row()
            row.prop(myprop, "Mushroom_Amount")

        row = self.layout.row()
        row.operator("mesh.island_generator", text="Generate Island")
class OT_Generate_Island(bpy.types.Operator):

    bl_idname = "mesh.island_generator"
    bl_label = "Generate_Island"
    bl_description = "Generate an island"

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

        
        scene = context.scene

        newCollection = bpy.context.blend_data.collections.new(name='new_collection')

        if(scene.my_props.Simple_Tree == True):
            simpleTree = SimpleTree()
            simpleTree.create_leaf_material(scene.my_props.Season)
            simpleTree.create_tribe_material()
            for i in range(scene.my_props.Simple_Tree_Amount):
                for j in range(1):
                    tree = simpleTree.normalTree([i,j,0], (i+1)*(j+1), scene.my_props.Tree_Height_Min, scene.my_props.Tree_Height_Max, scene.my_props.Branch_Length_Min, scene.my_props.Branch_Length_Max, scene.my_props.Season)
                    newCollection.objects.link(tree)
                    bpy.data.collections["Collection"].objects.unlink(tree)

        if(scene.my_props.Stone == True):   
            stone = OneStone()
            for i in range(scene.my_props.Stone_Amount):
                stoneObject = stone.createStone()
                newCollection.objects.link(stoneObject)
                bpy.data.collections["Collection"].objects.unlink(stoneObject)

        if(scene.my_props.Fir == True):
            fir = FirTree()
            for i in range(scene.my_props.Fir_Amount):
                firObject = fir.createFirTree(scene.my_props.Season)
                newCollection.objects.link(firObject)
                bpy.data.collections["Collection"].objects.unlink(firObject)

        if(scene.my_props.Mushroom == True):
            mushroom = OneMushroom()
            for i in range(scene.my_props.Mushroom_Amount):
                mushroomObject = mushroom.createMushroom(scene.my_props.Season)
                newCollection.objects.link(mushroomObject)
                bpy.data.collections["Collection"].objects.unlink(mushroomObject)
        """ newCollection.objects.link(bpy.data.objects["fir"])
        bpy.data.collections["Collection"].objects.unlink(bpy.data.collections["Collection"].objects["fir"])

        newCollection.objects.link(bpy.data.objects["mushroom"])
        bpy.data.collections["Collection"].objects.unlink(bpy.data.collections["Collection"].objects["mushroom"]) """


        ground = Ground()
        ground.createGround(scene.my_props.Island_Size, scene.my_props.Island_Height, scene.my_props.Season, scene.my_props.Amount_Objects)

        water = Water() 
        water.createWater(scene.my_props.Season, scene.my_props.Island_Size)

        boat = Boat()
        boat.createBoat(scene.my_props.Island_Size)
        
        return {"FINISHED"}

classes = [MainPanel, OT_Generate_Island, MySettings] 

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    
    bpy.types.Scene.my_props = bpy.props.PointerProperty(type=MySettings)
 
def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

    del bpy.types.Scene.my_props
 
if __name__ == '__main__':
    register()