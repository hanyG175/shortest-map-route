from aima1.utils import *
from aima1.logic import *

book_params = ["title", "genre", "author", "year", "rating"]

rules = [
    #rules for making the books different from each other
    expr("Different(x,y) ==> Different(y,x)"),
    expr("BookTitle(book,title) & BookTitle(book1,title1) & Different(book1,book) ==> DifferentBook(book,book1)"),
    expr("DifferentBook(x,y) ==> DifferentBook(y,x)"),
    
    #Recommendation rules :
    
    expr("BookGenre(book,genre) & UserLikes(genre) ==> Recommend(book)"),#recommend books from preferred Genre.
    expr("BookAuthor(book,author) & UserLikes(author) ==> Recommend(book)"),#recommend books from preferred Author.
    expr("BookRating(book,rating) & UserLikesRating(rating) ==> Recommend(book)"),#recommend books from minimum Rating range.
    expr("BookYear(book,year) & UserLikesYear(year) ==> Recommend(book)"),#recommend books from a specific Year range.
    expr("HasRead(book,title) & BookAuthor(book,author) & BookAuthor(book2,author) & DifferentBook(book,book2) ==> Recommend(book2)"), #recommend books from the same Author.
    expr("HasRead(book,title) & BookGenre(book,genre) & BookGenre(book2,genre) ==> Recommend(book2)"), #recommend books from the same Genre.
    

]
#Facts (database) are going to come from google books api
facts = [
    #example of structured book parameters with ID = B1:
    expr("BookTitle(B1,ToKillaMockingbird)"),
    expr("BookGenre(B1,Fiction)"),
    expr("BookAuthor(B1,HarperLee)"),
    expr("BookRating(B1,High)"),
    expr("BookYear(B1,New)"),
    
    #example of structured book parameters with ID = B2:
    expr("BookAuthor(B2,HarperLee)"),
    expr("BookTitle(B2,Hany)"),    
    
    #differentiating books:
    expr("DifferentBook(B2,B1)"),

]

kb = FolKB(rules+facts)

#this is the facts that the user inserts, exp: UserLikes(Fantasy)
kb.tell(expr("HasRead(B1,ToKillaMockingbird)"))


for book in list(fol_fc_ask(kb,expr("Recommend(book)"))):
    #this line iterates over the inferred results (Book ID's) and prints the book names according to the ID
    print("Your recommended book is: ",list(fol_bc_ask(kb,expr(f"BookTitle({book[Symbol("book")]},x)")))[0][Symbol("x")])
