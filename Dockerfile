FROM debian:latest
#install required packages
RUN apt-get update --fix-missing -qq && apt-get install -y -q \
	ffmpeg\
	git\
	unzip\
	python3\
	python3-pip\
	sed

#Fetch discord bot files
RUN sudo git clone https://github.com/shadowdaf/Discord-Bot.git
#create .env file
ARG DISCORD_TOKEN
ARG RCON_PASSWORD
RUN echo "DISCORD_TOKEN=${DISCORD_TOKEN}" > /Discord-Bot/.env
RUN echo "RCON_PASSWORD=${RCON_PASSWORD}" >> /Discord-Bot/.env

RUN chmod 755 /Discord-Bot/startup.sh

ENTRYPOINT ["/bin/bash","-c","/Discord-Bot-main/startup.sh"]