import requests
from bs4 import BeautifulSoup

def extract_metadata(url):
    try:
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        og_title = soup.find('meta', property='og:title')
        og_description = soup.find('meta', property='og:description')
        og_image = soup.find('meta', property='og:image')

        if og_title and og_description:
            title = og_title.get('content')
            description = og_description.get('content')
            image = og_image.get('content') if og_image else None
        else:
            title = soup.title.string if soup.title else None
            meta_description = soup.find('meta', attrs={'name': 'description'})
            description = meta_description.get('content') if meta_description else None
            image = None

        return {'title': title, 'description': description, 'image': image}

    except requests.RequestException as e:
        print(f"Error: {e}")
        return None


