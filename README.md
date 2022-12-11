# political_bots_mvp
As part of the AssemblyAI Hackathon 2022, this project will serve as an MVP for "political bots" where you can talk directly to the AI form of Joe Biden and Donald Trump! This application also comes with an "explainability" option to showcase why the model chose to respond in the way it did - this can also be used to reference what the politician said previously about a given subject.

## Training Commands

* Note: I have a gaming laptop 3080 so I can't load more into vRAM :( && timing constraints means I'll do less epochs
```
python train.py --model_name_or_path C:\Users\Mark\Code\political_bots\GODEL\models\GODEL-Base --train_file C:\Users\Mark\Code\political_bots\GODEL\data\politics\data\trump_convos_train.json --validation_file C:\Users\Mark\Code\political_bots\GODEL\data\politics\data\trump_convos_val.json --test_file C:\Users\Mark\Code\political_bots\GODEL\data\politics\data\trump_convos_test.json --output_dir C:\Users\Mark\Code\political_bots\GODEL\models\fine_tuned_trump_v1 --per_device_train_batch_size=4 --per_device_eval_batch_size=4 --max_target_length 512 --max_length 512 --num_train_epochs 10 --save_steps 10000 --num_beams 5 --exp_name trump_v1 --preprocessing_num_workers 24
```
```
python train.py --model_name_or_path C:\Users\Mark\Code\political_bots\GODEL\models\GODEL-Base --train_file C:\Users\Mark\Code\political_bots\GODEL\data\politics\data\biden_convos_train.json --validation_file C:\Users\Mark\Code\political_bots\GODEL\data\politics\data\biden_convos_val.json --test_file C:\Users\Mark\Code\political_bots\GODEL\data\politics\data\biden_convos_test.json --output_dir C:\Users\Mark\Code\political_bots\GODEL\models\fine_tuned_biden_v1 --per_device_train_batch_size=4 --per_device_eval_batch_size=4 --max_target_length 512 --max_length 512 --num_train_epochs 10 --save_steps 10000 --num_beams 5 --exp_name biden_v1 --preprocessing_num_workers 24
```

## Work Log
* **[12/9/22 12:40PM]** Working on cloning [GODEL](https://github.com/microsoft/GODEL) to start setting up the training pipeline. Also will start work on creating a scraper to get the data from [factba](https://factba.se/). I checked `robots.txt` and it doesn't say I can't scrape so I'm going to use this as my data source since they have transcripts for Joe Biden & Donald Trump.

* **[12/9/22 3:14PM]** Got `GODEL` cloned and the scraper written. Scraping now. Going to start on wireframing the front end now. And need to write a second scraper.

* **[12/9/22 7:09PM]** Things have finished scraping. So now I gotta do some data engineering to get it in the right format for `GODEL` to train on. Also starting the piping of the actual app.

* **[12/9/22 7:19PM]** Seems to be in the right format now. Going to try to kick off training.

* **[12/9/22 7:26PM]** Ok, we are training first bot. Should take 13 more hours it looks like to get through 10 epochs. 

* **[12/9/22 9:47PM]** Finally figured out a CORS issue. Frontend and backend now communicate. Time to make frontend components.

* **[12/10/22 7:42AM]** Stopped training of first bot and starting second training.

* **[12/10/22 8:41AM]** Figured out how to calculate sentence/paragraph similarity for explanability.

* **[12/10/22 1:10PM]** Going to start working on completing backend first.

* **[12/10/22 6:10PM]** Backend seems to be good. Now doing frontend. Getting compile errors.

* **[12/10/22 8:48PM]** Frontend...I can't get components to communicate with each other how I want so...now I think I'm going to implement redux. Yikes. Also I stopped all model training. Not as good as I want but with time constraints I'll take it.

* **[12/10/22 9:44PM]** Finally have basic redux set up. Now going to try to add component to showcase "explainability".

* **[12/10/22 11:51PM]** Ran into lots of issues getting global state working. Now it works so...now I'm going to add that component. Hoping to get this on AWS tonight. Need to hook up the backend now to the frontend as well.

* **[12/11/22 5:10AM]** In the final stretch. It is going to be close if I finish everything on time! But here we go.

* **[12/11/22 6:39AM]** MVP coding is complete...for now. Going to try and get this on AWS.

* **[12/11/22 12:23PM]** Ended up getting on GCP due to not having enough vCPUs on AWS. Made video and presentation. Going to test one more time.