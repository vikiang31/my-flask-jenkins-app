# My Flask Jenkins App

Flask-based weather tracking app with automated testing, Docker image build, Jenkins pipeline, and Docker Hub publishing.

## Project Overview

This project started as a simple Flask web app and was later extended into a small weather tracker application.

The app:
- serves a home page
- exposes a health check endpoint
- stores weather observations in a SQLite database
- allows reading and adding weather records through API endpoints

The CI pipeline:
- pulls the code from GitHub
- runs automated tests with pytest
- builds a Docker image
- pushes the image to Docker Hub

