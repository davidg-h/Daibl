FROM python:3.9

WORKDIR /app

RUN pip3 install pip setuptools wheel --upgrade
RUN apt-get update && apt-get install -y ffmpeg

# TODO tokens will be with .env file es authetication
ENV DISCORD_TOKEN=<your_token>
ENV DISCORD_GUILD=<guild_or_server_name>
ENV HUGGINGFACEHUB_API_TOKEN=<your_api_token>
ENV PROJECT_PATH=<path/to/project> # Full path to project to simplify imports (if you want to read further into this google Python Path)
ENV DATABASE_PATH=<path/to/database_of_context_documents>

COPY sanitized_req.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

# check if ffmpeg is installed
RUN ls /usr/bin/ffmpeg
# move it to project folder
RUN mv /usr/bin/ffmpeg /app/assets

################################
# when container is starting main.py is executed
################################

CMD [ "python", "discord_bot/main/main.py" ]
