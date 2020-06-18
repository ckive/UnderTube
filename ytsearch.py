from youtube_search import YoutubeSearch as yts

results = yts('search terms', max_results=50).to_dict()
len(results)
