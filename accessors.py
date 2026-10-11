import json
from pathlib import Path

from dto import Note


class NoteManager:

    def __init__(self, path: str = "notes.json"):
        self.path = Path(path)
        self._notes: list[Note] = self._load()
        self._next_id: int = max((n.id for n in self._notes), default=0) + 1

    def _load(self) -> list[Note]:
        if not self.path.exists():
            return []
        try:
            with self.path.open("r", encoding="utf-8") as f:
                raw = json.load(f)
            return [Note.from_dict(item) for item in raw]
        except json.JSONDecodeError as e:
            print(f"Невалидный JSON: {e}")
            return []
        except ValueError as e:
            print(f"Ошибка в данных: {e}")
            return []

    def _save(self) -> None:
        with self.path.open("w", encoding="utf-8") as f:
            json.dump(
                [note.to_dict() for note in self._notes],
                f,
                ensure_ascii=False,
                indent=4,
            )

    def add(self, text: str) -> None:
        text = text.strip()
        if not text:
            print("Текст заметки не может быть пустым")
            return
        note = Note(id=self._next_id, text=text)
        self._notes.append(note)
        self._next_id += 1
        self._save()
        print(f"Заметка №{note.id} сохранена")

    def list(self) -> None:
        if not self._notes:
            print("Заметок нет")
            return
        for note in self._notes:
            self._print_note(note)

    def delete(self, raw: str) -> None:
        try:
            note_id = int(raw)
        except ValueError:
            print("Напишите номер заметки")
            return

        for i, note in enumerate(self._notes):
            if note.id == note_id:
                self._notes.pop(i)
                self._save()
                print(f"Заметка №{note_id} удалена")
                return

        print(f"Заметки с id={note_id} нет")

    def find(self, text: str) -> None:
        text = text.strip()
        if not text:
            print("Введите текст для поиска")
            return

        found = [n for n in self._notes if text in n.text]
        if not found:
            print(f"По запросу «{text}» ничего не найдено")
            return

        for note in found:
            self._print_note(note)

    @staticmethod
    def _print_note(note: Note) -> None:
        print(
            f"Заметка №{note.id}\n"
            f"Текст: {note.text}\n"
            f"Добавлена: {note.date.strftime('%Y-%m-%d %H:%M')}\n"
            f"{'-' * 30}"
        )