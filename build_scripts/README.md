# Build scripts folder
This is a folder to quickly build things needed for the workshop.  

## Workshop attendee
If you are a workshop attendee, you can safely ignore this entire directory. It is only for instructors

## Instructors
Currently the only script in this folder is one to work with google colab.
```colab_nb_builder.py```
This script will insert relevant cells needed for a notebook to run on google colab at the top of every notebook
For this repository, this will include:
- Instructions and general information for running on google colab
- pip installing needed packages
- mounting your google drive to use as data storage
  
This script should only add these cells to notebooks 02 and onwards, notebook 00 is specific, and notebook 01 will just be copied over (little to no package imports).

To use it, simply run from it the main directory:
```
python build_scripts/colab_nb_builder.py
```
