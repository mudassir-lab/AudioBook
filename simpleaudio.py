import pyttsx3
import PyPDF2
import requests
from tkinter import *
from tkinter import messagebox as m_box

root = Tk()
root.geometry("420x150")
photo = PhotoImage(file='i.png')
root.iconphoto(False,photo)
root.title("Audible")
root.configure(bg='black')
Label(root,text="Welcome",font="Arial 24 bold",fg='white',bg='black',pady=10).grid(column=4)
name = Label(root,text="ENTER URL:",padx=15,fg='white',bg='black')
name.grid(row=1,column=3)
select = Label(root,text="SELECT  VOICE",padx=30,fg='white',bg='black')
select.grid(row=2,column=3)

url = StringVar()
entry1 = Entry(root,textvariable=url,width=30,relief=RIDGE)
entry1.grid(row=1,column=4)
vo = IntVar()

R1 = Radiobutton(root, text="Male", variable=vo, value=0,fg='white',bg='black',selectcolor='black')
R1.grid(row=2,column=4)
R2 = Radiobutton(root, text="Female", variable=vo, value=1,fg='white',bg='black',selectcolor='black')
R2.grid(row=2,column=5)



def run():

    try:  # try getting
        response = requests.get(url.get(), stream=True)  # get web request
    except:  # in case of an error, close the program
        # erm=Label(root, text="There might be an issue with the internet or url.", fg="red", bg='black')
        # erm.grid(row=4,column=4)
        m_box.showerror('Erorr','Enter valid url or check internet connection!!!')
        entry1.delete(0, 'end')
    else:
        if response.status_code != 200:  # 200 means ok, if not close the program
            m_box.showerror('Erorr','Enter Valid Url  !!!')
            entry1.delete(0, 'end')
        else:
            entry1.delete(0, 'end')
            with open("n.pdf", "wb") as pdf:
                for chunk in response.iter_content(chunk_size=1024):
                    # writing one chunk at a time to pdf file
                    if chunk:
                        pdf.write(chunk)

            # file_url = 'http://codex.cs.yale.edu/avi/db-book/db4/slide-dir/ch1-2.pdf'

            book = open('n.pdf', 'rb')
            try:
                pdfReader = PyPDF2.PdfFileReader(book)
            except:
                m_box.showerror('Erorr', ' File is crupted  !!!')
            else:
                pages = pdfReader.numPages

                speaker = pyttsx3.init()
                # rate = speaker.getProperty('rate')
                speaker.setProperty('rate', 150)
                voices = speaker.getProperty('voices')
                speaker.setProperty('voice', voices[vo.get()].id)
                for num in range(0, pages):
                    page = pdfReader.getPage(num)
                    text = page.extractText()
                    speaker.say(text)
                    speaker.runAndWait()

Button(text="Enter",bg="blue",command=run).grid(row=1,column=5,ipadx=10)
root.mainloop()