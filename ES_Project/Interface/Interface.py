from io import BytesIO
import sys
sys.path.append("C:\\Users\\LENOVO\\Code\\AI\\ES_Project")
sys.path.append("C:\\Users\\LENOVO\\Code\\AI\\ES_Project\\Logic")
from Logic.GoogleBooksApiCall import *
from PIL import Image, ImageTk
import Logic.aima1
from Logic.ProjectLogic import infer_books


from ctypes import windll
import tkinter as tk
from tkinter import ttk  # for nicer widgets
if windll.shcore:
    windll.shcore.SetProcessDpiAwareness(1)
class BookRecommendationSystem(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('Book Recommendation System')
        self.geometry('1920x1080')  # Increased width to better fit the grid of books

        # Top frame
        self.top_frame = tk.Frame(self, height=200, bg='#eeeeee')
        self.top_frame.pack(fill=tk.X)
        self.top_frame.pack_propagate(False)  # Prevents the frame from resizing to fit its contents

        # Bottom frame
        self.bottom_frame = tk.Frame(self, bg='light blue')
        self.bottom_frame.pack(fill=tk.BOTH, expand=True)

        # Canvas and scrollbar setup as before
        self.canvas = tk.Canvas(self.bottom_frame)
        self.scrollbar = ttk.Scrollbar(self.bottom_frame, orient="vertical", command=self.canvas.yview)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Binding the configure event of the canvas with a function
        self.canvas.bind('<Configure>', self.on_configure)

        # Placeholder for genres, replace with actual genres you want to include
        self.genres = ["Adventure","Fiction","Romance","Mystery","Thrillers","Science","History","Horror","Religion","Poetry","Drama","Comedy","Cooking"]

        # Frame for book cards
        self.cards_frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.cards_frame, anchor='nw')

        # Setup options with checkboxes and other widgets
        self.setup_options()

        # Function to add book cards to the grid      
    def setup_options(self):
        # Search section
        search_frame = tk.LabelFrame(self.top_frame, text="Any Favourite Authors?", bg='#eeeeee')
        search_frame.grid(row=0, column=0, padx=10, pady=5, sticky="nw")

        self.search_var = tk.StringVar()
        tk.Entry(search_frame, textvariable=self.search_var, width=50).pack(side=tk.LEFT, padx=5)
        tk.Button(search_frame, text='Search', command=self.on_search).pack(side=tk.LEFT, padx=5)

        # Rating selection section
        rating_frame = tk.LabelFrame(self.top_frame, text="Rating", bg='#eeeeee')
        rating_frame.grid(row=1, column=1, padx=10, pady=5, sticky="nw")

        self.rating_var = tk.DoubleVar()
        tk.Scale(rating_frame, from_=0, to=5, orient='horizontal', variable=self.rating_var).pack(fill=tk.X, padx=5)
        self.rating_label = tk.Label(rating_frame, text="Select minimum rating")
        self.rating_label.pack(pady=5)
        self.rating_var.trace("w", self.update_rating_label)

        # Publication year selection
        year_frame = tk.LabelFrame(self.top_frame, text="Publication Year", bg='#eeeeee')
        year_frame.grid(row=1, column=3, padx=10, pady=5, sticky="nw")

        self.year_var = tk.IntVar()
        current_year = 2024  # Replace with the current year retrieved dynamically if needed
        ttk.Combobox(year_frame, textvariable=self.year_var, values=list(map(str,range(1900, current_year+1)))).pack(fill=tk.X, padx=5,pady=10)
        
        # Genre selection section
        genre_frame = tk.LabelFrame(self.top_frame, text="Genres", bg='#eeeeee')
        genre_frame.grid(row=1, column=0, padx=10, pady=5, sticky="nw")

        self.genre_vars = {}
        for genre in self.genres:
            self.genre_vars[genre] = tk.BooleanVar()
            cb = tk.Checkbutton(genre_frame, text=genre, variable=self.genre_vars[genre], bg='#eeeeee')
            cb.grid(row=1, column=self.genres.index(genre), sticky='w', padx=10, pady=10)

        # Add more filtering options here using a similar pattern
        b = tk.Button(self.top_frame, text='Load', command=self.on_search)
        b.grid(row=2, column=0, padx=10, pady=5, sticky="nw")
    def update_rating_label(self, *args):
        rating = self.rating_var.get()
        self.rating_label.config(text=f'Select minimum rating: {rating:.1f}')
    def on_configure(self, event):
        # Set the scroll region to encompass the inner frame
        self.canvas.configure(scrollregion=self.canvas.bbox('all'))
    def add_book_cards(self,books):
        # Determine columns for grid layout
        columns = 7
        for i in range(len(books)):
            book = books[i]
            row = i // columns
            column = i % columns
            frame = tk.Frame(self.cards_frame, bg='white', borderwidth=1, relief='sunken')
            
            image_url = book["volumeInfo"].get("imageLinks")['thumbnail']
            if image_url:
                try:
                    image_response = requests.get(image_url)
                    if image_response.status_code == 200:
                        image_data = BytesIO(image_response.content)
                        cover_image = Image.open(image_data)
                        cover_photo = ImageTk.PhotoImage(cover_image)
                        cover_label = tk.Label(frame, image=cover_photo)
                        cover_label.image = cover_photo  # Keep a reference to prevent garbage collection
                        cover_label.pack(pady=5)
                except Exception as e:
                    print("Error loading image:", e)
            title = book["volumeInfo"].get("title", "Unknown Title")
            trruncated_title = description_text[:100] + "..." if len(title) > 100 else title
            title_label = tk.Label(frame, text=trruncated_title, font=("Arial", 12, "bold"),wraplength=200,bg='white',width=20)
            title_label.pack(pady=5)
            
            author_label = tk.Label(frame, text="Author: " + ", ".join(book["volumeInfo"].get("authors", ["Unknown Author"])), font=("Arial", 10),bg='white',wraplength=200)
            author_label.pack()
            
            rating_label = tk.Label(frame, text="Rating: " + str(book["volumeInfo"].get("averageRating", 0.0)), bg='white',font=("Arial", 10))
            rating_label.pack()
            
            categories_label = tk.Label(frame, text="Genres: " + ", ".join(book["volumeInfo"].get("categories", ["N/A"])),bg='white', font=("Arial", 10))
            categories_label.pack()
            
            publication_year_label = tk.Label(frame, text="Publication Date: " + str(book["volumeInfo"].get("publishedDate", 0)),bg='white', font=("Arial", 10))
            publication_year_label.pack()
                
            description_text = book["volumeInfo"].get("description", "No description available")
            truncated_description = description_text[:150] + "..." if len(description_text) > 100 else description_text
            description_label = tk.Label(frame, text="Description: " + truncated_description, wraplength=230,bg='white', justify=tk.LEFT)        
            description_label.pack()
                
            frame.grid(row=row, column=column, sticky='nsew', padx=10, pady=10)
            self.cards_frame.grid_columnconfigure(column, weight=1)

        # This is used to ensure that the card frames do not shrink or expand
        # beyond what's required by the label dimensions
        self.cards_frame.pack_propagate(False)
    def clear_book_cards(self):
        # Remove all the book cards from the cards_frame
        for widget in self.cards_frame.winfo_children():
            widget.destroy()
    def on_search(self):
        self.clear_book_cards()
        # Getting user input:
        author = self.search_var.get()
        selected_genres = [genre for genre, var in self.genre_vars.items() if var.get()]
        min_rating = self.rating_var.get()
        year = self.year_var.get()
        print(author,selected_genres,min_rating,year)
        books = infer_books(author,selected_genres)
        
        if year: 
            if not books:
                for y in range(year,2025):
                    b = infer_books(year=str(y))
                    if b :
                        for book in b:
                            books.append(book)
            # else:
            #     for book in books:
            #         if int(book.get("publishedDate")[0:4]) <= year:
            #             books.remove(book)
            
        if min_rating:
            if not books:
                if min_rating >= 4.0:
                    b = infer_books(rating="High")
                else:
                    b = infer_books(rating="Low") + infer_books(rating="High")
                if b :
                    for book in b:
                        books.append(book)
            # else:
            #     for book in books:
            #         if float(book) <= min_rating:
            #             books.remove(book)
        
        google_books =  [] 
        for book in books:
            google_books.append(get_books_by_title(str(book))[0])
        self.add_book_cards(google_books)
        

if __name__ == "__main__":
    app = BookRecommendationSystem()
    app.mainloop()