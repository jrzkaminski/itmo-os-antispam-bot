# itmo-os-antispam-bot

---

![License](https://img.shields.io/github/license/jrzkaminski/itmo-os-antispam-bot?style=flat&logo=opensourceinitiative&logoColor=white&color=blue)
[![OSA-improved](https://img.shields.io/badge/improved%20by-OSA-yellow)](https://github.com/aimclub/OSA)

---

## Overview

itmo-os-antispam-bot is a tool designed to automatically protect Telegram supergroups from spam. It identifies and blocks spammers, particularly those posting in Russian, helping maintain a clean and safe communication environment for group members.

---

## Table of Contents

- [Core features](#core-features)
- [Installation](#installation)
- [Contributing](#contributing)
- [License](#license)
- [Citation](#citation)

---
## Core features

1. **Spam Detection**: The bot utilizes a ruBERT model to classify incoming messages in Telegram supergroups as spam or not spam, enabling proactive moderation.
2. **New Member Tracking**: The bot tracks newly joined members of the Telegram group and monitors their first message for potential spam content.
3. **Automated Ban**: Upon detecting a spam message from a new member, the bot automatically deletes the message and bans the user from the group.
4. **Logging and Error Handling**: The bot includes comprehensive logging for debugging and error handling mechanisms to ensure stability and provide insights into its operation.

---

## Installation

Install itmo-os-antispam-bot using one of the following methods:

**Build from source:**

1. Clone the itmo-os-antispam-bot repository:
```sh
git clone https://github.com/jrzkaminski/itmo-os-antispam-bot
```

2. Navigate to the project directory:
```sh
cd itmo-os-antispam-bot
```

3. Install the project dependencies:

```sh
pip install -r requirements.txt
```

---

## Contributing

- **[Report Issues](https://github.com/jrzkaminski/itmo-os-antispam-bot/issues)**: Submit bugs found or log feature requests for the project.

---

## License

This project is protected under the MIT License. For more details, refer to the [LICENSE](https://github.com/jrzkaminski/itmo-os-antispam-bot/tree/main/LICENSE) file.

---

## Citation

If you use this software, please cite it as below.

### APA format:

    jrzkaminski (2024). itmo-os-antispam-bot repository [Computer software]. https://github.com/jrzkaminski/itmo-os-antispam-bot

### BibTeX format:

    @misc{itmo-os-antispam-bot,

        author = {jrzkaminski},

        title = {itmo-os-antispam-bot repository},

        year = {2024},

        publisher = {github.com},

        journal = {github.com repository},

        howpublished = {\url{https://github.com/jrzkaminski/itmo-os-antispam-bot.git}},

        url = {https://github.com/jrzkaminski/itmo-os-antispam-bot.git}

    }

---
