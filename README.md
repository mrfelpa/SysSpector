# Installation and Configuration

- Requirements

- Python 3.8+
- Pip
- Virtualenv (optional, but recommended)
- Dependencies listed in the requirements.txt file

# Clone the repository
        
        git clone https://github.com/mrfelpa/SysSpector.git

        cd SysSpector

# Create a virtual environment

    python -m venv venv
    source venv/bin/activate # On Windows: venv\Scripts\activate

# Install the dependencies

    pip install -r requirements.txt

- The tool uses an API key for authentication, which must be configured as an environment variable:

      export API_KEY='your key'

- On Windows (PowerShell):
  
      env:API_KEY='your key'

  # Use

  - Start the API Server

        python sysspector.py --mode api

   This will start a Flask server listening on ***port 8000.***

  # CLI for Analysis

- The tool includes a command line interface (CLI) for interaction:

        python sysspector.py --mode cli
        python syspector.py analyze --system "SYSTEM_ID"
  
  # Examples

        curl -X POST http://localhost:8000/graphql -H "Content-Type: application/json" -H "Authorization: Bearer your key" --data '{"query":"{ getSystemInfo { docker ip hostname } }"}'

- This command queries System Information via GraphQL.
 
        curl -X POST http://localhost:8000/graphql -H "Content-Type: application/json" -H "Authorization: Bearer your key" --data '{"query":"{ analyzeSystemInfo { prediction confidence } } "}'

- This command performs anomaly detection.

# PS If the server does not start because port 8000 is already in use, change the port manually:

        python sysspector.py --mode api --port 8080
