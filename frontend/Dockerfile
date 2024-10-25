# Build stage
# Using node:20 as base image for building the application
# We avoid alpine to prevent native dependency issues (like with Rollup)
# 'as build' names this stage so we can reference it later
FROM node:20 as build

# Set the working directory inside the container to /app
WORKDIR /app

COPY package*.json ./

# Clean installation of dependencies
# rm -rf node_modules - Removes any existing node_modules directory
# rm package-lock.json - Removes existing lock file
# npm cache clean --force - Clears npm cache to ensure fresh install
# This aggressive cleaning helps avoid issues with Rollup's optional dependencies
# See: https://github.com/npm/cli/issues/4828
RUN rm -rf node_modules package-lock.json \
    && npm cache clean --force \
    && npm install

# Copy the rest of the project files
COPY . .

# Build the Vue application
RUN npm run build

# Production stage
# Use nginx as the production server
# This creates a new stage with a clean nginx image
# Much smaller than the node image used for building
FROM nginx

# Copy the built application from the build stage
# --from=build specifies to copy from the stage named 'build'
# Copies the contents of /app/dist to nginx's default serving directory
COPY --from=build /app/dist /usr/share/nginx/html

# Document that the container will listen on port 80
EXPOSE 80

# Command to run nginx
# -g daemon off keeps nginx in the foreground
# This is important for Docker as the container stops when the main process stops
CMD ["nginx", "-g", "daemon off;"]

