# Changelog

## [Unreleased]

### Added
- Created `test_tts_docker.sh` script for testing the TTS Docker service.
- Added instructions in README.md for running the TTS Docker service test.

## [0.2.0] - 2023-12-15

### Changed
- Updated `report.py` to remove `ChromeType` import and simplify the `initialize_driver` function.
- Modified `requirements.txt` to ensure correct versions of libraries are installed.
- Updated the `.env` file to use `./` as the default `GIT_REPO_PATH`.
- Removed `CHROME_DRIVER_PATH` from the `.env` file as it's no longer needed.
- Updated `report.py` to use `webdriver_manager` for automatic Chrome driver management.
- Modified `clone_repo` function in `report.py` to use SSH for cloning repositories, with a fallback to HTTPS.
- Significantly enhanced `analyze_commits` function to process all commits and README content in a single API call, providing a more comprehensive summary.
- Implemented logging functionality in `report.py` to save logs to a file and display them in the console.
- Added timestamps to commit information in the `analyze_commits` function for more precise change tracking.
- Moved all TTS-related files (tts_service.py, Dockerfile.tts, requirements_tts.txt) to a separate 'tts' folder.
- Modified init_tts.sh to automatically start the report script after the TTS service is ready.

### Added
- Added `webdriver_manager` and `requests` to the project dependencies.
- Added saving of a single, comprehensive AI summary in `raw_summary.txt` for each repository.
- Added a new `logs` folder to store log files for each script execution.
- Added Chrome options for headless mode and improved compatibility.
- Created a new 'tts' folder to organize Text-to-Speech service files.
- Added init_tts.sh script for easy setup and management of the TTS Docker service.
- Added automatic execution of report.py in init_tts.sh after TTS service is ready.

### Removed
- Removed the need for manually specifying the Chrome driver path.
- Removed individual commit summaries in favor of a single, comprehensive repository summary.

## [0.1.0] - 2023-12-01

### Added
- Initial release of the report generation tool.
- Basic functionality to clone repositories, analyze commits, and generate summaries.
- Integration with OpenAI API for commit analysis.
- Simple text-to-speech conversion for summaries.
- Basic README with setup and usage instructions.
