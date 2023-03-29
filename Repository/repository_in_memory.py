from Domain.entity import Entity
from Repository.repository import Repository


class RepositoryInMemory(Repository):
    def __init__(self):
        self.entitati = {}

    def read(self, id_entity=None):
        '''
        citeste filmele sau filmul cu id-ul specificat
        :param id_entity: id film
        :return:
        '''
        if id_entity is None:
            return list(self.entitati.values())

        if id_entity in self.entitati:
            return self.entitati[id_entity]
        else:
            return None

    def add(self, entity: Entity):
        '''
        adauga entity
        :param entity: film de adaugat
        :return:
        '''
        if self.read(entity.id_entity) is not None:
            raise KeyError('Exista deja o entitate cu id-ul dat! ')
        self.entitati[entity.id_entity] = entity

    def delete(self, id_entity: str):
        '''
        sterge entity
        :param id_entity: id film de sters
        :return:
        '''
        if self.read(id_entity) is None:
            raise KeyError("Nu exista nicio entitate cu id-ul dat!")
        del self.entitati[id_entity]

    def modify(self, entity: Entity):
        '''
        modifica entity
        :param entity: film
        :return: entity modificat
        '''
        if self.read(entity.id_entity) is None:
            raise KeyError("Nu exista nicio entitate cu id-ul dat!")
        self.entitati[entity.id_entity] = entity
