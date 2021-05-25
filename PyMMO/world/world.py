from ..helpers import NEW_PLAYER_ENTITY, KILL_PLAYER_ENTITY, LOG
from ..entity.entity import Entity
from random import random


class World:
    def __init__(self, name='Default World'):
        self.name = name
        self.entities = {}
        
    def update(self, message):
        if NEW_PLAYER_ENTITY in message:
            self.add_entity(id=message[NEW_PLAYER_ENTITY])
            
        elif KILL_PLAYER_ENTITY in message:
            self.kill_entity(id=message[KILL_PLAYER_ENTITY])
            
        return self
    
    def random_name(self):
        return str(random())[2:]

    
    def add_entity(self, id, entity_class=Entity, **kwargs):
        entity = entity_class(id, **kwargs)
        self.entities[entity.id] = entity
        return self.entities
    
    def kill_entity(self, id):
        self.entities.pop(id)
    

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
    