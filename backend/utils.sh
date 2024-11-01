#logged in user
aws sts get-caller-identity
aws sts get-caller-identity --profile cloudtechcrafters.com

#login
aws sso login --profile cloudtechcrafters.com

# list aws region, users and account info
aws sts get-caller-identity --profile cloudtechcrafters.com
#Queue Gazettes loggroup
sam logs --profile cloudtechcrafters.com --cw-log-group /aws/lambda/kenya-law-gazettes-DownloadGazettesFunction-FqH7hv4PqZZ1 --tail

#Gazette download loggroup
sam logs --profile cloudtechcrafters.com --cw-log-group /aws/lambda/kenya-law-gazettes-DownloadGazetteFunction-VzkbtxSjz0xl  --tail
