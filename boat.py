import bpy
import random
import decimal

class Boat():


    def createBoat(_self, _islandSize):
        filepath = "//boat.blend"
        name = "Boot"

        with bpy.data.libraries.load(filepath, link=True) as (data_from, data_to):
            for coll_name in data_from.collections: 
                if not coll_name.startswith(name):
                    continue
                data_to.collections.append(coll_name)

        #collection erstellen in die man dann die anderen collections reinlädt
        #gibt es die collection schon? wenn nicht -> neue erstellen mit dem Namen Boat-Scene
    
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
            print("ISLAND SIZE")
            print(_islandSize)
            
            empty.location.x = float(decimal.Decimal(random.randrange(_islandSize*100, 490))/100)
            empty.location.y = float(decimal.Decimal(random.randrange(_islandSize*100, 490))/100)
            empty.location.z = 0.07
            empty.scale.x = 0.1
            empty.scale.y = 0.1
            empty.scale.z = 0.1