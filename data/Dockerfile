# This Dockerfile is used to create a container that serves static files from the ./app/data directory
# using http-server. It uses the latest Node.js image and installs http-server globally.
# It sets the command to run http-server with CORS enabled on the ./app/data directory.
FROM node:latest
RUN npm install -g http-server
CMD ["http-server", "./app/data", "--cors"]