class Level:
    _instance = None

    def __init__(self):
        if Level._instance is not None:
            raise RuntimeError("Level already exists - use Level.get_instance() instead")
        self.layer_background = []
        self.layer_level = []
        self.layer_entity = []
        self.layer_overlay = []

        self.objgroups = self.construct_objgroups()

        Level._instance = self

    def construct_objgroups(self):
        groups = {"transitions": self.construct_room_transitions(),
                  "solid": self.construct_solid(),
                  "camera_cutoff": self.construct_camera_cutoff()}
        self.objgroups = groups
        return groups

    def get_obj_all(self):
        return self.layer_background + self.layer_level + self.layer_entity

    def construct_room_transitions(self):
        return [obj for obj in self.layer_level if type(obj).__name__ == "RoomTransition"]

    def get_room_transitions(self):
        return self.objgroups["transitions"]

    def get_player_spawner(self, spawner_id):
        return [obj for obj in self.layer_level if type(obj).__name__ == "PlayerSpawner" and obj.spawner_id == spawner_id]

    def construct_camera_cutoff(self):
        return [obj for obj in self.layer_level if type(obj).__name__ == "CameraCutoff"]

    def get_camera_cutoff(self):
        return self.objgroups["camera_cutoff"]

    def construct_solid(self):
        return [obj for obj in self.layer_level if obj.solid]

    def get_solid(self):
        return self.objgroups["solid"]

    def get_layer_entity_playerless(self):
        return [obj for obj in self.layer_entity if not type(obj).__name__ == "PlayerEntity"]

    def clear_level(self):
        self.layer_level = []
        self.layer_entity = []
        self.layer_overlay = []
        self.layer_overlay = []

        self.construct_objgroups()

    def add_background(self, obj, supress=False):
        self.layer_background.append(obj)
        if not supress: self.construct_objgroups()

    def add_level(self, obj, supress=False):
        self.layer_level.append(obj)
        if not supress: self.construct_objgroups()

    def add_entity(self, obj, supress=False):
        self.layer_entity.append(obj)
        if not supress: self.construct_objgroups()

    def add_overlay(self, obj):
        self.layer_overlay.append(obj)

    def remove(self, obj, layer, supress=False):
        layer.remove(obj)
        if not supress: self.construct_objgroups()
        return layer

    def cleanse_level(self, supress=False):
        self.layer_level = []
        if not supress: self.construct_objgroups()

    def cleanse_entity_playerless(self, supress=False):
        from player.player_big import PlayerBig
        from player.player_small import PlayerSmall

        self.layer_entity = [PlayerBig.inst(), PlayerSmall.inst()]
        if not supress: self.construct_objgroups()

    def cleanse_background(self, supress=False):
        self.layer_background = []
        if not supress: self.construct_objgroups()

    @classmethod
    def inst(cls):
        return cls._instance