import os
import requests
import geocoder
from bs4 import BeautifulSoup
from pyzillow.pyzillow import ZillowWrapper, GetDeepSearchResults
os.environ["GOOGLE_API_KEY"] = open('tokens/google-token.txt').read()
os.environ['ZILLOW_API_KEY'] = open('tokens/zillow-token.txt').read()

def get_zillow_image(url):
    """
        Returns the Zestimate for a given url input, or None if that address is not listed.
    """
    req_headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.8',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
    }
    with requests.Session() as s:
        r = s.get(url, headers=req_headers)
        soup = BeautifulSoup(r.content, 'html.parser')
    img = soup.find_all('img')
    img_src = img[0]['src']
    return img_src

def address_to_price_and_image(address):
    """
    Returns the tuple (zestimate, img_src)
    or returns -1 if the address couldn't be found
    or returns -2 if the address isn't listed on Zillow
    """
    google_api_key = os.environ["GOOGLE_API_KEY"]
    zillow_api_key = os.environ['ZILLOW_API_KEY']
    base_url = "https://maps.googleapis.com/maps/api/geocode/json"
    endpoint = f"{base_url}?address={address}&key={google_api_key}"
    r = requests.get(endpoint)
    if r.status_code not in range(200, 299):
        return 'INVALID ADDRESS'
    results = r.json()['results'][0]
    address = results['formatted_address']
    address_stub = address[:address.index(',')]
    zip_code = address.replace(', USA', '')[-5:]
    zillow_data = ZillowWrapper(zillow_api_key)
    try:
        house_data = zillow_data.get_deep_search_results(address_stub, zip_code, True)
        house_data = GetDeepSearchResults(house_data)
        zestimate = int(house_data.zestimate_amount)
        zestimate = '$' + f'{zestimate:,}'
        zillow_id = house_data.zillow_id
        url_for_img_search = 'https://www.zillow.com/homedetails/' + zillow_id + '_zpid/'
        img = get_zillow_image(url_for_img_search)
        return [zestimate, img]
    except Exception as e:
        return 'HOUSE NOT FOUND'
