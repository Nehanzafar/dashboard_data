from SourceProcessing.LastFM.LastFM_processing import LastFMProcesser
from ExportProcessing.LastFM.data_processing import processer

# import the transformers
import ExportProcessing.transformers.LastFM as LastFM

def main():
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



if __name__ == "__main__":
    main()



