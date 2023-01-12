import json, urllib.parse, urllib.request, sys

ROOT_URL = "http://webhose.io/search"


def read_webhose_key():
    try:
        with open('search.key', 'r') as f:
            return f.readline().strip()
    except:
        raise IOError('search.key file not found.')


def run_query(search_terms, size=10):

    wh_key = read_webhose_key()

    if not wh_key:
        raise KeyError('Webhose key not found')

    query = urllib.parse.quote(search_terms)
    search_url = f"{ROOT_URL}?token={wh_key}&format=json&q={query}&sort=relevancy&size={size}"
    results = []

    try:
        response = urllib.request.urlopen(search_url).read().decode('utf-8')
        json_response = json.loads(response)

        results = [{
            'title': post['title'],
            'link': post['url'],
            'summary': post['text'][:200]} for post in json_response['posts']
        ]

    except:
        print("Error when querying the Webhose API")

    return results


if __name__ == '__main__':
    # python webhose_search.py "example search"
    try:
        query = sys.argv[1]
    except IndexError:
        query = input("Enter a query to search:\n")

    for result in run_query(query):
        print(f"Title: {result['title']}\nSummary: {result['summary']}\n")