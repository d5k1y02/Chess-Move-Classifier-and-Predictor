# Chess-Move-Classifier

This program is designed to use datasets from https://database.lichess.org/ but any pgn file should work. Run DataProcessor.py to select games within certain elo ranges. Default is 1000 to 1200 and 10000 games for training and 3000 games for testing. Then run CriteriaClassifier.py on the dataset from the processor to set up the data for training and testing. Note that it inexplicably stops somewhere between 3500 and 4000 positions so it won't process all 10000 games. Finally, train the network CriteriaPredictor.py on the dataset from the classifier.
