import bpy
import typing


class Cabin: 
    def floor(_self)-> object:
        floorgang=[]
        for i in range(16):
            bpy.ops.mesh.primitive_cylinder_add(vertices=7, depth=8, radius=0.25, enter_editmode=False, align='WORLD', location=(0, 0.5*i, 0), scale=(1, 1, 1), rotation=(0,1.57079633,0))
            tribe=bpy.data.objects.get("Cylinder")
            tribe.name="floorplank"+str(i)
            floorgang.append(tribe)
        for i in floorgang:
            i.select_set(True)
        bpy.ops.object.join()
        floor_object= bpy.data.objects.get("floorplank15")
        floor_object.name="floor"
        return floor_object

    def wall(_self, _direction)->object:
        rot=(0,0)
        trans=(0,0)
        if(_direction=="west"):
            trans=(0, 7.25)
            rot=(0,1.57079633)
        elif(_direction=="east"):
            trans=(0, 0.25)
            rot=(0,1.57079633)
        elif(_direction=="north"):
            trans=(3.5, 3.75)
            rot=(1.57079633,0)
        elif(_direction=="south"):
            trans=(-3.5, 3.75)
            rot=(1.57079633,0)

        wall=[]
        for i in range(8):
            bpy.ops.mesh.primitive_cylinder_add(vertices=7, depth=8, radius=0.25, enter_editmode=False, align='WORLD', location=(trans[0], trans[1], 0.5+0.5*i), scale=(1, 1, 1), rotation=(rot[0],rot[1],0))
            tribe=bpy.data.objects.get("Cylinder")
            tribe.name="wallplank"+str(i)
            wall.append(tribe)
        for i in wall:
            i.select_set(True)
        bpy.ops.object.join()
        wall_object= bpy.data.objects.get("wallplank7")
        wall_object.name="wall"+_direction
        return wall_object

    def roof(_self) -> object:
        roof_planks=[]
        for i in range(15):
            bpy.ops.mesh.primitive_cube_add(enter_editmode=False, align='WORLD', location=(4.5-0.31*i, 3.5, 4+0.1*i), scale=(0.268, 5, 0.074),rotation=(0,0.52708943,0))
            plank=bpy.data.objects.get("Cube")
            plank.name="plank0"+str(i)
            roof_planks.append(plank)
        for i in range(15):
            bpy.ops.mesh.primitive_cube_add(enter_editmode=False, align='WORLD', location=(-4.5+0.31*i, 3.5, 4+0.1*i), scale=(0.268, 5, 0.074),rotation=(0,-0.52708943,0))
            plank=bpy.data.objects.get("Cube")
            plank.name="plank1"+str(i)
            roof_planks.append(plank)
        for i in range(5):
            bpy.ops.mesh.primitive_cube_add(enter_editmode=False, align='WORLD', location=(0, 7, 4+0.28*i), scale=(0.14, 4-0.79*i, 0.074),rotation=(1.57079633,1.57079633,0))
            plank=bpy.data.objects.get("Cube")
            plank.name="plank2"+str(i)
            roof_planks.append(plank)
        for i in range(5):
            bpy.ops.mesh.primitive_cube_add(enter_editmode=False, align='WORLD', location=(0, 0.25, 4+0.28*i), scale=(0.14, 4-0.79*i, 0.074),rotation=(1.57079633,1.57079633,0))
            plank=bpy.data.objects.get("Cube")
            plank.name="plank3"+str(i)
            roof_planks.append(plank)

        for i in roof_planks:
            i.select_set(True)
        bpy.ops.object.join()
        roof_object= bpy.data.objects.get("plank34")
        roof_object.name="roof"
        return roof_object

    def schornstein(_self) ->object:
        bpy.ops.mesh.primitive_torus_add(align='WORLD', location=(1, 6, 5.3), major_segments=4, minor_segments=4, major_radius=1, minor_radius=1.2, abso_major_rad=1.25, abso_minor_rad=0.75)
        bpy.ops.transform.resize(value=(0.2, 0.2, 1), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
        schonrstein_objekt = bpy.data.objects.get("Torus")
        schonrstein_objekt.name="schornstein"
        return schonrstein_objekt

    def create_wood_material(_self) -> bpy.types.Material:
        mat_cabinwood: bpy.types.Material = bpy.data.materials.new("cabinwoodmaterial")
        mat_cabinwood.use_nodes = True
        nodes_cabinwood: typing.List[bpy.types.Node] = mat_cabinwood.node_tree.nodes
        nodes_cabinwood["Principled BSDF"].inputs[0].default_value = 0.114 ,0.041 ,0.010 ,1
        return mat_cabinwood

    def create_roof_material(_self) -> bpy.types.Material:
        mat_roof: bpy.types.Material = bpy.data.materials.new("cabinwoodmaterial")
        mat_roof.use_nodes = True
        nodes_roof: typing.List[bpy.types.Node] = mat_roof.node_tree.nodes
        nodes_roof["Principled BSDF"].inputs[0].default_value = 0.016 ,0.004 ,0.006,1
        return mat_roof

    def create_schonrstein_material(_self) -> bpy.types.Material:
        mat_roof: bpy.types.Material = bpy.data.materials.new("cabinwoodmaterial")
        mat_roof.use_nodes = True
        nodes_roof: typing.List[bpy.types.Node] = mat_roof.node_tree.nodes
        nodes_roof["Principled BSDF"].inputs[0].default_value = 0.115 ,0.115 ,0.115,1
        return mat_roof


    def createDoor(_self, wall:object) ->object:
        bpy.ops.mesh.primitive_cube_add(enter_editmode=False, align='WORLD', location=(0, 0, 1.75), scale=(1, 1, 1.5),rotation=(0,0,0))
        cube = bpy.data.objects.get("Cube")
        modifier_bool = wall.modifiers.new("Door Bool", "BOOLEAN")
        modifier_bool.object = cube
        bpy.context.view_layer.objects.active = wall
        bpy.ops.object.modifier_apply(modifier="Door Bool")
        bpy.context.view_layer.objects.active = cube
        bpy.ops.object.delete(use_global=False, confirm=False)

        bpy.ops.mesh.primitive_cube_add(enter_editmode=False, align='WORLD', location=(-0.7, 0.09, 1.5), scale=(0.07, 0.1, 0.07),rotation=(0,0,0))
        doorhandle=bpy.data.objects.get("Cube")
        doorhandle.name = "doorhandle"
        door_planks = []
        door_planks.append(doorhandle)
        for i in range(6):
            bpy.ops.mesh.primitive_cube_add(enter_editmode=False, align='WORLD', location=(0.05, 0.25, 0.5+0.5*i), scale=(0.95, 0.1, 0.24),rotation=(0,0,0))
            plank=bpy.data.objects.get("Cube")
            plank.name = "plank" + str(i)
            door_planks.append(plank)
        for i in door_planks:
            i.select_set(True)
        bpy.ops.object.join()
        door_objekt = bpy.data.objects.get("plank5")
        bpy.ops.object.shade_smooth()
        door_objekt.name="door"
        return door_objekt

    def createWindow(_self, wall:object) -> object:
        xVal=0
        if(wall.name == "wallnorth"):
            xVal=3.5
        elif(wall.name == "wallsouth"):
            xVal=-3.5
        bpy.ops.mesh.primitive_cube_add(enter_editmode=False, align='WORLD', location=(xVal, 3.5, 2.5), scale=(0.75, 0.6, 0.75),rotation=(0,0,0))
        cube = bpy.data.objects.get("Cube")
        modifier_bool = wall.modifiers.new("Window Bool", "BOOLEAN")
        modifier_bool.object = cube
        bpy.context.view_layer.objects.active = wall
        bpy.ops.object.modifier_apply(modifier="Window Bool")
        bpy.context.view_layer.objects.active = cube
        bpy.ops.object.delete(use_global=False, confirm=False)

        windowComponents = []
        bpy.ops.mesh.primitive_cube_add(enter_editmode=False, align='WORLD', location=(xVal, 3.5, 3.2), scale=(0.25, 0.6, 0.1),rotation=(0,0,0))
        windowTop=bpy.data.objects.get("Cube")
        windowTop.name="Window_Top"
        windowComponents.append(windowTop)
        bpy.ops.mesh.primitive_cube_add(enter_editmode=False, align='WORLD', location=(xVal, 3.5, 1.8), scale=(0.25, 0.6, 0.1),rotation=(0,0,0))
        windowBottom=bpy.data.objects.get("Cube")
        windowBottom.name="Window_Bottom"
        windowComponents.append(windowBottom)
        bpy.ops.mesh.primitive_cube_add(enter_editmode=False, align='WORLD', location=(xVal, 3, 2.5), scale=(0.25, 0.1, 0.75),rotation=(0,0,0))
        windowLeft=bpy.data.objects.get("Cube")
        windowLeft.name="Window_Left"
        windowComponents.append(windowLeft)
        bpy.ops.mesh.primitive_cube_add(enter_editmode=False, align='WORLD', location=(xVal, 4, 2.5), scale=(0.25, 0.1, 0.75),rotation=(0,0,0))
        windowRight=bpy.data.objects.get("Cube")
        windowRight.name="Window_Right"
        windowComponents.append(windowRight)

        bpy.ops.mesh.primitive_cylinder_add(vertices=7, depth=1.5, radius=0.05, enter_editmode=False, align='WORLD', location=(xVal, 3.5, 2.5), scale=(1, 1, 1), rotation=(0,0,0))
        vert=bpy.data.objects.get("Cylinder")
        vert.name="winVert"
        windowComponents.append(vert)
        bpy.ops.mesh.primitive_cylinder_add(vertices=7, depth=1, radius=0.05, enter_editmode=False, align='WORLD', location=(xVal, 3.5, 2.5), scale=(1, 1, 1), rotation=(1.57079633,0,0))
        hor=bpy.data.objects.get("Cylinder")
        hor.name="winHor"
        windowComponents.append(hor)

        for i in windowComponents:
            i.select_set(True)
        bpy.ops.object.join()
        window_objekt = bpy.data.objects.get("winHor")
        window_objekt.name = "window"
        return window_objekt

    def pivitPoint(_self)->object:
        bpy.ops.mesh.primitive_plane_add(size=0.01, enter_editmode=False, align='WORLD', location=(0, 3.5, -1), scale=(1, 1, 1))
        pivot=bpy.data.objects.get("Plane")
        pivot.name="pivot"
        return pivot

    def stilts(_self)->object:
        stilts = []
        for i in range(6):
            bpy.ops.mesh.primitive_cylinder_add(vertices=7, depth=1.5, radius=0.25, enter_editmode=False, align='WORLD', location=(3.5, 0+1.5*i, -0.75), scale=(1, 1, 1), rotation=(0,0,0))
            stilt = bpy.data.objects.get("Cylinder")
            stilt.name = "stilt0"+str(i)
            stilts.append(stilt)
        for i in range(6):
            bpy.ops.mesh.primitive_cylinder_add(vertices=7, depth=1.5, radius=0.25, enter_editmode=False, align='WORLD', location=(-3.5, 0+1.5*i, -0.75), scale=(1, 1, 1), rotation=(0,0,0))
            stilt = bpy.data.objects.get("Cylinder")
            stilt.name = "stilt1"+str(i)
            stilts.append(stilt)
        for i in stilts:
            i.select_set(True)
        bpy.ops.object.join()
        stilts_objekt = bpy.data.objects.get("stilt15")
        stilts_objekt.name = "stilts"
        return stilts_objekt

    def createCabin(_self)->object:
        cabinComponents = []

        floor_object = _self.floor()
        westWall_object = _self.wall("west")
        eastWall_object = _self.wall("east")
        northWall_object = _self.wall("north")
        southWall_object = _self.wall("south")
        roof_object = _self.roof()
        schornstein_objekt = _self.schornstein()
        door_object = _self.createDoor(eastWall_object)
        stilts_object = _self.stilts()

        windowNorth_object = _self.createWindow(northWall_object)
        windowSouth_object = _self.createWindow(southWall_object)
        pivot = _self.pivitPoint()

        woodMaterial = _self.create_wood_material()
        roofMaterial = _self.create_roof_material()
        schornsteinMaterial = _self.create_schonrstein_material()

        floor_object.data.materials.append(woodMaterial)
        westWall_object.data.materials.append(woodMaterial)
        eastWall_object.data.materials.append(woodMaterial)
        northWall_object.data.materials.append(woodMaterial)
        southWall_object.data.materials.append(woodMaterial)
        roof_object.data.materials.append(roofMaterial)
        schornstein_objekt.data.materials.append(schornsteinMaterial)
        door_object.data.materials.append(roofMaterial)
        windowNorth_object.data.materials.append(roofMaterial)
        windowSouth_object.data.materials.append(roofMaterial)
        stilts_object.data.materials.append(woodMaterial)

        bpy.context.view_layer.objects.active = pivot
        cabinComponents.append(pivot)
        cabinComponents.append(westWall_object)
        cabinComponents.append(eastWall_object)
        cabinComponents.append(northWall_object)
        cabinComponents.append(southWall_object)
        cabinComponents.append(door_object)
        cabinComponents.append(roof_object)
        cabinComponents.append(schornstein_objekt)
        cabinComponents.append(windowSouth_object)
        cabinComponents.append(windowNorth_object)
        cabinComponents.append(floor_object)
        cabinComponents.append(stilts_object)

        for i in cabinComponents:
            i.select_set(True)
        bpy.ops.object.join()
        cabin_object = bpy.data.objects.get("pivot")
        cabin_object.name = "Cabin"
        bpy.ops.transform.resize(value=(0.2, 0.2, 0.2))
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
        return cabin_object