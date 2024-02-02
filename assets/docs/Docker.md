# Steps to get Docker configured to run Daibl in a container

---
-> | [Back](/README.md)
-|-

<details>
<summary>Table of Contents</summary>

- [Install Docker Environment](#install-docker-environment)
  - [Install WSL](#windows-only-install-wsl-windows-subsystem-for-linux)
- [Deploying and pushing an image](#deploying-and-pushing-an-image)
</details>

*Disclaimer: As our bot should be able to run on any machine, this implementation is still in the test phase. Use at own risk.*

## Install [Docker Environment](https://www.docker.com/)

This makes it possible to monitor and run your images and containers.
To get more familiar with docker and its environment read the [documentation](https://docs.docker.com/get-started/)

[Install Docker on other OS](https://docs.docker.com/get-docker/)

Getting started:

- [Learn Docker in 12 Minutes 🐳](https://www.youtube.com/watch?v=YFl2mCHdv24)

- [Learn Docker in 7 Easy Steps - Full Beginner's Tutorial](https://www.youtube.com/watch?v=gAkwW2tuIqE)

### Windows only: Install [WSL](https://learn.microsoft.com/en-us/windows/wsl/install-manual) (Windows Subsystem for Linux)

As most of our devs have a Windows machine this step was necessary to run Docker. The Windows Subsystem for Linux (WSL) is a compatibility layer in Windows that enables users to run a Linux distribution directly on a Windows machine without the need for a traditional dual-boot setup. 

### Get [Docker VS Code Extension](https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-docker) from Microsoft

[Documentation and overview](https://code.visualstudio.com/docs/containers/overview) on how it works in VS Code

---
---

## Deploying and pushing an image

Every working update should be [uploaded/deployed in an image](https://www.youtube.com/watch?v=z58g7_dHeMA) to be accessed and shared with the other developers to make working and maintaining the project more easier.

### Bonus Information:

#### <ins>Limit VM Ressources</ins>

As running a docker container locally is pretty resource intense (especially on ram) you can define a .wslconfig file to [limit the VMs ressources](https://learn.microsoft.com/en-us/windows/wsl/wsl-config).

#### <ins>Debug Docker Container</ins>

As a developer you need to debug code. For this reason debugging a docker container is necessary. Here is a [tutorial](https://www.youtube.com/watch?v=qCCj7qy72Bg ) on how to do it inside a container.

#### <ins>Usefull commands:</ins>

Create an image and name/tag it: (flags are optional)

```sh
docker build --no-cache --progress=plain -t daibl_image .
# -t is a flag to tag/name our image (in our case: "daibl_image")
# --progress=plain shows the output of the commands in the Dockerfile
# --no-cache is pretty self explanatory
```

Sources: [1](https://docs.docker.com/get-started/)

Run the image in a named container:

```sh
docker run --name=daibl -it daibl_image
# --name=<container_name> names the container (in our case: "daibl")
# -it running containers interactively, the interactive flag is just -i, the extra -t (combined as -it above) is an option that allows you to connect to a shell like bash
``` 

Sources: [1](https://docs.docker.com/get-started/02_our_app/), [2](https://epcced.github.io/2020-12-08-Containers-Online/03-running-containers/index.html)

Clean up your docker environment:

```sh
docker system prune    # clean up everything
docker image prune     # clean up unused images
docker container prune # clean up stopped containers
# -f flag bypass the  conformation prompt
```

Sources: [1](https://docs.docker.com/config/pruning/), [2](https://www.freecodecamp.org/news/how-to-remove-all-docker-images-a-docker-cleanup-guide/)