# from cProfile import label
# import ttkthemes as tt
# import tkinter as tk
from ctypes import windll
from io import BytesIO
import sys
sys.path.append("C:\\Users\\LENOVO\\Code\\AI\\ES_Project")
from Logic.GoogleBooksApiCall import *
from PIL import Image, ImageTk


# def get_name():
#     book = entry.get()
#     results = get_books_by_title(book)
#     for r in results:
#         print("Title:", r["volumeInfo"]["title"])
#         print("Authors:", r["volumeInfo"].get("authors", ["Unknown"]))
#         print("Published Date:", r["volumeInfo"].get("publishedDate", "Unknown"))
#         print("Description:", r["volumeInfo"].get("description", "No description available"))
#         print("-------------------")
        
# # Set DPI (dots per inch) awareness
if windll.shcore:
    windll.shcore.SetProcessDpiAwareness(1)


import tkinter as tk

# Sample book data (replace with your actual data source or logic)
books = {
    "Fantasy": [
        {"title": "The Lord of the Rings", "author": "J.R.R. Tolkien"},
        {"title": "A Song of Ice and Fire", "author": "George R.R. Martin"}
    ],
    "Mystery": [
        {"title": "And Then There Were None", "author": "Agatha Christie"},
        {"title": "The Murder on the Orient Express", "author": "Agatha Christie"}
    ],
    "Science Fiction": [
        {"title": "Dune", "author": "Frank Herbert"},
        {"title": "Project Hail Mary", "author": "Andy Weir"}
    ]
}

def recommend_books():
    genre = genre_var.get()
    if genre:
        recommended_books = books[genre]
        recommendation_text.set(f"Based on your selection, here are some recommendations:\n")
        for book in recommended_books:
            recommendation_text.set(recommendation_text.get() + f"- {book['title']} by {book['author']}\n")

# Initialize the Tkinter interface
root = tk.Tk()
root.title("Book Recommendation Expert System")
window_width = 800
window_height = 800
root.geometry(f"{window_width}x{window_height}")
# Genre selection label and radio buttons:
genre_label = tk.Label(root, text="Select your preferred genre:")
genre_label.pack()

genre_var = tk.StringVar(root)  # To store the selected genre

genre_fantasy = tk.Radiobutton(root, text="Fantasy", variable=genre_var, value="Fantasy")
genre_fantasy.pack()

genre_mystery = tk.Radiobutton(root, text="Mystery", variable=genre_var, value="Mystery")
genre_mystery.pack()

genre_scifi = tk.Radiobutton(root, text="Science Fiction", variable=genre_var, value="Science Fiction")
genre_scifi.pack()

# Recommendation button
recommend_button = tk.Button(root, text="Recommend Books", command=recommend_books)
recommend_button.pack()

# Recommendation text box
recommendation_text = tk.StringVar(root)
recommendation_label = tk.Label(root, text="Recommended Books:")
recommendation_label.pack()

# recommendation_display = tk.Text(root, height=10, width=50, state="disabled")
# recommendation_display.config(font=("Arial", 12))
# recommendation_display.insert(tk.END, recommendation_text.get())
# recommendation_display.pack()


# frame = tk.Frame(root,width=800, height=400, bd=1, relief="solid" ,background="brown")
# frame.pack(padx=10, pady=10)
# entry = tk.Entry(frame, width=52 )
# entry.pack( padx=10, pady=10)
# button_add = tk.Button(frame, text="Search book", width=25 , height= 1)
# button_add.pack( padx=10, pady=10)
def load_cards():
    # Clear existing cards
    for card in card_frames:
        card.destroy()
    
    # Fetch data from the API
    books = get_books_by_genre("Fiction")
    i=0
    for book in books:
        
        card_frame = tk.Frame(root, relief=tk.RAISED, borderwidth=2, width=200,height=100)
        card_frame.pack(side=tk.LEFT, padx=10, pady=10)
        image_url = book["volumeInfo"].get("imageLinks")['thumbnail']
        if image_url:
            try:
                image_response = requests.get(image_url)
                if image_response.status_code == 200:
                    image_data = BytesIO(image_response.content)
                    cover_image = Image.open(image_data)
                    cover_photo = ImageTk.PhotoImage(cover_image)
                    cover_label = tk.Label(card_frame, image=cover_photo)
                    cover_label.image = cover_photo  # Keep a reference to prevent garbage collection
                    cover_label.pack(pady=5)
            except Exception as e:
                print("Error loading image:", e)
        title_label = tk.Label(card_frame, text=book["volumeInfo"].get("title", "Unknown Title"), font=("Arial", 12, "bold"),wraplength=180)
        title_label.pack(pady=5)
        
        author_label = tk.Label(card_frame, text="Author: " + ", ".join(book["volumeInfo"].get("authors", ["Unknown Author"])), font=("Arial", 10),wraplength=180)
        author_label.pack()
        
        rating_label = tk.Label(card_frame, text="Rating: " + str(book["volumeInfo"].get("averageRating", "N/A")), font=("Arial", 10))
        rating_label.pack()
        
        categories_label = tk.Label(card_frame, text="Categories: " + ", ".join(book["volumeInfo"].get("categories", ["N/A"])), font=("Arial", 10))
        categories_label.pack()
        
        publication_year_label = tk.Label(card_frame, text="Publication Date: " + str(book["volumeInfo"].get("publishedDate", "Not Assigned")), font=("Arial", 10))
        publication_year_label.pack()
            
        description_text = book["volumeInfo"].get("description", "No description available")
        truncated_description = description_text[:100] + "..." if len(description_text) > 100 else description_text
        description_label = tk.Label(card_frame, text="Description: " + truncated_description, wraplength=200, justify=tk.LEFT)        
        description_label.pack(pady=5)

        
                                
        card_frames.append(card_frame)
        i+=1
        if i == 10:
            break
        elif (i + 1) % 3 == 0:  # Adjust 3 to the number of cards you want per row
                tk.Frame(root, height=1, bd=1, relief=tk.SUNKEN).pack(fill=tk.X, padx=10, pady=5)  # Spacer between rows

# Create tkinter root
root.title("Book Cards")

# Create a list to store card frames
card_frames = []

# Add a button to load cards
load_button = tk.Button(root, text="Load Cards", command=load_cards)
load_button.pack( padx=10, pady=10)

# Run the tkinter event loop

root.mainloop()
