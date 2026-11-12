import pandas as pd

from utils.logger import logger

# transformer to process the api data for HardCover
# UserLib data
def transformer_userlib(data) -> pd.DataFrame:
    # logger for logging data
    log = logger("HardCover UserLib Transformer")
    
    try:
        usefullData = data["data"]["me"][0]["user_books"]
    except Exception as e:
        log.error(f"An Error has occured trying to access the passed data:\n{e}")
    
    books = []
    images = []
    try:
        # usefullData has the recenttracks.track branch
        try:
            for data in usefullData:

                # Main data data
                books.append({
                    "ID": data["id"],
                    "first_read_date": data["first_read_date"],
                    "last_read_date": data["last_read_date"],
                    "status_id": data["status_id"],
                    "book_id": data["book"]["id"],
                    "book_name": data["book"]["title"],
                    "book_description": data["book"]["description"],
                    "book_pages": data["book"]["release_year"],
                    "book_pages": data["book"]["pages"],
                    "book_rating": data["book"]["rating"],
                    "author_name": data["book"]["contributions"][0]["author"]["name"],
                    "author_id": data["book"]["contributions"][0]["author"]["id"],

                })

                # Image data

                images.append({
                    "book_name": data["book"]["title"],
                    "book_id": data["book"]["id"],
                    "image_id": data["book"]["image"]["id"],
                    "image_height": data["book"]["image"]["height"],
                    "image_width": data["book"]["image"]["width"],
                    "image_ratio": data["book"]["image"]["ratio"],
                    "image_url": data["book"]["image"]["url"],
                    })
        except Exception as e:
            log.error(f"Error while Parsing Data:\n{e}")  
        try:
            data = [
                pd.DataFrame(books), 
                pd.DataFrame(images)
                ]

            # all the future transfomers must have both of these attributes
            data[0].attrs['Name'] = 'UserLib'
            data[0].attrs['type'] = 'books'
            data[1].attrs['Name'] = 'UserLib'
            data[1].attrs['type'] = 'images'

            return data
        except Exception as e:
            log.message("Failed to convert data to Pandas dataframe")
            log.error(e)  
    except Exception as e:
        log.message("Failed to process data!")
        log.error(e)  