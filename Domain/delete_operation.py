from Domain.entity import Entity
from Domain.undo_redo_operation import UndoRedoOperation
from Repository.repository import Repository


class DeleteOperation(UndoRedoOperation):
    def __init__(self,
                 repository: Repository,
                 obiect_sters: Entity):
        self.__repository = repository
        self.__obiect_sters = obiect_sters

    def do_undo(self):
        self.__repository.add(self.__obiect_sters)

    def do_redo(self):
        self.__repository.delete(self.__obiect_sters.id_entity)
