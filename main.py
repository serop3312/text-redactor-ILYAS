import os
import sys


class TextEditor:
    def __init__(self):
        self.filename = None
        self.lines = [""]
        self.cursor_row = 0
        self.cursor_col = 0
        self.modified = False

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def display(self):
        self.clear_screen()
        print("=" * 60)
        name = self.filename if self.filename else "[Без имени]"
        mark = " *" if self.modified else ""
        print(f" Файл: {name}{mark}")
        print("=" * 60)

        # Показываем строки с номерами, вокруг курсора
        start = max(0, self.cursor_row - 10)
        end = min(len(self.lines), start + 20)
        for i in range(start, end):
            marker = ">" if i == self.cursor_row else " "
            line = self.lines[i]
            if i == self.cursor_row:
                # подсвечиваем позицию курсора
                line = line[:self.cursor_col] + "|" + line[self.cursor_col:]
            print(f"{marker}{i+1:3d}| {line}")

        print("=" * 60)
        print(f" Строка: {self.cursor_row+1}  Колонка: {self.cursor_col+1}  "
              f"Всего строк: {len(self.lines)}")
        print("=" * 60)
        print(" Команды: :w - сохранить | :o - открыть | :q - выход")
        print(" :n - новый файл | :h - справка")
        print("=" * 60)

    def help_screen(self):
        self.clear_screen()
        print("=" * 60)
        print(" СПРАВКА")
        print("=" * 60)
        print(" В режиме редактирования вводите текст построчно.")
        print(" После нажатия Enter строка добавляется в буфер.")
        print()
        print(" Команды (вводятся вместо текста):")
        print("   :w           - сохранить файл")
        print("   :w имя       - сохранить как 'имя'")
        print("   :o           - открыть файл")
        print("   :o имя       - открыть файл 'имя'")
        print("   :n           - создать новый файл")
        print("   :d N         - удалить строку N")
        print("   :i N текст   - вставить текст в строку N")
        print("   :r N текст   - заменить строку N")
        print("   :p           - показать весь текст")
        print("   :q           - выход")
        print("   :h           - эта справка")
        print("=" * 60)
        input(" Нажмите Enter для возврата...")

    def save(self, filename=None):
        if filename:
            self.filename = filename
        if not self.filename:
            self.filename = input(" Имя файла для сохранения: ").strip()
            if not self.filename:
                print(" Отменено.")
                return
        try:
            with open(self.filename, 'w', encoding='utf-8') as f:
                f.write("\n".join(self.lines))
            self.modified = False
            print(f" Сохранено в '{self.filename}'")
        except Exception as e:
            print(f" Ошибка сохранения: {e}")
        input(" Нажмите Enter...")

    def open_file(self, filename=None):
        if not filename:
            filename = input(" Имя файла для открытия: ").strip()
        if not filename:
            return
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                content = f.read()
            self.lines = content.split("\n") if content else [""]
            self.filename = filename
            self.cursor_row = 0
            self.cursor_col = 0
            self.modified = False
            print(f" Открыт файл '{filename}'")
        except FileNotFoundError:
            print(f" Файл '{filename}' не найден. Создан новый.")
            self.lines = [""]
            self.filename = filename
            self.modified = False
        except Exception as e:
            print(f" Ошибка: {e}")
        input(" Нажмите Enter...")

    def show_all(self):
        self.clear_screen()
        print("=" * 60)
        print(" СОДЕРЖИМОЕ")
        print("=" * 60)
        for i, line in enumerate(self.lines):
            print(f"{i+1:3d}| {line}")
        print("=" * 60)
        input(" Нажмите Enter...")

    def process_command(self, cmd):
        parts = cmd.strip().split(maxsplit=2)
        if not parts:
            return True
        op = parts[0].lower()

        if op == ":q":
            if self.modified:
                ans = input(" Есть несохранённые изменения. Выйти? (y/n): ").lower()
                if ans != 'y':
                    return True
            return False
        elif op == ":w":
            self.save(parts[1] if len(parts) > 1 else None)
        elif op == ":o":
            self.open_file(parts[1] if len(parts) > 1 else None)
        elif op == ":n":
            self.lines = [""]
            self.filename = None
            self.modified = False
            self.cursor_row = 0
            self.cursor_col = 0
        elif op == ":h":
            self.help_screen()
        elif op == ":p":
            self.show_all()
        elif op == ":d":
            if len(parts) < 2 or not parts[1].isdigit():
                print(" Использование: :d N")
                input(" Enter...")
                return True
            n = int(parts[1]) - 1
            if 0 <= n < len(self.lines):
                del self.lines[n]
                if not self.lines:
                    self.lines = [""]
                self.cursor_row = min(self.cursor_row, len(self.lines) - 1)
                self.modified = True
            else:
                print(" Неверный номер строки")
                input(" Enter...")
        elif op == ":i":
            if len(parts) < 3 or not parts[1].isdigit():
                print(" Использование: :i N текст")
                input(" Enter...")
                return True
            n = int(parts[1]) - 1
            text = parts[2]
            if 0 <= n <= len(self.lines):
                self.lines.insert(n, text)
                self.modified = True
            else:
                print(" Неверный номер строки")
                input(" Enter...")
        elif op == ":r":
            if len(parts) < 3 or not parts[1].isdigit():
                print(" Использование: :r N текст")
                input(" Enter...")
                return True
            n = int(parts[1]) - 1
            text = parts[2]
            if 0 <= n < len(self.lines):
                self.lines[n] = text
                self.modified = True
            else:
                print(" Неверный номер строки")
                input(" Enter...")
        else:
            print(f" Неизвестная команда: {op}. Введите :h для справки.")
            input(" Enter...")
        return True

    def run(self):
        print(" Простой текстовый редактор. Введите :h для справки.")
        input(" Нажмите Enter для начала...")
        while True:
            self.display()
            line = input(f"{self.cursor_row+1}> ")
            if line.startswith(":"):
                if not self.process_command(line):
                    break
            else:
                # добавляем новую строку после текущей позиции
                self.lines.insert(self.cursor_row + 1, line)
                self.cursor_row += 1
                self.cursor_col = 0
                self.modified = True


def main():
    editor = TextEditor()

    # если передан файл аргументом — открываем
    if len(sys.argv) > 1:
        editor.open_file(sys.argv[1])

    try:
        editor.run()
    except KeyboardInterrupt:
        print("\n Выход.")
    print(" До свидания!")


if __name__ == "__main__":
    main()