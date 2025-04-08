# importing all necessary libraries
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
from datetime import datetime

def get_driver():
    """ Return: a new instance of chrome driver with specific options """
    # create a new instance of chrome options
    chrome_options = Options()
    #chrome_options.add_argument("--headless") # chrome pages are hidden
    chrome_options.add_experimental_option( "prefs", { "profile.managed_default_content_settings.images": 2})
    
    return webdriver.Chrome(chrome_options)

def webtoon_info_to_link(webtoon_id, n_episode):
    """ converts webtoon info to it's link """
    return "https://www.webtoons.com/en/-/-/-/viewer?title_no=" + str(webtoon_id) + "&episode_no=" + str(n_episode)

def accept_cookies(driver):
    """ accept cookies on the page """
    # ensure cookie the element is loaded
    wait = WebDriverWait(driver, 10)
    host_element = wait.until(EC.presence_of_element_located((By.ID, 'cmpwrapper'))) 

    # find the cookie element and refuse it
    button_inside_shadow_root = driver.execute_script('return arguments[0].shadowRoot.querySelector("a.cmpboxbtnno")', host_element)
    button_inside_shadow_root.click()

def date_formater(unformatted_date):
    """  returns a date formated for the sql database """
    date_obj = datetime.strptime(unformatted_date, "%b %d, %Y")
    mysql_date = date_obj.strftime("%Y-%m-%d")
    return mysql_date

def get_top_comment_info(driver, webtoon_id, n_episode):
    """
    scrapes the comments of one webtoon episode
    Args: webtoon info, needed to create it's link
    Return: a list of tuples (username, date, content, nb_replies, nb_upvotes, nb_downvotes)
    """

    link = webtoon_info_to_link(webtoon_id, n_episode)
    driver.get(link)
    accept_cookies(driver)
  
    wait = WebDriverWait(driver, 30)
    visible_comments = wait.until(EC.visibility_of_all_elements_located((By.XPATH, '//ul[@class="wcc_CommentList__list"]//li[@class="wcc_CommentItem__root"]')))
    
    top_auteurs = []
    
    for comment in visible_comments:
        try:
            username = comment.find_element(By.XPATH, './/span[@class="wcc_CommentHeader__name"]').text
            print("username: " + username)
            date = date_formater(comment.find_element(By.XPATH, './/time[@class="wcc_CommentHeader__createdAt"]').text)
            print("date: " + date)
            body = comment.find_elements(By.XPATH, './/div[@class="wcc_TextContent__root"]//p[@class="wcc_TextContent__content"]//span')
            content_box = comment.find_element(By.XPATH, './/p[@class="wcc_TextContent__content"]//span[not(@class)]')
            content = content_box.text
            print("content: " + content)
            nb_replies = comment.find_element(By.XPATH, './/button[@class="wcc_Button__root wcc_ReplyFolderToggle__root"]').text.split()[1]
            print("nb_replies: " + nb_replies)
            nb_upvotes = comment.find_element(By.XPATH, './/div[@class="wcc_CommentReaction__root"]//button[1]').text
            print("nb_upvotes: " + nb_upvotes)
            nb_downvotes = comment.find_element(By.XPATH, './/div[@class="wcc_CommentReaction__root"]//button[2]').text
            print("nb_downvotes: " + nb_downvotes)
            
            if len(body) == 4:
                top_auteurs.append((username, date, content, nb_replies, nb_upvotes, nb_downvotes))
        except:
            pass
    
    driver.quit()
        
    return top_auteurs


def get_top_comments_info(webtoon_id, nb_episode):
    driver = get_driver()
    top_auteurs = []

    
    for n_episode in range(1, nb_episode+1):
        print("episode : ", n_episode)
        link = webtoon_info_to_link(webtoon_id, n_episode)
        driver.get(link)
        
        if n_episode == 1:
            accept_cookies(driver)
    
        wait = WebDriverWait(driver, 20)
        visible_comments = wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'li.wcc_CommentItem__root')))
            
        for comment in visible_comments[:3]:
            try:
                body = comment.find_elements(By.CSS_SELECTOR, 'div.wcc_TextContent__root p.wcc_TextContent__content span')


                if len(body) == 4:
                    username = comment.find_element(By.CSS_SELECTOR, "a.wcc_CommentHeader__name, span.wcc_CommentHeader__name").text
                    date = date_formater(comment.find_element(By.CSS_SELECTOR, 'time.wcc_CommentHeader__createdAt').text)
                    content = comment.find_element(By.XPATH, './/p[@class="wcc_TextContent__content"]//span[not(@class)]').text
                    nb_replies = comment.find_element(By.XPATH, './/button[@class="wcc_Button__root wcc_ReplyFolderToggle__root"]').text.split()[1]
                    nb_upvotes = comment.find_element(By.XPATH, './/div[@class="wcc_CommentReaction__root"]//button[1]').text
                    nb_downvotes = comment.find_element(By.XPATH, './/div[@class="wcc_CommentReaction__root"]//button[2]').text
                    
                    top_auteurs.append((username, date, content, nb_replies, nb_upvotes, nb_downvotes))
                else:
                    break
            except Exception as e:
                print(e)
    
    driver.quit()
        
    return top_auteurs

if __name__ == "__main__":
    start_time = time.time()

    print(get_top_comments_info(2480, 5))

    end_time = time.time()
    execution_time = end_time - start_time
    print("Time taken:", execution_time, "seconds")
