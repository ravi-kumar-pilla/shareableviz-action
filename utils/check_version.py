import os
import requests
from pathlib import Path

VERSION_FILE_PATH = "VERSION"


def get_action_version():
    try:
        with open(VERSION_FILE_PATH, "r") as file:
            content = file.read()
            return content
    except FileNotFoundError:
        print(f"The file {VERSION_FILE_PATH} was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


def is_action_version_valid(action_endpoint, action_name, action_version):
    print(f"Check if {action_name} {action_version} is on GitHub Marketplace")
    response = requests.get(action_endpoint, timeout=10)
    print(response.status_code)
    if response.status_code == 404:
        # Version doesn't exist on GitHub Marketplace - do release
        print(f"Starting the release of {action_name} {action_version}")
        return True
    else:
        print(f"Skipped: {action_name} {action_version} already exists on PyPI")
        return False


if __name__ == "__main__":
    """Check if an action needs to be released"""
    base_path = Path()
    new_release = "false"
    action_name = "shareableviz-action"
    action_version = get_action_version()

    action_endpoint = f"https://github.com/marketplace/actions/{action_name}?version=v{action_version}"

    if is_action_version_valid(action_endpoint, action_name, action_version):
        new_release = "true"

    env_file = os.getenv("GITHUB_ENV")
    with open(env_file, "a") as env_file:
        env_file.write(f"NEW_RELEASE={new_release}\n")
        if new_release == "true":
            env_file.write(
                f"ACTION_NAME={action_name}\nACTION_VERSION={action_version}\n"
            )
