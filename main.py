import pickle
import re
import tkinter as tk
import webbrowser
from tkinter import messagebox, filedialog , colorchooser

from win32comext.shell.demos.servers.folder_view import make_item_enum

from Model.edit import *


class NotepadUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Untitled   - AI Notepad")
        self.master.geometry("960x540")
        self.master.configure(bg="#f2fef7")
        self.master.protocol("WM_DELETE_WINDOW",lambda: self.quit(False))
        photo = tk.PhotoImage(file='website/rsc/JT.png')
        self.master.wm_iconphoto(False, photo)
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
        fileMenu.add_command(label="New...", command=lambda: self.new_file(
            False), accelerator="Ctrl+N")
        fileMenu.add_command(label="New Window    ", command=lambda: self.new_window(
            False), accelerator="Ctrl+Shift+N")
        fileMenu.add_separator()
        fileMenu.add_command(label="Open", command=lambda: self.open_file(
            False), accelerator="Ctrl+O")
        fileMenu.add_command(label="Save...", command=lambda: self.save_file(
            False), accelerator="Ctrl+S")
        fileMenu.add_command(label="Save As", command=lambda: self.save_as(
            False), accelerator="Ctrl+Shift+S")
        fileMenu.add_separator()
        fileMenu.add_command(label="Exit", command=lambda: self.quit(
            False), accelerator="Ctrl+Q")

        menuBar.add_cascade(label="File", menu=fileMenu)

        # Edit Menu
        editMenu = tk.Menu(menuBar, tearoff=0, bg="#f2fef7")
        editMenu.add_command(label="Cut", command=lambda: self.cut(
            False), accelerator="Ctrl+X")
        editMenu.add_command(label="Copy", command=lambda: self.copy(
            False), accelerator="Ctrl+C")
        editMenu.add_command(label="Paste", command=lambda: self.paste(
            False), accelerator="Ctrl+V")
        editMenu.add_separator()
        editMenu.add_command(label="Select All", command=lambda: self.select_all(
            False), accelerator="Ctrl+A")
        editMenu.add_separator()
        editMenu.add_command(label="Clear the page", command=lambda : self.clear(False))
        editMenu.add_command(label="Background color", command=lambda : self.change_back_ground_color())
        editMenu.add_command(label="Font color", command=lambda: self.change_font_color())

        menuBar.add_cascade(label="Edit", menu=editMenu)

        # View Menu
        viewMenu = tk.Menu(menuBar, tearoff=0, bg="#f2fef7")
        zoomMenu = tk.Menu(viewMenu, tearoff=0, bg="#f2fef7")
        viewMenu.add_cascade(label="Zoom", menu=zoomMenu)
        zoomMenu.add_command(label="Zoom in", command=lambda : self.zoomIn())
        zoomMenu.add_command(label="Zoom out", command=lambda : self.zoomOut())
        viewMenu.add_separator()
        viewMenu.add_command(label="Status bar", command="")

        menuBar.add_cascade(label="View", menu=viewMenu)

        # About Menu
        aboutMenu = tk.Menu(menuBar, tearoff=0, bg="#f2fef7")
        aboutMenu.add_command(label="About Notepad AI", command=self.about)
        menuBar.add_cascade(label="About", menu=aboutMenu)

        # report bug menu
        bugMenu = tk.Menu(menuBar, bg="#f2fef7", borderwidth=0)
        bugMenu.add_command(label="Report a bug", command=lambda: self.new_file(
            False), accelerator="Ctrl+N")
        menuBar.add_cascade(label="report", menu=bugMenu)
        # Scrollbar
        scrollbar = tk.Scrollbar(self.master, background="#f2fef7")
        scrollbar.pack(side="right", fill="y")

        # text Area
        global textArea
        textArea = tk.Text(self.master, borderwidth=0,
                           font=("Lucida Console", 12),
                           selectbackground="skyblue",
                           selectforeground="black",
                           yscrollcommand=scrollbar.set,
                           undo=True,
                           highlightthickness=0)
        textArea.pack(fill=tk.BOTH, expand=True)

        # Status bar
        global statusBar
        statusBar = tk.Label(self.master, text="Status",
                             borderwidth=0, height=1, bg="#f2fef7", anchor=tk.E, padx=10)
        statusBar.pack(side=tk.RIGHT)

        # Cofigure scrollbar
        scrollbar.config(command=textArea.yview)

        # Columns and Rows
        global colandline
        colandline = tk.Label(self.master,
                              borderwidth=0, height=1, bg="#f2fef7", anchor=tk.W, padx=10)
        colandline.pack(side=tk.LEFT)

        # Col & line status bar
        def rowcol(ev=None):
            r, c = textArea.index('insert').split('.')
            colandline['text'] = f'Ln {r} , Col {c}'

        textArea.event_add(
            '<<REACT>>', *('<Motion>', '<ButtonRelease>', '<KeyPress>', '<KeyRelease>'))
        b = textArea.bind('<<REACT>>', rowcol)
        rowcol()  # get the ball rolling
        textArea.focus()

        # Right click Menu
        rcMenu = tk.Menu(textArea, tearoff=0, bg="#f2fef7")
        def menu_commands(e):
            if e == 1:    
                rcMenu.add_command(label="Add to dictionary", command=lambda: self.add_to_Dictionary(False))
                rcMenu.add_command(label="Search Google", command=lambda: self.searsh(False))
                rcMenu.add_separator()
            if e == 2:    
                rcMenu.add_command(label="Search Google", command=lambda: self.searsh(False))
                rcMenu.add_separator()
            rcMenu.add_command(label="Scan for errors", command=lambda: self.scaner(False), accelerator="Alt+C")
            rcMenu.add_separator()
            rcMenu.add_command(label="Cut", command=lambda: self.cut(
                        False), accelerator="Ctrl+X")
            rcMenu.add_command(label="Copy", command=lambda: self.copy(
                        False), accelerator="Ctrl+C")
            rcMenu.add_command(label="Paste", command=lambda: self.paste(
                        False), accelerator="Ctrl+V")
            rcMenu.add_separator()
            rcMenu.add_command(label="Exit", command=lambda: self.quit(False))

        # Binding for the right click menu
        # Call rcMenu
        def call_rcMenu(e):
            rcMenu.delete(0, tk.END)
            call_suggestions_menu(e)
            rcMenu.tk_popup(e.x_root, e.y_root)

        def call_suggestions_menu(e):
            # START
            location = textArea.index('current')

            col = int(location.split('.')[1])
            row = int(location.split('.')[0])
            letter = textArea.get(str(row) + "." + str(col))
            print("letter" + letter.strip() + "fucking")
            if letter.strip() != "":

                search = True
                while search:
                    if letter != " " and col != 0:
                        col -= 1
                        letter = textArea.get(str(row) + "." + str(col))
                    else:
                        search = False
                if col == 0:
                    start = str(row) + "." + str(col)
                else:
                    start = str(row) + "." + str(col + 1)

                # END
                location = textArea.index('current')

                col = int(location.split('.')[1])
                row = int(location.split('.')[0])
                letter = textArea.get(location)
                search = True
                while search:
                    if letter != " " and col != 0:
                        col += 1
                        letter = textArea.get(str(row) + "." + str(col))
                    else:
                        search = False
                end = str(row) + "." + str(col)

                textArea.tag_add(tk.SEL, start, end)

                word = textArea.get(start, end)
                with open('Model/vocab.pkl', 'rb') as f:
                    updated_vocab = pickle.load(f)
                    f.close()
                with open('Model/probs.pkl', 'rb') as f:
                    updated_probs = pickle.load(f)
                    f.close()
                if word not in updated_vocab:
                    list_ = get_corrections(word, updated_probs, updated_vocab)
                    print('hdachi ll dayr lmachkil ', list_)
                    if len(list_) != 0:
                        list_ = [list_[i][0] for i in range(len(list_))]

                        labels = list_[:5]
                        # suggestion_med = map(list_,min_edit_distance())
                        suggestion_med = [min_edit_distance(word, list_[i]) for i in range(len(list_))]
                        print('sugg med', suggestion_med)
                        print('list sugg', list_)
                        word_med = {}
                        for i in range(len(list_)):
                            # word_med.update({tuple(list_[i]): suggestion_med[i]})  # Convert list_[i] to a tuple
                            word_med.update({"".join(list_[i]): suggestion_med[i]})
                        sorted_suggestion = dict(sorted(word_med.items(), key=lambda x: x[1]))
                        print('word_med', word_med)
                        print('sorted ', sorted_suggestion)
                        sorted_keys = list(sorted_suggestion.keys())
                        sorted_values = list(sorted_suggestion.values())

                        # sorted_labels = sorted(labels, key=lambda x: x[1], reverse=True)
                        # suggestions = [sorted_labels[i][0] for i in range(len(sorted_labels))]

                        # Right click Menu that will contain the words
                        def sugg1():
                            textArea.replace(start, end, sorted_keys[0])

                        def sugg2():
                            textArea.replace(start, end, sorted_keys[1])

                        def sugg3():
                            textArea.replace(start, end, sorted_keys[2])

                        def sugg4():
                            textArea.replace(start, end, sorted_keys[3])

                        def sugg5():
                            textArea.replace(start, end, sorted_keys[4])

                        for i in range(len(sorted_suggestion)):
                            if i == 0:
                                rcMenu.add_command(label=sorted_keys[i], command=sugg1,
                                                   accelerator='med(' + str(sorted_values[i]) + ')')

                            if i == 1:
                                rcMenu.add_command(label=sorted_keys[i], command=sugg2,
                                                   accelerator='med(' + str(sorted_values[i]) + ')')

                            if i == 2:
                                rcMenu.add_command(label=sorted_keys[i], command=sugg3,
                                                   accelerator='med(' + str(sorted_values[i]) + ')')

                            if i == 3:
                                rcMenu.add_command(label=sorted_keys[i], command=sugg4,
                                                   accelerator='med(' + str(sorted_values[i]) + ')')

                            if i == 4:
                                rcMenu.add_command(label=sorted_keys[i], command=sugg5,
                                                   accelerator='med(' + str(sorted_values[i]) + ')')
                    rcMenu.add_separator()
                    menu_commands(1)
                else:
                    menu_commands(2)
            else:
                menu_commands(0)

        textArea.bind("<Button-3>",call_rcMenu)

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
        self.master.bind("<space>", self.correct)
        self.master.bind("<Return>", self.correct)
        self.master.bind("<Alt-Key-c>", self.scaner)
        self.master.bind("<Alt-Key-C>", self.scaner)


    def location(self, e):
        location = textArea.index('current')

        col = int(location.split('.')[1])
        row = int(location.split('.')[0])
        letter = textArea.get(str(row) + "." + str(col))
        search = True
        while search:
            if letter != " " and col != 0:
                col -= 1
                letter = textArea.get(str(row) + "." + str(col))
            else:
                search = False
        if col == 0:
            start = str(row) + "." + str(col)
        else:
            start = str(row) + "." + str(col + 1)

        # END
        word_len = len(textArea.get(start, tk.END).split(" ")[0])
        end = str(row) + "." + str(col + word_len+1)
        return start, end
    
    def searsh(self,e):
        start, end = self.location(e)
        # remove underline
        textArea.tag_config("underline", underline=False)
        textArea.tag_add("underline", start, end)

        # add word to vocabulary
        word = textArea.get(start, end).lower()
        url = 'https://www.google.com/search?q='+word
        webbrowser.open_new_tab(url)

    def add_to_Dictionary(self, e):
        start, end = self.location(e)
        # remove underline
        
        textArea.tag_add("underline",start,end)
        textArea.tag_config("underline", underline=False)

        # add word to vocabulary
        word = textArea.get(start,end).lower()
        print(word)
        vocab.add(word)

        # add word to probabilities
        probs[str(textArea.tag_add("underline",start,end))]='1e-06'
        print('word ',textArea.get(start,end),'added to vocab and will not be underlined')

        with open('Model/vocab.pkl','wb') as f:
            pickle.dump(vocab,f)
            f.close()

        with open('Model/probs.pkl', 'wb') as s:
            pickle.dump(probs, s)
            s.close()

        self.correct(False)

    def last(self, e):
        text = textArea.get(1.0, tk.END).strip().lower()
        print("letter"+text+"fucking")
        #w = text.split(" ")[-1]
        if text != "":
            lis = re.findall('\w+', text)
            print('list ',lis)
            w = lis[-1]

            print(w)
            return str(w).strip().lower()

    def scaner(self, e):
        text = textArea.get(1.0, tk.END).strip().lower()
        if text != "":
            list_ = re.findall('\w+', text)
            for w in list_:
                start_index = '1.0'
                with open('Model/vocab.pkl','rb') as f :
                    updated_vocab = pickle.load(f)
                # we loop through the entire textarea to get all occurences of w not only first one
                while True:
                    pos_start = textArea.search(w, start_index, tk.END)
                    if not pos_start:
                        break
                    pos_end = pos_start + f'+{len(w)}c'
                    if w not in updated_vocab:
                        textArea.tag_config("underline", underline=True, underlinefg="red")
                        textArea.tag_add("underline", pos_start, pos_end)
                    start_index = pos_end

    
    # Correct word

    def correct(self, e):
        w = self.last(e)
        start_index = '1.0'
        with open('Model/vocab.pkl','rb') as f :
            updated_vocab = pickle.load(f)
        # we loop through the entire textarea to get all occurences of w not only first one
        while True:
            pos_start = textArea.search(w, start_index, tk.END)
            if not pos_start:
                break
            pos_end = pos_start + f'+{len(w)}c'
            if w not in updated_vocab:
                textArea.tag_config("underline", underline=True, underlinefg="red")
                textArea.tag_add("underline", pos_start, pos_end)
            start_index = pos_end


    # Quit

    def quit(self, e):
        answer = messagebox.askyesno(title= "Exit",message="Are you sure you want to quit?")
        if answer:
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
                                                                            ("Text file",
                                                                             "*.txt"),
                                                                            ("SQL file",
                                                                             "*.sql"),
                                                                            ("HTML file",
                                                                             "*.html"),
                                                                            ("Python file",
                                                                             "*.py")
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
            ("Text file",
             "*.txt"),
            ("SQL file",
             "*.sql"),
            ("HTML file",
             "*.html"),
            ("Python file",
             "*.py")
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
        messagebox.showinfo(
            title="Welcome User!",
            message="This an intelligent notepad that will auto-correct & auto-complete your notes!\n Have a great day sir!")

    def clear(self, e):
        textArea.delete(1.0,tk.END)

    def change_back_ground_color(self):
        color = colorchooser.askcolor()[1]  # Open color dialog and get the chosen color
        textArea.config(bg=color)

    def change_font_color(self):
        # Open a color chooser dialog
        color = colorchooser.askcolor()[1]

        # Delete any existing "default" tag
        textArea.tag_delete("default")

        # Configure a new "default" tag with the selected color
        textArea.tag_configure("default", foreground=color)

        # Apply the "default" tag to all existing text in the Text widget
        textArea.tag_add("default", "1.0", tk.END)

    def zoomIn(self):
        # Get the current font size of the Text widget
        current_font = textArea['font']
        print(current_font)
        font_size = int(current_font.split(' ')[-1])

        # Calculate the new font size after applying the zoom factor
        new_font_size = int(font_size +2)

        # Update the font size in the Text widget
        textArea.config(font=(current_font.split(' ')[0], new_font_size))

    def zoomOut(self):
        current_font = textArea['font']
        print(current_font)
        font_size = int(current_font.split(' ')[-1])

        # Calculate the new font size after applying the zoom factor
        new_font_size = int(font_size - 2)

        # Update the font size in the Text widget
        textArea.config(font=(current_font.split(' ')[0], new_font_size))


if __name__ == "__main__":
    # Create and show the UI
    root = tk.Tk()
    NotepadUI(root)
    root.mainloop()