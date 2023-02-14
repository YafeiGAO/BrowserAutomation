import pandas as pd
from selenium import webdriver
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from lxml import html

pathCSV = "mmy.csv"
recallList = pd.read_csv(pathCSV)
recallList['Found'] = False
recallList['Results'] = 0
print(recallList)
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
browser=webdriver.Chrome(options=chrome_options)
error_list = []
for idx, recall in recallList.head(3).iterrows():
    recall_name = f"{idx}_{recall.Year}_{recall.Make}_{recall.Model}]"
    url = f"https://www.nhtsa.gov/vehicle/{recall.Year}/{recall.Make}/{recall.Model}#recalls"
    print(f"Open {url}")
    browser.get(url)
    timeout = 10
    try:
        element_present = EC.presence_of_element_located((By.ID, 'block-nhtsa-content'))
        WebDriverWait(browser, timeout).until(element_present)
        print ("Page is ready!")
    except TimeoutException:
        print ("Timed out waiting for page to load.")
        error_list.append(recall_name)
        continue
        
    not_found_page = browser.find_element(By.CLASS_NAME, "vehicle-detail-not-found")
    #multi_model_page = browser.find_element(By.CLASS_NAME, "vehicle-detail vehicle-detail--multiple-choice container-fluid")
    print(not_found_page)
    #print(multi_model_page)
    if not_found_page:
        continue
    elif not_found_page==1:
        print ("Multi vehcile models found")
        recallList.at[idx, 'Results'] = 2
        recallList.at[idx, 'Found'] = True
    else:
        recallList.at[idx, 'Results'] = 1
        recallList.at[idx, 'Found'] = True

        
        htmlstring = browser.page_source
        with open(f'./HTMLs2/{recall_name}.html', "w") as file:
            file.write(htmlstring)

        with open(f'./HTMLs2/{recall_name}.html', "r") as file:
            tree = html.fromstring(file.read())

        detailedStr = tree.xpath('//*[@id="recalls"]//text()')
        print(detailedStr)
print(recallList)


<div class="vehicle-detail vehicle-detail--multiple-choice container-fluid"><div class="row"><div class="col-md-12"><h1><span></span></h1></div> <div class="col-md-4"><a href="/vehicle/2020/AUDI/A6/4%252520DR/FWD" title="2020 AUDI A6 4 DR FWD"><div class="vehicle-base-details compact compact--multiple"><h1><span>2020</span> AUDI A6 <small>4 DR FWD</small></h1> <img alt="2020 AUDI A6" src="https://static.nhtsa.gov/images/vehicles/13283_st0640_046.png" onerror="'this.onerror=null;this.src=' + this.noClass" class="vehicle-base-details--hero"> <div><span>7
                    <span>Recalls</span></span> <span>
                    0
                    <span>Investigations</span></span> <span>
                    12
                    <span>Complaints</span></span> <span class=""><span><img src="/themes/custom/nhtsa/images/star-rating/5.png" alt="hi star" class="vehicle-base-details--rating"> <!----></span> <span>Overall Safety Rating</span></span></div> <!----></div></a></div><div class="col-md-4"><a href="/vehicle/2020/AUDI/A6/4%252520DR/AWD" title="2020 AUDI A6 4 DR AWD"><div class="vehicle-base-details compact compact--multiple"><h1><span>2020</span> AUDI A6 <small>4 DR AWD</small></h1> <img alt="2020 AUDI A6" src="https://static.nhtsa.gov/images/vehicles/13293_st0640_046.png" onerror="'this.onerror=null;this.src=' + this.noClass" class="vehicle-base-details--hero"> <div><span>7
                    <span>Recalls</span></span> <span>
                    0
                    <span>Investigations</span></span> <span>
                    12
                    <span>Complaints</span></span> <span class=""><span><img src="/themes/custom/nhtsa/images/star-rating/5.png" alt="hi star" class="vehicle-base-details--rating"> <!----></span> <span>Overall Safety Rating</span></span></div> <!----></div></a></div></div></div>
