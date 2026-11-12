import pandas as pd

from utils.logger import logger

# transformer to process the api data for lastFM
# recenttracks data
def transformer_recenttracks(data) -> pd.DataFrame:
    # logger for logging data
    log = logger("LastFM recenttracks Transformer")
    usefullData = data["recenttracks"]["track"]

    
    tracks = []
    images = []
    try:
        # usefullData has the recenttracks.track branch
        for product in usefullData:

            # Main product data
            tracks.append({
                "artist_name": product["artist"]["#text"],
                "artist_mbid": product["artist"]["mbid"],
                "streamable": product["streamable"],
                "album_name": product["album"]["#text"],
                "album_mbid": product["album"]["mbid"],

                "track_name": product["name"],
                "url": product["url"],
                "date": product["date"]["#text"],
            })

            # Image data
            for image in product.get("image", {}):
                images.append({
                    "artist": product["artist"]["#text"],
                    "image_size": image["size"],
                    "image_url": image["#text"]
                })
        data = [
            pd.DataFrame(tracks), 
            pd.DataFrame(images)
            ]

        # all the future transfomers must have both of these attributes
        data[0].attrs['Name'] = 'recenttracks'
        data[0].attrs['type'] = 'tracks'
        data[1].attrs['Name'] = 'recenttracks'
        data[1].attrs['type'] = 'images'

        return data

    except Exception as e:
        log.message("Failed to process data!")
        log.error(e)  

def transformer_topartists(data) -> pd.DataFrame:
    # logger for logging data
    log = logger("LastFM TopArtists Transformer")
    usefullData = data["topartists"]["artist"]

    
    tracks = []
    images = []
    try:
        # usefullData has the recenttracks.track branch
        for product in usefullData:

            # Main product data
            tracks.append({
                "artist_name": product["name"],
                "artist_mbid": product["mbid"],
                "streamable": product["streamable"],
                "playcount": product["playcount"],
                "url": product["url"],
                "rank": product["@attr"]["rank"]
            })

            # Image data
            for image in product.get("image", {}):
                images.append({
                    "artist": product["name"],
                    "image_size": image["size"],
                    "image_url": image["#text"]
                })
        data = [
            pd.DataFrame(tracks), 
            pd.DataFrame(images)
            ]

        # all the future transfomers must have both of these attributes
        data[0].attrs['Name'] = 'topartists'
        data[0].attrs['type'] = 'tracks'
        data[1].attrs['Name'] = 'topartists'
        data[1].attrs['type'] = 'images'

        return data

    except Exception as e:
        log.message("Failed to process data!")
        log.error(e)  
