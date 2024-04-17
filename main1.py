import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import WebDriverException
from extension import proxies
import sys
import time
import urllib.parse
from urllib.parse import urlparse, parse_qs
# Proxy authentication information - Uncomment and modify if proxies are needed
# proxy = {
#     'http': 'http://username:password@proxy-address:port',
#     'https': 'https://username:password@proxy-address:port'
# }
username = 'sp43xuny7n'
password = 'i1NRxNR_66x+xO6A4'
endpoint = 'gate.dc.smartproxy.com'
mainport = 20001
globalid = 0
globalcityname=''
def setanotherport(port):
    port = port+1
    if port>37959:
        return 20001
    else:
        return port

def get_links(html):
    a_tags = html.find_all('a', attrs={"class": "css-19v1rkv"})
    links = [tag.get("href") for tag in a_tags if tag.get(
        "href") and tag.get("href").startswith("/biz/")]
    return links


def get_place_name(html):
    h1_tag = html.find("h1", attrs={"class": "css-hnttcw"})
    return h1_tag.text if h1_tag else "Name not found"


def get_image_url(html):
    img_section = html.find("section", attrs={"aria-label": "Photos & videos"})
    img_tag = img_section.find("img") if img_section else None
    return img_tag.get("src") if img_tag else "Image URL not found"


def get_business_details(html):
    meta_tag = html.find("meta", attrs={"property": "og:description"})
    business = meta_tag.get("content").split(
        "Established") if meta_tag else ["Details not found", ""]
    return business[0], "Established" + business[1] if len(business) > 1 else "Establishment date not found"


def get_owner_details(html):
    owner_section = html.find(
        "section", attrs={"aria-label": "About the Business"})
    owner_name_tag = owner_section.find(
        "p", attrs={"data-font-weight": "bold"}) if owner_section else None
    owner_bio_tag = owner_section.find(
        "span", attrs={"width": "0"}) if owner_section else None
    return owner_name_tag.text if owner_name_tag else "Owner name not found", owner_bio_tag.text if owner_bio_tag else "Owner biography not found"


def get_contactinfo(html):
    elements = html.find_all(class_='css-djo2w')
    texts = [element.get_text(strip=True) for element in elements]

    if len(texts) < 2:
            return ["Website info not available", "Phone number not available"]

    website = texts[0][16:]  # Assuming the website is always in the first element
    phone_number = texts[1][12:]  # Assuming the phone number is always in the second element
    return [website, phone_number]
    # First three characters are the day


def get_timelist(html):
    elements = html.find_all(class_='css-29kerx')
    texts = [element.get_text(strip=True) for element in elements]
    split_list = []
    for item in texts:
        if item:
            day = item[:3]  # First three characters are the day
            time = item[3:]  # The rest is the time
            split_list.append(day)
            split_list.append(time)

    # Display the split list
    # print(split_list)
    return split_list


def get_imageGaleryurl(html):
    a_tags = html.find_all('a', attrs={"class": "css-19v1rkv"})
    links = [tag.get("href") for tag in a_tags if tag.get(
        "href") and tag.get("href").startswith("/biz_photos")]
    # print("dddd",links)
    if links:
        return links[0]
    else:
        # Handle the case where no valid links are found
        # print("No valid links found")
        return None


def get_imageGalerylist(url):
    # print("url",url)
    if url != "":
        link = f"https://www.yelp.com{url}"
        global mainport
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'}

        proxies = {'http': f'http://sp43xuny7n:i1NRxNR_66x+xO6A4@gate.dc.smartproxy.com:{mainport}',  # Your username, password for proxy authentication, and desired endpoint within punctuation marks ('')
                'https': f'https://sp43xuny7n:i1NRxNR_66x+xO6A4@gate.dc.smartproxy.com:{mainport}'}
        mainport = setanotherport(mainport)

        r = requests.get(link)
        time.sleep(2)
        html1 = BeautifulSoup(r.content, 'html.parser')
        #  photo-box-img
        img_tags = html1.find_all('img', attrs={"class": "photo-box-img"})
        links = [tag.get("src") for tag in img_tags]
        # print(links)
        return links
    else:
        return []


def get_videourlList(url):
    if url != "":
        link = f"https://www.yelp.com{url}"
        global mainport
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'}

        proxies = {'http': f'http://sp43xuny7n:i1NRxNR_66x+xO6A4@gate.dc.smartproxy.com:{mainport}',  # Your username, password for proxy authentication, and desired endpoint within punctuation marks ('')
                'https': f'https://sp43xuny7n:i1NRxNR_66x+xO6A4@gate.dc.smartproxy.com:{mainport}'}
        mainport = setanotherport(mainport)

        # r = requests.get(link, headers=headers, proxies=proxies)
        r = requests.get(link, proxies=None)
        time.sleep(2)
        html1 = BeautifulSoup(r.content, 'html.parser')
        videos = html1.find_all('video')

        # List to hold all src attributes
        src_list = []

        # Iterate over each video tag
        for video in videos:
            # Check if video tag itself has a src attribute
            if video.has_attr('src'):
                src_list.append(video['src'])

            # Additionally check for source tags within the video tag
            sources = video.find_all('source')
            for source in sources:
                if source.has_attr('src'):
                    src_list.append(source['src'])
        return src_list
        # Print all src attributes found
        # print(src_list)


def get_avg_review(html):
    div_tag = html.find(
        'div', class_='arrange-unit__09f24__rqHTg arrange-unit-fill__09f24__CUubG css-v3nuob')

    # Check if the div_tag is found
    if div_tag:
        # Find the <span> within this <div>
        span_tag = div_tag.find('span', class_='css-1p9ibgf')

        # Check if the span_tag is found and get its text
        if span_tag:
            span_text = span_tag.get_text(strip=True)
            return span_text
        else:
            return "0"
    else:
        return "0"


def get_highlighting_HTS(html):
    # mobile-text-medium__09f24__MZ1v6 css-1dtv2dz
    # arrange__09f24__LDfbs gutter-2__09f24__CCmUo layout-wrap__09f24__GEBlv layout-6-units__09f24__pP1H0 css-1qn0b6x
    outer_div = html.find(
        'div', class_='arrange__09f24__LDfbs gutter-2__09f24__CCmUo layout-wrap__09f24__GEBlv layout-6-units__09f24__pP1H0 css-1qn0b6x')
    highlighting_HTS = []
    # Check if the outer_div is found
    if outer_div:
        # Find the inner <div> within this outer <div>
        inner_spans = outer_div.find_all(
            'span', class_='mobile-text-medium__09f24__MZ1v6 css-1dtv2dz')

        # Check if the inner_div is found and get its text
        for inner_span in inner_spans:
            spantext = inner_span.get_text()
            highlighting_HTS.append(spantext)
            # print("Found text:", div_text)
        return highlighting_HTS
    else:
        return highlighting_HTS


def get_services_offers(html):

    outer_div = html.find(
        'div', class_='arrange__09f24__LDfbs gutter-auto__09f24__W9jlL layout-2-units__09f24__PsGVW css-1qn0b6x')
    services_offers = []
    # Check if the outer_div is found
    if outer_div:
        # Find the inner <div> within this outer <div>
        inner_divs = outer_div.find_all('div', class_='css-174a15u')

        # Check if the inner_div is found and get its text
        for inner_div in inner_divs:
            div_text = inner_div.get_text(strip=True)
            services_offers.append(div_text)
            # print("Found text:", div_text)
        return services_offers
    else:
        return services_offers


def get_booking_link(url):
    # print("Initializing WebDriver...")
    # Configure Chrome options for headless execution
    # chrome_options = webdriver.ChromeOptions()
    # global mainport
    # proxies_extension = proxies(username, password, endpoint, mainport)
    # mainport = setanotherport(mainport)

    # chrome_options.add_extension(proxies_extension)
    # # chrome_options.add_argument(f"user-agent={headers['User-Agent']}")
    # chrome_options.add_argument("--headless=new")


    # driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)


    chrome_options = Options()
    chrome_options.add_argument("--headless=new")

    # Initialize WebDriver with options
    driver = webdriver.Chrome(options=chrome_options)

    try:
        # print("Navigating to URL...")
        driver.get(url)

        # print("Waiting for the element...")
        # Wait until the animation is likely to be complete (e.g., up to 10 seconds)
        a_tag = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, "section.css-2entjo a.css-1j3dh7m"))
        )
        # print("Element is visible.")

        # Get href attribute
        a_href = a_tag.get_attribute('href')
        # print(f"Found href: {a_href}")
        return a_href

    except TimeoutException:
        print("Timed out waiting for page to load or element to become visible.")
        return ' '
    finally:
        print("Closing WebDriver...")
        driver.quit()


def get_full_address(html):
    # Find the <div> with its specific class
    div_tag = html.find(
        'div', class_='arrange__09f24__LDfbs gutter-1-5__09f24__vMtpw css-1qn0b6x')

    # Initialize an empty list to hold all addresses
    fulladress = ""
    addresses = []

    # Check if the div_tag is found
    if div_tag:
        # Find all <p> tags within this <div>
        p_tags = div_tag.find_all('p')

        # Iterate over each p_tag found and get its text
        for p_tag in p_tags:
            if p_tag:
                address = p_tag.get_text(strip=True)
                fulladress += address + " "
                # addresses.append(address)

    # Return the list of addresses, or an empty list if none are found
    return fulladress.strip()  # Strip any trailing spaces

def get_price(html):
    #  css-14r9eb
    span_tag = html.find_all(
        'span', class_='css-14r9eb')
    # print(span_tag)
    if len(span_tag) > 1:
        return span_tag[1].get_text()
    else:
        return 'free'
def get_claimed(html):
    # bullet--dark__09f24__iJ3M2 css-13pss27
    myclaim=''
    span_tag = html.find(
        'span', class_='bullet--dark__09f24__iJ3M2 css-13pss27')
    span_tag2 = html.find(
        'span', class_='bullet--light__09f24__TY0D4 css-14r9eb')
    
    if span_tag:
        spantext = span_tag.get_text()
        myclaim+=spantext+" "
    elif span_tag2:
        spantext = span_tag2.get_text()
        myclaim+=spantext+" "
    
    # print(myclaim)
    return myclaim
def get_category(html):
    myclaim=''
    span_tag1 = html.find('span',class_="css-1xfc281")
    if span_tag1:
        myclaim+=span_tag1.get_text(separator=" ", strip=True)
    return myclaim
def format_qa_to_json(qa_list):
    structured_qa = []
    for i in range(0, len(qa_list), 2):
        if i + 1 < len(qa_list):
            question = qa_list[i].replace("Q:", "").strip()
            answer = qa_list[i+1].replace("A:", "").strip()
            structured_qa.append({
                "id": i // 2,
                "question": question,
                "answer": answer
            })
    return structured_qa


def get_bussiness_FAQ(html):
    section_tag = html.find('section', {'aria-label': "Ask the Community"})

    # Initialize a list to store texts
    texts = []

    # Check if the section_tag is found
    if section_tag:
        # Find all <div> elements with the specified class within the section
        div_tags = section_tag.find_all('div', class_='css-laf5de')

        # Extract text from each <div> tag and add it to the list
        for div in div_tags:
            text = div.get_text(strip=True)
            texts.append(text)

    # Print the list of texts
    # print(texts)
    formatted_qa_list = format_qa_to_json(texts)

    # Convert the list of dictionaries to a JSON string
    json_output = json.dumps(formatted_qa_list, indent=2)
    return json_output


def get_allreviws(html, num):

    li_elements = html.find_all('li', class_='css-1q2nwpv')

    # Filter 'li' elements that contain a 'div' with class 'css-1qn0b6x'
    filtered_li_elements = [
        li for li in li_elements if li.find('a', class_='css-vzslx5')]

    details_list = []

    # Iterate over each 'li' element
    for li in filtered_li_elements:
        item_details = {}
        # Find the 'a' tag with class 'css-vzslx5' and get its text
        a_tag = li.find('a', class_='css-19v1rkv')
        item_details['a_tag_text'] = a_tag.text.strip() if a_tag else ' '

        # Find the first 'span' tag with class 'css-qgunke' and get its text
        span_css_qgunke = li.find('span', class_='css-qgunke')
        item_details['span_css_qgunke_text'] = span_css_qgunke.text.strip(
        ) if span_css_qgunke else ' '

        # Find the second 'span' tag with class 'raw__09f24__T4Ezm' and get its text
        span_raw = li.find('span', class_='raw__09f24__T4Ezm')
        item_details['span_raw_text'] = span_raw.text.strip(
        ) if span_raw else ''

        # Get the 'svg' tag and its HTML content
        # svg_tag = li.find('svg')
        # item_details['svg_html'] = str(svg_tag) if svg_tag else None
        # Add the details to the list
        div_so0evj = li.find('div', class_='css-so0evj')
        if div_so0evj:
            imgs = div_so0evj.find_all('img')
            img_srcs = [img['src'] for img in imgs if 'src' in img.attrs]
            item_details['img_srcs'] = (', ').join(img_srcs)
        fill_colors = [
            "rgba(251,67,60,1)",
            "rgba(255,173,72,1)",
            "rgba(255,100,61,1)",
            "rgba(255,135,66,1)",
            "rgba(255,204,75,1)"
        ]
        countrange = 0
        for color in fill_colors:
            svg_tags = li.find_all('div', {
                                   'class': 'arrange__09f24__LDfbs gutter-1__09f24__yAbCL vertical-align-middle__09f24__zU9sE css-1qn0b6x'})
            for svg in svg_tags:
                if not svg.find_parent('div', {'class': 'css-tq6h5w'}):
                    temprange = len(svg.find_all('path', {'fill': color}))
                    if countrange < temprange:
                        countrange = temprange
        item_details['range'] = countrange/2.0

        # print(type(item_details['img_srcs']))
        # Add the details to the list
        details_list.append(item_details)
    # print(type(details_list))
    # details_list1 = ', '.join(details_list)
    details_string = ''
    index = num+1
    for itemi in details_list:
        item_details_string = f" {index}: {{ \n " \
                              f" 'name': '{itemi.get('a_tag_text', '')}'' ,\n " \
                              f"'location': '{itemi.get('span_css_qgunke_text', '')}', \n" \
                              f"'range': '{itemi.get('range', '')}', \n" \
                              f"'comments': '{itemi.get('span_raw_text', '')}', \n " \
                              f"'imagelinks': '{itemi.get('img_srcs', '')}' }} \n"
        details_string += f"{item_details_string}\n"
        index = index+1
    # print(details_string)

    return details_string
    # Print the list of details
    # for details in details_list:
    # print(details)
    # Output the findings
    # for li in filtered_li_elements:
    #     print(li.prettify())
    # print(filtered_li_elements.__len__())


def getEachReviewPageSource(url):
    index = 0
    allviews = ''
    while True:
        addurl = f"start={index}"
        full_url = f"{url}&{addurl}"
        # print(full_url)  # for debugging to see the URL being requested
        # global mainport
        # headers = {
        #     'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'}

        # proxies = {'http': f'http://sp43xuny7n:i1NRxNR_66x+xO6A4@gate.dc.smartproxy.com:{mainport}',  # Your username, password for proxy authentication, and desired endpoint within punctuation marks ('')
        #         'https': f'https://sp43xuny7n:i1NRxNR_66x+xO6A4@gate.dc.smartproxy.com:{mainport}'}
        # mainport = setanotherport(mainport)

        # r = requests.get(full_url, headers=headers, proxies=proxies)
        # # response = requests.get(full_url, proxies=proxies)
        # time.sleep(2)

        
        try: # Adjust based on the observed load time of the page
            # chrome_options = webdriver.ChromeOptions()
            # global mainport
            # proxies_extension = proxies(username, password, endpoint, mainport)
            # mainport = setanotherport(mainport)

            # chrome_options.add_extension(proxies_extension)
            # # chrome_options.add_argument(f"user-agent={headers['User-Agent']}")
            # chrome_options.add_argument("--headless=new")


            # driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
            chrome_options = Options()
            chrome_options.add_argument("--headless=new")
            # chrome_options.add_argument("--disable-gpu")

            # Initialize WebDriver with options
            driver = webdriver.Chrome(options=chrome_options)
            driver.get(full_url)
            time.sleep(5)
            page_source = driver.page_source
            html = BeautifulSoup(page_source, 'html.parser')
            # driver.quit()



            li_elements = html.find_all('li', class_='css-1q2nwpv')
            filtered_li_elements = [
                li for li in li_elements if li.find('a', class_='css-vzslx5')]
            # print('valid ', index)
            # Check if there are filtered elements to determine if we should continue
            if not filtered_li_elements:
                # with open('out.html', 'a', encoding='utf-8') as f:
                #     f.write(str(html))  # convert HTML to string before writing
                # print("No more reviews found. Exiting loop.")
                    # print(index)
                break  # exit the loop if no filtered elements are found

            pageriview = get_allreviws(html, index)
            allviews += f"{pageriview}"
            index += 10  # increment to get the next set of results
        
        except WebDriverException as e:
            print(f"An error occurred: ")
        finally:
            driver.quit()
    # print(allviews)
    return allviews
def get_geolocation(html):
    container = html.find('div', class_='container__09f24__fZQnf css-1rocox3')
    
    # Initialize a list to store the results
    image_sources = []
    decoded_coords=''
    if container:
        # Find all img tags within the div
        img_tags = container.find_all('img')
        for img in img_tags:
            # Get 'src' and 'srcset' attributes
            src = img.get('src', 'No src attribute')
            srcset = img.get('srcset', 'No srcset attribute')
            
            # Append the results with image details
            image_sources.append({'src': src, 'srcset': srcset})
            center_param = srcset.split('center=')[1].split('&')[0]
            # Decode the URL encoding
            decoded_coords = urllib.parse.unquote(center_param)
    return decoded_coords

def scrape_business_page(url):
    global mainport
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'}

    proxies1 = {'http': f'http://sp43xuny7n:i1NRxNR_66x+xO6A4@gate.dc.smartproxy.com:{mainport}',  # Your username, password for proxy authentication, and desired endpoint within punctuation marks ('')
                'https': f'https://sp43xuny7n:i1NRxNR_66x+xO6A4@gate.dc.smartproxy.com:{mainport}'}
    mainport = setanotherport(mainport)

    # r = requests.get(url, headers=headers, proxies=proxies1)
    r = requests.get(url)
    # time.sleep(2)
    html = BeautifulSoup(r.content, 'html.parser')
    # return
    # reviews = getEachReviewPageSource(url)
    reviews=''
    global globalcityname
    global globalid
    place_name = get_place_name(html)
    image_url = get_image_url(html)
    # print(place_name,image_url)
    # return
    business_specialties, business_history = get_business_details(html)
    owner_name, owner_bio = get_owner_details(html)
    contactinfo = get_contactinfo(html)
    if len(contactinfo)>1:
        place_phone = contactinfo[1]
        place_website = contactinfo[0]
    else:
        place_phone=''
        place_website=''
    place_openingList = get_timelist(html)
    get_claimed1 = get_claimed(html)
    get_cagegory1 = get_category(html)
    price=get_price(html)
    geolocation=get_geolocation(html)
    # print(geolocation)
    lenghth = place_openingList.__len__()
    if lenghth>13:
        place_opening_Monday = place_openingList[0]
        place_opening_Monday_time = place_openingList[1]
        place_opening_Tuesday = place_openingList[2]
        place_opening_Tuesday_time = place_openingList[3]
        place_opening_Wednesday = place_openingList[4]
        place_opening_Wednesday_time = place_openingList[5]
        place_opening_Thursday = place_openingList[6]
        place_opening_Thursday_time = place_openingList[7]
        place_opening_Fridy = place_openingList[8]
        place_opening_Fridy_time = place_openingList[9]
        place_opening_Saturday = place_openingList[10]
        place_opening_Saturday_time = place_openingList[11]
        place_opening_Sunday = place_openingList[12]
        place_opening_Sunday_time = place_openingList[13]
    else:
        place_opening_Monday=''
        place_opening_Monday_time=''
        place_opening_Tuesday=''
        place_opening_Tuesday_time=''
        place_opening_Wednesday=''
        place_opening_Wednesday_time=''
        place_opening_Thursday=''
        place_opening_Thursday_time=''
        place_opening_Fridy=''
        place_opening_Fridy_time=''
        place_opening_Saturday=''
        place_opening_Saturday_time=''
        place_opening_Sunday=''
        place_opening_Sunday_time=''
    # booking_link = get_booking_link(url)
    booking_link=' '
    if booking_link==' ':
        booking_type  = 'contact '
    else:
        booking_type = 'external' 
    bussiness_faq = get_bussiness_FAQ(html)
    # print(bussiness_faq)
    # print(type(bussiness_faq))
    gallery_url = get_imageGaleryurl(html)

    if gallery_url:

        
        imageGalerylist = get_imageGalerylist(get_imageGaleryurl(html))
        
        imageGalerylist = ', '.join(imageGalerylist)
        
        videoList = get_videourlList(get_imageGaleryurl(html))
        
        videoList = ', '.join(videoList)
    
    else:
        
        imageGalerylist='[]'
	    
        videoList=[]    
	
    avg_review = get_avg_review(html)
    services_offers = get_services_offers(html)
    services_offers = ', '.join(services_offers)

    highlighting_HTS = get_highlighting_HTS(html)
    highlighting_HTS = ','.join(highlighting_HTS)

    full_address = get_full_address(html)

    return {
        "id":f"{globalid}",
        "place_name": place_name,
        "image_url": image_url,
        'Price': price,
        "business_specialties": business_specialties,
        "business_history": business_history,
        "owner_name": owner_name,
        "owner_bio": owner_bio,
        "Category": get_cagegory1,
        'Place_type': 'N/A',
        "highlighting_HTS": highlighting_HTS,
        "services_offers": services_offers,
        "City": globalcityname,
        "full_address": full_address,
        'Geo_location':geolocation,
        'place_opening_Monday': place_opening_Monday,
        'place_opening_Monday_time': place_opening_Monday_time,
        'place_opening_Tuesday ': place_opening_Tuesday,
        'place_opening_Tuesday_time': place_opening_Tuesday_time,
        'place_opening_Wednesday': place_opening_Wednesday,
        'place_opening_Wednesday_time': place_opening_Wednesday_time,
        'place_opening_Thursday': place_opening_Thursday,
        'place_opening_Thursday_time ': place_opening_Thursday_time,
        'place_opening_Fridy': place_opening_Fridy,
        'place_opening_Fridy_time': place_opening_Fridy_time,
        'place_opening_Saturday': place_opening_Saturday,
        'place_opening_Saturday_time': place_opening_Saturday_time,
        'place_opening_Sunday': place_opening_Sunday,
        'place_opening_Sunday_time ': place_opening_Sunday_time,
        'place_phone': place_phone,
        'place_email': 'n/a',
        'place_website': place_website,
        "place_images_Gallery": imageGalerylist,
        'place_video_url': videoList,
        "avg_review": avg_review,
        "place_booking_type": booking_type,
        "Place_BOOKING_Link": booking_link,
        'Business_status':   get_claimed1,
        'reviews': reviews,
        "Bussiness_FAQ": bussiness_faq,
        'yelp_url': url,
    }

# Main function to initiate the scraping


def main():
    # url = "https://www.yelp.com/biz/lumia-dental-new-york-4?osq=Dentists"
    # # url="https://www.yelp.com/biz/zen-dental-studio-san-francisco-2?osq=Dentist"
    # business_data = scrape_business_page(url)
    # print(business_data)
    # return
    url1 = sys.argv[2]
    proxy_file = sys.argv[4]
    agent_file = sys.argv[6]
    output_file = sys.argv[8]
    max_listings = sys.argv[10] if len(sys.argv) > 10 else None
    print(f"scraping {max_listings} listing of the url {url1}")
    # print(output_file)
    parsed_url = urlparse(url1)
    query_string = parsed_url.query

    # Parse the query string into a dictionary
    query_params = parse_qs(query_string)

    # Get the value associated with 'find_loc'
    city_name = query_params.get('find_loc', [None])[0]
    global globalcityname
    globalcityname = city_name

    # url = 'https://www.yelp.com/search?find_desc=Dentist&find_loc=San+Francisco%2C+CA'
    # url='https://www.yelp.com/search?find_desc=Dentist&find_loc=San+Francisco%2C+CA'
    # # r = requests.get(url)  # proxies=proxy if needed
    pagenumber = 0
    while True:
        global mainport
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'}

        proxies = {'http': f'http://sp43xuny7n:i1NRxNR_66x+xO6A4@gate.dc.smartproxy.com:{mainport}',  # Your username, password for proxy authentication, and desired endpoint within punctuation marks ('')
                    'https': f'https://sp43xuny7n:i1NRxNR_66x+xO6A4@gate.dc.smartproxy.com:{mainport}'}
        mainport = setanotherport(mainport)
        # print(mainport)
        url = f"{url1}&start={pagenumber*10}"
       
        # url = url1+f"&start={pagenumber}"
        pagenumber = pagenumber+1
        # r = requests.get(url, headers=headers, proxies=proxies)
        r = requests.get(url)
        # print(r.text)
        # # r = requests.get(url)
        # time.sleep(2)
        # # print(r.content)
        html = BeautifulSoup(r.text, 'html.parser')
        # with open('out.html', 'a', encoding='utf-8') as f:
        #     f.write(str(html))  # convert HTML to string before writing
        # print(html)
        links = get_links(html)
        if len(links)<9:
            print(f"done! scraped {max_listings} listing saved to {output_file}")
            return
        if (pagenumber-1)*10>=int(max_listings):
            print(f"done! scraped {max_listings} listing saved to {output_file}")
            return
        # print(links)
        # return
        for link in links:
            full_url = f"https://www.yelp.com{link}"
            # Add , proxies=proxy if using proxies
            business_data = scrape_business_page(full_url)
            # print(business_data)
            
            df = pd.DataFrame([business_data])

            # Check if the file exists
            if output_file.endswith('.csv'):
                # If the file exists, append to it
                if os.path.exists(output_file):
                    df.to_csv(output_file, mode='a', header=False, index=False)
                else:
                    df.to_csv(output_file, index=False)
            elif output_file.endswith('.xlsx'):
                if os.path.exists(output_file):
                    # If the file exists, read the existing data and append the new data
                    with pd.ExcelWriter(output_file, mode='a', engine='openpyxl', if_sheet_exists='overlay') as writer:
                        existing_data = pd.read_excel(output_file)
                        new_data = pd.concat([existing_data, df], ignore_index=True)
                        new_data.to_excel(writer, index=False)
                else:
                    # If the file does not exist, create it
                    df.to_excel(output_file, index=False)

                # print('Data written to output.xlsx')
            else:
                raise ValueError("Unsupported file extension. Use .csv or .xlsx")
            print(f"listing {full_url} -> scraped ")
            # break
        # full_url=f"https://www.yelp.com/biz/britesmile-san-francisco-2?osq=dentist"
    full_url=f"https://www.yelp.com/biz/all-smiles-dental-san-francisco-5?osq=dentist"

    business_data = scrape_business_page(full_url)
    print(business_data)
    return
if __name__ == "__main__":
    main()
