# GROUNDTRUTH

### Description
GROUNDTRUTH is a DevTool that suggests automatic documentation changes as you develop your code. Using webhooks, GROUNDTRUTH can receive your code changes and suggest real-time documentation changes. 


### Table of Contents
1. [Installation](#installation)
2. [Dependencies](#dependencies)
3. [Usage](#usage)
4. [Contributing](#contributing)

### Installation
Step-by-step guide to install and run the project.

1. Clone the repository:
   ```bash
   git clone https://github.com/Hassanmushtaq524/groundtruth.git

2. Navigate to your project
   ```bash
   cd groundtruth
   
3. Navigate to your project
   ```bash
   cd groundtruth
   
4. Install required dependencies
   ```bash
   pip install -r requirements.txt

5. Setup backend/.env 
   ```plaintext
   # Database configuration
   GROQ_API_KEY=<your_groq_key>
   OPENAI_API_KEY=<your_openai_key>
   
6. Setup ngrok:
   Login to ngrok and follow instructions
   ```bash
   ngrok HTTP <BACKEND_PORT>

### Usage
Step-by-step guide to use and run the project.

1. Run reflex
   ```bash
   reflex run

Make sure reflex is set up to run. This will launch both your backend and your frontend.

