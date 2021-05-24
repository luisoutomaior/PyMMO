class Entity:
    def __init__(self, entity_spec: dict):
        self.spec = entity_spec
        
    def update_spec(self, entity_spec: dict):
        self.spec = entity_spec
        return self.spec


