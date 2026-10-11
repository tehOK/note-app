from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Note:
    id: int
    text: str
    date: datetime = field(default_factory=datetime.now)

    def to_dict(self):
        return {
            "id": self.id,
            "text": self.text,
            "date": self.date.isoformat(),
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Note":
        try:
            return cls(
                id=int(data["id"]),
                text=str(data["text"]),
                date=datetime.fromisoformat(data["date"]),
            )
        except (KeyError, ValueError) as e:
            raise ValueError(f"Невалидная заметка: {data}") from e