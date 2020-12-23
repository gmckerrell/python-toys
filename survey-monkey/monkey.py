import requests
import json

class Client:
    """
    This class is used to make requests to the survey monkey API.

    api_token  - access token
    cache_file - if specified will load and save a local cache of any
                 retrieved data when client is used in a "with" context.
    """
    def __init__(self, api_token, cache_file=None, **request_kargs):
        self._session = requests.session()
        self._baseUrl = "https://api.surveymonkey.net/v3"
        self._request_kargs = request_kargs
        self._headers = {
            "Authorization": f"bearer {api_token}",
            "Content-Type":  "application/json",
            "Accept":        "application/json"
            
        }
        self._cache_file = cache_file
        self._cache = {}

    def get(self, path):
        if not path in self._cache:
            self._cache[path] = self._session.get(
                f"{self._baseUrl}/{path}",
                headers=self._headers,
                **self._request_kargs
            ).json()

        return self._cache[path]

    def __enter__(self):
        if self._cache_file:
            try:
                with open(self._cache_file) as file:
                    self._cache = json.load(file)
            except FileNotFoundError:
                pass
        return self
    
    def __exit__(self, type, value, traceback):
        if self._cache_file:
            with open(self._cache_file, 'w') as file:
                json.dump(self._cache, file, indent=" ")

class Survey:
    """
    Use a client to retrieve survey monkey data then
    convert the survey results into a python friendly format
    """
    def __init__(self, client, detail):
        self.id        = detail['id']
        self.title     = detail['title']
        self.nickname  = detail['nickname']
        self._client   = client
        self._basepath = f"surveys/{self.id}"

    def details(self):
        return self._client.get(f"{self._basepath}/details")

    def questions(self):
        questions = {}
        choices = {}
        rows = {}
        for page in self.details()["pages"]:
            for question in page["questions"]:
                questions[question["id"]] = question
                if "answers" in question:
                    answers = question["answers"]
                    if "rows" in answers:
                        for row in answers["rows"]:
                            rows[row["id"]] = row["text"]
                    if "choices" in answers:
                        for choice in answers["choices"]:
                            choices[choice["id"]] = choice["text"]

        results = []
        question_list = []
        results.append(question_list)
        for r in self.responses():
            question_list.clear()
            response = []
            for page in r["pages"]:
                for q in page["questions"]:
                    question = questions[q["id"]]
                    answers  = {}
                    for a in q["answers"]:
                        if "row_id" in a:
                            row_name = rows[a["row_id"]]
                        else:
                            row_name = "_no_rows"
                        if "choice_id" in a:
                            answer = choices[a["choice_id"]]
                        if "text" in a:
                            answer = a["text"]
                        if question["family"] in ("single_choice", "open_ended"):
                            answers[row_name] = answer
                        else:
                            values = answers.setdefault(row_name, [])
                            values.append(answer)
                    if "_no_rows" in answers :
                        response.append(answers["_no_rows"])
                    else:
                        response.append(answers)
                    question_list.append(question["headings"][0]["heading"])

            results.append(response)
        return results

    def responses(self):
        responses = self._client.get(f"{self._basepath}/responses")
        results = []
        for response in responses["data"]:
            results.append(
                self._client.get(
                    f"{self._basepath}/responses/{response['id']}/details"
                )
            )
        return results

def surveys(client):
    """
    get a list of Survey instances
    """
    return [
        Survey(client, detail) for detail in client.get("surveys")['data']
    ]
