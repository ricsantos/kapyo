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
session.get_events()

#Get the Stream link for a given event id
session.get_stream(id="")
```
Check the Docs for more info


## Thanks
Much love to etopiei for his work on Unoffical Kayo Desktop App [MIT](https://github.com/etopiei/kayo)
and matthuisman for doing [the hard work](https://github.com/wrxtasy/plugin.video.kayo.sports/) of documenting the Apis on which this work is based.

