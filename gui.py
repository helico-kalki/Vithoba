from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPalette, QIcon, QColor
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QVBoxLayout, QLineEdit, QListWidget, QListWidgetItem, QDialog
import sys, json, os, random

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
window.setWindowIcon(QIcon("logo-red.png"))
window.setGeometry(100,100,500,400)
w_palette = window.palette()
w_palette.setColor(QPalette.ColorRole.Window, QColor("#111119"))
window.setPalette(w_palette)
window.setAutoFillBackground(True)
window.setWindowTitle("Vithoba Flashcards")

class FlashCardWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.index = 0 if flashcards else -1
        self.previous_index = -1
        self.total_cards = len(flashcards)
        self.flip_count = 0
        self.invert_mode = False
        self.writing_mode = False
        self.initUI()
        self.history = []
        
        
    def initUI(self):
        self.counter_label = QLabel(f"Total cards: {self.total_cards} | Flips: 0")
        self.counter_label.setStyleSheet("color: white; font-family: 'Inter'; font-size: 15px")
        
        self.question_label = QLabel()
        self.question_label.setStyleSheet("color: white; font-family: 'Inter'; font-size: 40px")
        self.answer_label = QLabel("")
        self.answer_label.setStyleSheet("font-family: 'Inter'; font-size: 40px; color: #8BE764")

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

        self.writing_button = QPushButton("Type")
        self.writing_button.setCheckable(True)
        self.writing_button.setStyleSheet("font-family: 'Inter'; font-size: 20px; background: #605E74; color: #111119; border: none; border-radius: 15px; height: 30px; width: 120px")
        self.writing_button.toggled.connect(self.toggle_writing_mode)

        self.answer_input = QLineEdit()
        self.answer_input.setStyleSheet("font-family: 'Inter'; font-size: 20px; background: #605E74; color: white; border: none; border-radius: 15px; height: 40px; padding: 0 10px;")
        self.answer_input.hide()
        self.answer_input.returnPressed.connect(self.check_answer)

        if not flashcards:
            self.question_label.setText("No flashcards available")
            self.button.hide()
        else:
            self.update_card_display()

        self.manage_button = QPushButton("...")
        self.manage_button.setStyleSheet("font-family: 'Inter'; font-size: 20px; background: #605E74; color: #111119; border: none; border-radius: 15px; height: 30px; width: 60px")
        self.manage_button.clicked.connect(self.open_manager)

        self.invert_button = QPushButton("Invert")
        self.invert_button.setCheckable(True)
        self.invert_button.setStyleSheet("font-family: 'Inter'; font-size: 20px; background: #605E74; color: #111119; border: none; border-radius: 15px; height: 30px; width: 60px")
        self.invert_button.toggled.connect(self.toggle_invert_mode)
        
        self.history_button = QPushButton("History")
        self.history_button.setCheckable(True)
        self.history_button.setStyleSheet("font-family: 'Inter'; font-size: 20px; background: #605E74; color: #111119; border: none; border-radius: 15px; height: 30px; width: 60px")
        self.history_button.toggled.connect(self.show_history_window)

        self.back_button = QPushButton("←")
        self.back_button.setStyleSheet("font-family: 'Inter'; font-size: 20px; background: #605E74; color: #111119; border: none; border-radius: 15px; height: 30px; width: 80px")
        self.back_button.clicked.connect(self.go_back)
        self.back_button.hide()

        layout = QVBoxLayout()
        layout.addWidget(self.question_label, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.answer_label, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.answer_input)
        layout.addWidget(self.rate_widget)
        layout.addWidget(self.button)
        layout.addWidget(self.counter_label, alignment=Qt.AlignmentFlag.AlignCenter)
        bottom_layout = QHBoxLayout()
        bottom_layout.addWidget(self.back_button)
        bottom_layout.addWidget(self.invert_button)
        bottom_layout.addWidget(self.writing_button)
        bottom_layout.addWidget(self.history_button)
        bottom_layout.addWidget(self.manage_button)
        layout.addLayout(bottom_layout)
        self.setLayout(layout)

    def show_answer(self):
        self.answer_label.setText(flashcards[self.index]["a"])
        self.button.hide()
        self.rate_widget.show()
        self.flip_count += 1
        self.update_counter()

    def next_card(self):
        if self.question_label.isHidden():
            self.question_label.show()
        if not flashcards:
            self.update_card_display()
            return

        self.previous_index = self.index

        weights = [card["w"] for card in flashcards]
        
        # Prevent choosing the same card twice in a row if there are other options
        if len(flashcards) > 1:
            weights[self.index] = 0

        total_weight = sum(weights)
        if total_weight == 0:
            # Fallback to original weights if all other cards have a weight of 0
            weights = [card["w"] for card in flashcards]

        self.index = random.choices(range(len(flashcards)), weights=weights, k=1)[0]
        self.update_card_display()

    def handle_button_click(self):
        if self.index == -1: return
        
        if self.writing_mode:
            if self.button.text() == "Check":
                self.check_answer()
            else:
                self.next_card()
        else:
            card = flashcards[self.index]
            if self.invert_mode:
                self.answer_label.setText(card["q"])
            else:
                self.answer_label.setText(card["a"])  
            self.button.hide()
            self.rate_widget.show()
            self.answer_label.show()
            self.flip_count += 1
            self.update_counter()

    def check_answer(self):
        user_answer = self.answer_input.text().strip().lower()
        
        if self.invert_mode:
            correct_answer = flashcards[self.index]["q"].strip().lower()
            display_answer = flashcards[self.index]["q"]
        else:
            correct_answer = flashcards[self.index]["a"].strip().lower()
            display_answer = flashcards[self.index]["a"]
        
        if user_answer == correct_answer:
            self.apply_rating("Good")
            self.answer_label.setText(display_answer)
            self.answer_label.setStyleSheet("font-family: 'Inter'; font-size: 40px; color: #8BE764")
        else:
            self.apply_rating("Bad")
            self.answer_label.setText(display_answer)
            self.answer_label.setStyleSheet("font-family: 'Inter'; font-size: 40px; color: #E12C29")
        
        self.question_label.hide()
        self.answer_label.show()
        self.answer_input.hide()
        self.button.setText("Next")
        self.button.show()

    def apply_rating(self, rating):
        card = flashcards[self.index]

        if rating == "Bad":
            card["w"] = min(int(card["w"]) + 2, 10)
        elif rating == "Okay":
            card["w"] = min(int(card["w"]) + 1, 7)
        elif rating == "Good":
            card["w"] = max(int(card["w"]) - 1, 1)

        save_flashcards(flashcards)

        history_entry = {
            "q": card["q"],
            "a": card["a"],
            "w": card["w"],
            "rating": rating,
            "inverted": self.invert_mode
        }
        self.history.append(history_entry)
        self.back_button.show()

    def handle_rating_click(self, button=None):
        sender = self.sender() if button is None else button
        
        if sender == self.rate_bad:
            rating = "Bad"
        elif sender == self.rate_okay:
            rating = "Okay"
        elif sender == self.rate_good:
            rating = "Good"
        else:
            rating = "Okay"

        self.apply_rating(rating)
        self.next_card()

    def go_back(self):
        if self.previous_index == -1 or not self.history:
            return

        self.index = self.previous_index
        self.previous_index = -1 

        self.history.pop()

        card = flashcards[self.index]
        if self.invert_mode:
            self.question_label.setText(card["a"])
            self.answer_label.setText(card["q"])
        else:
            self.question_label.setText(card["q"])
            self.answer_label.setText(card["a"])
        
        self.button.hide()
        self.rate_widget.show()
        self.back_button.hide()

    def show_history_window(self, checked):
        if checked:
            self.history_window = QWidget()
            self.history_window.setWindowTitle("History")
            self.history_window.setGeometry(150, 150, 400, 400)
            self.history_window.setWindowIcon(QIcon("logo-red.png"))
            w_palette = self.history_window.palette()
            w_palette.setColor(QPalette.ColorRole.Window, QColor("#111119"))
            self.history_window.setPalette(w_palette)
            self.history_window.setAutoFillBackground(True)

            layout = QVBoxLayout()
            list_widget = QListWidget()
            list_widget.setStyleSheet("""
                QListView {
                    background-color: #111119;
                    font-family: 'Inter';
                    font-size: 15px;
                    border: none;
                    outline: none;
                }
                QListView::item {
                    color: white;
                    background-color: #605E74;
                    border: none;
                    height: 60px; 
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
                rating = entry["rating"]
                rating_color = "white"  
                if rating == "Bad":
                    rating_color = "#E12C29"  
                elif rating == "Good":
                    rating_color = "#8BE764"  

                green_color = "#8BE764"

                if entry.get("inverted", False):
                    question_part = f'<b><font color="{green_color}">{entry["q"]}</font></b> &larr; {entry["a"]}'
                else:
                    question_part = f'{entry["q"]} &rarr; <font color="{green_color}"><b>{entry["a"]}</b></font>'

                html_text = f"""
                <div style='font-family: "Inter"; color: white; font-size: 15px;'>
                    {question_part}<br>
                    <font color='{rating_color}'>{rating}</font>, weight: <b>{entry['w']}</b>
                </div>
                """

                item = QListWidgetItem()
                label = QLabel(html_text)
                label.setWordWrap(True) 

                item.setSizeHint(label.sizeHint())

                list_widget.addItem(item)
                list_widget.setItemWidget(item, label)

            layout.addWidget(list_widget)
            self.history_window.setLayout(layout)
            self.history_window.show()
            self.history_window.closeEvent = lambda event: self.history_button.setChecked(False)
        elif hasattr(self, 'history_window') and self.history_window.isVisible():
            self.history_window.close()

    def update_counter(self):
        self.counter_label.setText(f"Total cards: {self.total_cards} | Flips: {self.flip_count}")

    def open_manager(self):
        self.manager = FlashCardManager(self)
        self.manager.show()

    def toggle_invert_mode(self, checked):
        self.invert_mode = checked
        if checked:
            self.invert_button.setStyleSheet("font-family: 'Inter'; font-size: 20px; background: #8BE764; color: #111119; border: none; border-radius: 15px; height: 30px; width: 60px")
        else:
            self.invert_button.setStyleSheet("font-family: 'Inter'; font-size: 20px; background: #605E74; color: #111119; border: none; border-radius: 15px; height: 30px; width: 60px")
        self.update_card_display()
    
    def toggle_writing_mode(self, checked):
        self.writing_mode = checked
        if checked:
            self.writing_button.setStyleSheet("font-family: 'Inter'; font-size: 20px; background: #8BE764; color: #111119; border: none; border-radius: 15px; height: 30px; width: 120px")
        else:
            self.writing_button.setStyleSheet("font-family: 'Inter'; font-size: 20px; background: #605E74; color: #111119; border: none; border-radius: 15px; height: 30px; width: 120px")
        self.update_card_display()

    def update_card_display(self):
        if self.index == -1 or not flashcards:
            self.question_label.setText("No flashcards available")
            self.answer_label.setText("")
            self.button.hide()
            self.rate_widget.hide()
            self.answer_input.hide()
            return

        card = flashcards[self.index]

        if self.invert_mode:
            self.question_label.setText(card["a"])  
            self.answer_label.setText("")           
        else:
            self.question_label.setText(card["q"])  
            self.answer_label.setText("")           

        self.rate_widget.hide()
        self.answer_label.hide()

        if self.writing_mode:
            self.button.setText("Check")
            self.answer_input.show()
            self.answer_input.clear()
            self.answer_input.setFocus()
        else:
            self.button.setText("Flip")
            self.answer_input.hide()

        self.button.show()

class FlashCardManager(QWidget):
    def __init__(self, parent_widget):
        super().__init__()
        self.parent_widget = parent_widget
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Manage Flashcards")
        self.setGeometry(150, 150, 400, 400)
        self.setWindowIcon(QIcon("logo-red.png"))
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
                outline: none;
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
            
            if not flashcards:
                self.parent_widget.index = -1
            else:
                if self.parent_widget.index >= len(flashcards):
                    self.parent_widget.index = len(flashcards) - 1

            self.parent_widget.update_card_display()
            self.parent_widget.update_counter()
            self.update_list()

    def add_card(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("New Flashcard")
        dialog.setWindowIcon(QIcon("logo-red.png"))
        dialog.setMinimumSize(300, 200)
        w_palette = dialog.palette()
        w_palette.setColor(QPalette.ColorRole.Window, QColor("#111119"))
        dialog.setPalette(w_palette)
        dialog.setAutoFillBackground(True)
        dialog.setModal(True)

        q_label = QLabel()
        q_label.setText("Question")
        q_label.setStyleSheet("color: white; font-family: 'Inter'; font-size: 15px")
        q_input = QLineEdit()
        q_input.setStyleSheet("border: none; border-radius: 10px; background-color: #605E74; color: white; font-family: 'Inter'; font-size: 15px; height: 30px; padding: 5px;")
        a_label = QLabel()
        a_label.setText("Answer")
        a_label.setStyleSheet("color: white; font-family: 'Inter'; font-size: 15px")
        a_input = QLineEdit()
        a_input.setStyleSheet("border: none; border-radius: 10px; background-color: #605E74; color: white; font-family: 'Inter'; font-size: 15px; height: 30px; padding: 5px;")

        save_button = QPushButton("Save")
        save_button.setStyleSheet("color: #111119; font-family: 'Inter'; font-size: 15px; background: #8BE764; border: none; height: 30px; border-radius: 15px;")
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
