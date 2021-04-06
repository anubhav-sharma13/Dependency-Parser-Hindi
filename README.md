### Data for Experiment
We have used the corpus which was taken from LTRC’s dataset. The data that was provided was already a parsed data by hindi shallow parser in Shakti Standard Form(SSF). For training , testing and evaluation this parsed data was used.The data can be downloaded from http://ltrc.iiit.ac.in/treebank_H2014/

### How to run the code
1. First clean data was obtained by using some maunal cleanig and the data is stored in the data folder with file names clean_development_data.txt , clean_testing_data.txt , clean_training_data.txt.
2. Next the simplified form of data can be extracted by running the following command
```python
    python3 data_extraction.py clean_training_data.txt > simplified_training_data.txt
```
Similar for development and testing data. The computed data is present in the data folder.
3. Next step of head extraction can be done by running the following command.
```python
    python3 head_extraction.py simplified_training_data.txt > head_extracted_training_data.txt
```
Similar for development and testing data. The computed data is present in the data folder.
4. Next step for dependency extraction can be done by running the following command.
``` python
    python3 dependencies_extraction.py head_extracted_training_data.txt > dependency_extracted_training_data.txt
```
Similar for development and testing data. The computed data is present in the data folder.
5. For finding the indicies of sentences which are not parsable, run the following command.
```python
    python3 arc_eager.py dependency_extracted_training_data.txt > index.txt
```
Similar for development and testing data. The computed data is present in the data folder.
6. To remove the non parsable sentences from dependency_extracted_training_data.txt copy the index list from index.txt file and assign that list to 'NULL_index = []' in clean_data.py file, and then run the following code.
```python
    python3 clean_data.py dependency_extracted_training_data.txt > parsable_dependency_extracted_training_data.txt 
```
Similar for development and testing data. The computed data is present in the data folder.
7. Next step is to create unknown dependencies, which can be done by running the following command.
```python
    python3 unknown_known_dependency_extraction.py parsable_dependency_extracted_development_data.txt > parsable_finalised_dependency_extracted_training_data.txt
```
Similar for development and testing data. The computed data is present in the data folder.
8. All the above steps were done using the codes in 'codes' folder and data in 'data' folder.
9. All the above steps for the codes in 'codes_with_psp' folder and data in 'data_with_psp' folder.
10. Now we will see how to run the models.
11. For models 1-6 training_data.txt, testing_data.txt , development_data.txt is formed by copying from the parsable_finalised_dependency_extracted_training_data.txt, parsable_finalised_dependency_extracted_testing_data.txt, parsable_finalised_dependency_extracted_development_data.txt present in the 'data' folder.
12. For models 7-11 training_data.txt, testing_data.txt , development_data.txt is formed by copying from the parsable_finalised_dependency_extracted_training_data.txt,parsable_finalised_dependency_extracted_testing_data.txt,parsable_finalised_dependency_extracted_development_data.txt present in the 'data_with_psp' folder.
13. Steps for running the models.
1 Form a file data.txt by appending the testing_data.txt, training_data.txt, development_data.txt into data.txt, by running the following commands on terminal.
``` 
    cat training_data.txt >> data.txt
    cat testing_data.txt >> data.txt
    cat development_data.txt >> data.txt
```
2. Run the following command
```python
    python3 get_data_lists.py data.txt
```
3. To train the model, run the following command
```python
    python3 model.py training_data.txt
```
4. To Predict using the trained model, run the following commnand
```python
    python3 predict_model.py testing_data.txt   
```

### Github link to Project repository
Our project can be accessed by clicking    [this](https://github.com/jashna14/Dependency-Parser-Hindi)

### Contribution by each team mate
The work was divided equally among both of us. Almost every component of the project has an input from both of us, so breakdow of work could not be possible. But we both agree that the we both had put in equal time and hard work for successfully completing this project.