
#  <img width="100" height="100" alt="logo-red" src="https://github.com/user-attachments/assets/f9434ad4-01d5-4381-8741-293cd0493aa3" />    Vithoba Flashcards 

🀄 Vithoba is a powerful Flashcard Tool built in Python. It has weight-functionality, so the cards don't just rotate randomly.  
Also, you can invert the flashcard and type in the answer instead of just flipping, if you want to.

📂 The flashcards are saved in the `flashcards.json` file, where they could also be edited of course.

---

## 📥 Installation
🔽 Download the **ZIP** with the green **Code** button and get the *Vithoba-main* folder out of the **ZIP**.

You'll most likely need to type this into the `Terminal` (Visual Studio Code), as you need `PyQt6`:

    pip install pyqt6

If not working, try:

    py -m pip install pyqt6

▶ **To start, just open the gui.py file.**

The font used is `Inter`, you'll have to install it on your own: https://fonts.google.com/specimen/Inter (it's not required, but recommended)
Of course, `Python` itself is required: https://www.python.org/downloads/

## 🖼 GUI

<img width="503" height="429" alt="image" src="https://github.com/user-attachments/assets/f78d74b0-3325-40b9-9731-3c2cad7f291a" />

---

<img width="497" height="424" alt="image" src="https://github.com/user-attachments/assets/3173bca3-8a74-4df8-afd8-ff35e39c0dbd" />

---

<img width="495" height="424" alt="image" src="https://github.com/user-attachments/assets/190642b8-6417-4288-8c15-b6dff298d078" />

---

## ✨ Features

### ⭕ General

- 💫 Flip (Show answer and rating menu)
- 〽 Rating

      Rate your own answer
      Bad, Okay or Good
      Depending on that the weight will change (Bad adds, Good removes)
      After rating, a new random flashcard will appear
      In writing mode, if your answer is correct, it will be rated Good, if incorrect, Bad.

- 🧱 Weight

      The weight will determine how often you get a flashcard
      You can edit it by hand in the flashcards.json file, if you want
  
- ▶ Next (Goes to the next flashcard, writing mode exclusive, as you don't rate on your own)
- 📈 Counter (Info: total number of flashcards and the count of flips done)

### ➖ Bottom Bar

- ◀ Go Back `←` (Updates rating of last flashcard)
- 🔳 Invert (Switches Question and Answer)
- 🅰 Type (Enable writing mode)
- 📔 History Menu

  Menu of Items:

      Question (←/→) Answer
      (Bad/Okay/Good), weight (1/2/3/...)
  
- 👔 Manage Menu `...`

  Menu of Items:

      Question → Answer

  🗑 **Delete** Selected Flashcard 
  
  ➕ **Add** Flashcard (with Popup)
  

## ♻ Changelog
08/29/25 | 1.1 | Added **Type** and **Go Back** function

08/28/25 | 1.0 | Base Version
