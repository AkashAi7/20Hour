# 20Hour Learning Tool - README

## Introduction
Welcome to the 20Hour Learning Tool! This project is a Generative AI-based tool developed using Azure OpenAI, Python, and Flask. Inspired by the principle of the "20-Hour Learning Method" popularized by Josh Kaufman, this tool aims to help users quickly acquire new skills by focusing on deliberate and efficient learning practices.

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Contributing](#contributing)
- [License](#license)

## Features
- **Generative AI Assistance**: Leverages Azure OpenAI to provide intelligent responses and learning guidance.
- **Flask Web Interface**: Easy-to-use web interface built with Flask.
- **Python Backend**: Robust backend using Python for processing and handling requests.
- **20-Hour Learning Framework**: Implements the 20-hour learning principle to help users master new skills efficiently.
- **Customization**: Easily customizable to fit various learning topics and user needs.

## Installation
To set up the 20Hour Learning Tool on your local machine, follow these steps:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/20Hour.git
   cd 20Hour
   



2. **Set Up a Virtual Environment (optional but recommended):**

    ```bash
       python3 -m venv venv
      source venv/bin/activate   # On Windows, use `venv\Scripts\activate`

3. **Install Dependencies:**

    ```bash
   pip install -r requirements.txt
   Configure Environment Variables:

4. **Create a .env file in the project root directory and add your Azure OpenAI credentials:**
   env
   AZURE_OPENAI_KEY=your_openai_key
   AZURE_OPENAI_ENDPOINT=your_openai_endpoint


5. Run the Flask Application:

   ```bash
    flask run
   
## Usage
Once the Flask application is running, open your web browser and navigate to http://127.0.0.1:5000. You will be presented with the 20Hour Learning Tool interface where you can start your learning journey.

## Key Functionalities
Skill Selection: Choose the skill you want to learn.
Guided Learning: Follow the steps provided by the AI to efficiently learn the new skill.
Progress Tracking: Monitor your learning progress and adjust your approach based on feedback.
Configuration
The 20Hour Learning Tool can be configured to suit different learning needs. Key configurations include:

Learning Modules: Customize or add new learning modules in the modules/ directory.
AI Settings: Adjust AI parameters in the config.py file to fine-tune the responses and guidance provided.
## Contributing
We welcome contributions to enhance the 20Hour Learning Tool. To contribute:

Fork the repository.
Create a new branch: git checkout -b feature/your-feature-name.
Commit your changes: git commit -m 'Add new feature'.
Push to the branch: git push origin feature/your-feature-name.
Open a pull request.
Please ensure your code adheres to our coding standards and includes relevant tests.



