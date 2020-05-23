# A simple multiprocess Web Crawler

## Getting started:
### Requirements:
Have `python 3.7.7` installed.

This is recommended through homebrew:
Which can be downloaded through: `/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"`


Then run:

`brew install python`

### Clone the Git Repository
`git clone https://github.com/jashansudan/Simple-Web-Crawler.git`

### Automatic Run
To run automated build and test:
`make test`
This automatically downloads requirements and runs the crawler with a test.
It's recommended to run this from a virtual environment.

### Manual Run
1. Install python requirements: `pip3 install -r requirements.txt`
2. Run the crawler with a supplied website: `python3 web_crawler.py <some_valid_website>`
