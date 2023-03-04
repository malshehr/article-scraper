# Article Scraping App

Article scraper consists of two main parts:

- Flask Application
- Scrapy project

Article scraper allows users to utilize scrapy crawlers to crawl articles and fetch the relevant data from HTML, parses it using 

beautiful soup library, then stores it in MongoDB collection. These crawlers are accessible via the defined Flask APIs.



## APIs

- ```
  /international-page [POST]
  ```

  API for scraping all the articles present on The Guardian International page

- ```
  /guardian-article [POST]
  ```

  API for scraping an article url passed by the user in the body request

- ```
  /find-article/<keyword> [GET]
  ```

​		API for finding articles that are relevant to the provided keyword

## Examples:

- ##### /international-page

  - ###### Request:

    ```
    http post localhost:5000/guardian-article article=https://www.theguardian.com/science/2023/mar/01/uk-satellite-launches-mps-committee-virgin-orbit-failed-mission
    ```

  - ###### Response:

    ```
    HTTP/1.0 200 OK
    Content-Length: 7
    Content-Type: application/json
    Date: Sat, 04 Mar 2023 18:57:30 GMT
    Server: Werkzeug/2.0.2 Python/3.10.6
    
    success
    ```

- ##### /guardian-article

  - ###### Request:

    ```
    http post localhost:5000/guardian-article article=https://www.theguardian.com/science/2023/mar/01/uk-satellite-launches-mps-committee-virgin-orbit-failed-mission
    ```

  - ###### Response:

    ```
    HTTP/1.0 200 OK
    Content-Length: 7
    Content-Type: application/json
    Date: Sat, 04 Mar 2023 18:57:30 GMT
    Server: Werkzeug/2.0.2 Python/3.10.6
    
    success
    ```

- ##### /find-article/*keyword*

  - ###### Request:

    ```
    http get localhost:5000/find-article/DiCaprio
    ```

  - ###### Response:

    ```
    HTTP/1.0 200 OK
    Content-Length: 3190
    Content-Type: application/json
    Date: Sat, 04 Mar 2023 19:01:12 GMT
    Server: Werkzeug/2.0.2 Python/3.10.6
    
    [
        {
            "_id": "64027e1a2dc221fe7b9af329",
            "author": "Maya Yang",
            "content": "\"New details have emerged of the actor Leonardo DiCaprio\\u2019s ties to Jho Low, the Malaysian financier turned fugitive currently wanted by international authorities over his links to one of the world\\u2019s largest corruption scandals.\\nOn Thursday, Bloomberg revealed previously undisclosed details from FBI documents in which authorities interviewed DiCaprio in 2018 about his relationship with Low, who is accused of involvement in a money-laundering scheme of over $4.5bn being siphoned from the Malaysian state investment fund, also known as 1MDB.\\nDiCaprio met Low at a nightclub in 2010 and went on to establish a close relationship, according to the report.\\n\\u201cI was working for him \\u2026 and that business also translates into being social. And so we saw each other more, and there was more interaction,\\u201d DiCaprio told a grand jury, according to the report.\\nThe two had at one point discussed ideas for a $1bn mega-fund for more film-making, as well as a Warner Bros theme park in Asia with rides based on DiCaprio\\u2019s movies. DiCaprio and Low also discussed the development of an eco-friendly resort in Belize.\\nAccording to the report, DiCaprio introduced Low as \\u201cmy man\\u201d while Low called DiCaprio \\u201cL-Dogg\\u201d. The two have also met each other\\u2019s mothers, the report said.\\nIn addition to Low financing the 2013 Oscar-nominated movie The Wolf of Wall Street, which DiCaprio starred in, Low also showered DiCaprio with various luxury gifts. Among those were Marlon Brandon\\u2019s $600,000 Oscar statue, as well as a $9m Jean-Michel Basquiat painting, according to the report.\\nAccording to a 2018 New York Times report, DiCaprio returned those gifts to authorities following investigations into Low\\u2019s alleged siphoning of billions of dollars from the Malaysian fund.\\nIn his interviews with the FBI, DiCaprio said that he had been told that Low\\u2019s wealth hailed from an unknown \\u201cwhale of whales\\u201d in Abu Dhabi, and that Low was the \\u201cMozart of the business world\\u201d.\\nThe Bloomberg report also revealed details from the FBI\\u2019s interviews with Kim Kardashian over her interactions with Low. Kardashian recounted to investigators that she once stayed up till 5am in a Las Vegas casino with Low, where he refused her attempts to return $350,000 worth of winnings.\\n\\u201cWhen Kardashian went to the casino counter to cash out the chips, we learned that she had approximately $350,000 in chips. Kardashian was given a trash bag full of $100 bills estimated to be worth $250,000,\\u201d the documents said.\\nIn 2021, the Department of Justice charged Low, who is believed to be hiding in China, with \\u201cback-channel lobbying\\u201d to influence the government into dropping its investigation into him and others involved in the 1MDB scandal.\"",
            "length": 2814,
            "publish_date": "2023-03-03T19:12:21.000Z",
            "title": "FBI grilled Leonardo DiCaprio over ties to Malaysian fugitive financier – report",
            "url": "https://www.theguardian.com/us-news/2023/mar/03/leonardo-dicaprio-jho-low-malaysian-1mdb-scandal"
        }
    ]
    ```

###### 



