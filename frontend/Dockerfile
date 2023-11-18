# syntax=docker/dockerfile:1.6

# DOCKER_BUILDKIT=1 docker image build --tag frontend .
# docker run --rm --name frontend -p 127.0.0.1:8080:8080 -ti frontend
FROM node:20

WORKDIR /app

# copy the package.json and lock file to install dependencies
COPY      package.json /app/
COPY package-lock.json /app/
COPY         yarn.lock /app/
# Install the dependencies and make the folder
RUN yarn

COPY babel.config.js /app/
COPY   vue.config.js /app/
COPY   jsconfig.json /app/

COPY src             /app/src
COPY public          /app/public

# ARG VUE_APP_API_BASE_URL=https://api.quantor.me/v1/
# Build the project and copy the files
# RUN npm run build
# RUN yarn build

# CMD ls
CMD ["yarn", "serve"]
