class Entity:
    def __init__(self, entity_spec: dict):
        self.spec = entity_spec
        self.id = entity_spec['id']
        
    def update_spec(self, entity_spec: dict):
        assert entity_spec['id'] == self.id
        self.spec = entity_spec
        return self.spec


