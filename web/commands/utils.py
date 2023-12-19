
def get_collection_photos(collection_id):
    UNSPLASH_API_URL = f"https://api.unsplash.com/collections/{collection_id}/photos"
    CLIENT_ID = "o4zOf4mzUZwc0c0XYch1G1a70tvMsLenetG_0y56Q2g"
    PER_PAGE = 30
    
    params = {
        "client_id": CLIENT_ID,
        "per_page": PER_PAGE,
        "page": 1
    }

    headers = {'Accept': 'application/json'}

    all_photos = []

    MAX_PAGE = 10

    while True:
        print(f"Fetching {collection_id} page: {params['page']}")
        response = requests.get(UNSPLASH_API_URL, headers=headers, params=params)

        if response.status_code == 200:
            current_photos = response.json()
            all_photos.extend([item['urls']['regular'] for item in current_photos])

            if params['page'] == 10:
                break
            
            if len(all_photos) < int(response.headers.get('X-Total')):
                params['page'] = params['page'] + 1
                time.sleep(3) 
            else:
                break
        else:
            print(f"Failed to fetch collection photos. Status code: {response.status_code}")
            break

    return all_photos