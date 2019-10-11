SHELL := /bin/bash
.PHONY: deploy
deploy:
	cd deploy/; \
	./wrapper.sh apply dev s3; \
	./wrapper.sh apply dev iam; \
	./wrapper.sh apply dev lambda; \
	./wrapper.sh apply dev api-gateway; \
