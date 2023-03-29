import jsonpickle

from Domain.entity import Entity
from Repository.repository_in_memory import RepositoryInMemory


class RepositoryJson(RepositoryInMemory):
    def __init__(self, filename):
        super().__init__()
        self.filename = filename

    def __read_file(self):
        try:
            with open(self.filename, "r") as f:
                return jsonpickle.loads(f.read())
        except Exception:
            return {}

    def __write_file(self):
        with open(self.filename, "w") as f:
            f.write(jsonpickle.dumps(self.entitati, indent=2))

    def read(self, id_entity=None):
        self.entitati = self.__read_file()
        return super().read(id_entity)

    def add(self, entity: Entity):
        self.entitati = self.__read_file()
        super().add(entity)
        self.__write_file()

    def delete(self, id_entity):
        self.entitati = self.__read_file()
        super().delete(id_entity)
        self.__write_file()

    def modify(self, entity: Entity):
        self.entitati = self.__read_file()
        super().modify(entity)
        self.__write_file()
