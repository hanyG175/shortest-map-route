import sys
sys.path.append("C:\\Users\\LENOVO\\Code\\AI\\ES_Project")
sys.path.append("C:\\Users\\LENOVO\\Code\\AI\\ES_Project\\Logic\\aima1")
from aima1.utils import *
from aima1.logic import *

from Logic.GoogleBooksApiCall import *

book_params = ["title", "genre", "author", "year", "rating"]

facts= [
expr("BookTitle(B16,Hamlet)"),
expr("BookGenre(B16,Drama)"),
expr("BookAuthor(B16,WilliamShakespeare)"),
expr("BookRating(B16,High)"),
expr("BookYear(B16,Y1603)"),

expr("BookTitle(B17,AStreetcarNamedDesire)"),
expr("BookGenre(B17,Drama)"),
expr("BookAuthor(B17,TennesseeWilliams)"),
expr("BookRating(B17,High)"),
expr("BookYear(B17,Y1947)"),

expr("BookTitle(B18,DeathofaSalesman)"),
expr("BookGenre(B18,Drama)"),
expr("BookAuthor(B18,ArthurMiller)"),
expr("BookRating(B18,High)"),
expr("BookYear(B18,Y1949)"),

expr("BookTitle(B19,TheCrucible)"),
expr("BookGenre(B19,Drama)"),
expr("BookAuthor(B19,ArthurMiller)"),
expr("BookRating(B19,High)"),
expr("BookYear(B19,Y1953)"),

expr("BookTitle(B20,RomeoandJuliet)"),
expr("BookGenre(B20,Drama)"),
expr("BookAuthor(B20,WilliamShakespeare)"),
expr("BookRating(B20,High)"),
expr("BookYear(B20,Y1597)"),

expr("BookTitle(B1,TreasureIsland)"),
expr("BookGenre(B1,Adventure)"),
expr("BookAuthor(B1,RobertLouisStevenson)"),
expr("BookRating(B1,High)"),
expr("BookYear(B1,Y1883)"),

expr("BookTitle(B2,TheHobbit)"),
expr("BookGenre(B2,Adventure)"),
expr("BookAuthor(B2,JRRTolkien)"),
expr("BookRating(B2,High)"),
expr("BookYear(B2,Y1937)"),

expr("BookTitle(B3,Dune)"),
expr("BookGenre(B3,ScienceFiction)"),
expr("BookAuthor(B3,FrankHerbert)"),
expr("BookRating(B3,High)"),
expr("BookYear(B3,Y1965)"),

expr("BookTitle(B4,TheAdventuresofSherlockHolmes)"),
expr("BookGenre(B4,Mystery)"),
expr("BookAuthor(B4,ArthurConanDoyle)"),
expr("BookRating(B4,High)"),
expr("BookYear(B4,Y1892)"),

expr("BookTitle(B5,1984)"),
expr("BookGenre(B5,Fiction)"),
expr("BookAuthor(B5,GeorgeOrwell)"),
expr("BookRating(B5,High)"),
expr("BookYear(B5,Y1949)"),

expr("BookTitle(B6,TheLostWorld)"),
expr("BookGenre(B6,Adventure)"),
expr("BookAuthor(B6,ArthurConanDoyle)"),
expr("BookRating(B6,Low)"),
expr("BookYear(B6,Y1912)"),

expr("BookTitle(B7,TheGreatGatsby)"),
expr("BookGenre(B7,Fiction)"),
expr("BookAuthor(B7,FScottFitzgerald)"),
expr("BookRating(B7,High)"),
expr("BookYear(B7,Y1925)"),

expr("BookTitle(B8,Neuromancer)"),
expr("BookGenre(B8,ScienceFiction)"),
expr("BookAuthor(B8,WilliamGibson)"),
expr("BookRating(B8,Low)"),
expr("BookYear(B8,Y1984)"),

expr("BookTitle(B9,TheHoundoftheBaskervilles)"),
expr("BookGenre(B9,Mystery)"),
expr("BookAuthor(B9,ArthurConanDoyle)"),
expr("BookRating(B9,High)"),
expr("BookYear(B9,Y1902)"),

expr("BookTitle(B10,ToKillaMockingbird)"),
expr("BookGenre(B10,Fiction)"),
expr("BookAuthor(B10,HarperLee)"),
expr("BookRating(B10,High)"),
expr("BookYear(B10,Y1960)"),

expr("BookTitle(B11,JurassicPark)"),
expr("BookGenre(B11,ScienceFiction)"),
expr("BookAuthor(B11,MichaelCrichton)"),
expr("BookRating(B11,High)"),
expr("BookYear(B11,Y1990)"),

expr("BookTitle(B12,TheAdventuresofTomSawyer)"),
expr("BookGenre(B12,Adventure)"),
expr("BookAuthor(B12,MarkTwain)"),
expr("BookRating(B12,Low)"),
expr("BookYear(B12,Y1876)"),

expr("BookTitle(B13,GoneGirl)"),
expr("BookGenre(B13,Mystery)"),
expr("BookAuthor(B13,GillianFlynn)"),
expr("BookRating(B13,High)"),
expr("BookYear(B13,Y2012)"),

expr("BookTitle(B14,BraveNewWorld)"),
expr("BookGenre(B14,ScienceFiction)"),
expr("BookAuthor(B14,AldousHuxley)"),
expr("BookRating(B14,High)"),
expr("BookYear(B14,Y1932)"),

expr("BookTitle(B15,TheDaVinciCode)"),
expr("BookGenre(B15,Mystery)"),
expr("BookAuthor(B15,DanBrown)"),
expr("BookRating(B15,Low)"),
expr("BookYear(B15,Y2003)")
    ]
rules = [
    #rules for making the books different from each other
    expr("Different(x,y) ==> Different(y,x)"),
    expr("BookTitle(book,title) & BookTitle(book1,title1) & Different(book1,book) ==> DifferentBook(book,book1)"),
    expr("DifferentBook(x,y) ==> DifferentBook(y,x)"),

    #Recommendation rules :
    expr("BookGenre(book,genre) & UserLikesGenre(genre) ==> Recommend(book)"),#recommend books from preferred Genre.
    expr("BookAuthor(book,author) & UserLikesAuthor(author) ==> Recommend(book)"),#recommend books from preferred Author.
    expr("BookRating(book,rating) & UserLikesRating(rating) ==> Recommend(book)"),#recommend books from minimum Rating range.
    expr("BookYear(book,year) & UserLikesYear(year) ==> Recommend(book)"),#recommend books from a specific Year range.

    expr("HasRead(book,title) & BookAuthor(book,author) & BookAuthor(book2,author) & DifferentBook(book,book2) ==> Recommend(book2)"), #recommend books from the same Author.
    expr("HasRead(book,title) & BookGenre(book,genre) & BookGenre(book2,genre) ==> Recommend(book2)"), #recommend books from the same Genre.
    ]

kb = FolKB(facts+rules)

def infer_books(author = "",genres = None ,rating = None,year = None):
    
    # Agenda :
    agenda = []
    
    # Adding the user preferences...
    if genres:
        for genre in genres:
            agenda.append(expr(f"UserLikesGenre({genre})")) 
    if author:
        agenda.append(expr(f"UserLikesAuthor({author})"))
    if rating:
        agenda.append(expr(f"UserLikesRating({rating})"))
    if year:
        agenda.append(expr(f"UserLikesYear(Y{year})"))
    # Working Memory
    memory = []
    seen = set() 
    while agenda:
        like = agenda.pop()
        if like in seen:
            continue
        seen.add(like)
        if fol_fc_ask(kb,like):
            memory.append(like)
        
        type = str(like.op).removeprefix("UserLikes")
        if type in seen:
            continue
        seen.add(type)
        for rule in rules:
            if type in str(rule):
                memory.append(rule)
                
    
    new_kb = FolKB(memory + facts)
    books = list(fol_bc_ask(new_kb,expr("Recommend(book)")))
    recommendations = []
    
    b = "" # used to avoid recommending the same book twice
    for book in books:
        #this line iterates over the inferred results (Book IDs) and prints the book names according to the ID
        if b ==  book[Symbol("book")]:
            continue
        recommendations.append(list(fol_bc_ask(kb,expr(f"BookTitle({book[Symbol("book")]},x)")))[0][Symbol("x")])
        b = book[Symbol("book")]
        
    return recommendations
    
