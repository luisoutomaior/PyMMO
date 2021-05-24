from ..helpers import NEW_ENTITY, LOG
from ..entity.entity import Entity
from random import random


class World:
    def __init__(self, name='Default World'):
        self.name = name
        self.entities = []
        
    def update(self, message):
        if message == NEW_ENTITY:
            name = self.random_name()
            self.add_entity({'name': f'entity_{name}'})
        return self
    
    def random_name(self):
        return str(random())[2:]

    
    def add_entity(self, entity_spec: dict):
        entity = Entity(entity_spec)
        self.entities.append(entity)
        return self.entities

    def main_loop(self, new_world):
        ########################
        # Do something to world
        # e.g. create new entities, add/change sprites, calculate stuff, etc
        LOG.info(self.name)
        LOG.info(new_world)
        
        # whatever you return will persist in the server
        # and will be consistent across all clients
        ########################
        return new_world

    def __str__(self):
        return f"World: {self.name}. Number of entities: {len(self.entities)}"
    