import json
import tiledmap

class MapBg:
    def __init__(self, filename):
        with open(filename, 'r') as f:
            mapjson = json.load(f)
        self.tmap = tiledmap.tiled_map_from_dict(mapjson)
        # print(self.tmap)
        # print(self.tmap.layers)
        # print(self.tmap.layers[0])
        print(self.tmap.layers[0].data)
        print(self.tmap.tilesets[0])

if __name__ == '__main__':
    mapbg = MapBg('res/desert.json')


