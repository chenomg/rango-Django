#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import requests


def read_bing_key():
    try:
        with open('bing.key', 'r') as f:
            bing_api_key = f.readline()
    except Exception:
        raise IOError('bing.key file not found')
    return bing_api_key


def run_query(search_terms, results_per_page=10):
    bing_api_key = read_bing_key()
    if not bing_api_key:
        raise KeyError('Bing key not found')
    root_url = 'https://api.cognitive.microsoft.com/bing/v7.0/search'
    offset = 0
    query = "{0}".format(search_terms)
    search_url = "{0}?q={1}&count={2}&offset={3}".format(
        root_url,
        query,
        results_per_page,
        offset,
    )
    results = []
    try:
        headers = {'Ocp-Apim-Subscription-Key': bing_api_key.strip()}
        response = requests.get(url=search_url, headers=headers)
        content = response.content
        json_content = json.loads(content)
        for result in json_content.get('webPages').get('value'):
            results.append({
                'title': result['name'],
                'link': result['url'],
                'summary': result['snippet']
            })
    except Exception as e:
        print('Error when querying the Bing Api')
        print('Error:', e)
        raise Warning('Error when querying the Bing Api')
    return results


def main():
    query = input('Query:')
    results = run_query(query)
    for r in results:
        print(r)


if __name__ == "__main__":
    main()
