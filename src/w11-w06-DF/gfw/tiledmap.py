from dataclasses import dataclass
from typing import Any, List, TypeVar, Type, cast, Callable


T = TypeVar("T")


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def from_bool(x: Any) -> bool:
    assert isinstance(x, bool)
    return x


def from_float(x: Any) -> float:
    assert isinstance(x, (float, int)) and not isinstance(x, bool)
    return float(x)


def to_float(x: Any) -> float:
    assert isinstance(x, (int, float))
    return x



@dataclass
class Layer:
    data: List[int]
    height: int
    id: int
    name: str
    opacity: int
    type: str
    visible: bool
    width: int
    x: int
    y: int

    @staticmethod
    def from_dict(obj: Any) -> 'Layer':
        assert isinstance(obj, dict)
        data = from_list(from_int, obj.get("data"))
        height = from_int(obj.get("height"))
        id = from_int(obj.get("id"))
        name = from_str(obj.get("name"))
        opacity = from_int(obj.get("opacity"))
        type = from_str(obj.get("type"))
        visible = from_bool(obj.get("visible"))
        width = from_int(obj.get("width"))
        x = from_int(obj.get("x"))
        y = from_int(obj.get("y"))
        return Layer(data, height, id, name, opacity, type, visible, width, x, y)

    def to_dict(self) -> dict:
        result: dict = {}
        result["data"] = from_list(from_int, self.data)
        result["height"] = from_int(self.height)
        result["id"] = from_int(self.id)
        result["name"] = from_str(self.name)
        result["opacity"] = from_int(self.opacity)
        result["type"] = from_str(self.type)
        result["visible"] = from_bool(self.visible)
        result["width"] = from_int(self.width)
        result["x"] = from_int(self.x)
        result["y"] = from_int(self.y)
        return result



@dataclass
class Tileset:
    columns: int
    firstgid: int
    image: str
    imageheight: int
    imagewidth: int
    margin: int
    name: str
    spacing: int
    tilecount: int
    tileheight: int
    tilewidth: int

    @staticmethod
    def from_dict(obj: Any) -> 'Tileset':
        assert isinstance(obj, dict)
        columns = from_int(obj.get("columns"))
        firstgid = from_int(obj.get("firstgid"))
        image = from_str(obj.get("image"))
        imageheight = from_int(obj.get("imageheight"))
        imagewidth = from_int(obj.get("imagewidth"))
        margin = from_int(obj.get("margin"))
        name = from_str(obj.get("name"))
        spacing = from_int(obj.get("spacing"))
        tilecount = from_int(obj.get("tilecount"))
        tileheight = from_int(obj.get("tileheight"))
        tilewidth = from_int(obj.get("tilewidth"))
        return Tileset(columns, firstgid, image, imageheight, imagewidth, margin, name, spacing, tilecount, tileheight, tilewidth)

    def to_dict(self) -> dict:
        result: dict = {}
        result["columns"] = from_int(self.columns)
        result["firstgid"] = from_int(self.firstgid)
        result["image"] = from_str(self.image)
        result["imageheight"] = from_int(self.imageheight)
        result["imagewidth"] = from_int(self.imagewidth)
        result["margin"] = from_int(self.margin)
        result["name"] = from_str(self.name)
        result["spacing"] = from_int(self.spacing)
        result["terrains"] = from_list(lambda x: to_class(Terrain, x), self.terrains)
        result["tilecount"] = from_int(self.tilecount)
        result["tileheight"] = from_int(self.tileheight)
        result["tilewidth"] = from_int(self.tilewidth)
        return result


@dataclass
class TiledMap:
    compressionlevel: int
    height: int
    infinite: bool
    layers: List[Layer]
    nextlayerid: int
    nextobjectid: int
    orientation: str
    renderorder: str
    tiledversion: str
    tileheight: int
    tilesets: List[Tileset]
    tilewidth: int
    type: str
    version: str
    width: int

    @staticmethod
    def from_dict(obj: Any) -> 'TiledMap':
        assert isinstance(obj, dict)
        compressionlevel = from_int(obj.get("compressionlevel"))
        height = from_int(obj.get("height"))
        infinite = from_bool(obj.get("infinite"))
        layers = from_list(Layer.from_dict, obj.get("layers"))
        nextlayerid = from_int(obj.get("nextlayerid"))
        nextobjectid = from_int(obj.get("nextobjectid"))
        orientation = from_str(obj.get("orientation"))
        renderorder = from_str(obj.get("renderorder"))
        tiledversion = from_str(obj.get("tiledversion"))
        tileheight = from_int(obj.get("tileheight"))
        tilesets = from_list(Tileset.from_dict, obj.get("tilesets"))
        tilewidth = from_int(obj.get("tilewidth"))
        type = from_str(obj.get("type"))
        version = from_str(obj.get("version"))
        width = from_int(obj.get("width"))
        return TiledMap(compressionlevel, height, infinite, layers, nextlayerid, nextobjectid, orientation, renderorder, tiledversion, tileheight, tilesets, tilewidth, type, version, width)

    def to_dict(self) -> dict:
        result: dict = {}
        result["compressionlevel"] = from_int(self.compressionlevel)
        result["height"] = from_int(self.height)
        result["infinite"] = from_bool(self.infinite)
        result["layers"] = from_list(lambda x: to_class(Layer, x), self.layers)
        result["nextlayerid"] = from_int(self.nextlayerid)
        result["nextobjectid"] = from_int(self.nextobjectid)
        result["orientation"] = from_str(self.orientation)
        result["renderorder"] = from_str(self.renderorder)
        result["tiledversion"] = from_str(self.tiledversion)
        result["tileheight"] = from_int(self.tileheight)
        result["tilesets"] = from_list(lambda x: to_class(Tileset, x), self.tilesets)
        result["tilewidth"] = from_int(self.tilewidth)
        result["type"] = from_str(self.type)
        result["version"] = from_str(self.version)
        result["width"] = from_int(self.width)
        return result


def tiled_map_from_dict(s: Any) -> TiledMap:
    return TiledMap.from_dict(s)


def tiled_map_to_dict(x: TiledMap) -> Any:
    return to_class(TiledMap, x)
