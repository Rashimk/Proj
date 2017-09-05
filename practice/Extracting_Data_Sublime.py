# Importing the necessary packages

import pandas as pd
import numpy as np
from scrapy.selector import Selector
from scrapy.http import HtmlResponse
import requests

import craigslist
from craigslist import CraigslistPersonals

# List of cities:
cities = ['seattle', 'sfbay', 'honolulu','losangeles', 'sandiego', 'newyork', 'boston', 'miami', 'austin', 'houston']


# Function required to extract the necessary data:

def extraction(site):
    
    cl = CraigslistPersonals(site = site, category='mis')
    results = cl.get_results(sort_by='newest', geotagged= True)
    
    title = []
    has_image = []
    url = []
    geo_tag = []
    where = []
    ids = []
    datetimes = []
    has_maps = []
    
    for result in results:
        title.append(result['name'])
        has_image.append(result['has_image'])
        url.append(result['url'])
        geo_tag.append(result['geotag'])
        where.append(result['where'])
        ids.append(result['id'])
        datetimes.append(result['datetime'])
        has_maps.append(result['has_map'])

    
    def missed_age(url):
        # initiate request
        response = requests.get(i)
        HTML = response.text

        # scrape
        age = Selector(text=HTML).xpath("//p[@class='attrgroup'][2]/span/b/text()").extract()
        return age
    
    def missed_height(url):
        # initiate request
        response = requests.get(i)
        HTML = response.text

        # scrape
        height = Selector(text=HTML).xpath("//span[@class='personals_attrbubble personals_'][2]/b/text()").extract()
        return height
    
    def missed_btype(url):
        # initiate request
        response = requests.get(i)
        HTML = response.text

        # scrape
        btype = Selector(text=HTML).xpath("//p[@class='attrgroup'][1]/span[@class='personals_attrbubble personals_'][1]/b/text()").extract()
        return btype
    
    def missed_title(url):

        # initiate request
        response = requests.get(i)
        HTML = response.text

        # scrape
        title = Selector(text=HTML).xpath("//span[@class='postingtitletext']/span[@id='titletextonly']/text()").extract()
        return title

    def missed_body(url):
        response = requests.get(i)
        HTML = response.text

        # scrape
        body = Selector(text=HTML).xpath("//section[@id='postingbody']/text()").extract()
        return body

    def missed_who4who(url):
        response = requests.get(i)
        HTML = response.text

        # scrape
        m4m = Selector(text=HTML).xpath("//h2[@class='postingtitle']/span[@class='postingtitletext']/text()").extract()
        return m4m

    
    def missed_id(url):
        response = requests.get(i)
        HTML = response.text

        # scrape
        id = Selector(text=HTML).xpath("//div[@class='postinginfos']/p[@class='postinginfo'][1]/text()").extract()
        return id
    
    # Required Lists
    title = []
    body = []
    m4m = []
    ids = []
    age = []
    height = []
    btype = []
    
    for i in url:

    # Calling the function written before

        a = missed_title(i)
        b = missed_body(i)
        c = missed_who4who(i)
        d = missed_id(i)
        e = missed_age(i)
        f = missed_height(i)
        g = missed_btype(i)
        
    # Appending the extracted lists on to the lists above
        title.append(a)
        body.append(b)
        m4m.append(c)
        ids.append(d)
        age.append(e)
        height.append(f)
        btype.append(g)
        
        
    clean = body
    
    # Cleaning my body section

    # First using .join to connect at ','
    cleaning = []
    for i in clean:
        i = ','.join(i)
        i = [i]
        cleaning.append(i)
        
    # Cleaning the body of my data
    # removing the unnessary gaps and fillers in the body section

    cleaned_body = []
    for bod in cleaning:
        for bo in bod:
            bo = bo.replace('\n','')
            bo = bo.replace('    ','')
            bo = bo.replace(',', '')
            z = bo
            cleaned_body.append(z)
        
    clean = m4m
    
# #   cLEANING IDS
#     for i in title:
#         i = i.replace('[','')
#         i = i.replace(']','')
    
    cleaning_m4m = []
    for i in clean:
        i = ','.join(i)
        i = [i]
        cleaning_m4m.append(i)
        
    cleaned_m4m = []
    
    
    for bod in cleaning_m4m:
        for bo in bod:
            if bo == '':
                cleaned_body.append(np.nan)
            else:
                bo = bo.replace(' - ', '')
                bo = bo.replace('\n','')
                bo = bo.replace('    ','')
                bo = bo.replace(',', '')
            z = bo
            cleaned_m4m.append(z)
            
    #  Creating a dataframe for finding who the connection is meant for
    df_m4m = pd.DataFrame(cleaned_m4m, columns=["Who_to"])
    
    # cleaning the ids extracted from the scrapping:
    ids_scrapy = []
    
    for i in ids:
        for g in i:
            idd = [int(s) for s in g.split() if s.isdigit()]
            ids_scrapy.append(idd)
            
#         title.append(result['name'])
#         has_image.append(result['has_image'])
#         url.append(result['url'])
#         geo_tag.append(result['geotag'])
#         where.append(result['where']) 
#         ids.append(result['id'])
#         datetimes.append(result['datetime'])
#         has_maps.append(result['has_map'])

    titlef = [val for sublist in title for val in sublist]
    agef = [val for sublist in age for val in sublist]
    btypef = [val for sublist in btype for val in sublist]
    heightf = [val for sublist in height for val in sublist]
    ids_scrapyf = [val for sublist in ids_scrapy for val in sublist]
    
    df_final = pd.DataFrame([ids_scrapyf, titlef, geo_tag, where, cleaned_m4m, agef, heightf, btypef, cleaned_body, datetimes, has_image, has_maps, url]).T
    df_final.columns = ["Ids", "Title", "Geo_Tag", "Where", "Who_to", "Age", "Height", "Body_type", "Body", "Datetime", "Has_Image", "Has_Maps", "URL"]
    df_final.insert(2, "City", site)
    return df_final

# First round
cities_first=[]
for city in cities:
    cities_first.append(extraction(city))
 

all_cities = pd.concat(cities_first, axis=0)


# Second Time Around
new_cities = []
for city in cities:
    new_cities.append(extraction(city))

all_new_cities = pd.concat(new_cities, axis=0)


# Combining the history with the present data
id_mask = ~all_new_cities.Ids.isin(all_cities.Ids.values)
filtered_new = all_new_cities[id_mask]
combined = pd.concat([all_cities, filtered_new], axis=0)

# Sorting the data
group = combined.sort_values('City')