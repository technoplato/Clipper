import logging
import os

from pyngrok import ngrok
import subprocess

from pyclipper.config.config import (
    ngrok_auth,
    ngrok_subdomain,
    twilio_phone_number,
    flask_port,
    cache_public_url,
)

logger = logging.getLogger(__name__)
d = logger.debug


def start_ngrok():
    ngrok.DEFAULT_NGROK_PATH = "/usr/local/bin/ngrok"
    ngrok_options = dict()
    if ngrok_auth and ngrok_subdomain:
        ngrok_options["subdomain"] = ngrok_subdomain

    public_url = ngrok.connect(
        port=flask_port, auth_token=ngrok_auth, options=ngrok_options
    )
    d(public_url)
    cache_public_url(public_url)
    twilio_phone_webhook_cmd = (
        f"twilio phone-numbers:update {twilio_phone_number} --sms-url {public_url}/sms"
    )
    process = subprocess.Popen(
        twilio_phone_webhook_cmd.split(),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
        env=os.environ,
    )
    stdout, stderr = process.communicate()
    d(stdout)
    d(stderr)

    ngrok_process = ngrok.get_ngrok_process()

    try:
        # Block until CTRL-C or some other terminating event
        ngrok_process.proc.wait()
    except KeyboardInterrupt:
        d(" Shutting down server.")
        ngrok.kill()
