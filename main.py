import tkinter as tk
from tkinter import scrolledtext, filedialog, messagebox
from textblob import TextBlob
import language_tool_python
import speech_recognition as sr

class AdvancedSpellGrammarChecker:
    def __init__(self, root):
        self.root = root
        self.root.title("AI-Based Spell & Grammar Checker")
        self.root.geometry("800x600")
        self.root.config(bg="#f4f4f4")
        self.tool = language_tool_python.LanguageTool('en-US')

        # Input Label
        tk.Label(root, text="Enter or Speak Text:", font=("Arial", 12), bg="#f4f4f4").pack(pady=5)

        # Input Text Area
        self.text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=90, height=10, font=("Arial", 11))
        self.text_area.pack(padx=10, pady=5)

        # Button Panel
        btn_frame = tk.Frame(root, bg="#f4f4f4")
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="🎙️ Voice Input", command=self.voice_input, bg="#2196f3", fg="white", padx=10).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="✅ Correct & Check Grammar", command=self.correct_text, bg="#4caf50", fg="white", padx=10).grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="💾 Save to File", command=self.save_to_file, bg="#ff9800", fg="white", padx=10).grid(row=0, column=2, padx=5)

        # Output Label
        tk.Label(root, text="Corrected Output with Grammar Suggestions:", font=("Arial", 12), bg="#f4f4f4").pack(pady=5)

        # Output Text Area
        self.result_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=90, height=15, font=("Arial", 11))
        self.result_area.pack(padx=10, pady=5)
        self.result_area.tag_config("highlight", foreground="red")

    def correct_text(self):
        original_text = self.text_area.get("1.0", tk.END).strip()
        if not original_text:
            messagebox.showwarning("Input Required", "Please enter some text.")
            return

        blob = TextBlob(original_text)
        corrected_blob = blob.correct()
        corrected_text = str(corrected_blob)

        # Highlight corrected words
        self.result_area.delete("1.0", tk.END)
        original_words = original_text.split()
        corrected_words = corrected_text.split()

        for i, word in enumerate(corrected_words):
            if i < len(original_words) and word.lower() != original_words[i].lower():
                self.result_area.insert(tk.END, word + " ", "highlight")
            else:
                self.result_area.insert(tk.END, word + " ")

        # Add grammar suggestions
        matches = self.tool.check(corrected_text)
        if matches:
            self.result_area.insert(tk.END, "\n\nGrammar Suggestions:\n", "bold")
            for match in matches:
                self.result_area.insert(tk.END, f"• {match.message} (Suggested: {match.replacements})\n")

    def voice_input(self):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            messagebox.showinfo("Voice Input", "Listening... Please speak.")
            try:
                audio = recognizer.listen(source, timeout=5)
                spoken_text = recognizer.recognize_google(audio)
                self.text_area.insert(tk.END, spoken_text + " ")
            except sr.UnknownValueError:
                messagebox.showerror("Error", "Sorry, could not understand audio.")
            except sr.RequestError:
                messagebox.showerror("Error", "Could not request results; check your internet.")
            except sr.WaitTimeoutError:
                messagebox.showerror("Error", "Listening timed out.")

    def save_to_file(self):
        corrected_text = self.result_area.get("1.0", tk.END).strip()
        if not corrected_text:
            messagebox.showwarning("Nothing to Save", "Please correct text before saving.")
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                 filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file_path:
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(corrected_text)
            messagebox.showinfo("Success", f"File saved to:\n{file_path}")

if __name__ == "__main__":
    root = tk.Tk()
    app = AdvancedSpellGrammarChecker(root)
    root.mainloop()
  