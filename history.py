#!/usr/bin/env python3

import re
import git
import rtyaml
import pathlib
import datetime

# get the git repo if needed
repo_dir = pathlib.Path('congress-legislators')
if not repo_dir.is_dir():
    git.Repo.clone_from('https://github.com/unitedstates/congress-legislators', repo_dir)
repo = git.Git(repo_dir)

def main():
    repo = git.Repo(repo_dir)

    print('loading all legislators')
    legis = rtyaml.load(open(repo_dir / 'legislators-historical.yaml'))
    legis.extend(rtyaml.load(open(repo_dir / 'legislators-current.yaml')))

    # examine each commit to the social yaml file and merge into results
    for commit in repo.iter_commits(paths=['legislators-social-media.yaml']):
        created = datetime.datetime.fromtimestamp(commit.committed_date)
        print('examining', created)
        for blob in commit.tree.blobs:
            if blob.path == 'legislators-social-media.yaml':
                try:
                    social = rtyaml.load(blob.data_stream)
                    merge(social, legis, created)
                except rtyaml.yaml.error.YAMLError as e:
                    print("yaml in commit didn't parse: {}".format(commit))

    output = path.Path('legislators.yaml')
    print('writing {}'.format(output))
    output.open('w').write(rtyaml.dump(legis))


def merge(social, legis, committed):
    "merge the social information into the legisltors, recording the date if needed"
    if type(social) != list:
        return

    date = committed.strftime('%Y-%m-%d')
    for s in social:

        # get the legislator
        l = find(s['id']['bioguide'], legis)

        # set the social property if needed
        if not 'social' in l:
            l['social'] = {}

        # add any new social info
        for platform, profile_id in s['social'].items():
            # youtube, fb, twitter, insta have case insensitive handles
            if type(profile_id) == str:
                profile_id = profile_id.lower()

            # ignore integer ids that aren't in platform ids, so we don't pull
            # in bugs in the data
            if "_id" not in platform and re.match(r'^\d+$', str(profile_id)):
                continue

            if platform not in l['social']:
                l['social'][platform] = {}
            if profile_id not in l['social'][platform]:
                l['social'][platform][profile_id] = date
            if date < l['social'][platform][profile_id]:
                l['social'][platform][profile_id] = date


def find(id, legis):
    "Find the legislator with bioguide id"
    matches = list(filter(lambda l: l['id']['bioguide'] == id, legis))
    assert len(matches) == 1
    return matches[0]


if __name__ == "__main__":
    main()

