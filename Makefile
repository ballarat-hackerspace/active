all:
	@echo "AWS_PROFILE='profile' make [website]"

website:
	aws s3 sync --delete --acl public-read html/ s3://ballarathacker.space/active/
