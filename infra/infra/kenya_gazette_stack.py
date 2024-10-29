import os
from aws_cdk import (
    Stack,
    aws_s3 as s3,
    aws_lambda as lambda_,
    aws_s3_notifications as s3n,
    aws_iam as iam,
    Duration,
    RemovalPolicy
)
from constructs import Construct

class KenyaGazetteStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create an S3 bucket to store gazette notices
        gazette_bucket = s3.Bucket(
            self, "KenyaGazetteBucket",
            bucket_name="XXXXXXXXXXXXXXXXXXXXX",
            versioned=True,
            encryption=s3.BucketEncryption.S3_MANAGED,
            removal_policy=RemovalPolicy.RETAIN
        )

        # Create a Lambda function to download and update notices
        gazette_lambda = lambda_.Function(
            self, "GazetteDownloaderLambda",
            runtime=lambda_.Runtime.PYTHON_3_9,
            handler="index.handler",
            code=lambda_.Code.from_asset("lambda"),
            timeout=Duration.seconds(300),
            environment={
                "BUCKET_NAME": gazette_bucket.bucket_name
            }
        )

        # Grant the Lambda function read/write permissions to the S3 bucket
        gazette_bucket.grant_read_write(gazette_lambda)

        # Add S3 event notification to trigger Lambda on object creation
        gazette_bucket.add_event_notification(
            s3.EventType.OBJECT_CREATED,
            s3n.LambdaDestination(gazette_lambda)
        )

        # Grant the Lambda function permission to scrape websites
        gazette_lambda.add_to_role_policy(
            iam.PolicyStatement(
                actions=["s3:PutObject", "s3:GetObject"],
                resources=[f"{gazette_bucket.bucket_arn}/*"]
            )
        )
