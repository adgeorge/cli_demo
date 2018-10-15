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


def update_lambda_code(sub_folder=first_arg):
    if sub_folder in ('tensor', 'tensoriot'):
        sub_folder = 'tensoroffice'
        lambda_name = "tensor_office"
    else:
        logger.error("No input name was given. Did not update lambda.")
        return 0

    code_folder_in_s3 = 's3://alexalexacode/'+sub_folder+'/'
    s3_bucket_name = 'alexalexacode'
    zip_name = 'archive.zip'

    # Copy files in project directory to venv site-packages
    call(['cp', '-r', '.', '../env/lib/python3.6/site-packages/'])

    # file path
    abspath = os.path.abspath(__file__)

    # project directory name
    dir_name = os.path.dirname(abspath)

    # Create a list of all files/folders in project directory
    files = os.listdir(dir_name)

    # Path to site-packages
    site_package = os.path.relpath('../env/lib/python3.6/site-packages', dir_name)

    # Change directory to site-packages
    os.chdir(site_package)

    # Creates a Zip file
    call(['zip', '-r', zip_name, '.'])

    # Copies Zip file to S3
    call(['aws', 's3', 'cp', zip_name, code_folder_in_s3])

    # Updates Lambda with new zip in S3
    call(['aws', 'lambda', 'update-function-code', '--function-name',
          lambda_name, '--s3-bucket', s3_bucket_name, '--s3-key', sub_folder+'/'+zip_name])

    # remove zip file
    call(['rm', zip_name])

    # remove project files from site-packages
    for file in files:
        if file != '__init__.py':
            call(['rm', "-rf", file])

    print("Done!")

    return 0


if __name__ == "__main__":
    update_lambda_code()
