class Entity:
    def __init__(self, id, entity_spec_or_gen=None, **kwargs):
        self.id = id
        
        if entity_spec_or_gen is None:
            self.spec = self.entity_spec_gen(id)
        elif isinstance(entity_spec_or_gen, dict):
            self.spec = self.update_spec(entity_spec_or_gen)
        else:
            self.spec = entity_spec_or_gen(id)
            
        for arg in kwargs:
            self.spec[arg] = kwargs[arg]
        
    def update_spec(self, entity_spec: dict):
        assert entity_spec['id'] == self.id
        self.spec = entity_spec
        return self.spec

    def entity_spec_gen(self, id):
        return {'id': id}

    def __getitem__(self, arg):
        return self.spec[arg]
    
    def __str__(self):
        return str(self.spec)