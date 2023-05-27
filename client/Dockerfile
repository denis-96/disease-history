FROM node:18-alpine as buil-stage

WORKDIR /app

COPY package.json .

RUN npm install

COPY . .

RUN npm run build


FROM nginx:stable-alpine

ARG PORT

COPY nginx.conf /etc/nginx/conf.d/default.conf.template

COPY entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh

RUN rm -rf /usr/share/nginx/html/*

COPY  --from=buil-stage  /app/build /usr/share/nginx/html

EXPOSE ${PORT}

CMD [ "/entrypoint.sh" ]
