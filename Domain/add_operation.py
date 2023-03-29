from Domain.entity import Entity
from Domain.undo_redo_operation import UndoRedoOperation
from Repository.repository import Repository


class AddOperation(UndoRedoOperation):
    def __init__(self,
                 repository: Repository,
                 obiect_adaugat: Entity):
        self.__repository = repository
        self.__obiect_adaugat = obiect_adaugat

    def do_undo(self):
        self.__repository.delete(self.__obiect_adaugat.id_entity)

    def do_redo(self):
        self.__repository.add(self.__obiect_adaugat)
