# AWS Serverless Amazon SNS Fanout Sample

The sample in this repository demonstrates how to implement the fanout messaging pattern to execute Lambda functions in two ways, using an AWS Lambda function and using an Amazon SNS published message.

## Requirements

### AWS Command Line Interface (CLI)

The examples are configured, packaged and deployed using the AWS [Serverless Application Model (SAM)](https://github.com/awslabs/serverless-application-model).  To use SAM, you must install and configure the AWS Command Line Interface (CLI).  Please see the link below for more detail to install and configure the CLI:

* [Installing the AWS Command Line Interface](http://docs.aws.amazon.com/cli/latest/userguide/installing.html)
* [Configuring the AWS CLI](http://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html)

### Amazon S3 Bucket

The AWS [Serverless Application Model (SAM)](https://github.com/awslabs/serverless-application-model) will be used to package the project in a zip archive and upload to S3 for deployment.  Before using SAM, you must create an Amazon S3 bucket in the account and region that you will use for uploading artifacts, and configure it with permissions for access using the AWS credentials configured in the prior step.  Please see the link below for more detail to create an Amazon S3 bucket:

* [Creating and Configuring an S3 Bucket](http://docs.aws.amazon.com/AmazonS3/latest/user-guide/create-configure-bucket.html)

### Clone GitHub Repository

The examples below can be executed from a local workstation after cloning this Git repository locally.  Please see the link below for more detail to clone the repository:

* [Cloning a Repository](https://help.github.com/articles/cloning-a-repository/)

## Instructions

### Package and Deploy

Once this repository has been cloned, the sample can be packaged and deployed using the AWS CLI and SAM.

To package the project, execute the following command in the project directory, replacing `S3_BUCKET` with the Amazon S3 bucket that you created in the requirements setup.  For more information on the CloudFormation Package command, please see this [link](http://docs.aws.amazon.com/cli/latest/reference/cloudformation/package.html).

```
aws cloudformation package --template-file template.yml --s3-bucket S3_BUCKET -artifacts --output-template-file output-template.yml
```

Once the package command has completed, the files in the directory will have been packaged into a zip archive, uploaded to the specified Amazon S3 bucket, and an output AWS CloudFormation template will be created with the S3 location of the archive.

The output AWS CloudFormation template is ready to be deployed using the following command.  Please replace the following with values for your stack:

* `STACK_NAME` with your custom stack name
* `S3_BUCKET_NAME` with the name of the S3 Bucket to receive uploads for processing
* `SNS_TOPIC_NAME` with the name of the SNS Topic for messaging publishing

```
aws cloudformation deploy --template-file output-template.yml --stack-name STACK_NAME --capabilities CAPABILITY_IAM --parameter-overrides S3BucketName=S3_BUCKET_NAME SnsTopicName=SNS_TOPIC_NAME
```

The S3 Bucket name and SNS Topic name must be specified and not generated to avoid a cyclical dependency when creating subscriptions, which is covered in more detail here: [How do I avoid the error "Unable to validate the following destination configurations" when using S3 event notifications in CloudFormation?](https://aws.amazon.com/premiumsupport/knowledge-center/unable-validate-destination-s3/)

### Validate

Once the CloudFormation stack has been created, you can test both methods for fanout by uploading files to the S3 bucket using different S3 prefixes.

To test the Lambda fanout strategy:

1. Use the S3 Bucket name when launching the stack and upload a file to the prefix `/uploads/lambda/`

2. Navigate to the Lambda service in the AWS Console and confirm that the `MediaInfoFunction`, `TranscodeAudioFunction`, and `FanoutFunction` Lambda functions were successfully invoked.

To test the SNS fanout strategy:

1. Use the S3 Bucket name when launching the stack and upload a file to the prefix `/uploads/sns/`.

2. Navigate to the Lambda service in the AWS Console and confirm that the `MediaInfoFunction` and `TranscodeAudioFunction` Lambda functions were successfully invoked.  The `FanoutFunction` Lambda function should ***not*** be invoked.
