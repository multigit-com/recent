# report
Recent updated projects with summary and WP API and OpenAI integration

## Setup

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/yourrepository.git
   cd yourrepository
   ```

2. Set up SSH keys for GitHub (if not already done):
   - Generate an SSH key pair:
     ```
     ssh-keygen -t ed25519 -C "your_email@example.com"
     ```
   - Add the SSH key to your GitHub account:
     - Copy the public key:
       ```
       cat ~/.ssh/id_ed25519.pub
       ```
     - Go to GitHub Settings > SSH and GPG keys > New SSH key
     - Paste your public key and save

3. Create and activate a virtual environment:
   ```
   python -m venv .venv
   source .venv/bin/activate  # On Windows, use `.venv\Scripts\activate`
   ```

4. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

5. Set up your environment variables:
   - Copy the `.env.example` file to `.env`:
     ```
     cp .env.example .env
     ```
   - Open the `.env` file and replace `your_openai_api_key` with your actual OpenAI API key.
   - The `GIT_REPO_PATH` is set to `./` by default, which means repositories will be cloned into the current directory. You can change this if needed.

6. Update the `REPO_LIST` in `report.py` with the repositories you want to analyze.

7. Set up and start the Text-to-Speech service, and run the report:
   - Make the initialization script executable:
     ```
     chmod +x init.sh
     ```
   - Run the initialization script:
     ```
     ./init.sh
     ```

## Usage

The `init.sh` script now handles everything:
- It starts the TTS service if it's not already running.
- It waits for the TTS service to be fully operational.
- It automatically runs the `report.py` script once the TTS service is ready.

To use the system, simply run:

```
./init.sh
```

This will set up the TTS service and start the report generation process.

## Testing

To run the test suite:

1. Ensure you're in the project directory and your virtual environment is activated.
2. Run the following command:
   ```
   python report.py test
   ```

This will execute a series of unit tests to verify the functionality of the report generation system.

### Testing the TTS Docker Service

To test the Text-to-Speech Docker service:

1. Make sure the TTS service is running (you can start it with `./init_tts.sh` if it's not already running).
2. Make the test script executable:
   ```
   chmod +x test_tts_docker.sh
   ```
3. Run the test script:
   ```
   ./test_tts_docker.sh
   ```

This will send a test request to the TTS service and generate an audio file named `test_tts_output.mp3`. You can play this file to verify that the TTS service is working correctly.
