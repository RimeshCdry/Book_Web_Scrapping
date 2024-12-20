import requests
from bs4 import BeautifulSoup
import sqlite3

# install git
# create repository in github

# go to gut bash
# git config --global user.name "Rimesh Chaudhary"
# git config --global user.email "rimeshcdry45@gmail.com"

# git init
# git status
# git diff
# git add .
# git commit -m "Your message"
# copy paste git code from github

# 1. git add .
# 2. git commit -m "Your message"
# 3. git push origin


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

page_no = 1

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