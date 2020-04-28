FROM node:10

# install gettext for envsubst
RUN apt-get update
RUN apt-get install -y gettext-base

ENV PORT 8080

ADD . /srv/staticapp
WORKDIR /srv/staticapp
RUN npm install

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]

EXPOSE 8080
CMD ["npm", "start"]