import enchant
import tkinter as tk
from tkinter.scrolledtext import ScrolledText

d = enchant.Dict("en_US")

def suggest_corrections(word):
    if not d.check(word):
        return d.suggest(word)
    return []

root = tk.Tk()
root.title("Spell Checker")

text_label = tk.Label(root, text="Enter text here:")
text_label.pack()
text = ScrolledText(root, font=("Helvetica", 16))
text.pack()
text.configure(background='#D3D3D3')

def correct_spelling():
    text_content = text.get("1.0", tk.END)
    words = text_content.split()
    for i, word in enumerate(words):
        if not d.check(word):
            suggestions = d.suggest(word)
            words[i] = suggestions[0] if suggestions else word
    new_text = " ".join(words)
    text.delete("1.0", tk.END)
    text.insert("1.0", new_text)

correct_button = tk.Button(root, text="Correct Spelling", command=correct_spelling, bg='#6A5ACD', fg='white', padx=10, pady=5)
correct_button.pack()

num_misspelled_label = tk.Label(root, text="0 misspelled words found")
num_misspelled_label.pack()

def highlight_misspelled_words():
    content = text.get("1.0", tk.END)
    num_misspelled = -1
    for tag in text.tag_names():
        text.tag_delete(tag)

    for word in content.split(" "):
        if not d.check(word):
            num_misspelled += 1
            position = content.find(word)
            text.tag_add(word, f"1.{position}", f"1.{position + len(word)}")
            text.tag_config(word, foreground="red",  underline=True)
            text.tag_bind(word, "<Enter>", lambda event, word=word: show_suggestions(event, word))
            text.tag_bind(word, "<Leave>", hide_suggestions)

    num_misspelled_label.configure(text=f"{num_misspelled} misspelled words found")

def show_suggestions(event, word):
    suggestions = suggest_corrections(word)
    if suggestions:
        menu = tk.Menu(text, tearoff=False)
        for suggestion in suggestions:
            menu.add_command(label=suggestion, command=lambda word=word, suggestion=suggestion: replace_word(word, suggestion))
        menu.tk_popup(event.x_root, event.y_root)

def hide_suggestions(event=None):
    menu.unpost() # hide the suggestions menu

def replace_word(word, suggestion):
    start_index = text.search(word, "1.0", tk.END)
    end_index = f"{start_index}+{len(word)}c"
    text.delete(start_index, end_index)
    text.insert(start_index, suggestion)

def check_spelling_and_highlight(event):
    set_status("Running spell check...")
    highlight_misspelled_words()
    check_spelling_and_highlight.after(500, check_spelling_and_highlight)

text.bind("<KeyRelease>", check_spelling_and_highlight)

status_bar = tk.Label(root, text="", bd=1, relief=tk.SUNKEN, anchor=tk.W)
status_bar.pack(side=tk.BOTTOM, fill=tk.X)

def set_status(message):
    status_bar.configure(text=message)

root.mainloop()