# ChatGPT Clone App

Welcome to the ChatGPT Clone App! This application is a clone of OpenAI's ChatGPT, providing similar functionality for conversational AI. The purpose of this README is to guide you through the process of setting up the app, creating database migrations, and configuring the necessary API keys and security settings.

## Table of Contents

1. [Introduction](#introduction)
2. [Prerequisites](#prerequisites)
3. [Installation](#installation)
4. [Database Migrations](#database-migrations)
5. [Configuration](#configuration)
   - [API Key](#api-key)
   - [Security Key](#security-key)
6. [Running the App](#running-the-app)
7. [Contributing](#contributing)
8. [License](#license)

## Introduction

The ChatGPT Clone App is designed to replicate the functionality of ChatGPT, utilizing the OpenAI API to provide responses to user queries. This app is built with a focus on ease of use and customization, allowing developers to extend and modify its features as needed.

## Prerequisites

Before you begin, ensure you have met the following requirements:
- Python 3.8 or higher
- pip (Python package installer)
- Django 3.2 or higher
- An OpenAI API key

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/chatgpt-clone-app.git
    cd chatgpt-clone-app
    ```

2. Create a virtual environment and activate it:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. Install the required packages:
    ```bash
    pip install -r req.txt
    ```

## Database Migrations

To set up the database, you need to create and apply migrations. Use the following commands:

1. Create migrations:
    ```bash
    python3 manage.py makemigrations
    ```

2. Apply migrations:
    ```bash
    python3 manage.py migrate
    ```

## Configuration

### API Key

To use the OpenAI API, you need to add your API key. Locate the `get_util.py` file and add your API key as shown below:

```python
# get_util.py

OPENAI_API_KEY = 'your-openai-api-key-here'
```
## settings.py
```
SECRET_KEY = 'your-secret-key-here'
```
