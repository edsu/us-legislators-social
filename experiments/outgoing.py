#!/usr/bin/env python3

import re
import csv
import rtyaml
import requests_html

http = requests_html.HTMLSession()

def make_url(platform, username):
    if platform == 'youtube':
        return 'https://www.youtube.com/user/{}'.format(username)
    elif platform == 'twitter':
        return 'https://twitter.com/{}'.format(username)
    elif platform == 'facebook':
        return 'https://www.facebook.com/{}'.format(username)
    elif platform == 'instagram':
        return 'https://www.instagram.com/{}'.format(username)
    else:
        return None

def check_url(url):
    resp = http.get(url)
    resp.html.render(sleep=10)
    if resp.is_redirect or resp.status_code != 200:
        return False
    if 'twitter.com' in url and re.search(r'This account doesn’t exist', resp.html.text):
        return False
    elif 'facebook.com' in url and re.search(r"This Content Isn't Available Right Now", resp.html.text):
        return False
    elif 'instagram.com' in url and re.search(r"Sorry, this page isn't available.", resp.html.text):
        return False

    return True

def main():
    legis = rtyaml.load(open('legislators-social-media-historical.yaml'))
    most = None
    max_accounts = 0

    out = csv.DictWriter(open('outgoing.csv', 'w'), fieldnames=[
        "name",
        "twitter", "twitter_ok",
        "youtube", "youtube_ok",
        "facebook", "facebook_ok",
        "instagram", "instagram_ok"
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
            for platform, usernames in p['social'].items():
                if len(usernames) > 1:
                    print('yikes', usernames)
                elif platform in ['youtube', 'facebook', 'instagram', 'twitter']:
                    username = list(usernames.keys())[0]
                    url = make_url(platform, username)
                    row[platform] = url
                    row[platform + '_ok'] = check_url(url)
            out.writerow(row)


if __name__ == "__main__":
    main()
