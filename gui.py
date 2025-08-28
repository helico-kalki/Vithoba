from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPalette, QColor, QIcon
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QPushButton, QHBoxLayout, QVBoxLayout, QListWidget, QListWidgetItem, QDialog, QLineEdit
import sys
import json
import os

DATA_FILE = "flashcards.json"

def load_flashcards():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_flashcards(flashcards):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(flashcards, f, ensure_ascii=False, indent=2)
flashcards = load_flashcards()

for card in flashcards:
    card["w"] = int(card.get("w", 1))

app = QApplication(sys.argv)
window = QMainWindow()
window.setWindowIcon(QIcon("logo2.png"))
window.setGeometry(100,100,400,400)
w_palette = window.palette()
w_palette.setColor(QPalette.ColorRole.Window, QColor("#111119"))
window.setPalette(w_palette)
window.setAutoFillBackground(True)
window.setWindowTitle("Vithoba Flashcards")

class FlashCardWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.index = 0 if flashcards else -1
        self.total_cards = len(flashcards)
        self.flip_count = 0
        self.invert_mode = False
        self.initUI()
        self.history = []
        
        
    def initUI(self):
        self.counter_label = QLabel(f"Total cards: {self.total_cards} | Flips: 0")
        self.counter_label.setStyleSheet("color: white; font-family: 'Inter'; font-size: 15px")
        
        self.question_label = QLabel(flashcards[self.index]["q"])
        self.question_label.setStyleSheet("color: white; font-family: 'Inter'; font-size: 40px")
        self.answer_label = QLabel("")
        self.answer_label.setStyleSheet("font-family: 'Inter'; font-size: 40px; color: #8BE764")

        if flashcards and 0 <= self.index < len(flashcards):
            card = flashcards[self.index]
            if self.invert_mode:
                self.question_label.setText(card["a"])  # Show answer
            else:
                self.question_label.setText(card["q"])  # Show question
        else:
            self.question_label.setText("No flashcards available")

        self.button = QPushButton("Flip")
        self.button.setStyleSheet("font-family: 'Inter'; font-size: 40px; background: #8BE764; border: none; height: 60px; width: 60px; border-radius: 30px")
        self.button.clicked.connect(self.handle_button_click)

        self.rate_bad = QPushButton()
        self.rate_bad.setText("Bad")
        self.rate_bad.setStyleSheet("font-family: 'Inter'; font-size: 30px; color: #111119; background: #E12C29; border: none; height: 60px; width: 60px; border-radius: 30px")
        self.rate_bad.clicked.connect(self.handle_rating_click)

        self.rate_okay = QPushButton()
        self.rate_okay.setText("Okay")
        self.rate_okay.setStyleSheet("color: #111119; font-family: 'Inter'; font-size: 30px; background: #605E74; border: none; height: 60px; width: 60px; border-radius: 30px")
        self.rate_okay.clicked.connect(self.handle_rating_click)

        self.rate_good = QPushButton()
        self.rate_good.setText("Good")
        self.rate_good.setStyleSheet("color: #111119; font-family: 'Inter'; font-size: 30px; background: #8BE764; border: none; height: 60px; width: 60px; border-radius: 30px")
        self.rate_good.clicked.connect(self.handle_rating_click)

        self.rate_layout = QHBoxLayout()
        self.rate_layout.addWidget(self.rate_bad)
        self.rate_layout.addWidget(self.rate_okay)
        self.rate_layout.addWidget(self.rate_good)

        self.rate_widget = QWidget()
        self.rate_widget.setLayout(self.rate_layout)
        self.rate_widget.hide()

        self.manage_button = QPushButton("...")
        self.manage_button.setStyleSheet("font-family: 'Inter'; font-size: 30px; background: #605E74; color: #111119; border: none; border-radius: 15px; height: 30px; width: 60px")
        self.manage_button.clicked.connect(self.open_manager)

        self.invert_button = QPushButton("Invert")
        self.invert_button.setCheckable(True)
        self.invert_button.setStyleSheet("font-family: 'Inter'; font-size: 20px; background: #605E74; color: #111119; border: none; border-radius: 15px; height: 30px; width: 60px")
        self.invert_button.toggled.connect(self.toggle_invert_mode)
        
        self.history_button = QPushButton("History")
        self.history_button.setCheckable(True)
        self.history_button.setStyleSheet("font-family: 'Inter'; font-size: 20px; background: #605E74; color: #111119; border: none; border-radius: 15px; height: 30px; width: 60px")
        self.history_button.toggled.connect(self.show_history_window)

        layout = QVBoxLayout()
        layout.addWidget(self.question_label, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.answer_label, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.rate_widget)
        layout.addWidget(self.button)
        layout.addWidget(self.counter_label, alignment=Qt.AlignmentFlag.AlignCenter)
        bottom_layout = QHBoxLayout()
        bottom_layout.addWidget(self.manage_button)
        bottom_layout.addWidget(self.invert_button)
        bottom_layout.addWidget(self.history_button)
        layout.addLayout(bottom_layout)
        self.setLayout(layout)

    def show_answer(self):
        self.answer_label.setText(flashcards[self.index]["a"])
        self.button.hide()
        self.rate_widget.show()
        self.flip_count += 1
        self.update_counter()

    def next_card(self):
        self.index = (self.index + 1) % len(flashcards)
        self.update_card_display()

    def handle_button_click(self):
        card = flashcards[self.index]
        if self.invert_mode:
            self.answer_label.setText(card["q"])
        else:
            self.answer_label.setText(card["a"])  
        self.button.hide()
        self.rate_widget.show()

    def handle_rating_click(self):
        sender = self.sender()
        card = flashcards[self.index]

        if sender == self.rate_bad:
            card["w"] = min(int(card["w"]) + 2, 10)
            rating = "Bad"
        elif sender == self.rate_okay:
            card["w"] = min(int(card["w"]) + 1, 7)
            rating = "Okay"
        elif sender == self.rate_good:
            card["w"] = min(int(card["w"]) - 1, 1)
            rating = "Good"

        history_entry = {
            "q": card["q"],
            "a": card["a"],
            "w": card["w"],
            "rating": rating
        }
        self.history.append(history_entry)

        self.next_card()

    def show_history_window(self):
        self.history_window = QWidget()
        self.history_window.setWindowTitle("History")
        self.history_window.setGeometry(150, 150, 400, 300)
        self.history_window.setWindowIcon(QIcon("logo2.png"))
        w_palette = self.palette()
        w_palette.setColor(QPalette.ColorRole.Window, QColor("#111119"))
        self.setPalette(w_palette)
        self.setAutoFillBackground(True)

        layout = QVBoxLayout()
        list_widget = QListWidget()
        list_widget.setStyleSheet("""
            QListView {
                background-color: #111119;
                font-family: 'Inter';
                font-size: 15px;
                border: none;
            }
            QListView::item {
                color: white;
                background-color: #605E74;
                border: none;
                height: 90px; 
                width: 30px; 
                border-radius: 5px
            }
            QListView::item:hover {
                background-color: #111119;
                color: #8BE764;
                font-family: 'Inter';
                border: none;
            }
            QListView::item:selected {
                background-color: #8BE764;
                color: #111119;
                font-family: 'Inter';
                border: none;
            }
        """)

        for entry in self.history:
            text = f'Question: {entry["q"]}\nAnswer: {entry["a"]}\nRating: {entry["rating"]} (Weight: {entry["w"]})'
            item = QListWidgetItem(text)
            list_widget.addItem(item)

        layout.addWidget(list_widget)
        self.history_window.setLayout(layout)
        self.history_window.show()

    def update_counter(self):
        self.counter_label.setText(f"Total cards: {self.total_cards} | Flips: {self.flip_count}")

    def open_manager(self):
        self.manager = FlashCardManager(self)
        self.manager.show()

    def toggle_invert_mode(self, checked):
        self.invert_mode = checked
        self.update_card_display()
    
    def update_card_display(self):
        card = flashcards[self.index]

        if self.invert_mode:
            self.question_label.setText(card["a"])  
            self.answer_label.setText("")           
        else:
            self.question_label.setText(card["q"])  
            self.answer_label.setText("")           

        self.rate_widget.hide()
        self.button.setText("Flip")
        self.button.show()

    def flip_card(self):
        if self.answer_label.isHidden():
            self.answer_label.show()
        else:
            self.answer_label.hide()

class FlashCardManager(QWidget):
    def __init__(self, parent_widget):
        super().__init__()
        self.parent_widget = parent_widget
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Manage Flashcards")
        self.setGeometry(150, 150, 400, 400)
        self.setWindowIcon(QIcon("logo2.png"))
        self.setStyleSheet("background-color: #111119")
        w_palette = self.palette()
        w_palette.setColor(QPalette.ColorRole.Window, QColor("#111119"))
        self.setPalette(w_palette)
        self.setAutoFillBackground(True)

        self.list_widget = QListWidget()
        self.list_widget.setStyleSheet("""
            QListView {
                background-color: #111119;
                font-family: 'Inter';
                font-size: 15px;
                border: none;
            }
            QListView::item {
                color: white;
                background-color: #605E74;
                border: none;
                height: 30px; 
                width: 30px; 
                border-radius: 5px
            }
            QListView::item:hover {
                background-color: #111119;
                color: #8BE764;
                font-family: 'Inter';
                border: none;
            }
            QListView::item:selected {
                background-color: #8BE764;
                color: #111119;
                font-family: 'Inter';
                border: none;
            }
        """)
        self.update_list()

        bottom_layout = QHBoxLayout()
        delete_button = QPushButton("🗑")
        delete_button.setStyleSheet("font-family: 'Inter'; font-size: 20px; color: #111119; background: #E12C29; border: none; height: 40px; width: 40px; border-radius: 20px")
        delete_button.clicked.connect(self.delete_card)
        add_button = QPushButton("+")
        add_button.setStyleSheet("color: #111119; font-family: 'Inter'; font-size: 20px; background: #8BE764; border: none; height: 40px; width: 40px; border-radius: 20px")
        add_button.clicked.connect(self.add_card)

        bottom_layout.addWidget(delete_button)
        bottom_layout.addWidget(add_button)
        layout = QVBoxLayout()
        layout.addWidget(self.list_widget)
        layout.addLayout(bottom_layout)
        
        self.setLayout(layout)

    def update_list(self):
        self.list_widget.clear()
        for card in flashcards:
            self.list_widget.addItem(f"{card['q']} → {card['a']}")

    def delete_card(self):
        selected = self.list_widget.currentRow()
        if selected >= 0:
            del flashcards[selected]
            save_flashcards(flashcards)
            self.parent_widget.total_cards = len(flashcards)
            self.parent_widget.update_counter()
            self.update_list()

    def add_card(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("New Flashcard")
        dialog.setWindowIcon(QIcon("logo2.png"))
        w_palette = dialog.palette()
        w_palette.setColor(QPalette.ColorRole.Window, QColor("#111119"))
        dialog.setPalette(w_palette)
        dialog.setAutoFillBackground(True)
        dialog.setModal(True)

        q_label = QLabel()
        q_label.setText("Question")
        q_label.setStyleSheet("color: white; font-family: 'Inter'; font-size: 15px")
        q_input = QLineEdit()
        q_input.setStyleSheet("border: none; border-radius: 10px; background-color: #605E74; color: white; font-family: 'Inter'; font-size: 15px; height: 30px; width: 30px")
        a_label = QLabel()
        a_label.setText("Answer")
        a_label.setStyleSheet("color: white; font-family: 'Inter'; font-size: 15px")
        a_input = QLineEdit()
        a_input.setStyleSheet("border: none; border-radius: 10px; background-color: #605E74; color: white; font-family: 'Inter'; font-size: 15px; height: 30px; width: 30px")

        save_button = QPushButton("Save")
        save_button.setStyleSheet("color: #111119; font-family: 'Inter'; font-size: 15px; background: #8BE764; border: none; height: 30px; width: 30px; border-radius: 15px")
        save_button.clicked.connect(lambda: self.save_card(dialog, q_input.text(), a_input.text()))

        layout = QVBoxLayout()
        layout.addWidget(q_label)
        layout.addWidget(q_input)
        layout.addWidget(a_label)
        layout.addWidget(a_input)
        layout.addWidget(save_button)
        dialog.setLayout(layout)
        dialog.exec()

    def save_card(self, dialog, question, answer):
        if question and answer:
            flashcards.append({"q": question, "a": answer, "w": 1})
            save_flashcards(flashcards)  
            self.parent_widget.total_cards = len(flashcards)
            self.parent_widget.update_counter()
            self.update_list()
            dialog.accept()

flashcard_widget = FlashCardWidget()
window.setCentralWidget(flashcard_widget)

window.show()
sys.exit(app.exec())
    
