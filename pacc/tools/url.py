from urlextract import URLExtract

extractor = URLExtract()


def getURLsFromString(string): return extractor.find_urls(string)
