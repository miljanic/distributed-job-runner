FROM node:13-alpine
ENV NODE_ENV development

WORKDIR /app
COPY ./package.json ./package-lock.json  ./
RUN npm install
COPY ./ ./
EXPOSE 3000
CMD [ "npm", "run", "start" ]
