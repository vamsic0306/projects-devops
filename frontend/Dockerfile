# frontend dockerfile
###############################################################
# FRONTEND DOCKERFILE (React + Vite)
# Produces a lightweight NGINX container
###############################################################

# Build stage
FROM node:20-alpine as build

WORKDIR /app
COPY package.json package-lock.json* ./
RUN npm install --legacy-peer-deps

COPY . .

RUN npm run build

# Production NGINX image
FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html

EXPOSE 3000

CMD ["nginx", "-g", "daemon off;"]
