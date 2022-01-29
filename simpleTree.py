import bpy
import random
import bmesh
import typing

class SimpleTree():
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

    def createBranch(_self, _branchVert, _endpointsOfTree, _direction, _bm, _edges, _lenMin, _lenMax):
        #print("ast")
        branchLength = int(random.uniform(_lenMin, _lenMax))
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
                #print(lastVertBranch.co)
                #print("ast Ende")
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

    def normalTree(_self, _root, _number, _treeLenMin, _treeLenMax, _branchLenMin, _branchLenMax) -> object:
    # Mesh und Objekt erstellen
        tree_mesh = bpy.data.meshes.new("tree_mesh")
        tree_object = bpy.data.objects.new("tree" + str(_number), tree_mesh)
        tree_object.name = "tree" + str(_number)
        tree_object.location = (_root[0], _root[1], _root[2])
        # Mesh in aktuelle Collection der Szene verlinken
        bpy.context.collection.objects.link(tree_object)
        # 
        bm = bmesh.new()
        bm.from_mesh(tree_mesh)
        bpy.data.meshes.new(name="treeMesh")
        edges = []
        endpointsOfTree = []
        treeHeight = int(random.uniform(_treeLenMin, _treeLenMax))
        vert_1 = bm.verts.new((0, 0, 0))
        lastVert = vert_1
        for i in range(treeHeight):
            if(i == treeHeight - 1): 
                endOfTribCoord = _self.getCoordNextStepTribe(lastVert.co)
                endpointsOfTree.append((endOfTribCoord[0], endOfTribCoord[1], endOfTribCoord[2]))
                newVert = bm.verts.new((endOfTribCoord[0], endOfTribCoord[1], endOfTribCoord[2]))
                edges.append([lastVert, newVert])
            else:
                newVert = bm.verts.new(_self.getCoordNextStepTribe(lastVert.co))
                newBranch = random.uniform(0,100)
                if(newBranch > 80 and newBranch < 85):
                    _self.createBranch(newVert, endpointsOfTree, "west", bm, edges, _branchLenMin, _branchLenMax)
                if(newBranch >= 85 and newBranch < 90):
                    _self.createBranch(newVert, endpointsOfTree, "east", bm, edges, _branchLenMin, _branchLenMax)
                if(newBranch >= 90 and newBranch < 95):
                    _self.createBranch(newVert, endpointsOfTree, "south", bm, edges, _branchLenMin, _branchLenMax)
                if(newBranch >= 95 and newBranch <= 100):
                    _self.createBranch(newVert, endpointsOfTree, "north", bm, edges, _branchLenMin, _branchLenMax)
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
            bpy.ops.mesh.primitive_cube_add(location=(i)) 
            bpy.context.object.modifiers.new(name="Subdivision", type='SUBSURF')
            bpy.context.object.parent = tree_object
            bpy.context.object.data.materials.append(bpy.data.materials.get("Leaf Material"))
            bpy.context.view_layer.objects.active = tree_object
            bpy.data.objects["tree" + str(_number)].select_set(True)
            bpy.ops.object.join()
        
        return tree_object