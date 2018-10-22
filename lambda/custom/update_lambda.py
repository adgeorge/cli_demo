from subprocess import call
import sys
import logging
import os


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


"""
This module is used to send a copy of the code in a zip file to a specified S3 bucket.
Make sure to download AWS CLI tool and then run "aws configure" to enter your credentials.
Once your credentials are logged in, you should be able to run this module with "python update_lambda.py"
"""

try:
    first_arg = sys.argv[1]
except IndexError:
    logger.info("No argument given.")
    first_arg = None

# ---- EDIT THE VARS BELOW TO MATCH YOUR PROJECT ----
# Relative path to your VirtualEnvs site-packages
PATH_TO_SITE_PACKAGES = "../../../env/lib/python3.6/site-packages/"

# Arbitrary name for the zip file sent to S3
ZIP_NAME = 'archive.zip'

# File for lambda entry point
LAMBDA_FILE = "lambda_function.py"

# Folder that contains all the skill logic
SKILL_FOLDER = "skill"

SKILL_CONFIG = {
    "demo_cli": {
        "SUB_FOLDER": "demo_cli",
        "LAMBDA_NAME": "ask-custom-testing-cli-default"
    }
}


def update_lambda_code(key=first_arg):
    if key in SKILL_CONFIG:
        sub_folder = SKILL_CONFIG[key]["SUB_FOLDER"]
        lambda_name = SKILL_CONFIG[key]["LAMBDA_NAME"]
    else:
        logger.error("No input name was given. Did not update lambda.")
        return 0

    code_folder_in_s3 = 's3://alexalexacode/'+sub_folder+'/'
    s3_bucket_name = 'alexalexacode'

    # Copy files in project directory to venv site-packages
    call(['cp', LAMBDA_FILE, PATH_TO_SITE_PACKAGES])
    call(['cp', '-r', SKILL_FOLDER, PATH_TO_SITE_PACKAGES])

    # __file__ path
    abspath = os.path.abspath(__file__)
    print("abspath: {}".format(abspath))

    # project directory name
    dir_name = os.path.dirname(abspath)
    print("dirname: {}".format(dir_name))

    # Create a list of all files/folders in project directory
    files = os.listdir(dir_name)
    print("files: {}".format(files))

    # Path to site-packages
    site_package = os.path.relpath(PATH_TO_SITE_PACKAGES, dir_name)
    print("site_packages: {}".format(site_package))

    # Change directory to site-packages
    os.chdir(site_package)

    # Creates a Zip file
    call(['zip', '-r', ZIP_NAME, '.'])

    # Copies Zip file to S3
    call(['aws', 's3', 'cp', ZIP_NAME, code_folder_in_s3])

    # Updates Lambda with new zip in S3
    call(['aws', 'lambda', 'update-function-code', '--function-name',
          lambda_name, '--s3-bucket', s3_bucket_name, '--s3-key', sub_folder+'/'+ZIP_NAME])

    # remove zip file
    call(['rm', ZIP_NAME])
    call(['rm', LAMBDA_FILE])
    call(['rm', '-r', SKILL_FOLDER])

    print("Done!")

    return 0


if __name__ == "__main__":
    update_lambda_code()
