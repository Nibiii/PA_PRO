# pull the base image
FROM node:alpine

# set the working direction
WORKDIR /app

# add `/app/node_modules/.bin` to $PATH
ENV PATH /app/node_modules/.bin:$PATH

# install app dependencies
COPY package.json ./

COPY package-lock.json ./

COPY . ./

RUN npm install && \
    npm install recharts bootstrap

# add app

# start app
CMD ["npm", "start"]
