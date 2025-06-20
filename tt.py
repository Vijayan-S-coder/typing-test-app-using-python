import tkinter as tk
import time
import random
import re
import wikipedia

# --- Get words from Wikipedia ---
def get_wiki_words():
    try:
        summary = wikipedia.summary(wikipedia.random(), sentences=2)
        words = summary.split()
        words = [word.strip('.,?!') for word in words if word.strip()]
        return words[:20]
    except:
        return ["Neon", "Typing", "Test", "is", "loading", "try", "again"]

# --- Clean word (remove punctuation + lowercase) ---
def clean_word(word):
    return re.sub(r'[^\w]', '', word.lower())  # removes all special characters

# --- Variables ---
words_list = get_wiki_words()
current_index = 0
start_time = None
correct_words = 0
time_left = 60

# --- Countdown Timer ---
def countdown():
    global time_left
    if time_left > 0:
        minutes = time_left // 60
        seconds = time_left % 60
        timer_label.config(text=f"{minutes:02d}:{seconds:02d}")
        time_left -= 1
        window.after(1000, countdown)
    else:
        end_typing()

# --- Start Timer on First Key ---
def start_timer(event):
    global start_time
    if start_time is None:
        countdown()
        start_time = time.time()

# --- Handle Enter Press ---
def handle_enter(event):
    global current_index, correct_words

    typed = clean_word(entry.get().strip())
    expected = clean_word(words_list[current_index])

    if typed == expected:
        entry.config(fg="#39FF14")  # Neon green
        correct_words += 1
        current_index += 1
        if current_index < len(words_list):
            word_label.config(text=words_list[current_index])
            entry.delete(0, tk.END)
    else:
        entry.config(fg="#FF3131")  # Neon red (wrong word)

# --- Simulate fade-out by changing text color ---
def fade_out(label, delay=100, step=10):
    def fade(i):
        if i >= 255:
            label.config(text="")
        else:
            gray = f"#{i:02x}{i:02x}{i:02x}"
            label.config(fg=gray)
            window.after(delay, fade, i + step)
    fade(0)

# --- End Typing Test ---
def end_typing():
    entry.config(state="disabled")
    word_label.pack_forget()
    entry.pack_forget()
    info_label.pack_forget()
    timer_label.pack_forget()

    total_time = 60
    wpm = round((correct_words / total_time) * 60, 2)
    accuracy = round((correct_words / len(words_list)) * 100, 2)

    result_label.config(
        text=f"✅ Done!\n🚀 WPM: {wpm}\n🎯 Accuracy: {accuracy}%\n⏱ Time Taken: 60s",
        fg="#00FFEA"
    )
    result_label.pack(pady=30)

    # Start fade-out after 5 seconds
    window.after(5000, lambda: fade_out(result_label))

# --- GUI Setup ---
window = tk.Tk()
window.title("🔥 Neon Typing Speed Test 🔥")
window.geometry("700x450")
window.configure(bg="#0F0F0F")

# --- Fonts and Styles ---
font_main = ("Consolas", 22, "bold")
font_word = ("Consolas", 30, "bold")
font_info = ("Consolas", 12)

# --- Title ---
tk.Label(window, text="💻 Neon Typing Test 💻", font=font_main, fg="#00FFFF", bg="#0F0F0F").pack(pady=10)

# --- Timer ---
timer_label = tk.Label(window, text="01:00", font=("Consolas", 20), fg="#39FF14", bg="#0F0F0F")
timer_label.pack()

# --- Word to Type ---
word_label = tk.Label(window, text=words_list[current_index], font=font_word, fg="#39FF14", bg="#0F0F0F")
word_label.pack(pady=20)

# --- Entry Box ---
entry = tk.Entry(window, font=("Consolas", 22), justify="center", width=20,
                 bg="#1a1a1a", fg="#39FF14", insertbackground="#39FF14",
                 highlightthickness=2, highlightbackground="#00FFFF")
entry.pack(pady=10)
entry.bind("<Key>", start_timer)
entry.bind("<Return>", handle_enter)
entry.focus()

# --- Info Label ---
info_label = tk.Label(window, text="Type the word and press Enter only if it's correct!",
                      font=font_info, fg="#AAAAAA", bg="#0F0F0F")
info_label.pack(pady=10)

# --- Result Label (starts hidden) ---
result_label = tk.Label(window, text="", font=("Consolas", 18), bg="#0F0F0F", justify="center")

# --- Footer ---
tk.Label(window, text="⚡ Designed in Python + Tkinter", font=("Consolas", 10),
         fg="#555555", bg="#0F0F0F").pack(side=tk.BOTTOM, pady=10)

window.mainloop()
