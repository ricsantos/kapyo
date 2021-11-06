
from dataclasses import dataclass

@dataclass
class KayoEvent:
    id: str
    title: str
    description: str
    sport: str
    series_id: int
    category_id: int

    @classmethod
    def from_dict(cls,event_dict):
        print(event_dict)
        inst = cls(id=event_dict["id"],
                   title=event_dict["title"],
                   description=event_dict["description"],
                   sport=event_dict["sport"],
                   series_id=event_dict["series_id"],
                   category_id=event_dict["category_id"])
        return inst