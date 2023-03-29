from typing import List

from Domain.undo_redo_operation import UndoRedoOperation
from Repository.repository import Repository


class CascadeDeleteOperation(UndoRedoOperation):
    def __init__(self,
                 repository: Repository,
                 rezervare_repository: Repository,
                 cascade: List):
        self.__repository = repository
        self.__rezervare_repository = rezervare_repository
        self.__cascade = cascade

    def do_undo(self):
        for i in range(len(self.__cascade) - 1):
            self.__rezervare_repository.add(self.__cascade[i])
        self.__repository.add(self.__cascade[len(self.__cascade) - 1])

    def do_redo(self):
        for i in range(len(self.__cascade) - 1):
            self.__rezervare_repository.delete(self.__cascade[0].id_entity)
        self.__repository.\
            delete(self.__cascade[len(self.__cascade) - 1].id_entity)
