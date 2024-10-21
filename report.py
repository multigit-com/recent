# Import necessary libraries
import os
import subprocess
from git import Repo
import openai
import pyttsx3
from selenium import webdriver
import ffmpeg
from dotenv import load_dotenv
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

# Define constants
REPO_LIST = [
    "github/biokomputer/react",
    "github/locamera/react",
    # ... other repositories
]

load_dotenv()

openai.api_key = os.getenv('OPENAI_API_KEY')
repo_path = os.getenv('GIT_REPO_PATH')

def initialize_driver():
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    return driver

def get_default_branch(repo_path):
    repo = Repo(repo_path)
    # Fetch the remote references
    repo.remotes.origin.fetch()
    # Get the default branch from the remote
    default_branch = repo.remotes.origin.refs.HEAD.ref.name
    return default_branch


# Function to clone repositories
def clone_repo(repo_path):
    # Construct the git URL
    git_url = f"https://github.com/{repo_path}.git"
    # Clone the repository using the GIT_REPO_PATH from .env
    clone_path = os.path.join(os.getenv('GIT_REPO_PATH'), repo_path)
    Repo.clone_from(git_url, clone_path)

# Function to analyze commits
def analyze_commits(repo_path):
    repo = Repo(repo_path)
    default_branch = get_default_branch(repo_path)
    print(f"The default branch is: {default_branch}")

    commits = list(repo.iter_commits(default_branch, since='1 month ago'))
    # Process commits to generate summaries
    summaries = []
    for commit in commits:
        # Use OpenAI API to generate summary
        summary = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"Summarize the following commit: {commit.message}",
            max_tokens=150
        )
        summaries.append(summary.choices[0].text.strip())
    return summaries

# Function to generate text-to-speech
def generate_audio(summary):
    engine = pyttsx3.init()
    engine.save_to_file(summary, 'summary.mp3')
    engine.runAndWait()

# Function to generate video
def generate_video(repo_path):
    # Use Selenium to open the project in a virtual browser
    driver = initialize_driver()
    driver.get(f"file://{repo_path}/index.html")
    # Record the session
    # ... (recording logic)
    driver.quit()

# Function to convert RDP to MP4
def convert_rdp_to_mp4(rdp_file):
    ffmpeg.input(rdp_file).output('output.mp4').run()

# Main execution
for repo in REPO_LIST:
    clone_repo(repo)
    summaries = analyze_commits(repo)
    for summary in summaries:
        generate_audio(summary)
    generate_video(repo)
    # Assume RDP file is generated
    convert_rdp_to_mp4('session.rdp')
