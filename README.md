# x-kom scrapy

## Scrap product data from [x-kom.pl](https://www.x-kom.pl/) only for education purpose.

Used random user-agent with `scrapy-user-agents` to workaround website robots protection.

### Spiders

* base - combined _**gpu**_ and _**cpu**_ spiders
    ```shell
    scrapy crawl gpu
    ```
* gpu
    ```shell
    scrapy crawl gpu
    ```
* cpu
    ```shell
    scrapy crawl cpu
    ```

### Example data [example.json](example.json)

```json
{
  "name": "Karta graficzna NVIDIA Palit GeForce GTX 1050 Ti StormX 4GB GDDR5",
  "link": "https://www.x-kom.pl/p/332036-karta-graficzna-nvidia-palit-geforce-gtx-1050-ti-stormx-4gb-gddr5.html",
  "price": 959.0,
  "last_updated": "2022-06-27T13:53:53.970626"
}
```

* name
* link
* last_updated - ISO format datetime
* price
* old_price - optional (price before discount)

### ~~Docker integration~~ - Warning - playwright is not currently working at Docker image

try out:

```shell
# build xkom-scrapy image
docker build -t xkom-scrapy .
 
 # run xkom-scrapy container and run base spider inside
docker run --rm xkom-scrapy sh -c "scrapy crawl base"
```
