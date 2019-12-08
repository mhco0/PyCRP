import os
import graphics
import rdt
from tkinter import * 
from tkinter import ttk
from tkinter import messagebox

class Library(object):
    """Library saves file.txt"""

    def __init__(self, sm):
        self.sm = sm
        self.Main_Menu()

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

    def Get_Books_From_Server(self):
        # Comunicação com o servidor pra pegar os livros existentes.
        books = ['Narnia.txt', 'Starwars.txt']

        return books

    def Download_Book(self, bookName, books):
        # Aqui vai usar o rdt pra receber o Livro.
        print("Baixando ", bookName)
        bookName = bookName + '.txt'
        exist = False
        for bname in books:
            if bname == bookName:
                exist = True
        if exist:
            ## Envia para o servidor
            print("Envia pro server")
            messagebox.showinfo("Download", "The book has been downloaded!")
        else:
            messagebox.showerror("ERROR", "The book doesn't exist!")


    def Download_Window(self):
        books = self.Get_Books_From_Server()
        txt = 'Books Avaible:  \n'
        for name in books:
            txt = txt + name[:len(name)-4] +', '
        txt = txt[:len(txt)-2] + '.'


        downWindow = Tk()
        downWindow.geometry("500x400")
        downWindow.minsize(width= 500, height = 200)
        downWindow.title("Download")
        downWindow.configure(bg = 'white')

        

        ltext = Label(downWindow, text = txt, fg = "black", bg="white",font = ("Purisa, 13"))
        ltext.pack(side = TOP, expand = YES, padx = 20, pady = 60, fill = BOTH)


        linput = Label(downWindow, text = "Write the book name: ", fg = "black", bg="white",font = ("Purisa, 10"))
        linput.pack(side= TOP, expand = YES, padx = 10, pady = 0, fill = BOTH)
        einput = Entry(downWindow)
        einput.pack(side= LEFT, expand = YES, padx = 10, pady = [0, 20], fill = BOTH)

        binput = Button(downWindow, text = 'Download', width=20,bg = "#20B2AA", fg ="white", command= lambda: self.Download_Book(einput.get(), books))
        binput.pack(side= BOTTOM, expand = YES, padx = 10, pady = [0, 20], fill = BOTH)

    def Upload_Book(self, bookName, myBooks):
        bookName = bookName + '.txt'
        exist = False
        for bname in myBooks:
            if bname == bookName:
                exist = True
        if exist:
            ## Envia para o servidor
            print("Envia pro server")
            messagebox.showinfo("Upload", "The book has been sent to the server!")
        else:
            messagebox.showerror("ERROR", "The book doesn't exist!")

    def Upload_Window(self):
        myBooks = os.listdir("./books")
        txt = 'Your books:  \n'
        for name in myBooks:
            txt = txt + name[:len(name)-4] +', '
        txt = txt[:len(txt)-2] + '.'

        uploadWindow = Tk()
        uploadWindow.geometry("500x400")
        uploadWindow.minsize(width= 500, height = 200)
        uploadWindow.title("Upload")
        uploadWindow.configure(bg = 'white')
    

        ltext = Label(uploadWindow, text = txt, fg = "black", bg="white",font = ("Purisa, 13"))
        ltext.pack(side = TOP, expand = YES, padx = 20, pady = 60, fill = BOTH)

        linput = Label(uploadWindow, text = "Write the book name: ", fg = "black", bg="white",font = ("Purisa, 10"))
        linput.pack(side= TOP, expand = YES, padx = 10, pady = 0, fill = BOTH)
        einput = Entry(uploadWindow)
        einput.pack(side= LEFT, expand = YES, padx = 10, pady = [0, 20], fill = BOTH)

        binput = Button(uploadWindow, text = 'Upload', width=20,bg = "#20B2AA", fg ="white", command= lambda: self.Upload_Book(einput.get(), myBooks))
        binput.pack(side= BOTTOM, expand = YES, padx = 10, pady = [0, 20], fill = BOTH)

    

    def Show_My_Books(self):
        myBooks = os.listdir("./books")
        txt = 'Your books:  \n\n'
        for name in myBooks:
            txt = txt + name[:len(name)-4] +', '
        txt = txt[:len(txt)-2] + '.'

        myBookWindow = Tk()
        myBookWindow.geometry("300x200")
        myBookWindow.minsize(width= 300, height = 200)
        myBookWindow.title("My Books")
        myBookWindow.configure(bg = 'white')
    
        ltext = Label(myBookWindow, text = txt, fg = "black", bg="white",font = ("Purisa, 13"))
        ltext.pack(side = TOP, expand = YES, padx = 20, pady = 60, fill = BOTH)

    def About(self):
        messagebox.showinfo("Created by","mvca, nss2, mhco e tmt2")
    
    def Main_Menu(self):
        root = Tk()
        root.geometry('700x400')
        root.minsize(width= 500, height = 300)

        root.title("Library Menu")

        menu = Menu(root)
        menu.configure(relief=GROOVE, borderwidth = 2, bg = '#D3D3D3')
        root.config(menu=menu, bg = 'white')

        filemenu = Menu(menu)
        filemenu.configure(relief=GROOVE, borderwidth = 1, bg = '#D3D3D3')
        menu.add_cascade(label="File", menu=filemenu) 
        filemenu.add_command(label="My books", command=self.Show_My_Books)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=root.quit)

        helpmenu = Menu(menu)
        menu.add_cascade(label="Help", menu=helpmenu)
        helpmenu.add_command(label="About...", command=self.About)

        ltext = Label(root, text = "Select an option: ", fg = "black", bg="white",font = ("Purisa, 16"))
        ltext.pack(side= TOP, expand = YES, padx = 20, pady = 0, fill = BOTH)

        but_Download = Button(root, text = 'Download a Book', width=50 ,bg = "#20B2AA", fg ="white", command= self.Download_Window)
        but_Download.pack(side= TOP, expand = YES, padx = 20, pady = [0, 20], fill = BOTH)
        
        but_Upload = Button(root, text = 'Upload a Book', width=50 ,bg = "#20B2AA", fg ="white", command= self.Upload_Window)
        but_Upload.pack(side= TOP, expand = YES, padx = 20, pady = [0, 20], fill = BOTH)

        but_Upload = Button(root, text = 'Quit', width=50 ,bg = "#20B2AA", fg ="white", command= root.quit)
        but_Upload.pack(side= TOP, expand = YES, padx = 20, pady = [0, 20], fill = BOTH)

def main():
    
    # assert len(sys.argv) == 2
    # #addrServer = input("Insira o endereço de domínio hospedeiro desejado: ")

    # #ipServer = get_ip_from_dns()

    sm = rdt.Rdt()
    # if sys.argv[1].lower() == "--udp":

    #     sm.config_transmitter(('localhost',5000))

    #     sm.send("teste meme so pra ver se vai".encode())
    # elif sys.argv[1].lower() == "--tcp":
    #     pass

    lb = Library(sm)
    mainloop()

if __name__ == "__main__":
    main()