"""
The goal of this project is to get tons of VC money.
"""
import sys
import requests


def fetch_stackoverflow_answer(question):
    """
    This API may not be great for fetching questions,
    https://api.stackexchange.com/docs/search

    Not good for very basic ones, maybe this should only be used on error messages?
    """
    # maybe try v1.1 if limits?
    search_endpoint = 'https://api.stackexchange.com/2.3/search'
    params = {
        'site': 'stackoverflow',
        'intitle': question,
        'sort': 'activity',
        'order': 'desc',
    }

    response = requests.get(search_endpoint, params=params)
    data = response.json()
    #print(f"{question}: {data}")
    if data['items']:
        # TODO parse all question ids to find best https://api.stackexchange.com/docs/types/question
        question_id = data['items'][0]['question_id']
        answer_endpoint = f'https://api.stackexchange.com/2.3/questions/{question_id}/answers'
        answer_params = {
            'site': 'stackoverflow',
            'order': 'desc',
            'sort': 'votes',
            'filter': '!9Z(-wzu0T'  # This filter returns only the answer body
        }
        answer_response = requests.get(answer_endpoint, params=answer_params)
        answer_data = answer_response.json()

        if answer_data['items']:
            return answer_data['items'][0]['body']

    return None


def query_to_prompt(query: str) -> str:
    # if has x, use x tool to append ot query

    if "search for " in query:
        a = query.split("search for ")[1]
        b = a.split(" then ")
        search_query = b[0]
        query_result = fetch_stackoverflow_answer(search_query)
        return f"{b[1]} based on stackoverflow result {query_result}"

    return f"{query}"


if __name__ == '__main__':
    query = " ".join(sys.argv[1:]).lower()

    prompt = query_to_prompt(query)

    # Put this into GPT manually
    print(prompt)


    # TODO needs to be able to make code from scratch
    # TODO needs to be able to edit code on a per-commit basis(e.g. manually add git fns)
