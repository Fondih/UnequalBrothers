from enum import Enum, auto


class Events(Enum):
    PLAYER_MOVE = auto()
    ROOM_LOADED = auto()
    ZOOM_CHANGE = auto()
    EDITOR_TERRAIN_CREATED = auto()