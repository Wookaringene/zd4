import os
import sqlite3
import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout,
                             QLabel, QTextEdit, QPushButton,
                             QFileDialog, QMessageBox, QInputDialog)
from PyQt5.QtGui import QColor

con = sqlite3.connect("test.db")
cursor = con.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS filestest (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        text TEXT,
        priority INTEGER
    )
""")
try:
    cursor.execute("INSERT INTO filestest (id, text, priority) VALUES (1, 'namefile', 1)")
    con.commit()
except sqlite3.IntegrityError:
    print("Запись с id=1 уже существует.")

class ToDoListApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Приложение для Заметок")
        self.setGeometry(100, 100, 600, 500)

        self.filename = None
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.label = QLabel("Введите текст заметки:")
        layout.addWidget(self.label)

        self.text_edit = QTextEdit()
        layout.addWidget(self.text_edit)

        self.create_button = QPushButton("Создать заметку")
        self.create_button.setStyleSheet("background-color: yellow; color: black;")
        self.create_button.clicked.connect(self.create_note)
        layout.addWidget(self.create_button)

        self.open_button = QPushButton("Открыть заметку")
        self.open_button.setStyleSheet("background-color: lightblue; color: black;")
        self.open_button.clicked.connect(self.open_note)
        layout.addWidget(self.open_button)

        self.save_button = QPushButton("Сохранить заметку")
        self.save_button.setStyleSheet("background-color: red; color: black;")
        self.save_button.clicked.connect(self.save_note)
        layout.addWidget(self.save_button)

        self.add_button = QPushButton("Добавить текст")
        self.add_button.setStyleSheet("background-color: green; color: black;")
        self.add_button.clicked.connect(self.add_text)
        layout.addWidget(self.add_button)

        self.setLayout(layout)

    def create_note(self):
        filename, _ = QFileDialog.getSaveFileName(self, "Создать заметку", "", "Text Files (*.txt);;All Files (*)")
        if filename:
            self.filename = filename
            self.save_note()

    def open_note(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Открыть заметку", "", "Text Files (*.txt);;All Files (*)")
        if filename:
            try:
                with open(filename, 'r', encoding='utf-8') as file:
                    content = file.read()
                self.text_edit.setText(content)
                self.filename = filename
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Не удалось открыть файл: {e}")

    def save_note(self):
        if not self.filename:
            self.create_note()
            if not self.filename:
                return

        try:
            with open(self.filename, 'w', encoding='utf-8') as file:
                file.write(self.text_edit.toPlainText())
            QMessageBox.information(self, "Успех", "Заметка сохранена!")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось сохранить файл: {e}")

    def add_text(self):
        if not self.filename:
            QMessageBox.warning(self, "Внимание", "Сначала откройте или создайте заметку.")
            return

        text, ok = QInputDialog.getText(self, "Добавить текст", "Введите текст для добавления:")
        if ok and text:
            try:
                with open(self.filename, 'a', encoding='utf-8') as file:
                    file.write('\n' + text)
                self.text_edit.append(text)
                QMessageBox.information(self, "Успех", "Текст добавлен!")
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Не удалось добавить текст: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    todo_app = ToDoListApp()
    todo_app.show()
    sys.exit(app.exec_())







