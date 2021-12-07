test:
	@coverage run -m pytest test/*.py
install_requirements:
	@pip install -r requirements.txt