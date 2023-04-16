import tkinter as tk
from tkinter import messagebox, filedialog


class NotepadUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Untitled   - AI Notepad")
        self.master.geometry("960x540")

        global current_opened_file
        current_opened_file = False

        global selected
        selected = False
        
        # Set up the UI elements

        # Menu
        # File Menu
        menuBar = tk.Menu(self.master, bg="#f2fef7", borderwidth=0)
        self.master.config(menu=menuBar)
        fileMenu = tk.Menu(menuBar, tearoff=0, bg="#f2fef7")
        fileMenu.add_command(label="New...", command=lambda: self.new_file(False), accelerator="Ctrl+N")
        fileMenu.add_command(label="New Window    ", command=lambda: self.new_window(False), accelerator="Ctrl+Shift+N")
        fileMenu.add_separator()
        fileMenu.add_command(label="Open", command=lambda: self.open_file(False), accelerator="Ctrl+O")
        fileMenu.add_command(label="Save...", command=lambda: self.save_file(False), accelerator="Ctrl+S")
        fileMenu.add_command(label="Save As", command=lambda: self.save_as(False), accelerator="Ctrl+Shift+S")
        fileMenu.add_separator()
        fileMenu.add_command(label="Exit", command=lambda: self.quit(False), accelerator="Ctrl+Q")

        menuBar.add_cascade(label="File", menu=fileMenu)

        # Edit Menu
        editMenu = tk.Menu(menuBar, tearoff=0, bg="#f2fef7")
        editMenu.add_command(label="Cut", command=lambda: self.cut(False), accelerator="Ctrl+X")
        editMenu.add_command(label="Copy", command=lambda: self.copy(False), accelerator="Ctrl+C")
        editMenu.add_command(label="Paste", command=lambda: self.paste(False), accelerator="Ctrl+V")
        editMenu.add_separator()
        editMenu.add_command(label="Select All", command=lambda: self.select_all(False), accelerator="Ctrl+A")
        editMenu.add_separator()
        editMenu.add_command(label="Clear the page", command="")
        editMenu.add_command(label="Background color", command="")

        menuBar.add_cascade(label="Edit", menu=editMenu)

        # View Menu
        viewMenu = tk.Menu(menuBar, tearoff=0, bg="#f2fef7")
        zoomMenu = tk.Menu(viewMenu, tearoff=0, bg="#f2fef7")
        viewMenu.add_cascade(label="Zoom", menu=zoomMenu)
        zoomMenu.add_command(label="Zoom in", command="")
        zoomMenu.add_command(label="Zoom out", command="")
        viewMenu.add_separator()
        viewMenu.add_command(label="Status bar", command="")

        menuBar.add_cascade(label="View", menu=viewMenu)

        # About Menu
        aboutMenu = tk.Menu(menuBar, tearoff=0, bg="#f2fef7")
        aboutMenu.add_command(label="About Notepad AI", command=self.about)
        menuBar.add_cascade(label="About", menu=aboutMenu)

        # Scrollbar
        scrollbar = tk.Scrollbar(self.master, background="#f2fef7")
        scrollbar.pack(side="right", fill="y")

        # text Area
        global textArea
        textArea = tk.Text(self.master, borderwidth=0, 
                           font=("typewriter", 14), 
                           selectbackground="yellow", 
                           selectforeground="black", 
                           yscrollcommand=scrollbar.set, 
                           undo=True,
                           highlightthickness=0)
        textArea.pack(fill=tk.BOTH, expand=True)

        # Status bar
        global statusBar
        statusBar = tk.Label(self.master, text="Status",
                             borderwidth=0, height=2, bg="#f2fef7", anchor=tk.E, padx=10)
        statusBar.pack(side=tk.BOTTOM, fill=tk.X)

        # Cofigure scrollbar
        scrollbar.config(command=textArea.yview)

        # Edit binding
        self.master.bind("<Control-Key-x>", self.cut)
        self.master.bind("<Control-Key-X>", self.cut)
        self.master.bind("<Control-Key-c>", self.copy)
        self.master.bind("<Control-Key-C>", self.copy)
        self.master.bind("<Control-Key-v>", self.paste)
        self.master.bind("<Control-Key-V>", self.paste)
        self.master.bind("<Control-Key-n>", self.new_file)
        self.master.bind("<Control-Key-s>", self.save_file)
        self.master.bind("<Control-S>", self.save_as)
        self.master.bind("<Control-Key-o>", self.open_file)
        self.master.bind("<Control-Key-O>", self.open_file)
        self.master.bind("<Control-Key-q>", self.quit)
        self.master.bind("<Control-Key-Q>", self.quit)
        self.master.bind("<Control-N>", self.new_window)
        self.master.bind("<Control-Key-a>", self.select_all)
        self.master.bind("<Control-Key-A>", self.select_all)

    # Quit 
    def quit(self, e):
        self.master.quit()

    # New file

    def new_file(self, e):
        textArea.delete("1.0", tk.END)
        self.master.title("New File   - AI Notepad")
        statusBar.config(text="New File")

        global current_opened_file
        current_opened_file = False

    # open file

    def open_file(self, e):
        textArea.delete("1.0", tk.END)

        # get file name
        filename = filedialog.askopenfilename(title="Open File", filetypes=(("All Files", "*.*"),
                                                                            ("Text file", "*.txt"),
                                                                            ("SQL file", "*.sql"),
                                                                            ("HTML file", "*.html"),
                                                                            ("Python file", "*.py")
                                                                            ))
        
        # Get the current file name
        global current_opened_file
        current_opened_file = filename

        # Get the name of the file
        name = filename.split("/")[-1]
        name = name[:name.find(".")]

        # title
        self.master.title(f'{name}   - AI Notepad')

        # Status
        statusBar.config(text=filename)

        # Open file
        text_file = open(filename, 'r')
        text = text_file.read()

        textArea.insert(tk.END, text)

        # Closing the file
        text_file.close()

    # New Window

    def new_window(self, e):
        root = tk.Tk()
        NotepadUI(root)
        root.mainloop()

    # Save As File

    def save_as(self, e):
        
        # get file name
        filename = filedialog.asksaveasfilename(defaultextension=".txt", title="Save As", filetypes=(
                                                                            ("All file", "*.*"),
                                                                            ("Text file", "*.txt"),
                                                                            ("SQL file", "*.sql"),
                                                                            ("HTML file", "*.html"),
                                                                            ("Python file", "*.py")
                                                                            ))
        if filename:
            
            name = filename.split("/")[-1]
            name = name[:name.find(".")]

            # title
            self.master.title(f'{name}   - AI Notepad')

            # Status
            statusBar.config(text=f'{filename}   - Saved')

            # Save file
            text_file = open(filename, 'w')
            text_file.write(textArea.get(1.0, tk.END))

            # Closing the file
            text_file.close()

    
    # Save File
    def save_file(self, e):

        if current_opened_file:
            # Save file
            text_file = open(current_opened_file, 'w')
            text_file.write(textArea.get(1.0, tk.END))

            # Status
            statusBar.config(text=f'{current_opened_file}   - Saved')

            # Closing the file
            text_file.close()
        else:
            self.save_as(e)


    # select all
    def select_all(self, e):
        textArea.tag_add(tk.SEL, "1.0", tk.END)
        textArea.mark_set(tk.INSERT, "1.0")
        textArea.see(tk.INSERT)
        return 'break'
    # Cut function
    def cut(self, e):
        global selected
        # Checking if we used the shortcut
        if e:
            selected = self.master.clipboard_get()
        elif textArea.selection_get():
            selected = textArea.selection_get()
            # delete the selected
            textArea.delete("sel.first", "sel.last")
            self.master.clipboard_clear()
            self.master.clipboard_append(selected)
            

    # Copy function
    def copy(self, e):
        global selected
        if e:
            selected = self.master.clipboard_get()
        elif textArea.selection_get():
            selected = textArea.selection_get()
            self.master.clipboard_clear()
            self.master.clipboard_append(selected)

    # Paste function
    def paste(self, e):
        global selected
        if e:
            selected = self.master.clipboard_get()
        elif selected:
            position = textArea.index(tk.INSERT)
            textArea.insert(position, selected)
            self.master.clipboard_clear()
            self.master.clipboard_append(selected)

    # About Message function
    def about(self):
        messagebox.showinfo(title="Welcome User!", message="This an intelligent notepad that will auto-correct & auto-complete your notes!\n Have a great day sir!")


if __name__ == "__main__":
    # Create and show the UI
    root = tk.Tk()
    NotepadUI(root)
    root.mainloop()
