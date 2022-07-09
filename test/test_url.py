from test.urls import test_urls
from package.__main__ import run


def test_url():

    assert isinstance(test_urls, list)
    assert len(test_urls) > 0

    # Append urls to list of urls
    url_list = []
    for url_item in test_urls:
        if isinstance(url_item, dict):
            url = url_item["url"]
        elif isinstance(url_item, str):
            url = url_item
        url_list.append(url)

    res = run(["--url", *url_list])

    for result_item in res:
        print(result_item)
