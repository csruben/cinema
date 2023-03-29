from dataclasses import dataclass

from Domain.entity import Entity


@dataclass
class CardClient(Entity):
    '''
    Creeaza un card client.
    '''
    nume: str
    prenume: str
    cnp: str
    data_nastere: str
    data_inregistrare: str
    puncte_acumulate: int
