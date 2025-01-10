from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time, random

username = input('username: ')
password = input('password: ')
replacement = input('text to replace comments with: ')

print('\nAttempting to delete comments. Please note that it will take a while to avoid rate limiting.')

global timer
timer = 2
browser = webdriver.Chrome()
actions = ActionChains(browser)

already_edited = lambda comment : comment.find_element(By.CLASS_NAME, 'usertext-body').text == replacement
click_child = lambda parent, selector : parent.find_element(By.CSS_SELECTOR, selector).click()

def comments_exist():
  return len(browser.find_elements(By.CLASS_NAME, 'comment')) > 0

def unedited_comments_exist():
  return any([not already_edited(comment) for comment in browser.find_elements(By.CLASS_NAME, 'comment')])

def posts_exist():
  return len(browser.find_elements(By.CLASS_NAME, 'link')) > 0

def try_click(btn, selector=None, tries=1, max_tries=3):
  global timer

  try:
    if selector is not None:
      click_child(btn, selector)
    else:
      btn.click()
    
    time.sleep(timer + random.random())
    
  except Exception as e:
    print(f"Request failed, slowing down ({tries}/{max_tries} tries on this button)")
    
    if tries < max_tries:
      timer += 1
      try_click(btn, selector=selector, tries=tries+1)
      
    else:
      print("Failed to click the button, you're probably being rate limited. Try again later.")
      exit()

def delete_text(field):
  field.click()
  actions.key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL).perform()
  field.send_keys(Keys.BACKSPACE)

def edit_comments():
  for comment in browser.find_elements(By.CLASS_NAME, 'comment'):
    if already_edited(comment):
      continue

    click_child(comment, 'a.edit-usertext')
    textbox = comment.find_element(By.TAG_NAME, 'textarea')
    delete_text(textbox)
    textbox.send_keys(replacement)
    try_click(comment, '.save')

def delete_items():
  for btn in browser.find_elements(By.CLASS_NAME, 'del-button'):
    click_child(btn, 'a.togglebutton')
    try_click(btn, 'a.yes')
    
def delete_page():
  while unedited_comments_exist():
    edit_comments()
    browser.refresh()
  
  time.sleep(timer)
  
  delete_items()
  browser.refresh()
  time.sleep(timer)

browser.get(f'https://old.reddit.com/login/?dest=https%3A%2F%2Fold.reddit.com%2Fuser%2F{username}%2Fcomments%2F')

time.sleep(timer)

username_input = browser.find_element(By.ID, 'login-username')
username_input.send_keys(username)
password_input = browser.find_element(By.ID, 'login-password')
password_input.send_keys(password)
password_input.send_keys(Keys.RETURN)

time.sleep(timer)
    
while comments_exist():
  try:
    while unedited_comments_exist():
      edit_comments()
      browser.refresh()
    
    time.sleep(timer)
    
    delete_items()
    browser.refresh()
    time.sleep(timer)
    
  except Exception as e:
    print("Ran into an error. Refreshing the page and trying again.")
    browser.refresh()
    
browser.get(f"https://old.reddit.com/user/{username}/submitted/")

while posts_exist():
  try:
    delete_items()
    browser.refresh()
    time.sleep(timer)
    
  except Exception as e:
    print("Ran into an error. Refreshing the page and trying again.")
    browser.refresh()
    
browser.quit()

print("Done!\n")
print(""" \
It's possible that anti-bot measures ended the script early, so check in a few minutes \
to see that the post history has actually been removed. If there's comments left over, \
just run the script again.
""")
