import bpy
import random
import bmesh
import typing

class SimpleTree():
    branches = []

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
        newBranchSpots = []
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
                newBranchSpots.append(newVert.co)
                _edges.append([lastVertBranch, newVert])
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
                newBranchSpots.append(lastVertBranch.co)
        _self.branches.append(newBranchSpots)

    def create_leaf_material(self, _season) -> bpy.types.Material:
        if(_season == "0"):
            leaveMaterialName = "simpleTreeLeaveSpring"
            leaveColor = (0.270 ,0.296 ,0.120 ,1)

        elif(_season == "1"):
            leaveMaterialName = "simpleTreeLeaveSummer"
            leaveColor = (0.195 ,0.347 ,0.018 ,1)

        elif(_season == "2"):
            leaveMaterialName = "simpleTreeLeaveAutumn"
            leaveColor = (0.806 ,0.414 ,0.056 ,1)
            
        elif(_season == "3"):
            leaveMaterialName = "simpleTreeLeaveWinter"
            leaveColor = (1,1,1,1)     

        mat_roof: bpy.types.Material = bpy.data.materials.new(leaveMaterialName)
        mat_roof.use_nodes = True
        nodes_roof: typing.List[bpy.types.Node] = mat_roof.node_tree.nodes
        nodes_roof["Principled BSDF"].inputs[0].default_value = leaveColor
        return mat_roof

    def create_tribe_material(self) -> bpy.types.Material:

        tribeMaterialName = "simpleTreeTribe"
        tribeColor = (0.114 ,0.041 ,0.010 ,1)

        mat_roof: bpy.types.Material = bpy.data.materials.new(tribeMaterialName)
        mat_roof.use_nodes = True
        nodes_roof: typing.List[bpy.types.Node] = mat_roof.node_tree.nodes
        nodes_roof["Principled BSDF"].inputs[0].default_value = tribeColor
        return mat_roof

    def createSimpleTree(_self, _root, _number, _treeLenMin, _treeLenMax, _branchLenMin, _branchLenMax, _season) -> object:
        tribeMaterialName = "simpleTreeTribe"

        if(_season == "0"):
                leaveMaterialName = "simpleTreeLeaveSpring"
        elif(_season == "1"):
                leaveMaterialName = "simpleTreeLeaveSummer"
        elif(_season == "2"):
                leaveMaterialName = "simpleTreeLeaveAutumn"
        elif(_season == "3"):
                leaveMaterialName = "simpleTreeLeaveWinter"

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
        trunk = bm.verts.new((0, 0, -0.2))
        vert_1 = bm.verts.new((0, 0, 0))
        edges.append([trunk, vert_1]) 
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
        tree_object.data.materials.append(bpy.data.materials.get(tribeMaterialName))
        bpy.context.view_layer.objects.active = tree_object     

        goalThiknes = 0.1
        startThikness = 0.8
        lastVertWasBranch = False
        lastVertThikness=0.35,0.35
        lastBranchVertThikness = 0.35,0.35

        for i, vert in enumerate(tree_object.data.skin_vertices[0].data):
            v = tree_object.data.vertices[i]
            if(i == 0):
                vert.radius = startThikness, startThikness
            if(_self.isBranch(v) == False):
                vert.radius = goalThiknes + ((startThikness - goalThiknes)/treeHeight) * (treeHeight/(i+1)) , goalThiknes + ((startThikness - goalThiknes)/treeHeight) * (treeHeight/(i+1))
                lastVertThikness = vert.radius[0], vert.radius[1]
                lastVertWasBranch = False
            else:
                if(lastVertWasBranch):
                    vert.radius = lastBranchVertThikness[0] /2, lastBranchVertThikness[1] /2
                    lastBranchVertThikness = vert.radius[0], vert.radius[1]
                    lastVertWasBranch = True
                else:
                    vert.radius = lastVertThikness[0] /2, lastVertThikness[1] /2
                    lastBranchVertThikness = vert.radius[0], vert.radius[1]
                    lastVertWasBranch = True
        
        tree_object.select_set(True)
        bpy.ops.object.modifier_apply(modifier="Skin")
        
        countEndpoints=0
        for i in endpointsOfTree:
            bpy.ops.mesh.primitive_cube_add(location=(i)) 
            bpy.context.object.modifiers.new(name="Subdivision", type='SUBSURF')
            if(countEndpoints==len(endpointsOfTree)-1):
                bpy.ops.transform.resize(value=(random.uniform(1.5, 2),random.uniform(1.5,2),random.uniform(1.5, 2)))
            else:
                bpy.ops.transform.resize(value=(random.uniform(0.5, 1.2),random.uniform(0.5, 1.2),random.uniform(0.5, 1.2)))
            bpy.context.object.parent = tree_object
            bpy.context.object.data.materials.append(bpy.data.materials.get(leaveMaterialName))
            bpy.context.view_layer.objects.active = tree_object
            bpy.data.objects["tree" + str(_number)].select_set(True)
            bpy.ops.object.join()
        
        return tree_object
    
    def isBranch(_self, _vert) ->bool:
        for branch in _self.branches:
            for i in branch:
                if(_vert.co == i):
                    return True
        return False