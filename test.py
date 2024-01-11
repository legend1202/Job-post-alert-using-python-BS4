import requests
from bs4 import BeautifulSoup
import csv

# Format data ==========================================
initdata = [
    ['ProductReference', 'Name', 'Band', "Small Description", "Images", "Video List", "Data sheet", "Fitment", "HTML description", "Features", "Shipping", "notes", "Specific 1", "Specific 1 Value", "Specific 2", "Specific 2 Value", "Specific 3", "Specific 3 Value", "Specific 4", "Specific 4 Value", "Specific 5", "Specific 5 Value", "Specific 6", "Specific 6 Value"]
]

filename = 'data.csv'

with open(filename, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(initdata)
    
    
# Scraping...==============================================
def runScrap(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    oneline = []
    
    productrefer = soup.find("span", {'class': 'editable'})
    productname = soup.find("div", {'class': 'pb-center-column'})
    productband = soup.find("p", {'id': 'product_manufacturer'})
    smalldesc = soup.find("div", {'id': 'short_description_content'})
    if productrefer is not None:
        productrefer = productrefer.get("content").strip()
    if productname is not None:
        productname = productname.find("h1").text.strip()
    if productband is not None:
        productband = productband.find("a").get_text().strip()
    if smalldesc is not None:
        smalldesc = smalldesc.contents[0].get_text().strip()
    
    videolist = ''
    
    videos = []
    
    if soup.find("div", {'id': 'short_description_content'}) is not None:
        videos = soup.find("div", {'id': 'short_description_content'}).find_all("a")
    for element in videos:
        text = element.get("href").strip()
        videolist += text + "; "
        
    images = soup.find("ul", {'id': 'thumbs_list_frame'})

    fieldsets = soup.find_all('fieldset', class_='attribute_fieldset')
    output = []
    for fieldset in fieldsets:
        label = fieldset.find('label', class_='attribute_label').text.strip()
        output.append(label)
        checked_option = fieldset.find('input', {'checked': 'checked'}).find_next_sibling('span').text.strip()
        output.append(checked_option)
    missing_elements = 12 - len(output)
    output.extend([""] * missing_elements)
    

    datasheet = soup.find("div", {'id': 'more_info_sheets'}).find('table')  
    
    fitment = soup.find(lambda tag: tag and 'Vehicles:' in tag.text)
    print(fitment)
    htmldesc = soup.find('', string=lambda text: 'options:' in text.lower())
    features = soup.find('', string=lambda text: 'features:'in text.lower())
    shipping = soup.find('', string=lambda text: 'shipping:' in text.lower())
    notes = soup.find('', string=lambda text: 'notes:' in text.lower())
    if fitment is not None:
        fitment = fitment.find_next_sibling('ul')
        print(fitment)
    if htmldesc is not None:
        htmldesc = htmldesc.find_next_sibling('ul')
    if features is not None:
        features = features.find_next_sibling('ul')
    if shipping is not None:
        shipping = shipping.find_next_sibling('p')
    if notes is not None:
        notes = notes.find_next_siblings()

    oneline = [productrefer, productname, productband, smalldesc, images, videolist, datasheet, fitment, htmldesc, features, shipping, notes]
    oneline += output
    
    filename = 'data.csv'

    with open(filename, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(oneline)
        
runScrap("https://redstarexhaustusa.com/bmw-x5m-f95-x6m-f96-primary-downpipes")
    
# # Get all links =========================================
# def getLinkxs(url):
#     response = requests.get(url)
#     soup = BeautifulSoup(response.content, "html.parser")
#     lis = soup.find_all('a', {'class': 'product-name'})
#     for lin in lis:
#         print(lin.get("href"))
#         runScrap(lin.get("href"))
               
# # Start =================================================
# response = requests.get("https://redstarexhaustusa.com")
# soup = BeautifulSoup(response.content, "html.parser")
# lis = soup.find('ul', {'class': 'sf-menu'}).contents
# links = []
# for li in lis:
#     anchor_tags = li.find('ul')
#     if anchor_tags:
#         for a in anchor_tags.find_all('a'):
#             href = a.get('href')
#             getLinkxs(href)


# response = requests.get("https://redstarexhaustusa.com")
# soup = BeautifulSoup(response.content, "html.parser")
# lis = soup.find('ul', {'class': 'sf-menu'}).contents
# links = []
# for li in lis:
#     anchor_tags = li.find('ul')
#     if anchor_tags:
#         for a in anchor_tags.find_all('a'):
#             href = a.get('href')
#             links.append(href)


# response = requests.get("https://redstarexhaustusa.com/nsx")
# soup = BeautifulSoup(response.content, "html.parser")
# lis = soup.find_all('a', {'class': 'product-name'})













# data = [
#     ['ProductReference', 'Name', 'Band', ''],
#     ['John', '25', 'New York'],
#     ['Alice', '30', 'London'],
#     ['Bob', '35', 'Paris']
# ]

# filename = 'data.csv'

# with open(filename, 'a', newline='') as file:
#     writer = csv.writer(file)
#     writer.writerow(['sdf', 'sfd', 'sdf'])

# print(f"Data saved to {filename}")


