# Refreshable Gimme

Emulates EC2 instance metadata credential provider backed by [Gimme AWS Creds](https://github.com/Nike-Inc/gimme-aws-creds). Good for long running jobs or services that require AWS credentials.
To start the server, run the following commands:
```bash
sudo ifconfig lo0 inet 169.254.169.254/32 add
pip3 install -r requirements
sudo python3 ec2_metadata_wrapper.py
```
On start up and subsequent refreshes, you will be prompted to authenticate with Okta using your Gimme AWS Creds configs. Setting up a default MFA factor of push|sms|call in `~/.okta_aws_login_config` is recommended as you will get alerted when the credentials are expiring. To learn more about this config file, check out the Gimme AWS Cred repo.
To force refresh the credentials, run `curl 169.254.169.254/refresh` or equivalent.