
#Queue Gazettes loggroup
sam logs --profile cloudtechcrafters.com --cw-log-group /aws/lambda/kenya-law-gazettes-DownloadGazettesFunction-FqH7hv4PqZZ1 --tail

#Gazette download loggroup
sam logs --profile cloudtechcrafters.com --cw-log-group /aws/lambda/kenya-law-gazettes-DownloadGazetteFunction-VzkbtxSjz0xl  --tail
