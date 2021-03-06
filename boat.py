import bpy
import random
import decimal
import math

class Boat():
    def createBoat(_self, _islandSize, _boatSpeed):
        filepath = "//boat.blend"
        name = "Boot"

        with bpy.data.libraries.load(filepath, link=True) as (data_from, data_to):
            for coll_name in data_from.collections: 
                if not coll_name.startswith(name):
                    continue
                data_to.collections.append(coll_name)
    
        scene = bpy.context.scene
        link_to_name = 'Boat-Scene'
        try:
            link_to = scene.collection.children[link_to_name]
        except KeyError:
            link_to = bpy.data.collections.new(link_to_name)
            scene.collection.children.link(link_to)

        for coll in data_to.collections: 
            empty = bpy.data.objects.new(coll.name, None)
            empty.instance_type = 'COLLECTION'
            empty.instance_collection = coll
            link_to.objects.link(empty)
            empty.location.z = 0.07
            empty.scale.x = 0.1
            empty.scale.y = 0.1
            empty.scale.z = 0.1

            #_self.randomLocation(empty, _islandSize)
            _self.animateBoat(empty, _islandSize, _boatSpeed)       

    def animateBoat(self, empty, _islandSize, _boatSpeed):
        frames = 250
        i = 0
        angle = 0
        _islandSize += 1
        rotationAngle = 0
        frameAnimationSteps = 5
        framesPerRound = frames / _boatSpeed
        anglePerFrame = 358 / (framesPerRound / frameAnimationSteps)
        anglePerFrameRadian = math.radians(anglePerFrame)
        
        while i <= frames:
            empty.location.x = float(decimal.Decimal(math.cos(angle)*_islandSize)) 
            empty.location.y = float(decimal.Decimal(math.sin(angle)*_islandSize)) 
            empty.keyframe_insert(data_path="location",frame=i)
            empty.rotation_euler[2] = rotationAngle
            empty.keyframe_insert("rotation_euler",frame=i)

            angle -= anglePerFrameRadian
            rotationAngle -= anglePerFrameRadian
            i += frameAnimationSteps 
        
    def randomLocation(self, empty, _islandSize): 
        locationX = float(decimal.Decimal(random.randrange(_islandSize*100, 470))/100)
        locationY = float(decimal.Decimal(random.randrange(_islandSize*100, 470))/100)

        probX = random.randrange(1, 100)
        probY = random.randrange(1, 100)

        if (probX > 50):
            locationX = locationX * -1
        if (probY > 50):
            locationY = locationY * -1
        
        empty.location.x = locationX
        empty.location.y = locationY
        empty.rotation_euler[2] = random.randrange(0, 360)
        empty.location.z = 0.07
        empty.scale.x = 0.1
        empty.scale.y = 0.1
        empty.scale.z = 0.1