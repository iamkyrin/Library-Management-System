import sqlite3
from tkinter import *
from tkinter.messagebox import askquestion
from tkinter.ttk import Combobox, Treeview, Style
from tkcalendar import DateEntry
import datetime
def main():
    conn = sqlite3.connect('../data/library.db')
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS Books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    quantity INTEGER NOT NULL)''')
    c.execute('''CREATE TABLE IF NOT EXISTS Borrowed_books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_name TEXT NOT NULL,
    book_id INTEGER NOT NULL,
    borrow_date TEXT NOT NULL,
    return_date TEXT NOT NULL,
    fine REAL)''')
    conn.commit()
    conn.close()

def create_existing_books():
    conn = sqlite3.connect('../data/library.db')
    c = conn.cursor()
    c.execute('''INSERT OR IGNORE INTO Books (id, title, quantity) VALUES (
    NULL, 'Learn Python', 0)''')
    c.execute('''INSERT INTO Books (id, title, quantity) VALUES (
    NULL, 'The Phoenix Project', 100)''')
    c.execute('''INSERT INTO Books (id, title, quantity) VALUES (
    NULL, "The IT Manager's Survival Guide", 20)''')
    c.execute('''INSERT INTO Books (id, title, quantity) VALUES (
    NULL, 'Introduction To Algorithms', 10)''')
    c.execute('''INSERT INTO Books (id, title, quantity) VALUES (
    NULL, 'The Art Of Readable Code', 10)''')
    c.execute('''INSERT INTO Books (id, title, quantity) VALUES (
    NULL, 'SQL Injection', 5)''')
    c.execute('''INSERT INTO Books (id, title, quantity) VALUES (
    NULL, 'Cross Site Scripting', 30)''')
    c.execute('''SELECT id FROM Books WHERE title = "Learn Python"''')
    learn_python_id = c.fetchone()[0]
    c.execute('''INSERT OR IGNORE INTO Borrowed_books (id, student_name, book_id, borrow_date, return_date, fine) VALUES (
    NULL, 'Daniel Faraday', ?, '10/07/2025', '10/25/2025', 0.0)''', (learn_python_id,))
    c.execute('''INSERT INTO Borrowed_books (id, student_name, book_id, borrow_date, return_date, fine) VALUES (
    NULL, 'Jarad Higgins', ?, '10/07/2025', '10/27/2025', 0.0)''', (learn_python_id,))


    conn.commit()
    conn.close()

if __name__ == '__main__':
    main()

def fetch_books():
    conn = sqlite3.connect('../data/library.db')
    c = conn.cursor()
    c.execute('SELECT title FROM Books WHERE quantity > 0')
    data = []
    for row in c.fetchall():
        data.append(row[0])
        print(data)
    return data

def fetch_students():
    conn = sqlite3.connect('../data/library.db')
    c = conn.cursor()
    c.execute('SELECT student_name FROM Borrowed_books')
    data = []
    for row in c.fetchall():
        data.append(row[0])
        print(data)

def fetch_book_quantity():
    conn = sqlite3.connect('../data/library.db')
    c = conn.cursor()
    c.execute('''SELECT quantity FROM Books''')
    data = []
    for row in c.fetchall():
        data.append(row[0])
        print(data)

def fetch_fine_value():
    conn = sqlite3.connect('../data/library.db')
    c = conn.cursor()

    c.execute('''SELECT fine FROM Borrowed_books''')
    data = []
    for row in c.fetchall():
        data.append(row[0])
        print(data)


def add_student():
    conn = sqlite3.connect('../data/library.db')
    c = conn.cursor()

    student_name = entry.get().title()
    book_title = combo.get()
    returnDate = return_date.get()
    borrowDate = borrow_date.get()
    today = datetime.date.today()
    return_date_value = return_date.get_date()


    c.execute('''SELECT id, quantity FROM Books WHERE title = ?''', (book_title,))
    result = c.fetchone()
    book_id = result[0]
    quantity = result[1]


    c.execute('''INSERT INTO Borrowed_books (student_name, book_id, borrow_date, return_date, fine) 
                 VALUES (?, ?, ?, ?, 0.0)''',
              (student_name, book_id, borrowDate, returnDate))


    c.execute('''UPDATE Books SET quantity = ? WHERE title = ?''', (quantity - 1, book_title))


    if return_date_value < today:
        days_overdue = (today - return_date_value).days
        total_fine_value = float(days_overdue * 5)

        c.execute('''UPDATE Borrowed_books SET fine = ? 
                    WHERE student_name = ? AND book_id = ?''',
                  (total_fine_value, student_name, book_id))
        print(f'days overdue: {days_overdue}, total fine value: {total_fine_value}')

    conn.commit()
    conn.close()

    getTreeWorking()
    label_confirmation = Label(frame_left, text='Successfully Added')
    label_confirmation.grid(row=5, column=1)
    entry.delete(0, END)
    combo.delete(0, END)

def delete_student():
    conn = sqlite3.connect('../data/library.db')
    c = conn.cursor()
    prompt_message = askquestion("Confirmation", message="Are you sure you want to delete this student?")
    if prompt_message == "yes":
        student_name = entry.get().title()
        book_id = combo.get()
        c.execute('''DELETE FROM Borrowed_books WHERE student_name = ?''', (student_name,))
        c.execute('''SELECT quantity FROM Books WHERE title = ?''', (book_id,))
        quantity = c.fetchone()[0]
        c.execute('''SELECT quantity FROM Books''')
        test = c.fetchall()
        add_quantity = quantity + 1
        c.execute('''UPDATE Books SET quantity = ? WHERE title = ?''', (add_quantity, book_id))
        conn.commit()
        conn.close()
        getTreeWorking()
        label_delete = Label(frame_left, text='Successfully Deleted')
        label_delete.grid(row=5, column=1)
        entry.delete(0, END)
        combo.delete(0, END)
        print(student_name)
        print(add_quantity)
        print(test)
    else:
        pass

def clear():
    entry.delete(0, END)
    return_date.delete(END)
    borrow_date.delete(END)
    combo.delete(0, END)
    borrow_date.delete(0, END)
    return_date.delete(0, END)
    today = datetime.date.today()
    return_date.set_date(today)
    borrow_date.set_date(today)


def getTreeWorking():
    for item in tree.get_children():
        tree.delete(item)

    conn = sqlite3.connect('../data/library.db')
    c = conn.cursor()


    c.execute('''SELECT Borrowed_books.id, Borrowed_books.student_name, Books.title, 
                        Borrowed_books.borrow_date, Borrowed_books.return_date, Borrowed_books.fine 
                 FROM Borrowed_books 
                 JOIN Books ON Borrowed_books.book_id = Books.id''')

    for row in c.fetchall():
        tree.insert('', 'end', values=row)
    highlight_fines()
    conn.close()

def search_tree():
    search_term = search_entry.get().title()

    # Clear current display
    for item in tree.get_children():
        tree.delete(item)

    conn = sqlite3.connect('../data/library.db')
    c = conn.cursor()
    c.execute('''SELECT Borrowed_books.id, Borrowed_books.student_name, Books.title, 
                        Borrowed_books.borrow_date, Borrowed_books.return_date, Borrowed_books.fine 
                 FROM Borrowed_books 
                 JOIN Books ON Borrowed_books.book_id = Books.id''')

    for row in c.fetchall():
        student_match = search_term in row[1]  # student_name
        book_match = search_term in row[2]  # book title

        if student_match or book_match:
            tree.insert('', 'end', values=row)


def total_borrowed_books():
    conn = sqlite3.connect('../data/library.db')
    c = conn.cursor()
    c.execute('''SELECT student_name FROM Borrowed_books''')
    data = []
    for row in c.fetchall():
        data.append(row[0])
        number_total = len(data)
        print(number_total)
        borrowed_books = Frame(window)
        borrowed_books.grid(row=0, column=1, sticky='ne')

        borrowed_books_label = Label(borrowed_books, font=('Arial', 16, 'bold'), text=f'Total Borrowed Books: {number_total}')

        borrowed_books_label.grid(row=0, column=1)

def return_date_update():
    try:
        borrow_date_value = borrow_date.get_date()
        return_date.config(mindate=borrow_date_value)
    except:
       pass

def highlight_fines():
    for item in tree.get_children():
        values = tree.item(item, 'values')
        if values and float(values[5] or 0) > 0:  # Check fine column (index 5)
            tree.tag_configure('fine', background='red', foreground='white')
            tree.item(item, tags=('fine',))


window = Tk()
window.geometry('1920x1080')
window.title('Student Book Tracker')

label_borrowed_books = Label(window, text='Borrow Books', font=('Arial', 16, 'bold'))
label_borrowed_books.grid(row=0, column=0)


frame_left = Frame(window, bd=2, relief=SUNKEN, pady=120, padx=30)
frame_left.grid(row=1, column=0, sticky='nw')
label = Label(frame_left, text='Student Name:')
label.grid(row=0, column=0)
entry = Entry(frame_left, font=('Arial', 20))
entry.grid(row=0, column=1)


label2 = Label(frame_left, text='Book:')
label2.grid(row=1, column=0)
combo = Combobox(frame_left, font=('Arial', 19), values=fetch_books())
combo.grid(row=1, column=1, padx=20, pady=20)

label3 = Label(frame_left, text='Borrow Date:')
label3.grid(row=2, column=0)
borrow_date = DateEntry(frame_left, date_pattern='mm/dd/yy', mindate=datetime.date.today(), width=50)
borrow_date.grid(row=2, column=1, padx=20, pady=10)
borrow_date.bind("<<DateEntrySelected>>", lambda e: return_date_update())

label4 = Label(frame_left, text='Return Date:')
label4.grid(row=3, column=0)
return_date = DateEntry(frame_left, date_pattern='mm/dd/yy', mindate=datetime.date.today(), width=50)
return_date.grid(row=3, column=1, padx=20, pady=10)


frame_button = Frame(frame_left)
frame_button.grid(row=4, column=1, padx=10, pady=10)
buttonAdd = Button(frame_button, text='Add', bg='green', fg='white', command=add_student)
buttonAdd.grid(row=0, column=1, padx=10, pady=10)
buttonDel = Button(frame_button, text='Delete', bg='red', fg='white', command=delete_student)
buttonDel.grid(row=0, column=2, padx=10, pady=10)
buttonClear = Button(frame_button, text='Clear' , bg='gray', fg='black', command=clear)
buttonClear.grid(row=0, column=3, padx=10, pady=10)


search_frame = Frame(window)
search_frame.grid(row=0, column=1, sticky='ew')

search_label = Label(search_frame, text='Search:')
search_label.grid(row=0, column=0)

search_entry = Entry(search_frame, font=('Arial', 12))
search_entry.grid(row=0, column=1, padx=10)


search_entry.bind('<KeyRelease>', lambda event: search_tree())


total_borrowed_books()
s = Style()
s.theme_use('clam')
s.configure('Treeview.Heading', background="blue", foreground="white")




tree_frame = Frame(window)
tree_frame.grid(row=1, column=1, sticky='ew')
tree = Treeview(tree_frame, columns=("col1", "col2", 'col3', 'col4', 'col5', 'col6'), show="headings", height=30)
tree.grid(row=1, column=1, padx=10, pady=10)
scrollbar = Scrollbar(tree_frame, orient='vertical')
scrollbar.grid(row=1, column=2, sticky='ns', pady=10, padx=10)
scrollbar.config(command=tree.yview)
tree.config(yscrollcommand=scrollbar.set)
tree.column('col1', width=50, stretch=False)   # ID
tree.column('col2', width=150, stretch=False)  # Student
tree.column('col3', width=250, stretch=False)  # Book
tree.column('col4', width=100, stretch=False)  # Borrow Date
tree.column('col5', width=100, stretch=False)  # Return Date
tree.column('col6', width=80, stretch=False)   # Fine
tree.grid(row=1, column=1, padx=10, pady=10)
tree.heading('col1', text='ID')
tree.heading('col2', text='Student')
tree.heading('col3', text='Book')
tree.heading('col4', text='Borrow Date')
tree.heading('col5', text='Return Date')
tree.heading('col6', text='Fine')




fetch_fine_value()
getTreeWorking()
window.mainloop()