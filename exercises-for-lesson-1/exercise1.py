import re


def domain_name(url):
    m = re.search("(?:(?:.+:\/\/)?(?:w*\.)?)?(.+?)\.", url)
    return m.group(1)
