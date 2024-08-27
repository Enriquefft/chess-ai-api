"""Project keys & settings module."""

import os


def get_required_env(env_name: str) -> str:
    """Validate and return an environmental variable."""
    env_var = os.getenv(env_name)
    if env_var is None:
        error_message = f"{env_name} environmental variable not found."
        raise RuntimeError(error_message)
    return env_var
