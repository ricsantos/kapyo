# Kapyo

Kapyo is a Python library for interacting with Kayo Apis.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install kapyo.

```bash
pip install kapyo
```

## Usage

```python
import kapyo

#activate a kapyo session which will automatically log you in and access your root profile
session = kapyo.setup("Credentials_file.json")

#Check the current events available
session.get_profile_events()

#Get the manifest link for a given event id
stream_links = session.get_stream_links(102331)

#Return some hmtl which contains the player set to play the stream
first_link = stream_link['data'][0]
first_link.to_iframe()

#Or if you going to do something fancy you can access the uri itself
first_link.uri

```


## Thanks
Much love to etopiei for his work on his [Unofficial Kayo Desktop App](https://github.com/etopiei/kayo)
and matthuisman for doing [the hard work](https://github.com/wrxtasy/plugin.video.kayo.sports/) of documenting the Apis on which both this projects are heavily based.

## License & Obvious things

I am not associated with Kayo Sports.
Do not use this package to spam their api servers (you will just get blocked anyways)

MIT License 2021
See License.txt for more info

