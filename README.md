# s-book-store

## Table of Contents
- [Prerequisites](#prerequisites)
- [Getting Started](#getting-started)
  - [Local Environment](#local-environment)
  - [Docker](#docker)
- [Usage](#usage)
- [License](#license)

## Prerequisites
- Python 3.11+
- Docker (if you want to use Docker for local development)
- gcloud cli and prepared bucket

## Getting Started
Migration is not a part of this service. 
Use [migration folder](./migrations) to prepare db

### Local Environment
1. Clone the repository:

   ```shell
   git clone https://github.com/Nav1Cr0ss/s-storage-api.git
   cd your-app

2. Create venv:

   ```shell
    python -m venv venv
    source venv/bin/activate
   
3. Install the required Python dependencies:
    ```shell
    pip install -r requirements.txt
   
4. Copy .example.env to .env:

    ```shell
    cp .env.example .env
   
5. Auth in gcloud
    ```shell
    gcloud auth application-default login
   
6. Run App

    ```shell
    python main.py
   
### Docker
1. Fill Google credentials file into env `GOOGLE_APPLICATION_CREDENTIALS`

2. Execute docker-compose
    ```shell
    docker-compose-up
   

### Usage
1. Use possible routes to make request and handle book store
    [Book Routes](internal/ports/http/drawing/router)

## License

This code and its associated files are the intellectual property of @Nav1Cr0ss and are provided under the following terms and conditions:

- You may use this code for personal and educational purposes.
- You must seek permission from the owner @Nav1Cr0ss for any other usage, including but not limited to commercial use, distribution, or modification.
- You may not remove or alter this license statement.

For inquiries or permissions, please contact @Nav1Cr0ss on GitHub.

This license is subject to change or modification at any time. By using this code, you agree to the terms and conditions outlined in this license statement.

© @Nav1Cr0ss 2023
