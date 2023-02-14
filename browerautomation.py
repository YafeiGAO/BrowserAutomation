from selenium import webdriver
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from lxml import html


recall_list=['2006_audi_a3', '2009_audi_q5', '2007_volvo_xc90']
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
browser=webdriver.Chrome(options=chrome_options)

for item in recall_list:
    url = f"https://www.nhtsa.gov/vehicle/{item.split('_')[0]}/{item.split('_')[1]}/{item.split('_')[2]}#recalls"
    print(f"Open {url}")
    browser.get(url)
    timeout = 30
    try:
        element_present = EC.presence_of_element_located((By.ID, 'recalls'))
        WebDriverWait(browser, timeout).until(element_present)
        print ("Page is ready!")
    except TimeoutException:
        print ("Timed out waiting for page to load.")
    
    htmlstring = browser.page_source
    with open(f'{item}.html', "w") as file:
        file.write(htmlstring)

    with open(f'{item}.html', "r") as file:
        tree = html.fromstring(file.read())

    detailedStr = tree.xpath('//*[@id="recalls"]//text()')
    print(detailedStr)
