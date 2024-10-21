import os
import shutil
import unittest
from unittest.mock import patch, MagicMock
from git import Repo
from report import analyze_commits, generate_audio, generate_video, create_repo_folder

class TestReport(unittest.TestCase):
    def setUp(self):
        self.test_repo_path = "./test_repo"
        self.test_output_path = "./test_output"
        
        # Create a test repository
        os.makedirs(self.test_repo_path, exist_ok=True)
        self.repo = Repo.init(self.test_repo_path)
        
        # Copy example file to the test repository
        shutil.copy("example_repo.py", os.path.join(self.test_repo_path, "example_repo.py"))
        
        # Commit the example file
        self.repo.index.add(["example_repo.py"])
        self.repo.index.commit("Initial commit")

    def tearDown(self):
        # Clean up test repository and output
        shutil.rmtree(self.test_repo_path, ignore_errors=True)
        shutil.rmtree(self.test_output_path, ignore_errors=True)

    @patch('report.OpenAI')
    def test_analyze_commits(self, mock_openai):
        mock_completion = MagicMock()
        mock_completion.choices[0].message.content = "Test summary"
        mock_openai.return_value.chat.completions.create.return_value = mock_completion

        summary = analyze_commits(self.test_repo_path)
        self.assertEqual(summary, "Test summary")

    @patch('report.requests.post')
    def test_generate_audio(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = b"Test audio content"
        mock_post.return_value = mock_response

        output_file = os.path.join(self.test_output_path, "test_audio.mp3")
        generate_audio("Test summary", output_file)
        
        self.assertTrue(os.path.exists(output_file))
        with open(output_file, "rb") as f:
            self.assertEqual(f.read(), b"Test audio content")

    @patch('report.webdriver.Chrome')
    def test_generate_video(self, mock_chrome):
        mock_driver = MagicMock()
        mock_chrome.return_value = mock_driver

        output_file = os.path.join(self.test_output_path, "test_video.png")
        generate_video(self.test_repo_path, output_file)
        
        mock_driver.get.assert_called_once()
        mock_driver.save_screenshot.assert_called_once_with(output_file)
        mock_driver.quit.assert_called_once()

    def test_create_repo_folder(self):
        repo_name = "test/repo"
        folder_path = create_repo_folder(repo_name)
        expected_path = os.path.join(self.test_output_path, "test_repo")
        
        self.assertEqual(folder_path, expected_path)
        self.assertTrue(os.path.exists(expected_path))

if __name__ == "__main__":
    unittest.main()
