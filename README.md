# scrape_internet

- Python script for scraping multiple domains at once and passing that information directly to a RDF database.

## Requirements

- Python 3.10

  ```bash
  python --version
  ```

## Setup

- ### 1. Install python3 packages

  ```bash
  cd ./scrape_internet
  python -m pip install -r ./requirements.txt
  ```

- ### 2. Install Firefox; Download `geckodriver` and add to your PATH

  - [Download Firefox](https://www.mozilla.org/en-US/firefox/new/)

    - **Linux**:

      ```bash
      sudo apt-get install firefox
      ```

  - Download `geckodriver` and add to your `PATH` variable

    - [Download `geckodriver`](https://github.com/mozilla/geckodriver/releases) for your respective operating system.
    - Unzip `geckodriver`/`geckodriver.exe` file. Move file into a preferred `PATH` directory.
    - Append the preferred directory to your `PATH` variable.
      - **[Windows Guide](https://www.computerhope.com/issues/ch000549.htm)**
      - **Linux**:
        - Append to your `.bashrc`/`.zshrc`

          ```bash
          export PATH="$HOME/geckodriver_dir/:$PATH"
          ```

  - WSL Setup

    - [Guide to install VcXsrv for running Firefox on WSL2](https://www.youtube.com/watch?v=4SZXbl9KVsw)

- ### 3. Update credentials

  - Edit credential files in folder `./credentials`

  - Ex: `./credentials/amazon.json`

    ```json
    {
        "email": "example@gmail.com",
        "password": "TEAM@blpl7get@wulk"
    }
    ```

## Example

- Command

  ```bash
  python ./run.py --url "https://www.bestbuy.com/site/apple-airtag-silver/6461348.p?skuId=6461348"
  ```

- Response

  ```json
  [{"type": "product", "productTitle": "Apple - AirTag - Silver", "sitePrice": "$29.00\nYour price for this item is $29.00"}]
  ```
