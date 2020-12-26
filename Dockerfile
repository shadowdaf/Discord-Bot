FROM python:3.8
RUN apt-get update --fix-missing -qq && apt-get install -y -q \
	ffmpeg
COPY startup.sh /
RUN chmod 755 /startup.sh
RUN mkdir DiscordBot
RUN cd DiscordBot
ENTRYPOINT ["/bin/bash","-c","/startup.sh"]