""" stores list of all unique words, tags, root words , chunk tags  in  data_lists.json"""

python3 get_data_lists.py data.txt 


"""  trains the model and stores it into finalised_model.sav """

python3 model.py training_data.txt


""" gets the train model from the finalised_model.py and predicts the output for testing set"""

python3 predict_model.py testing.txt