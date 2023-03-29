from dataclasses import dataclass

from Domain.entity import Entity


@dataclass
class Film(Entity):
    '''
    Creeaza un film.
    '''
    titlu_film: str
    an_aparitie_film: int
    pret_bilet_film: float
    in_program: str
