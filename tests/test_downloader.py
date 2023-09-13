import json
import pytest
from offvsix.main import VSCodeExtensionDownloader, cli
from click.testing import CliRunner

def mock_requests_post(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

    if args[0] == 'https://marketplace.visualstudio.com/_apis/public/gallery/extensionquery':
        return MockResponse({"results": [{"extensions": [{"versions": [{"version": "1.0"}]}]}]}, 200)

    return MockResponse(None, 404)

# Testing the function
def test_vscode_extension_downloader(monkeypatch):
    monkeypatch.setattr('requests.post', mock_requests_post)
    downloader = VSCodeExtensionDownloader('ms-python.python')
    downloader.download()

# Testing the CLI
def test_cli(monkeypatch):
    monkeypatch.setattr('requests.post', mock_requests_post)
    runner = CliRunner()
    result = runner.invoke(cli, ['ms-python.python'])
    assert 'already exists. Use --no-cache to force re-download' in result.output

def test_cli_no_cache(monkeypatch):
    monkeypatch.setattr('requests.post', mock_requests_post)
    runner = CliRunner()
    result = runner.invoke(cli, ['ms-python.python', '--no-cache'])
    assert 'Successfully downloaded to:' in result.output