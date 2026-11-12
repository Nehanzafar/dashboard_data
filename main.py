from SourceProcessing.LastFM.LastFM_processing import LastFMProcesser
from ExportProcessing.LastFM.data_processing import processer

# import the transformers
import ExportProcessing.transformers.LastFM as LastFM
import ExportProcessing.transformers.Hardcover as Hardcover


# import Harcover processors
from SourceProcessing.HardCover.HardCover_processing import HardCoverProcessor

def main():

    """
    This is the Fetching and Processing sequence for LastFM API
    The api is a simple rest api and the processor only fetches using HTTP
    and pulls data and transforms it into usable data from JSON to tabular data that is stored in
    Excel and SQL database
    """
    process = LastFMProcesser()
    recenttracksJSON = process.fetch_data({
        "method": "user.getRecentTracks",
        "format": "json",
        "limit": 10
    })

    processer_recenttracks = processer(recenttracksJSON)

    # transform the data using prebuilt transformers
    processer_recenttracks.process(LastFM.transformer_recenttracks)
    

    processer_recenttracks.convert_to_sql()
    processer_recenttracks.convert_to_excel()

    topartistsJSON = process.fetch_data({
    "method": "user.gettopartists",
    "format": "json",
    "limit": 10
    })
    processer_topartists = processer(topartistsJSON)
    processer_topartists.process(LastFM.transformer_topartists)

    processer_topartists.convert_to_excel()
    processer_topartists.convert_to_sql()



    """
    This is the processor for HardCover that is a Graphql API
    The processor requests the information and tranforms it the same way we transform LastFM data
    """
    process = HardCoverProcessor()

    userlibJSON = process.fetch_data(
        """
        query MyLibrary {
        me {
            id
            username

            user_books {
            id
            status_id
            rating
            date_added
            first_read_date
            last_read_date

            book {
                id
                title
                description
                pages
                release_year
                rating

                contributions {
                author {
                    id
                    name
                }
                }
                image {
                    height
                    id
                    imageable_id
                    imageable_type
                    ratio
                    url
                    width
                }
            }

            user_book_reads {
                started_at
                finished_at
                progress_pages
                progress_seconds
            }
            }


        }
        }
        """
    )

    processer_userlib = processer(userlibJSON)

    # transform the data using prebuilt transformers
    processer_userlib.process(Hardcover.transformer_userlib)
    

    processer_userlib.convert_to_sql()
    processer_userlib.convert_to_excel()

    

if __name__ == "__main__":
    main()



