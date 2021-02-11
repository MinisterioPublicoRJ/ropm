clean:
    find . -regex '.*\.pyc' -exec rm {} \;
    find . -regex '.*~' -exec rm {} \;
    rm -rf reg-settings.py MANIFEST dist build *.egg-info .tox

lint:
    @autoflake -ir . --remove-all-unused-imports --remove-unused-variables
    @isort . -m 3 -l 120 --tc
    @black . -l 120
    @flake8 .

test: clean
    @python -m pytest .

.PHONY: clean help lint test
