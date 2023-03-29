from typing import Protocol

from Domain.entity import Entity


class Repository(Protocol):
    def read(self, id_entity=None):
        ...

    def add(self, entity: Entity):
        ...

    def delete(self, id_entity: str):
        ...

    def modify(self, entity: Entity):
        ...
