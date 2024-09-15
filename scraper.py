import time
import pyperclip
from dotenv import load_dotenv
import os

# selenium
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

# local
from llm import llm

load_dotenv()

DOWNLOAD_DIR = os.environ['DOWNLOAD_DIR']
PHONE_NUMBER = os.environ['PHONE_NUMBER']


chrome_service = Service(executable_path=os.environ['CHROME_DRIVER_PATH'])
options = Options()
# options.add_argument('--headless=new')
# options.add_argument('--disable-gpu')
options.add_argument('--remote-debugging-port=9222') 
driver = webdriver.Chrome(service=chrome_service, options=options)


buttons = driver.find_element(By.CLASS_NAME, 'artdeco-pagination__pages--number').find_elements(By.CLASS_NAME, 'artdeco-pagination__indicator')
num_buttons = len(buttons)


for i in range(num_buttons):
    if i != 0:
        # in order to get away from stale element error
        buttons = driver.find_element(By.CLASS_NAME, 'artdeco-pagination__pages--number').find_elements(By.CLASS_NAME, 'artdeco-pagination__indicator')
        buttons[i].click()

    job_items = driver.find_elements(By.CLASS_NAME, 'jobs-search-results__list-item')

    for job_item in job_items:
        job_item.click()

        time.sleep(2)  # Adjust the sleep time as needed

        job_description = driver.find_element(By.ID, 'job-details').text
        llm_output = llm(job_description)

        # switch to overleaf
        driver.switch_to.window(driver.window_handles[0])


        # click into editor
        tex_editor = driver.find_element(By.CLASS_NAME, 'cm-line')
        tex_editor.click()


        line_number = 1
        begin_projects_section_line = 1
        end_technical_skills_line = 1
        actions = ActionChains(driver)
        while line_number <= 500:  # Move the cursor until you see \section{Projects}
            # tex_editor = driver.find_elements(By.CLASS_NAME, 'cm-line')[-1] # just to keep DOM refreshed

            # left, right, right, right, down
            actions.key_down(Keys.COMMAND).send_keys(Keys.LEFT).key_up(Keys.COMMAND).perform() # go to beginning of line first
            actions.key_down(Keys.SHIFT).key_down(Keys.COMMAND).send_keys(Keys.RIGHT*2).key_up(Keys.SHIFT).key_up(Keys.COMMAND).perform() # highlight the text
            actions.key_down(Keys.COMMAND).send_keys('c').send_keys(Keys.LEFT).key_up(Keys.COMMAND).perform() # Perform the copy command (CMD + C)
            copied_text = pyperclip.paste()
            if copied_text != "":
                actions.send_keys(Keys.RIGHT)

            if "\\" in copied_text:
                copied_text = copied_text.replace("\\", "")


            if "Projects" in copied_text:
                begin_projects_section_line = line_number
            elif "end" in copied_text and "itemize" in copied_text and begin_projects_section_line > 1:
                end_technical_skills_line = line_number
                actions.send_keys(Keys.DOWN).perform()
                break

            actions.send_keys(Keys.DOWN).perform()
            line_number += 1

        while True:
            actions.key_down(Keys.SHIFT).send_keys(Keys.UP*2).key_up(Keys.SHIFT).perform() # highlight
            actions.key_down(Keys.COMMAND).send_keys('c').key_up(Keys.COMMAND).perform() # Perform the copy command (CMD + C)
            actions.send_keys(Keys.DELETE).perform()

            copied_text = pyperclip.paste()

            if "Projects" in copied_text:
                actions.send_keys(Keys.RETURN*2).perform() # give some space for next projects section
                break

        
        pyperclip.copy(llm_output)
        tex_editor = driver.find_element(By.CLASS_NAME, 'cm-activeLine').click()
        actions.key_down(Keys.COMMAND).send_keys('v').key_up(Keys.COMMAND).perform() 


        # recompile & save as PDF
        recompile_button = driver.find_element(By.CLASS_NAME, 'split-menu-button').click()
        time.sleep(4)

        save_pdf = driver.find_element(By.CLASS_NAME, 'fa-download').click()
        time.sleep(4)
        
        
        # switch back to LinkedIn
        driver.switch_to.window(driver.window_handles[1])
        easy_apply_element = driver.find_element(By.XPATH, "//*[starts-with(@aria-label, 'Easy Apply')]").click()


        # put in phone number
        phone_number_element = driver.find_element(By.XPATH, "//input[@type='text' and contains(@aria-describedby, 'phoneNumber-nationalNumber')]")
        phone_number_element.send_keys(PHONE_NUMBER)

        # click next
        driver.find_element(By.XPATH, "//*[@aria-label='Continue to next step']").click()

        # upload Resume
        # upload_resume_element = driver.find_element(By.XPATH, "//*[starts-with(@aria-label, 'Upload resume button.')]")
        file_input = driver.find_element(By.XPATH, "//input[@type='file']")

        # get most recently downloaded Resume
        downloaded_files = os.listdir(DOWNLOAD_DIR)
        downloaded_files.sort(key=lambda x: os.path.getmtime(os.path.join(DOWNLOAD_DIR, x)), reverse=True)  # sort by time
        latest_file = os.path.join(DOWNLOAD_DIR, downloaded_files[0])  # most recently downloaded file 

        # Full path of the downloaded Resume
        file_input.send_keys(latest_file)

        # Wait to ensure the upload completes
        time.sleep(3)

        # click next
        driver.find_element(By.XPATH, "//*[@aria-label='Continue to next step']").click()


        # allow some time for user to input other fields
        time.sleep(60)

driver.quit()