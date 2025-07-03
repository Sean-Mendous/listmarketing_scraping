import os
import questionary
from app.logger.logger import logger

def ask_client_folder():
    client_dir = "clients"
    folders = [name for name in os.listdir(client_dir)
            if os.path.isdir(os.path.join(client_dir, name))]

    if not folders:
        logger.error("No folder found")
        raise RuntimeError("No folder found")
    else:
        selected_client = questionary.select(
            "Select a folder:",
            choices=folders
        ).ask()

    logger.info(f"Selected folder: {selected_client}")
    return selected_client

def ask_logic():
    selected_logic = questionary.select(
        "Select a run_flow logic:",
        choices=["list", "indivisual"]
    ).ask()

    logger.info(f"Selected logic: {selected_logic}")
    return selected_logic