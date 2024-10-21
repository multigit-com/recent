# Import necessary libraries
import os
import subprocess
from git import Repo, GitCommandError
from openai import OpenAI
import pyttsx3
from selenium import webdriver
import ffmpeg
from dotenv import load_dotenv
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import requests
import logging
from datetime import datetime

# Define constants
REPO_LIST = [
    "biokomputer/python",
    "locamera/react",
    # ... other repositories
]

load_dotenv()

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
base_repo_path = os.getenv('GIT_REPO_PATH')
output_base_path = os.path.join(base_repo_path, 'output')

# Set up logging
log_folder = os.path.join(base_repo_path, 'logs')
os.makedirs(log_folder, exist_ok=True)
log_file = os.path.join(log_folder, f'report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log')

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)

def initialize_driver():
    chrome_service = Service(ChromeDriverManager().install())
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')  # Run in headless mode
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
    return driver

def get_default_branch(repo):
    repo.remotes.origin.fetch()
    default_branch = repo.remotes.origin.refs.HEAD.ref.name
    return default_branch

def clone_or_update_repo(repo_name):
    clone_path = os.path.join(base_repo_path, repo_name.split('/')[-1])
    if os.path.exists(clone_path):
        logging.info(f"Repository {repo_name} already exists. Updating...")
        try:
            repo = Repo(clone_path)
            origin = repo.remotes.origin
            origin.fetch()
            origin.pull()
            logging.info(f"Successfully updated {repo_name}")
            return clone_path
        except GitCommandError as e:
            logging.error(f"Failed to update {repo_name}: {str(e)}")
            return None
    else:
        ssh_url = f"git@github.com:{repo_name}.git"
        try:
            Repo.clone_from(ssh_url, clone_path)
            logging.info(f"Successfully cloned {repo_name} using SSH")
            return clone_path
        except GitCommandError as e:
            logging.warning(f"Failed to clone {repo_name} using SSH: {str(e)}")
            logging.info("Falling back to HTTPS method...")
            https_url = f"https://github.com/{repo_name}.git"
            try:
                Repo.clone_from(https_url, clone_path)
                logging.info(f"Successfully cloned {repo_name} using HTTPS")
                return clone_path
            except GitCommandError as e:
                logging.error(f"Failed to clone {repo_name} using HTTPS: {str(e)}")
                return None

def analyze_commits(repo_path):
    repo = Repo(repo_path)
    default_branch = get_default_branch(repo)
    logging.info(f"The default branch is: {default_branch}")

    commits = list(repo.iter_commits(default_branch, since='1 month ago'))
    
    # Get the README content
    readme_content = ""
    try:
        readme_content = repo.git.show(f"{default_branch}:README.md")
    except GitCommandError:
        readme_content = "README.md not found in the default branch."

    # Prepare the commit information
    commit_info = []
    for commit in commits:
        files_changed = commit.stats.files.keys()
        commit_info.append(f"""
Commit: {commit.hexsha[:7]}
Author: {commit.author}
Timestamp: {commit.committed_datetime.isoformat()}
Message: {commit.message}
Files Changed: {', '.join(files_changed)}
""")

    # Prepare the prompt
    prompt = f"""Analyze the following repository information and provide a comprehensive summary:

README.md Content:
{readme_content}

Recent Commits (from newest to oldest):
{''.join(commit_info)}

Please provide a detailed summary of the recent changes and developments in this repository. Include key features, bug fixes, and any significant updates mentioned in the commits or README. Highlight the main focus areas of development and any notable trends in the recent work. When referencing specific changes, please include their timestamps.
"""

    # Send the prompt to OpenAI API
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that analyzes git repositories and summarizes recent developments."},
            {"role": "user", "content": prompt}
        ]
    )
    
    summary = response.choices[0].message.content.strip()
    return summary


def generate_audio(summary, output_file):
    tts_service_url = "http://localhost:5000/synthesize"
    try:
        response = requests.post(tts_service_url, json={"text": summary}, timeout=5)
        if response.status_code == 200:
            with open(output_file, 'wb') as f:
                f.write(response.content)
            logging.info(f"Generated audio summary using TTS service: {output_file}")
        else:
            raise Exception(f"TTS service returned status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        logging.warning(f"Failed to connect to TTS service: {str(e)}. Falling back to pyttsx3.")
        engine = pyttsx3.init()
        engine.save_to_file(summary, output_file)
        engine.runAndWait()
        logging.info(f"Generated audio summary using pyttsx3: {output_file}")
    except Exception as e:
        logging.error(f"Failed to generate audio summary: {str(e)}")


def generate_video(repo_path, output_file):
    driver = initialize_driver()
    driver.get(f"file://{repo_path}/index.html")
    driver.save_screenshot(output_file)
    driver.quit()

def convert_rdp_to_mp4(rdp_file, output_file):
    ffmpeg.input(rdp_file).output(output_file).run()

def create_repo_folder(repo_name):
    folder_name = repo_name.replace('/', '_')
    folder_path = os.path.join(output_base_path, folder_name)
    os.makedirs(folder_path, exist_ok=True)
    return folder_path

def main():
    try:
        for repo_name in REPO_LIST:
            logging.info(f"Processing repository: {repo_name}")
            repo_path = clone_or_update_repo(repo_name)
            if repo_path:
                try:
                    output_folder = create_repo_folder(repo_name)
                    summary = analyze_commits(repo_path)
                    
                    raw_summary_file = os.path.join(output_folder, 'raw_summary.txt')
                    with open(raw_summary_file, 'w') as f:
                        f.write(summary)
                    logging.info(f"Saved raw summary to {raw_summary_file}")
                    
                    audio_file = os.path.join(output_folder, 'summary.mp3')
                    generate_audio(summary, audio_file)
                    
                    video_file = os.path.join(output_folder, 'video.png')
                    generate_video(repo_path, video_file)
                    logging.info(f"Generated video (screenshot): {video_file}")
                    
                    logging.info(f"Completed processing for {repo_name}")
                except Exception as e:
                    logging.error(f"Error processing {repo_name}: {str(e)}")
            else:
                logging.warning(f"Skipping {repo_name} due to cloning/updating failure")
    except KeyboardInterrupt:
        logging.info("Operation interrupted by user. Exiting gracefully...")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {str(e)}")
    finally:
        logging.info("Script execution completed.")

if __name__ == "__main__":
    main()
