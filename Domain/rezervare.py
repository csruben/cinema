from dataclasses import dataclass

from Domain.entity import Entity


@dataclass
class Rezervare(Entity):
    '''
    Creeaza o rezervare.
    '''
    id_film: str
    id_card_client: str
    data_ora_rezervare: str
