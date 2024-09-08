# Listing Owner Project

This project is a Django web application that uses PostgreSQL as the database and is containerized with Docker. Follow the steps below to set up and run the project.

## Prerequisites

Make sure you have the following installed on your machine:

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Getting Started

### 1. Clone the Repository

First, clone the repository to your local machine and navigate into the project directory:

```bash
https://github.com/pouriafarhadi/RealtynaTask__ListingOwner.git
```
### 2. Build the Docker Containers
Build the Docker images for the project by running:

```bash
docker-compose build
```
This command will set up the necessary Docker containers for your Django app, PostgreSQL database, and pgAdmin.

### 3. Start the Services
Once the build is complete, start the Docker containers by running:
```bash
docker-compose up
```
Run Django commands:
### 4. Run Command
You can run any Django management command using:
```bash
docker-compose exec backend sh -c "python manage.py makemigrations" 
docker-compose exec backend sh -c "python manage.py migrate" 
```
This will start the following services:

### backend:
#### The Django application running on  
```plaintext
http://localhost:8000
```


### db: PostgreSQL database
#### pgadmin: PostgreSQL management interface available on
```plaintext
http://localhost:5050
```

