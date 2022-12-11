# Build step #1: build the React front end
FROM node:16-alpine as build-step
WORKDIR /app
ENV PATH /app/node_modules/.bin:$PATH
COPY ./political_bots_frontend/package.json ./
COPY ./political_bots_frontend/package-lock.json ./
COPY ./political_bots_frontend/src ./src
COPY ./political_bots_frontend/public ./public
RUN npm install
CMD [ "npm", "run", "start" ]

# RUN npm run build

# # Build step #2: build an nginx container
# FROM nginx:stable-alpine
# COPY --from=build-step /app/build /usr/share/nginx/html
# COPY nginx.default.conf /etc/nginx/conf.d/default.conf