import logging
import os
from . import api
import sys

logging_level = {"INFO": logging.INFO, "WARNING": logging.WARNING, "ERROR" : logging.ERROR, "DEBUG" : logging.DEBUG}

def get_env_opt(key, default):
    """Get optional environment varaiable. If it is not set, the default is returned."""
    val = os.environ.get(key)
    if(val is None):
        return default
    return val

def get_env_req(key, err_message : str):
    """Get required environment variable. If it is no set, an error is logged and the program exits."""
    val = os.environ.get(key)
    if(val is None):
        logging.error(err_message)
        exit(1)
    return val

def get_envs() -> dict:
    env = dict()
    env["username"] = get_env_req("USERNAME", "Please define USERNAME. Exiting...")
    env["domain_number"] = get_env_req("DOMAIN_NUMBER", "Please define DOMAIN_NUMBER. Exiting...")
    env["password"] = get_env_req("PASSWORD", "Please define PASSWORD. Exiting...")
    env["otp_key"] = get_env_opt("OTP_KEY", "")
    env["domain"] = get_env_req("DOMAIN", "Please define DOMAIN. Exiting...")
    env["txt_value"] = get_env_opt("TXT_VALUE", os.environ.get("CERTBOT_VALIDATION", ""))
    env["logging_level"] = get_env_opt("LOGGING", "INFO")
    env["contract"] = get_env_req("CONTRACT", "Please define CONTRACT. Exiting...")
    return env

def validate_env(env: dict):
    """Validates, if the environment variables have valid values."""
    if(not env["txt_value"]):
        logging.error("CERTBOT_VALIDATION or TXT_VALUE must be set. Exiting...")
        exit(1)

    if( env["logging_level"] not in logging_level.keys()):
        logging.error("LOGGING must be one of 'INFO', 'WARNING', 'ERROR' or 'DEBUG'. Exiting...")
        exit(1)




def update_challenge_record(api_client: api.Api, txt_value: str) -> bool:
    """Writes the current Certbot challenge to the ACME TXT record."""
    logging.info("Updating _acme-challenge TXT record...")
    return api_client.update_address("_acme-challenge", "TXT", txt_value)
        

def main():
    """Main funcition."""
    env = get_envs()
    logging.basicConfig(stream=sys.stdout,level=logging_level[env["logging_level"]],format='%(asctime)s [%(levelname)s]: %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
    logging.info("Starting...")
    validate_env(env)
    a = api.Api(username=env["username"],password=env["password"],otp_key=env["otp_key"],domain_number=env["domain_number"],contract=env["contract"])

    return 0 if update_challenge_record(a, env["txt_value"]) else 1

if __name__ == "__main__":
    sys.exit(main())
