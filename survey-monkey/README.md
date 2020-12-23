# A simple interface to the survey monkey API
The [REST API](https://developer.surveymonkey.com/api/v3/) provided by survey monkey is very comprehensive, but as a consequence can be complex to use.

This modules provides a simplified interface for retrieving survey results in a python friendly manner.
### Required scopes
In order for this module to access survey results the following access scopes need to be assigned to the `API_TOKEN` (See your App settings)
- View Surveys
- View Responses
- View Response Details


## Usage
### `monkey.Client(API_TOKEN, [cache_file=FILENAME])`
- low level client for accessing the API (used by the `Survey` class)
- can specify a `cache_file` which is a file name in which retrieved API data can be stored. The REST API can limit the number of requests per-day, so this provides the means of caching results to avoid too many requests. When used in a [python `with` context](https://docs.python.org/3/whatsnew/2.6.html#pep-343-the-with-statement) any REST API reqponses will be written to the specified file on exit from the context. The next time the code runs it will read data from that cache file, before trying to call the REST API. This means that multiple (wasted) calls are avoided during development.
  - If you want to force retrieval of all data via the REST API, simply delete the cache file.

### `monkey.surveys(CLIENT)`
This function will create and return a list of `Survey` instances that can be used to retrieve results.

### `monkey.Survey`
This class will use a `Client` instance to obtain survey responses, and will combine that with the original survey questions to provide a human readable set of results.

The results will take the following format
```
[
    ["QUESTION_ONE", "QUESTION_TWO", "QUESTION_THREE",...],
    [RESPONSE1_ONE, RESPONSE1_TWO, RESPONSE1_THREE, ...],
    [RESPONSE2_ONE, RESPONSE2_TWO, RESPONSE2_THREE, ...],
    ...
]
```
Each `RESPONSE` element will be shaped according to the question type.
- Open ended
  - `"A_STRING_RESPONSE"`
- Single Choice
  - `"CHOICE_NUMBER_TWO"`
- Multiple Selection
  - `[ONE, TWO, THREE]`
- Multiple Choice
  - `{ "item1": [ONE, TWO, THREE], "item2": "HELLO" }`
  
## Example Code
```python
import monkey
import json

with monkey.Client(API_TOKEN, cache_file="monkey.json") as client:
    for survey in monkey.surveys(client):
        questions = survey.questions()
    
        print(survey.title)
        print(
            json.dumps(questions, indent=" ")
        )
```
