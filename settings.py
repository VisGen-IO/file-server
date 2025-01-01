import os
import json
import environ
from middleware.s3_secret_manager import get_secret

env = environ.Env(
    DEBUG=(bool, False),
)

environ.Env.read_env()

ENV_MODE = env('ENV_MODE', default='production')

if ENV_MODE == 'local':
    with open('env.json') as json_env_file:
        json_env = json.load(json_env_file)
        os.environ.update(json_env)
elif ENV_MODE == 'production':
    secrets = get_secret()
    os.environ.update(secrets)

AWS_ACCESS_KEY = env('AWS_ACCESS_KEY')
AWS_SECRET_KEY = env('AWS_SECRET_KEY')
AWS_BUCKET_NAME = env('AWS_BUCKET_NAME')
AWS_PROFILE_FILES_FOLDER = env('AWS_PROFILE_FILES_FOLDER')
AWS_DOCUMENT_FILES_FOLDER = env('AWS_DOCUMENT_FILES_FOLDER')
S3_REGION_NAME = env('S3_REGION_NAME')
AWS_FILE_URL = env('AWS_FILE_URL')
