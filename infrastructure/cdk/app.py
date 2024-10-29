import aws_cdk as cdk

from infrastructure.cdk.stacks.backend import BackendStack

app = cdk.App()
BackendStack(app, "InfraStack",
                  # env=cdk.Environment(account='851725533694', region='us-east-1'),
                  )

app.synth()
