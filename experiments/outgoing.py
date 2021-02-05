#!/usr/bin/env python3

import re
import csv
import twarc
import rtyaml
import requests
import requests_html

http = requests_html.HTMLSession()
twitter = twarc.Twarc()

def main():
    legis = rtyaml.load(open('../legislators.yaml'))
    most = None
    max_accounts = 0

    out = csv.DictWriter(open('outgoing.csv', 'w'), fieldnames=[
        "name",
        "url",
        "url_ok",
        "user_id",
        "new_url"
    ])

    out.writeheader()

    for p in legis:

        if 'social' not in p:
            continue

        # see if the legislator was/is in the 116 and 117 congresses
        is_116 = False
        is_117 = False
        for term in p['terms']:
            if term['end'] == '2021-01-03':
                is_116 = True
            if term['start'] == '2021-01-03':
                is_117 = True

        # if they were in the 116 but not the 117 output their social media
        if is_116 and not is_117:
            row = {'name': p['name']['official_full']}
            if 'twitter' in p['social']:
                username = list(p['social']['twitter'].keys())[0]
                row['url'] = 'https://twitter.com/{}'.format(username)
                row['url_ok'] = check_url(row['url'])
            if 'twitter_id' in p['social']:
                row['user_id'] = list(p['social']['twitter_id'].keys())[0]
                if row['url_ok'] == False:
                    row['new_url'] = get_new_url(row['user_id'])

            out.writerow(row)

def check_url(url):
    resp = http.get(url)
    resp.html.render(sleep=10)
    if resp.is_redirect or resp.status_code != 200:
        return False
    elif re.search(r'This account doesn’t exist', resp.html.text):
        return False
    else:
        return True

def get_new_url(id):
    id = str(id)
    try:
        user = next(twitter.user_lookup([id]))
        if user:
            return 'https://twitter.com/' + user['screen_name']
    except requests.exceptions.HTTPError:
        pass
    return None

if __name__ == "__main__":
    main()
