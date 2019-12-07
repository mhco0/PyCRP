import os
import graphics
import rdt
from tkinter import * 
from tkinter import ttk
from tkinter import messagebox

class Library:
    """Library saves file.txt"""

    def __init__(self):
        pass

    def OpenBook(self, nameBook = "marcos"):
        nameBook = nameBook + ".txt"
        allBooks = os.listdir("./books")
        print(allBooks)
        for name in allBooks:
            if nameBook == name:
                path = "./books/" + nameBook
                book = open(path, 'r')
                text = book.read()
                print(text)
                book.close()
        return text
    
    def SaveBook(self, nameBook= "Marcos", text= "oi\neu\nsou\nmarcos"):
        nameBook = nameBook + ".txt"
        allBooks = os.listdir("./books")
        print(allBooks)
        bookExist = False
        for name in allBooks:
            if name == nameBook:
                bookExist = True
                print("The book already exist!")
                break

        if not bookExist:
            path = "./books/" + nameBook
            newBook = open(path, 'x')
            newBook.write(text)
            newBook.close()

    def ShowBooks(self):
        allBooks = os.listdir("./books")

    def About(self):
        messagebox.showinfo("Created by","mvca, nss2, mhco, ...")

    def MeuMenu(self):
        root = Tk()
        root.geometry('500x300')
        root.title("Library Menu")

        menu = Menu(root)
        root.config(menu=menu)

        filemenu = Menu(menu)
        menu.add_cascade(label="File", menu=filemenu) 
        filemenu.add_command(label="My books", command=self.ShowBooks)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=root.quit)

        helpmenu = Menu(menu)
        menu.add_cascade(label="Help", menu=helpmenu)
        helpmenu.add_command(label="About...", command=self.About)

        but_Download = 
        
def main():
    lb = Library()
    lb.MeuMenu()
    mainloop()

if __name__ == "__main__":
    main()