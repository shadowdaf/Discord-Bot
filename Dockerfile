FROM python:3.8
COPY startup.sh /
RUN chmod 755 /startup.sh
RUN mkdir DiscordBot
RUN cd DiscordBot
ENTRYPOINT ["/bin/bash","-c","/startup.sh"]