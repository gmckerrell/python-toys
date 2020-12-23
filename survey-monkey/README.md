# A simple interface to the survey monkey API
The [REST API](https://developer.surveymonkey.com/api/v3/) provided by survey monkey is very comprehensive, but as a consequence can be complex to use.

This modules provides a simplified interface for retrieving survey results in a python friendly manner.

## Usage
### `monkey.Client(API_TOKEN, [cache_file=FILENAME])`
- low level client for accessing the API (used by the `Survey` class)
- can specify a `cache_file` which is a file name in which retrieved API data can be stored. The REST API can limit the number of requests per-day, so this provides the means of caching results to avoid too many requests.

### `monkey.surveys(CLIENT)`

### `monkey.Survey()`

- Firstly you need to create a `client` instance.
- Then the `surveys()` function can be used to get a list of `Survey` objects.


## Example Code
```python
import monkey
import json

with monkey.Client(API_TOKEN, cache_file="monkey.json") as client:
    for survey in monkey.surveys(client):
        questions = surveys[0].questions()
    
        print(survey.title)
        print(
            json.dumps(questions, indent=" ")
        )
```
