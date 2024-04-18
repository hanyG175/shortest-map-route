
base_url = "https://www.googleapis.com/books/v1/volumes"
import requests

# Making api calls from the google books link

# 1- The main function for making the request but not explicitly called
def get_books(query):
    url = "https://www.googleapis.com/books/v1/volumes"
    params = {
        "q": query,
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print("Error:", response.status_code)
        return None
# 2- A function for getting books by genres if asked by the user
def get_books_by_genre(genre):
    query = f"subject:{genre}"
    items = get_books(query).get("items", [])
    filtered_items = []
    for item in items:
        # Making sure the books are in English...
        if "description" in item["volumeInfo"] and item["volumeInfo"]["description"]:
            if item["volumeInfo"].get("language", "") == "en":
                filtered_items.append(item)
    if filtered_items :
        return filtered_items   

# 3- A function for getting books by authors if asked by the user
def get_books_by_author(author):
    query = f"inauthor:{author}"
    items = get_books(query).get("items", [])
    filtered_items = []
    for item in items:
        if "description" in item["volumeInfo"] and item["volumeInfo"]["description"]:
            if item["volumeInfo"].get("language", "") == "en":
                filtered_items.append(item)
    if filtered_items :
        return filtered_items   

# 4- A function for testing ...
def get_books_by_title(title):
    items = get_books(title).get("items", [])
    filtered_items = []
    latest_published_date = None
    for item in items:
        if "description" in item["volumeInfo"] and item["volumeInfo"]["description"]:
            if item["volumeInfo"].get("language", "") == "en":
                filtered_items.append(item)
                published_date = item["volumeInfo"].get("publishedDate")
                if published_date and (latest_published_date is None or published_date > latest_published_date):
                    latest_published_date = published_date
    if latest_published_date:
        filtered_items = [item for item in filtered_items if item["volumeInfo"].get("publishedDate") == latest_published_date]
    
    if filtered_items :
        return filtered_items
