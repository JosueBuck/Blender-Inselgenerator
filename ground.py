import bpy
import random
import typing

class Ground():
    def createGroundMaterial(_self, _season) -> bpy.types.Material:

        if(_season == "0"):
            groundMaterialName = "groundMaterialSpring"
            groundColors = [(0.001,0.015,0.000468,1), (0.006,0.061,0.002,1), (0.08,0.236,0.017,1), (0.01,0.008,0.004,1)]
        elif(_season == "1"):
            groundMaterialName = "groundMaterialSummer"
            groundColors = [(0.001,0.015,0.000468,1), (0.006,0.061,0.002,1), (0.08,0.236,0.017,1), (0.01,0.008,0.004,1)]
        elif(_season == "2"):
            groundMaterialName = "groundMaterialAutumn"
            groundColors = [(0.001,0.015,0.000468,1), (0.006,0.061,0.002,1), (0.08,0.236,0.017,1), (0.01,0.008,0.004,1)]
        elif(_season == "3"):
            groundMaterialName = "groundMaterialWinter"
            groundColors = [(0.001,0.015,0.000468,1), (0.006,0.061,0.002,1), (0.08,0.236,0.017,1), (0.01,0.008,0.004,1)]

        mat_ground: bpy.types.Material = bpy.data.materials.new(groundMaterialName)
        mat_ground.use_nodes = True
        nodes_ground: typing.List[bpy.types.Node] = mat_ground.node_tree.nodes
        #colorRamp Node
        nodes_colorRamp: bpy.types.Node = nodes_ground.new("ShaderNodeValToRGB")
        nodes_colorRamp.color_ramp.elements[0].color = groundColors[0]
        nodes_colorRamp.color_ramp.elements[0].position = 0.373
        nodes_colorRamp.color_ramp.elements[1].color = groundColors[1]
        nodes_colorRamp.color_ramp.elements[1].position = 0.991
        nodes_colorRamp.color_ramp.elements.new(0.75)
        nodes_colorRamp.color_ramp.elements[1].color = groundColors[2]
        nodes_colorRamp.color_ramp.elements.new(0.1)
        nodes_colorRamp.color_ramp.elements[0].color = groundColors[3]
        nodes_colorRamp.color_ramp.interpolation = "CONSTANT"
        #Tex Coordinate
        nodes_TexCoord: bpy.types.Node = nodes_ground.new("ShaderNodeTexCoord")
        #Seperate XYZ
        nodes_seperateXYZ: bpy.types.Node = nodes_ground.new("ShaderNodeSeparateXYZ")
        nodes_ground["Principled BSDF"].inputs[4].default_value = 0
        nodes_ground["Principled BSDF"].inputs[5].default_value = 0.264
        nodes_ground["Principled BSDF"].inputs[7].default_value = 0.932
        mat_ground.node_tree.links.new(nodes_TexCoord.outputs[1], nodes_seperateXYZ.inputs[0])
        mat_ground.node_tree.links.new(nodes_seperateXYZ.outputs[2], nodes_colorRamp.inputs[0])
        mat_ground.node_tree.links.new(nodes_colorRamp.outputs[0], nodes_ground["Principled BSDF"].inputs[0])
        return mat_ground


    def createGroundGeoNodes(_self, amountObjects) -> bpy.types.NodeTree:
        ground_geoNodes: bpy.types.NodeTree = bpy.data.node_groups.new("Ground Geo Nodes", "GeometryNodeTree")
        groupInput: bpy.types.Node = ground_geoNodes.nodes.new("NodeGroupInput")

        attSep: bpy.types.Node = ground_geoNodes.nodes.new("GeometryNodeAttributeSeparateXYZ")
        attSep.inputs[1].default_value = "normal"
        attSep.inputs[5].default_value = "nz"

        attMathASin: bpy.types.Node = ground_geoNodes.nodes.new("GeometryNodeAttributeMath")
        attMathASin.operation = 'ARCSINE'
        attMathASin.inputs[1].default_value = "nz"
        attMathASin.inputs[7].default_value = "nz"
        attMathToDeg: bpy.types.Node = ground_geoNodes.nodes.new("GeometryNodeAttributeMath")
        attMathToDeg.operation = 'DEGREES'
        attMathToDeg.inputs[1].default_value = "nz"
        attMathToDeg.inputs[7].default_value = "nz"

        attMapRange: bpy.types.Node = ground_geoNodes.nodes.new("GeometryNodeAttributeMapRange")
        attMapRange.inputs[1].default_value = "nz"
        attMapRange.inputs[2].default_value = "nz"
        attMapRange.inputs[3].default_value = 60
        attMapRange.inputs[4].default_value = 90.6

        pointDist: bpy.types.Node = ground_geoNodes.nodes.new("GeometryNodePointDistribute")
        pointDist.inputs[3].default_value = "nz"
        pointDist.inputs[2].default_value = amountObjects

        pointScale: bpy.types.Node = ground_geoNodes.nodes.new("GeometryNodePointScale")
        pointScale.input_type = 'FLOAT'
        pointScale.inputs[3].default_value = 0.14
        attRand: bpy.types.Node = ground_geoNodes.nodes.new("GeometryNodeAttributeRandomize")
        attRand.inputs[1].default_value = "rotation"
        attRand.inputs[5].default_value = 0
        pointInst: bpy.types.Node = ground_geoNodes.nodes.new("GeometryNodePointInstance")
        pointInst.instance_type = 'COLLECTION'
        pointInst.use_whole_collection = False
        pointInst.inputs[2].default_value = bpy.data.collections["new_collection"]
        joinGeo: bpy.types.Node = ground_geoNodes.nodes.new("GeometryNodeJoinGeometry")
        groupOut: bpy.types.Node = ground_geoNodes.nodes.new("NodeGroupOutput")
        ground_geoNodes.links.new(groupInput.outputs[0],attSep.inputs[0])
        ground_geoNodes.links.new(attSep.outputs[0],attMathASin.inputs[0])
        ground_geoNodes.links.new(attMathASin.outputs[0],attMathToDeg.inputs[0])
        ground_geoNodes.links.new(attMathToDeg.outputs[0],attMapRange.inputs[0])
        ground_geoNodes.links.new(attMapRange.outputs[0],pointDist.inputs[0])
        ground_geoNodes.links.new(pointDist.outputs[0],pointScale.inputs[0])
        ground_geoNodes.links.new(pointScale.outputs[0],attRand.inputs[0])
        ground_geoNodes.links.new(attRand.outputs[0],pointInst.inputs[0])
        ground_geoNodes.links.new(pointInst.outputs[0],joinGeo.inputs[0])
        ground_geoNodes.links.new(groupInput.outputs[0],joinGeo.inputs[0])
        ground_geoNodes.links.new(joinGeo.outputs[0],groupOut.inputs[0])
        return ground_geoNodes


    def createGround(_self, _islandSize, _islandHeight, _season, _amountObjects):


        groundMaterialName = "groundMaterial"

        if(_season == "0"):
            groundMaterialName = "groundMaterialSpring"
        elif(_season == "1"):
            groundMaterialName = "groundMaterialSummer"
        elif(_season == "2"):
            groundMaterialName = "groundMaterialAutumn"
        elif(_season == "3"):
                groundMaterialName = "groundMaterialWinter"

        _self.createGroundMaterial(_season)
        bpy.ops.mesh.primitive_uv_sphere_add(segments=60, ring_count=60,enter_editmode=True, align='WORLD', scale=(_islandSize, _islandSize, _islandHeight))
        bpy.ops.object.editmode_toggle()
        tex = bpy.data.textures.new(name = "cloud", type="CLOUDS")
        tex.noise_scale = random.uniform(0.51,1.37)
        tex.noise_depth = 1
        tex.noise_type = "HARD_NOISE"
        bpy.context.object.modifiers.new(name="Displace", type='DISPLACE')
        bpy.context.object.modifiers['Displace'].texture = tex
        bpy.context.object.data.materials.append(bpy.data.materials.get(groundMaterialName))


        bpy.context.object.modifiers.new("GeoNodesModifier", "NODES")
        bpy.context.object.modifiers['GeoNodesModifier'].node_group = _self.createGroundGeoNodes(_amountObjects)

        bpy.ops.transform.resize(value=(1, 1, random.uniform(0.3,0.5)), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
        bpy.ops.object.shade_smooth()