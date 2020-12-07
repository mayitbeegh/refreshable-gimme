from gimme_aws_creds.main import GimmeAWSCreds
from gimme_aws_creds.ui import CLIUserInterface
from botocore.credentials import RefreshableCredentials
from flask import Flask


class CredentialDataSource(CLIUserInterface):
    def result(self, result):
        pass


from dateutil.tz import tzlocal, tzutc
import datetime
import http

app = Flask(__name__)
expected_keys = ['access_key', 'secret_key', 'token', 'expiry_time']


def gimme_aws_creds_as_metadata():
    aws_creds = GimmeAWSCreds()
    aws_creds.handle_action_configure()
    aws_creds.handle_action_register_device()
    aws_creds.handle_action_list_profiles()
    aws_creds.handle_action_store_json_creds()
    aws_creds.handle_action_list_roles()

    for data in aws_creds.iter_selected_aws_credentials():
        one_hour_from_now = datetime.datetime.now(tzutc()) + datetime.timedelta(hours=1)
        return dict(access_key=data['credentials']['aws_access_key_id'],
                    secret_key=data['credentials']['aws_secret_access_key'],
                    token=data['credentials']['aws_session_token'], expiry_time=one_hour_from_now.isoformat())


@app.route('/refresh')
def refresh():
    global credential_loader
    credential_loader = RefreshableCredentials.create_from_metadata(metadata=gimme_aws_creds_as_metadata(),
                                                                    method='gimme-aws-creds',
                                                                    refresh_using=gimme_aws_creds_as_metadata,
                                                                    )
    return '', http.HTTPStatus.NO_CONTENT


@app.route('/latest/meta-data/instance-id')
def get_instance_id():
    return 'i-eeeeeeeeeeeeeeeef'


@app.route('/latest/api/token', methods=['PUT'])
def get_token():
    return 'letmein'


@app.route('/latest/meta-data/iam/security-credentials/')
def get_rolename():
    return 'supersecretrole'


@app.route('/latest/meta-data/iam/security-credentials/supersecretrole')
def get_creds():
    global credential_loader
    credentials = credential_loader.get_frozen_credentials()  # _expiry_time
    return dict(Code="Success", LastUpdated="dunno", Type="dunno", AccessKeyId=credentials.access_key,
                SecretAccessKey=credentials.secret_key, Token=credentials.token,
                Expiration=credential_loader._expiry_time)

    # return {
    #     "Code" : "Success",
    #     "LastUpdated" : "2012-04-26T16:39:16Z",
    #     "Type" : "AWS-HMAC",
    #     "AccessKeyId" : "ASIAIOSFODNN7EXAMPLE",
    #     "SecretAccessKey" : "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY",
    #     "Token" : "token",
    #     "Expiration" : "2017-05-17T15:09:54Z"
    # }


if __name__ == "__main__":
    refresh()
    app.run(host='169.254.169.254', port=80)
