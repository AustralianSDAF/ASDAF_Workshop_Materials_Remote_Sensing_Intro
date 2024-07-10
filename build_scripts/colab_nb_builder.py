#!/bin/env python
# A specific script to be run only in this repository

import json
from pathlib import Path
import logging
import shutil

log = logging.getLogger(__name__)


def get_requirements_cell(requirements_path: str | Path) -> dict:
    """turns a requirements.txt into jupyter cell data"""
    with open(requirements_path, "r") as f:
        cell_data = f.readlines()
    for i, line in enumerate(cell_data):
        # Check for comments or empty lines, append !pip install to everything else
        if (len(line.strip()) == 0) or (line.strip()[0] in ["#", "\n"]):
            continue
        cell_data[i] = "!pip install " + line

    extra_lines = [
        "# This cell has been automatically inserted from build/google_colab_cell.py\n",
        "# It should make this notebook google-colab compatible!\n",
        "\n" "!pip install --upgrade pip \n",
    ]

    for i, line in enumerate(extra_lines):
        cell_data.insert(i, line)

    jupyter_cell = {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": cell_data,  # readlines' output format is the jupyter format
    }
    return jupyter_cell


def colabify_notebooks(
    input_notebook_path: str | Path,
    output_notebook_path: str | Path = None,
    requirements_path: str | Path = "requirements.txt",
) -> None:
    """Adds cell(s) to a jupyter notebook for it to work in google colab

    Parameters
    ----------
    input_notebook_path
        the notebook you want to use as a template
    output_notebook_path : optional
        the path to where you wish to save the notebook.
        If left out this will be in colab_notebooks/name_colab.ipynb
    requirements_path : optional
        the path to the requirements file to be inserted
    """
    normal_nb_path = Path(input_notebook_path)
    if output_notebook_path is None:
        output_notebook_path = Path("colab_notebooks") / (
            normal_nb_path.with_suffix("").name + "_colab.ipynb"
        )

    with open(normal_nb_path, "r") as normal_nb_f:
        notebook_json = json.load(normal_nb_f)

    colab_cell = get_requirements_cell(requirements_path)
    notebook_json["cells"].insert(0, colab_cell)

    output_notebook_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_notebook_path, "w") as colab_nb_f:
        json.dump(notebook_json, colab_nb_f, indent=1)
    return


def main():
    """CLI function for this script.

    Notes
    -----
    Run this script from the main directory (ie with python build_scripts/script_name.py)
    """
    logging.basicConfig(level=logging.INFO)
    log.info("Starting script")

    notebooks_fpath = Path("notebooks")
    colab_notebooks_fpath = Path("notebooks_colab")
    requirements = "google_requirements.txt"

    nbs = list(notebooks_fpath.glob("*.ipynb"))
    # Filter notebooks to remove ones that cant have/dont need changes
    nbs_to_convert = [nb for nb in nbs if (nb.name[:2] not in ["00", "01"])]
    # Filter notebooks for ones that need to be copied
    nbs_to_copy = [nb for nb in nbs if (nb.name[:2] in ["01"])]

    log.info(
        f"Notebooks to copy: {len(nbs_to_copy)}, notebooks to convert: {len(nbs_to_convert)}"
    )
    for old_fpath in nbs_to_copy:
        old_fpath.parent.mkdir(parents=True, exist_ok=True)
        new_fpath = colab_notebooks_fpath / (old_fpath.stem + "_colab.ipynb")
        log.info(f"Copying {old_fpath} to {new_fpath}")
        shutil.copy(old_fpath, new_fpath)

    for old_fpath in nbs_to_convert:
        old_fpath.parent.mkdir(parents=True, exist_ok=True)
        new_fpath = colab_notebooks_fpath / (old_fpath.stem + "_colab.ipynb")
        log.info(f"Colabifying {old_fpath} at {new_fpath}")
        colabify_notebooks(
            old_fpath,
            requirements_path=requirements,
            output_notebook_path=new_fpath,
        )
    log.info("Done! Exiting")
    return


if __name__ == "__main__":
    main()
