FROM debian:latest
#install required packages
RUN apt-get update --fix-missing -qq && apt-get install -y -q \
	ffmpeg\
	curl\
	unzip\
	python3\
	python3-pip\
	sed

#Fetch discord bot files
RUN curl -O -fkSL https://github.com/shadowdaf/Discord-Bot/archive/v0.1.2-alpha.tar.gz
RUN tar xz -f v0.1.2-alpha.tar.gz
RUN mv Discord-Bot-0.1.2-alpha Discord-Bot-main
#create .env file
ARG DISCORD_TOKEN
ARG RCON_PASSWORD
RUN echo "DISCORD_TOKEN=${DISCORD_TOKEN}" > /Discord-Bot-main/.env
RUN echo "RCON_PASSWORD=${RCON_PASSWORD}" >> /Discord-Bot-main/.env

RUN chmod 755 /Discord-Bot-main/startup.sh

ENTRYPOINT ["/bin/bash","-c","/Discord-Bot-main/startup.sh"]