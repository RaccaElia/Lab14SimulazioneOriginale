from dataclasses import dataclass

@dataclass
class Cromosoma:
    id: int
    geni: list

    def __hash__(self):
        return hash(self.id)

    def __str__(self):
        return str(self.id)