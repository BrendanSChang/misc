FROM node:10-alpine
WORKDIR /app
COPY package.json .
RUN npm install
COPY . .
EXPOSE 3000
ARG script=start
ENV SCRIPT=${script}
ENTRYPOINT ["sh", "-c", "npm ${SCRIPT}"]

