from selenium import webdriver
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from random import randint
import time, json
import pandas as pd
import streamlit as st

from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager


# Log out of naukri if logged in
# search for any job role (machine learning in this case) and location (India)
# Remove parameters in url (works fine)


# Generate url to navigate pages
def generate_url(index):
    if index == 1:
        return "https://www.naukri.com/machine-learning-jobs-in-india"
    return f"https://www.naukri.com/machine-learning-jobs-in-india-{index}"


def setup_driver():   
    options = webdriver.ChromeOptions()
    options.headless = True
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=options)


def scroll_page(driver, scrolls=4):
    for _ in range(scrolls):  
        driver.execute_script("window.scrollBy(0, 800);")
        time.sleep(1.5)


def get_job_cards(driver):
    try:
        product_cards = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, "section.styles_job-desc-container__txpYf")
        )
    )
        return product_cards
    except:
        print("No products found")
        driver.quit()
        exit()


def extract_job_data(product_cards):
    data = []
    text = ""

    # find years of experience
    # experience_container_css = ".styles_jhc__exp__k_giM"
    xpath_selector = "//div[@class='styles_jhc__exp__k_giM']/span"

    for card in product_cards:
        try: 
            job_title = card.find_element(By.XPATH, "//header//h1").text.strip()
            text = text + " " + job_title
        except: 
            job_title = "N/A"

        try: 
            experience_element = card.find_element(By.XPATH, xpath_selector)
            experience_text = experience_element.text
            text = text + " " + experience_text
        except: 
            experience_text = "N/A"

        try: 
            salary_element = card.find_element(By.XPATH, "//div[@class='styles_jhc__salary__jdfEC']/span")
            salary = salary_element.text
            text = text + " " + salary
        except:
            salary = "N/A"

        try: 
            location_element = card.find_element(By.XPATH, "//div[@class='styles_jhc__loc___Du2H']/span/a")
            location = location_element.text
            text = text + " " + location
        except:
            location = "N/A"

        try: 
            job_description = card.find_element(By.CSS_SELECTOR, "div.styles_JDC__dang-inner-html__h0K4t").text 
            text = text + " " + job_description
        except: 
            job_description = "N/A"

        try: 
            other_details = card.find_element(By.CSS_SELECTOR, "div.styles_other-details__oEN4O").text 
            text = text + " " + other_details
        except: 
            other_details = "N/A"

        try: 
            education = card.find_element(By.CSS_SELECTOR, "div.styles_education__KXFkO").text 
            text = text + " " + education
        except: 
            education = "N/A"
        
        try: 
            skills = card.find_element(By.CSS_SELECTOR, "div.styles_key-skill__GIPn_").text
            text = text + " " + skills
        except: 
            skills = "N/A"


        data.append({
            "job_title" :job_title,
            "experience": experience_text,
            "salary": salary,
            "location": location,
            "job_description": job_description,
            "other_details": other_details,
            "education": education,
            "skills": skills
        })

        return text

# class JobData(BaseModel):
#     '''Job details'''
#     job_title: str = Field(description="Title of job"),
#     experience_text: str = Field(description="Experience that applicant must have"),
#     salary: str = Field(description="Salary offered for this role"),
#     location: str = Field(description="Location of the company"),
#     job_description: str= Field(),
#     other_details: str = Field(),
#     education: str = Field(description="Minimum education"),
#     skills: list = Field()