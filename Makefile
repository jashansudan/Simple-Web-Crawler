.PHONY: test rescale nuro databricks setup

test: setup rescale

rescale: setup
	@python3 web_crawler.py "http://rescale.com"

nuro: setup
	@python3 web_crawler.py "https://nuro.ai/"

databricks: setup
	@python3 web_crawler.py "https://databricks.com/"

setup: 
	pip3 install -r requirements.txt
