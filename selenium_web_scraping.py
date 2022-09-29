import xlsxwriter
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep

############ first create directory >>>>> "xlsx" ##############

PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH)

url = "https://www.grubhub.com/restaurant/la-shish-kabob-3117-n-sharon-amity-rd-charlotte/754359"

driver.get(url)


restaurant_name = driver.find_element(By.CLASS_NAME, 'u-text-wrap.u-stack-y-1')
restaurant_address = driver.find_element(By.CLASS_NAME, 'restaurantAbout-info-address.u-line-bottom.u-line--thin.u-line--light')
restaurant_description = driver.find_element(By.XPATH, '/html/head/meta[9]')

print(f"Restaurant name: {restaurant_name.text}")
print(f"Restaurant Header Description: {restaurant_description.text}")
print(f"Restaurant Adress: {restaurant_address.text}")
print(f"Restaurant City: {restaurant_address.text.split()[-3]}")
print(f"Restaurant State: {restaurant_address.text.split()[-2],restaurant_address.text.split()[-1]}")

#stars
element = driver.find_element(By.CSS_SELECTOR, "#restaurantPage-reviewHighlights > div.clearfix.u-unclickable.restaurantReviews-heading.u-line-bottom.u-line--thin > div > div.s-col-md-8.s-form-group > div:nth-child(2) > span > div > span:nth-child(1) > div")
attributeValue = element.get_attribute("style")
if attributeValue == "background-position: 0px -192px;":
    star = "5 stars"
elif attributeValue == "background-position: 0px -168px;":
    star = "4.5 stars"
elif attributeValue == "background-position: 0px -144px;":
    star = "4 stars"
elif attributeValue == "background-position: 0px -120px;":
    star = "3.5 stars"
elif attributeValue == "background-position: 0px -96px;":
    star = "3 stars"
elif attributeValue == "background-position: 0px -48px;":
    star = "2 stars"
elif attributeValue == "background-position: 0px -48px;":
    star = "1 star"


print(f"Restaurant Stars: {star}")

#reviews
reviews = driver.find_elements(By.CLASS_NAME, "restaurant-review-item.review-container--restaurant")
print("Reviews count: ", len(reviews))
  

menu = driver.find_elements(By.CLASS_NAME, 'menuItem.menuItem--list.u-clickable.u-inset-1')

    
workbook = xlsxwriter.Workbook(f'xlsx/{restaurant_name.text.replace(" ","_")}.xlsx')
worksheet = workbook.add_worksheet()

#headers
worksheet.write('A1', 'Category Name')
worksheet.write('B1', 'Item Name')
worksheet.write('C1', 'Item Description')
worksheet.write('D1', 'Item Price')
  
c = 1
for n, i in enumerate(menu, 1):
    item_name = i.find_element(By.CLASS_NAME,'menuItemRegular-name.u-text-ellipsis')
    item_description = i.find_element(By.CLASS_NAME, 'u-text-secondary.menuItemNew-description--truncate.u-margin-bottom-cancel')
    item_price = i.find_element(By.CLASS_NAME, 'menuItem-priceAmount.h6.s-textBox-title.u-margin-bottom-cancel')
    desc =  len(item_description.text)
    worksheet.write(f'B{c}', item_name.text)
    worksheet.write(f'D{c}', item_price.text)
    print(f"{n}) Name: {item_name.text} - Price: {item_price.text}")
    c += 1
    if desc > 0:
        print(f"Description: {item_description.text}\n")
        worksheet.write(f'C{c}', item_description.text) 
    driver.execute_script("window.scrollBy(0, 90)")
    sleep(0.1)


workbook.close()
sleep(60)
driver.quit()