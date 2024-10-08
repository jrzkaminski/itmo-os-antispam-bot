# itmo-os-antispam-bot


![Black](https://img.shields.io/badge/code%20style-black-000000.svg)


[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)


A simple implementation of anti-spam bot for itmo opensource chat.

## Features

Currently, the bot can successfully ban spammers in telegram supergroups based on ruBERT classification. Only supports russian language.

## Planned features
- Expand the bot into other languages;
- Appeal option for blocked users;
- Add option to ban spammers in channels comment section and groups with topics;
- Add docker compose file to run the bot in a container;
- Add a homoglyph tool and language detection instead of explicitly handling homoglyphs.

## How to contribute
Contributions are very welcome, send your PR and I'll review it as soon as I have time.

## Acknowledgements
Thanks to the authors of [fine-tuned ruBERT](https://huggingface.co/NeuroSpaceX/ruSpamNS_V1) for spam-detection.
Thanks to [@MaksimZyryanov](https://github.com/MaksimZyryanov) for QA of the bot to fix some bugs.
Thanks to [Deev Roman](https://github.com/deevroman) for some hints regarding telegram API.
