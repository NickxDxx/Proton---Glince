import time
from time import sleep
import random
import cv2
import sqlite3
from PIL import Image
import numpy as np
from datetime import datetime
import csv
from selenium import webdriver
from io import BytesIO
from random import uniform
from colorlog import ColoredFormatter
import logging
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

from twocaptcha import TwoCaptcha
import os
import sys





script_dir = os.path.dirname(os.path.abspath(__file__))
folder_name = "Database"
folder_path = os.path.join(script_dir, folder_name)
os.makedirs(folder_path, exist_ok=True)
csv_file_path = os.path.join(folder_path, "Proton Mail.csv")

def browser_config( us = False, al = False):
    options = webdriver.ChromeOptions()
    if us:
        HOSTNAME = "al.smartproxy.com"
        PORT = '10000'
        proxy_str = '{hostname}:{port}'.format(hostname=HOSTNAME, port=PORT)
        options.add_argument('--proxy-server={}'.format(proxy_str))
    if al:
        HOSTNAME = "al.smartproxy.com"
        PORT = '33000'
        proxy_str = '{hostname}:{port}'.format(hostname=HOSTNAME, port=PORT)
        options.add_argument('--proxy-server={}'.format(proxy_str))

    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument(("--enable-popup-blocking"))
    options.add_experimental_option("useAutomationExtension", False)
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    # options.add_argument(f"--user-agent={user_agent_chrome.random}")
    # options.add_experimental_option("excludeSwitches", ['enable-automation'])
    # options.add_experimental_option('useAutomationExtension', False)
    browser = webdriver.Chrome(options=options)
    browser.maximize_window()
    return browser, al, us

def create_logger(name):
    formatter = ColoredFormatter(
    "%(log_color)s%(levelname)s: %(log_color)s%(asctime)s: %(blue)s%(message)-10s  ",
    datefmt=None,
    reset=True,
    log_colors={
    'DEBUG':    'cyan',
    'INFO':     'cyan',
    'WARNING':  'yellow',
    'ERROR':    'red',
    'CRITICAL': 'red',
    },

    style='%'
    )
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)
    return logger
logger = create_logger("Proton")

def info(input_):
    logger.info(input_)

def write_to_csv(csv_file_path, header, data):
    if not os.path.isfile(csv_file_path):
        with open(csv_file_path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(header)
    with open(csv_file_path, mode='a', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(data)

def random_sleep(a=1, b=2):
    sleep(uniform(a,b))

def browser_scroll(browser, scroll = int):
    browser.execute_script(f"window.scrollBy(0, {scroll});")
    
def browser_wait(browser, condition, by_ = str, element=str, wait=30):
    what_condition_mapping = {
        "clickable": EC.element_to_be_clickable,
        "visible": EC.visibility_of_element_located,
    }
    by_mapping = {
        "id": By.ID,
        "name": By.NAME,
        "xpath": By.XPATH,
    }
    by = by_mapping[by_]
    condition = what_condition_mapping[condition]
    element = WebDriverWait(browser, wait).until(
        condition((by, element)))
    return element

def iframe_switchto(browser, xpath, wait=40):
    WebDriverWait(browser, wait).until(EC.frame_to_be_available_and_switch_to_it(
        (By.XPATH, xpath)))
    return True

def input_send_by_clickable(browser, xpath, inputs_to_send = None, tag = None, wait=15):
    element = WebDriverWait(browser, wait).until(EC.element_to_be_clickable(
        (By.XPATH, xpath)))
    if element:
        time.sleep(random.uniform(0, 1))
        element.click()
        for char in inputs_to_send:
            element.send_keys(char)
            time.sleep(random.uniform(0, 0.1))

def click_xpath_clickable(browser, xpath, tag= None, wait= 30):
    element = WebDriverWait(browser, wait).until(EC.element_to_be_clickable(
        (By.XPATH,
         xpath)))
    random_sleep(1, 3)
    element.click()
    logger.info(f"{tag} CLICK SUCCESS.")
    random_sleep(1, 3)
    return True

def click_xpath_visibility(browser, xpath, wait=30, tag=None):
    try:
        element = WebDriverWait(browser, wait).until(EC.visibility_of_element_located(
            (By.XPATH,
             xpath)))
        random_sleep(1, 3)
        element.click()
        logger.info(f"{tag} CLICK SUCCESS.")
        return True
    except:
        logger.critical(f"{tag} CLICK FAILURE, STAYS IN.")
        while True:
            random_sleep(100, 200)
        return False

def click_xpath_presence(browser, xpath, wait=30, tag=None):
    try:
        element = WebDriverWait(browser, wait).until(EC.presence_of_element_located(
            (By.XPATH,
             xpath)))
        random_sleep(1, 3)
        element.click()
        logger.info(f"{tag} CLICK SUCCESS.")
        return True
    except:
        logger.critical(f"{tag} CLICK FAILURE, STAYS IN.")
        while True:
            random_sleep(100, 200)
        return False

def click_on_button_text_located(browser, text, wait=30):
    element = WebDriverWait(browser, wait).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, f"button:contains('''{text}''')")))
    random_sleep(0.2, 0.5)
    element.click()
    logger.info(f"Browser click {text} complete.")
    random_sleep(0.2, 0.5)

def located_by_text(browser, text, wait=30):
    element = WebDriverWait(browser, wait).until(
        EC.text_to_be_present_in_element((By.CSS_SELECTOR, text)))

def click_on_css_clickable(browser, word = "Next", wait=30):
    try:
        element = WebDriverWait(browser, wait).until(
            EC.text_to_be_present_in_element((By.CSS_SELECTOR, word)))
        random_sleep(1, 2)
        element.click()
        logger.info(f"Browser click {word} complete.")
        random_sleep(1, 2)
    except:
        logger.critical("CURRENT CLICK NOT FOUND, STAYS IN.")
        while True:
            random_sleep(100,200)

def terms_click(browser, messages, xpath, wait=30):
    element = WebDriverWait(browser, wait).until(EC.presence_of_element_located(
        (By.XPATH,
         xpath)))
    element.click()
    logger.info(messages)

def click_new (browser, xpath, tag = None, wait = 30):
    try:
        element = WebDriverWait(browser, wait).until(EC.presence_of_element_located(
            (By.XPATH,
             xpath)))
        time.sleep(random.uniform(0, 0.3))
        element.click()
        logger.info(f"{tag} Click Complete.")
        return True
    except:
        logger.critical(f"{tag} Click Failed")
        return False

def click_move_to_presence(browser, xpath, tag = None, wait = 30):
    try:
        element = WebDriverWait(browser, wait).until(EC.presence_of_element_located(
            (By.XPATH,
             xpath)))
        time.sleep(random.uniform(0, 0.3))
        action = ActionChains()
        action.move_to_element(element).click()
        logger.info(f"{tag} Click Complete.")
        return True
    except:
        logger.critical(f"{tag} Click Failed")
        return False

def create_window_and_switch_to_right_one(browser):
    browser.execute_script("window.open();")
    browser.switch_to.window(browser.window_handles[-1])
    random_sleep()
    info("switch to right window")

def switch_to_default_window(browser):
    browser.switch_to.window(browser.window_handles[0])
    logger.debug("switch to [0] window")
    random_sleep()


def fill(browser, xpath, text_fill, tag = None, wait = 30 ):
    try:
        element = WebDriverWait(browser, wait).until(EC.presence_of_element_located(
            (By.XPATH,
             xpath)))
        time.sleep(random.uniform(0, 0.3))
        element.send_keys(text_fill)
        logger.info(f"{tag} fill Complete.")
        return True
    except:
        logger.critical(f"{tag} fill Failed")
        return False

def CAPTCHAS_DETECT_AND_SOLVE(browser):
    try:
        captcha_window = WebDriverWait(browser, 30).until(EC.frame_to_be_available_and_switch_to_it(
            (By.XPATH, "/html/body/div[1]/div[4]/div/main/div/div[2]/div/div[2]/iframe")))
        if captcha_window:
            logger.info("CAPTCHA IFRAME FOUND AND SWITCHED.")
            try:
                h_captcha = WebDriverWait(browser, 5).until(EC.frame_to_be_available_and_switch_to_it(
                    (By.XPATH, '/html/body/div[1]/iframe')))
                if h_captcha:
                    logger.critical("hcaptcha found.")
                    return "hcaptcha found"
                    sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
                    
                    

                    else:
                        print("2captcha response success.")
                        browser.switch_to.parent_frame()
                        print("Switch to parent iframe.")
                        browser.execute_script(
                            'document.getElementsByName("h-captcha-response")[0].innerHTML = "{}";'.format(
                                str(result['code'])))
                        print("injected")

                        scripts = browser.find_elements(By.TAG_NAME,'script')
                        print("scripts found")
                        for script in scripts:
                            if 'tokenCallback' in script.get_attribute('innerHTML'):
                                print("captcha_token get")
                                response = str(result['code'])
                                browser.execute_script(f'tokenCallback("{response}");')
                                print("tokencallback excuted")
                        print("submitted success.")
                        return "hcaptcha success"
            except:
                pass


            WebDriverWait(browser, 30).until(EC.frame_to_be_available_and_switch_to_it(
                (By.NAME, "pcaptcha")))
            logger.info("P-CAPTCHA WINDOW OR EMAIL DETECTED.")
            try:
                next_button = WebDriverWait(browser, 30).until(EC.presence_of_element_located(
                    (By.XPATH, "/ html / body / div / div / div / div / div / div / div[2] / button[1]")))
            except:
                logger.critical("NEXT BUTTON FOR P-CAPTCHA WINDOW NOT FOUND, CAN'T SCROLL TO. WHILE LOOP STAYS IN.")
                while True:
                    time.sleep(1000)


            browser.execute_script("arguments[0].scrollIntoView();", next_button)
            logger.info("P-CAPTCHA NEXT BUTTON SCROLL INTO VIEW.")
            canvas = WebDriverWait(browser, 30).until(EC.element_to_be_clickable(
                (By.XPATH, "/ html / body / div / div / div / div / div / div / div[1] / canvas")))
            logger.info("CANVAS FOUND.")
           

    except:
        logger.critical("CAPTCHA WINDOW FAILURE")
        return "CAPTCHA WINDOW FAILURE"


def proton_signup(browser, email, email_upwork, passwords, al, us):
    proton_sign_up_url = "https://account.proton.me/signup?plan=free&billing=12&ref=prctbl&minimumCycle=12&currency=EUR&product=mail&language=en"
    browser.get(proton_sign_up_url)
    # Detect Iframe
    iframe_switchto(browser, "/html/body/div[1]/div[4]/div[1]/main/div[1]/div[2]/form/iframe")
    input_send_by_clickable(browser, "/html/body/div[1]/div/div[1]/div/div[1]/input", email, "username")
    browser.switch_to.default_content()
    input_send_by_clickable(browser,"/html/body/div[1]/div[4]/div[1]/main/div[1]/div[2]/form/div[3]/div[1]/div/div[1]/input", passwords, "password1 ")
    input_send_by_clickable(browser,"/html/body/div[1]/div[4]/div[1]/main/div[1]/div[2]/form/div[4]/div[1]/div/div[1]/input", passwords, "password2.")
    click_xpath_clickable(browser,"/html/body/div[1]/div[4]/div[1]/main/div[1]/div[2]/form/button")
    feedback = CAPTCHAS_DETECT_AND_SOLVE(browser)
    if feedback == "P-CAPTCHA COMPLETED.":
        pass
    else:
        return "CAPTCHA WINDOW FAILURE"
    browser.switch_to.default_content()
    result = click_xpath_clickable(browser,'/html/body/div[1]/div[4]/div/main/div/div[2]/form/button')
    if result:
        # accounts success.
        logger.info(f">>>>> {email} CREATION SUCCESS.")
        timestamp = datetime.utcnow()
        header = ["email", "pass", "us", "al", "time"]
        data = [email, passwords, us, al, timestamp]
        write_to_csv(csv_file_path, header, data)
    else:
        logger.critical(f"{email} CREATION FAILURE, AFTER P-CAPTCHA EMAIL CLICK BUTTON NOT DETECTED")
        return False
    try:
        click_xpath_clickable(browser, "/html/body/div[1]/div[4]/div/main/div/div[2]/form/button[2]")
        click_xpath_clickable(browser, "/html/body/div[4]/dialog/div/div[3]/div/button[1]")
        click_xpath_clickable(browser, "/html/body/div[4]/dialog/div/div[2]/div[3]/div/div/div[1]/div[2]/button[2]")
        click_xpath_clickable(browser, "/html/body/div[4]/dialog/div/div/div[3]/div/div/footer/button")
        click_xpath_clickable(browser,  "/html/body/div[4]/dialog/div/div/div[3]/div/div/footer/button[2]")
        click_xpath_clickable(browser,  "/html/body/div[4]/dialog/div/div/div[3]/div/div/footer/button[2]")
    except:
        pass
    return 000

def proton_login(browser,email,passwords):
    browser.get("https://account.proton.me/login?product=generic&language=en")
    input_send_by_clickable(browser,"proton_user",email, "/html/body/div[1]/div[4]/div[1]/main/div[1]/div[2]/form/div[2]/div[1]/div/div/input")
    input_send_by_clickable(browser,"proton_passwords", passwords, "/html/body/div[1]/div[4]/div[1]/main/div[1]/div[2]/form/div[3]/div[1]/div/div[1]/input")
    time.sleep(1)
    click_xpath_clickable(browser,"Click", "/html/body/div[1]/div[4]/div[1]/main/div[1]/div[2]/form/button")




# def upwork_signin_and_setting(browser, email, passwords, database):
#     value = signin(browser,email,passwords)
#     if value:
#         timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#         commander, connection = connect_database(database)
#         commander.execute(
#             "INSERT INTO proton_email_register (email, password, email_brand, timestamp) VALUES (?, ?, ?, ?)",
#             (email, passwords, "proton", timestamp))
#
#         # Commit the changes and close the connection
#         connection.commit()
#         connection.close()
#         
#        
#                 # timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#                 # commander, connection = connect_database(database)
#                 # commander.execute(
#                 #     "INSERT INTO proton_email_register (email, password, email_brand, timestamp) VALUES (?, ?, ?, ?)",
#                 #     (email, passwords, "proton", timestamp))
#
#                 # # Commit the changes and close the connection
#                 # connection.commit()
#                 # connection.close()



def upwork_notification_email_click(browser):
    WebDriverWait(browser, 100).until(
        EC.visibility_of_element_located((By.XPATH, "//*[contains(text(), 'Upwork Notifications')]")))

    browser.find_element(By.XPATH, "//*[contains(text(), 'Upwork Notifications')]").click()
    browser.refresh()
    # Switch to email content iframe
    WebDriverWait(browser, 30).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH,
                                                                     "/html/body/div[1]/div[3]/div/div/div/div[2]/div/div/div/main/div/div/section/div/div[3]/div/div/div/article/div[2]/div/iframe")))
    logger.info("Iframe- Email content iframe switched to.")
    # Click the email
    element = WebDriverWait(browser, 100).until(
        EC.visibility_of_element_located((By.XPATH, "//*[contains(text(), 'Verify Email')]")))
    element.click()
    logger.info("Verify Email clicked")
    # Click the email_link
    browser.switch_to.default_content()
    WebDriverWait(browser, 100).until(
        EC.visibility_of_element_located((By.XPATH, "//*[contains(text(), 'Confirm')]")))
    browser.find_element(By.XPATH, "//*[contains(text(), 'Confirm')]").click()
    logger.info("Email link clicked")
    # Switch to new window
    # WebDriverWait(browser, 30).until(EC.number_of_windows_to_be(3))
    # window_handles = browser.window_handles
    # browser.switch_to.window(window_handles[1])
    # logger.info("Switch to the newest window")






