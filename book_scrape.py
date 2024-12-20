import requests
from bs4 import BeautifulSoup
import sqlite3


def create_database():
    conn = sqlite3.connect("books.sqlite3")
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS books(
	    title varchar(255) not null,
	    currency varchar(255) not null,
        price int not null     
        );
        """
    )
    conn.commit()
    conn.close()
    
def insert_book(title,currency, price):
    conn = sqlite3.connect("books.sqlite3")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO books (title,currency, price) VALUES (?, ?, ?)", (title, currency, price))
    conn.commit()
    conn.close()



URL = "https://books.toscrape.com/"

def scrape_book(url):
    response = requests.get(url)
    print(response.status_code)
    if response.status_code != 200:
        print(f"Failed to fetch the page, status code: {response.status_code}")
        return
    
    response.encoding = response.apparent_encoding # english bahek ko language lae encode garxa yaha
    # print(response.text) # print data
    
    soup = BeautifulSoup(response.text,"html.parser")
    books = soup.find_all("article",class_= "product_pod")
    # print(books)
    
    for book in books:
        title = book.h3.a["title"]
        price_text = book.find("p",class_="price_color").text
        # print(title,price_text)
        
        currency = price_text[0]
        price = price_text[1:]
        # print(title, currency, price)
        insert_book(title, currency, price)

def delete_table():
        conn = sqlite3.connect("books.sqlite3")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM books;")
        conn.commit()
        conn.close()
        
# delete_table()        
create_database()    
scrape_book(URL)