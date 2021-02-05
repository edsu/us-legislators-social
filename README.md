# us-legislators-social

This project is a small experiment with all the fine data about US
Congressional legislators over in the [congress-legislators] repository. In
addition to all the information about House representatives and Senators One of
the things that is available in this repository are links to politician's
social media accounts. To keep things simple this file only includes
information for current officials. So when legislators leave office their entry
in this file is removed. The information isn't rolled into the other historical
data, which makes looking back at what these accounts were impossible.

But fortunately Git has a record of the old entries. This repository contains
an amalgamation of the *legislators-current.yaml* and
*legislators-historical.yaml* data files that is merged with the
*legislators-social-media.yaml* file. In order reconstruct the historical data
the git revision history for *legislators-social-media.yaml* is wound backwards
and parsed.

Here's an example of a reconstituted entry:

```yaml
- id:
    bioguide: B001288
    lis: S370
    thomas: '02194'
    govtrack: 412598
    opensecrets: N00035267
    votesmart: 76151
    wikipedia: Cory Booker
    ballotpedia: Cory Booker
    fec:
    - S4NJ00185
    cspan: 84679
    maplight: 2051
    wikidata: Q1135767
    google_entity_id: kg:/m/06p430
    icpsr: 41308
  name:
    first: Cory
    middle: Anthony
    last: Booker
    official_full: Cory A. Booker
  bio:
    birthday: '1969-04-27'
    gender: M
  terms:
  - type: sen
    start: '2013-10-31'
    end: '2015-01-03'
    state: NJ
    class: 2
    party: Democrat
    state_rank: junior
    url: http://www.booker.senate.gov
    phone: 202-224-3224
    address: 141 Hart Senate Office Building Washington DC 20510
    office: 141 Hart Senate Office Building
    contact_form: http://www.booker.senate.gov/?p=contact
  - type: sen
    start: '2015-01-06'
    end: '2021-01-03'
    state: NJ
    class: 2
    party: Democrat
    state_rank: junior
    url: https://www.booker.senate.gov
    phone: 202-224-3224
    address: 717 Hart Senate Office Building Washington DC 20510
    office: 717 Hart Senate Office Building
    contact_form: https://www.booker.senate.gov/?p=contact
    fax: 202-224-8378
  - type: sen
    start: '2021-01-03'
    end: '2027-01-03'
    state: NJ
    class: 2
    state_rank: junior
    party: Democrat
    url: https://www.booker.senate.gov
    contact_form: https://www.booker.senate.gov/?p=contact
    address: 717 Hart Senate Office Building Washington DC 20510
    office: 717 Hart Senate Office Building
    phone: 202-224-3224
  social:
    twitter:
      senbooker: '2017-09-28'
      senbookeroffice: '2017-02-24'
      corybooker: '2016-05-09'
      senbookerofc: '2013-11-23'
    twitter_id:
      2167097881: '2015-08-02'
      15808765: '2017-02-21'
    youtube:
      sencorybooker: '2014-02-05'
    youtube_id:
      uc6flymqns1vettnvza7gopa: '2015-02-17'
```

## Install & Run

You can simply use the `legislators.yaml` file that is included here. But if
you want you can rerun it at any time, which will clone the
congress-legislators repository, wind back the revisions and write out a new
legislators.yaml:

    pip3 install -r requirements.txt
    python3 history.py

One of the downsides to winding back the revision history is that it also can
accidentally bring in bugs that have been fixed. If you notice any please
submit an issue ticket. Maybe it makes sense to roll some of this functionality
into the original repository...

[congress-legislators]: https://github.com/unitedstates/congress-legislators
    
