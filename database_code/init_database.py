import pymysql
from datetime import datetime, timedelta
from get_credentials import *
from main_scraping import *

def clear_database(cursor):
    sql = "DELETE FROM top_comments;"
    cursor.execute(sql)
    sql = "DELETE FROM webtoons;"
    cursor.execute(sql)
    sql = "DELETE FROM users;"
    cursor.execute(sql)
    
u, p =  credentials()

# database connection
connection = pymysql.connect(host="localhost", 
                             port=3306, 
                             user=u, 
                             passwd=p, 
                             database="webtoon_scraping")
cursor = connection.cursor()
clear_database(cursor)

# TODO: Get a random webtoon
webtoon_info = ["7686", "https://www.webtoons.com/en/comedy/fantasy-high/list?title_no=7686", "Fantasy High", "Denassey", "Dimension 20"]
webtoon_id, link, name, artist, author = webtoon_info

sql = "SELECT webtoons.id FROM webtoons WHERE webtoons.id = %s"
cursor.execute(sql, (webtoon_id))

#Insert artist
cursor.execute("SELECT users.is_artist FROM users WHERE users.username = %s", (artist))
result = cursor.fetchone()
print(result)
if result == None:
    cursor.execute("INSERT INTO users (username, is_author, is_artist) VALUES (%s, %s, %s)", (artist, 0, 1))
else:
    cursor.execute("UPDATE users SET is_artist = %s WHERE users.username = %s", (1, artist))
    
#Insert author     
cursor.execute("SELECT users.is_author FROM users WHERE users.username = %s", (author))
result = cursor.fetchone()
print(result)

if result == None:
    cursor.execute("INSERT INTO users (username, is_author, is_artist) VALUES (%s, %s, %s)", (author, 1, 0))
else:
    cursor.execute("UPDATE users SET is_author = %s WHERE users.username = %s", (1, author))

# Get artist_id        
sql = "SELECT users.id FROM users WHERE users.username = %s"
cursor.execute(sql, (artist))
artist_id = cursor.fetchone()[0]   

# Get author_id
sql = "SELECT users.id FROM users WHERE users.username = %s"
cursor.execute(sql, (author))
author_id = cursor.fetchone()[0]  

sql = "INSERT INTO webtoons (id, link, name, id_artist, id_author) VALUES (%s, %s, %s, %s, %s)"
cursor.execute(sql, (webtoon_id, link, name, artist_id, author_id))

# Now, add the top_comments of this webtoon
n_episode = 0

while True:
    new_driver = get_driver()
    try:
        n_episode += 1
        top_comments_info = get_top_comment_info(new_driver, webtoon_id, n_episode)
        
        for comment_info in top_comments_info:
            username, date, content, nb_replies, nb_up, nb_down = comment_info
            
            # check if user in users
            cursor.execute("SELECT users.id FROM users WHERE users.username = %s", (username))
            user_id = cursor.fetchone()
            
            if user_id == None:
                cursor.execute("INSERT INTO users (username, is_author, is_artist) VALUES (%s, %s, %s)", (username, 0, 0))
                cursor.execute("SELECT users.id FROM users WHERE users.username = %s", (username))
                user_id = cursor.fetchone()
            
            user_id = user_id[0]
            
            sql = "INSERT INTO top_comments (id_user, id_webtoon, n_episode, upload_date, content, nb_replies, nb_upvotes, nb_downvotes) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, (user_id, webtoon_id, n_episode, date, content, nb_replies, nb_up, nb_down))
    
    except Exception as e:
        print("We reached the end")
        break

# needed to make the changes to the database official
connection.commit()
connection.close()