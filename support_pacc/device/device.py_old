class Device:
    instances = []

    def __init__(self):
        self.instances.append(self)

    def __del__(self):
        if self in self.instances:
            self.instances.remove(self)
