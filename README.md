# Data engineering Python (Take home Technical assessment).

There are 5 scripts in the root of this repo/directory:
The first three "test_x".py are named for the purpose of the assessment. They are not solely testing files.
The last two files "test_test_x.py" are testing files for their respective number.
- test_1.py
- test_2.py
- test_3.py
- test_test_2.py
- test_test_3.py

In each script is a comment block still left in of what needs to be done to solve the test for that particular script. The remaining comments are there to explain the code.

## Working with the code
- Python3 was used along with the modules for pytest, pylint, requests and pandas.
- To install these please use the command below.
**pip3 install -r requirements.txt**
- Then can run the respective files using the command **python3 test_x.py**
- for the testing files use the command pytest **test_test_x.py**

----------------------------------------------------------------------------------
# Original instructions of the 3 tests(assessment-Ministry of Justice).
### Test 1
This asks you to extract and structure data from the file `sample.log`. You'll need to complete 2 short functions.

When you think you have the answer, run `python test_1.py` and it will be automatically tested.

### Test 2
This asks you do get data from an API and match it with data from the file `people.csv`. 

You're free to approach this however you like. We'll ask you to describe your approach and reasoning during the interview.

### Test 3
This asks you to fix a broken function and then write a unit test for it.
