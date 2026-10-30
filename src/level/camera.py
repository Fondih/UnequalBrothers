class Camera:
    _instance = None

    def __init__(self, pos, scale=1):
        if Camera._instance is not None:
            raise RuntimeError("Camera already exists - use Camera.get_instance() instead")

        self.pos = pos  # center in middle of camera
        self.scale = scale  # not yet implemented
        Camera._instance = self

    def get_pos(self):
        return self.pos

    def set_pos(self, pos):
        self.pos = pos

    @classmethod
    def get_instance(cls):
        return cls._instance