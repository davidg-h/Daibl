# Daibl (Discord AI Bot Learning)

[![Contributors][contributors-shield]][contributors-url]
[![python](https://img.shields.io/badge/min._Python-3.9-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org)
[![pytorch](https://img.shields.io/badge/PyTorch-latest-EE4C2C.svg?style=flat&logo=pytorch)](https://pytorch.org)
![Static Badge](https://img.shields.io/badge/Example%20Badge-8A2BE2)
![Static Badge](https://img.shields.io/badge/Example%202-blue)

---

<details>
<summary>Table of Contents:</summary>

- [About the project](#about-the-project)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
- [Development environment](#development-environment)
  - [Folder structure](#folder-structure)
  - [Modules](#modules)
  - [Docker environment](#docker-environment)
  - [Virtual environment activation](#virtual-environment-activation)
  - [For Pair-Programming](#for-pair-programming)
- [Contributing](#contributing)
- [Authors](#authors)
- [License](#license)
- [Remarks](#remarks)

</details>

## About The Project

Daibl is a university project to help students learn more about AI-Technologies. The acronym Daibl stands for **D**iscord **AI** **B**ot **L**earning. Daibl is a bot inspired by Jarvis (Iron Man) which can answer general and TH Nuernberg related questions, to help students (especially new ones) navigate their school life easier.



## Getting Started

![Setup](assets/docs/docs_images/clone_project.gif)

Create a $`\textcolor{red}{\text{.env file}}`$ in the **[daibl/discord_bot/main](discord_bot/main/example.env)** directory and set the environment variables: (read the [remarks](#remarks) after creating the file)

```sh
# .env example
DISCORD_TOKEN=<your_token>
DISCORD_GUILD=<guild-or-server_name>
PROJECT_PATH=<path/to/project> # Full path to project to simplify imports (if you want to read further into this google Python Path)
```

### Prerequisites

### Installation

## Usage

TODO add graphic of pipeline and data processing

## Development environment

### Folder structure

```sh
📦assets # resources and assets for the project
 ┣ 📂docs
 ┣ 📂ffmpeg-6.0-full_build
 ┗ ...
📦discord_bot
 ┣ 📂main
 ┃  ┣ 📂Bot     # Bot application
 ┃  ┣ 📂LLM     # Communicating module with Large-Language-models
 ┃  ┣ 📂STT     # Module for live transcription (ASR)
 ┃  ┣ 📂TTS_Bot # Module for text-to-speech
 ┃  ┣ 📂util    # Module for utilities
 ┃  ┣ 📜main.py # main entry point
 ┃  ┗ 📜.env    # token and keys
 ┗ (📂test) # possible test folder
 ```

### Modules

### Docker environment

The discord bot should be runable in any environment. For this purpose we use Docker. So file paths may be different when running on Windows. Devs should read through our [Docker documentation](assets/docs/Docker.md) to work on the project.

### **Virtual environment activation**

The virtual environment is used to make packaging easier and to only install the needed dependencies. To setup the virtual environment look into the corresponding [virtual environment documentation](assets/docs/Venv.md)

### For Pair-Programming

#### Change user.name and user.email to evenly split contributions

```sh
git config user.name <UserName>
git config user.email <Email-of-account>
```

## Contributing

- [ ] [Create](https://docs.gitlab.com/ee/user/project/repository/web_editor.html#create-a-file) or [upload](https://docs.gitlab.com/ee/user/project/repository/web_editor.html#upload-a-file) files
- [ ] [Add files using the command line](https://docs.gitlab.com/ee/gitlab-basics/add-file.html#add-a-file-using-the-command-line) or push an existing Git repository with the following command:

```sh
mkdir daibl
cd daibl
git clone https://git.informatik.fh-nuernberg.de/devpsoft_studios/daibl.git
```

or

```sh
cd existing_repo
git remote add origin https://git.informatik.fh-nuernberg.de/devpsoft_studios/daibl.git
git branch -M main
```

## Authors

## License

Click [this](/LICENSE) to read the license.

---

## Remarks

You must adjust paths in some files / python scripts. For example the [tts-training-file line 35](discord_bot/main/TTS_Bot/Train_Voice/Training_Scripts/train_vits_win.py).

**In general:**
Every time the user/developer has to make a change for path reasons it will be marked as

```
# !!Change!! ...
```

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
<!-- https://shields.io/badges (Bagde generator)-->
[contributors-shield]: https://img.shields.io/github/contributors/github_username/repo_name.svg?style=for-the-badge
[contributors-url]: https://github.com/github_username/repo_name/graphs/contributors