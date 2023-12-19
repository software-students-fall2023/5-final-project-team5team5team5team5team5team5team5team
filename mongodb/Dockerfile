# Use an official MongoDB image as a base image
FROM mongo:latest

# Expose the default MongoDB port
EXPOSE 27017

# Set environment variables, if needed
# ENV MONGODB_VERSION=6.0-ubi8

# Start MongoDB when the container starts
CMD ["mongod", "--bind_ip_all"]
