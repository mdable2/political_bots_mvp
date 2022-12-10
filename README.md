# political_bots_mvp
As part of the AssemblyAI Hackathon 2022, this project will serve as an MVP for "political bots" where you can talk directly to the AI form of Joe Biden and Donald Trump! This application also comes with an "explainability" option to showcase why the model chose to respond in the way it did - this can also be used to reference what the politician said previously about a given subject.

## Work Log
* [12/9/22 12:40PM] Working on cloning [GODEL](https://github.com/microsoft/GODEL) to start setting up the training pipeline. Also will start work on creating a scraper to get the data from [factba](https://factba.se/). I checked `robots.txt` and it doesn't say I can't scrape so I'm going to use this as my data source since they have transcripts for Joe Biden & Donald Trump.

* [12/9/22 3:14PM] Got `GODEL` cloned and the scraper written. Scraping now. Going to start on wireframing the front end now. And need to write a second scraper.

* [12/9/22 7:09PM] Things have finished scraping. So now I gotta do some data engineering to get it in the right format for `GODEL` to train on. Also starting the piping of the actual app.