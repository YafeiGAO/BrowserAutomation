from selenium import webdriver
from lxml import html
from selenium.webdriver.chrome.options import Options
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
browser=webdriver.Chrome()
browser.get('https://www.nhtsa.gov/vehicle/2006/AUDI/A3/4%252520DR/FWD%25252FAWD#recalls')
htmlstring = browser.page_source
browser.close()
with open("yourhtmlfile.html", "w") as file:
    file.write(htmlstring)

with open("/Users/yafei/Desktop/2006 AUDI A3 4 DR FWD_AWD _ NHTSA.html", "r") as file:
    tree = html.fromstring(file.read())

detailedStr = tree.xpath('//*[@id="recalls380"]/div[1]/div[1]/p2/text()')
print(detailedStr)
