import json, subprocess
from os.path import join, normpath, dirname

dir_test = normpath(dirname(__file__))


def test_url():
    test_urls: list = json.load(open(join(dir_test, "urls.json")))

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

    output = subprocess.run(
        ["python", "run.py", "--url", *url_list], capture_output=True, text=True
    )

    if len(output.stderr) > 0:
        print(output.stderr)
        raise ValueError("Encountered error while running script. Error printed above.")

    test_results = json.loads(output.stdout)
    for result_item in test_results:
        print(result_item)


if __name__ == "__main__":
    test_url()
