from accessors import NoteManager
from constants import HELP


def main() -> None:
    manager = NoteManager()
    print("Заметки. Введите /help для помощи")

    while True:
        try:
            raw = input("> ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nВыход")
            break

        if not raw:
            continue

        parts = raw.split(maxsplit=1)
        command = parts[0]
        arg = parts[1] if len(parts) > 1 else ""

        if command == "/help":
            print(HELP)
        elif command == "add":
            manager.add(arg)
        elif command == "list":
            manager.list()
        elif command == "delete":
            manager.delete(arg)
        elif command == "find":
            manager.find(arg)
        else:
            print(f"Неизвестная команда: {command}. Введите /help")


if __name__ == "__main__":
    main()