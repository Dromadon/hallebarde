SHELL := /bin/bash
.PHONY: deploy package
deploy:
	cd deploy/; \
	./wrapper.sh apply dev s3; \
	./wrapper.sh apply dev iam; \
	./wrapper.sh apply dev lambda; \
	./wrapper.sh apply dev api-gateway; \

package:
	cd app/; \
	rm package/*.zip; \
	zip -j package/hello-world.zip hallebarde/hello-world.py; \
	zip -j package/get-presigned-url.zip hallebarde/get-presigned-url.py; \
	zip -j package/authorizer.zip hallebarde/authorizer.py; \
