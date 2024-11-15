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

'''
Traceback (most recent call last):
  File "D:/Lectures/2024_2/2dgp/git/src/w11-w06-DF/map_bg.py", line 16, in <module>
    mapbg = MapBg('res/desert.json')
  File "D:/Lectures/2024_2/2dgp/git/src/w11-w06-DF/map_bg.py", line 8, in __init__
    self.tmap = tiledmap.tiled_map_from_dict(mapjson)
  File "D:/Lectures/2024_2/2dgp/git/src/w11-w06-DF/tiledmap.py", line 270, in tiled_map_from_dict
    return TiledMap.from_dict(s)
  File "D:/Lectures/2024_2/2dgp/git/src/w11-w06-DF/tiledmap.py", line 231, in from_dict
    editorsettings = Editorsettings.from_dict(obj.get("editorsettings"))
  File "D:/Lectures/2024_2/2dgp/git/src/w11-w06-DF/tiledmap.py", line 65, in from_dict
    assert isinstance(obj, dict)
AssertionError
'''
