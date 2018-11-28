from ipywidgets.widgets import SelectionRangeSlider
from notebook import notebookapp
import pandas as pd
import urllib
import json
import os
import ipykernel
import glob


def notebook_name():
    """Returns the name of the Notebook or None if it cannot be determined
    NOTE: works only when the security is token-based or there is also no password
    """
    connection_file = os.path.basename(ipykernel.get_connection_file())
    kernel_id = connection_file.split('-', 1)[1].split('.')[0]

    for srv in notebookapp.list_running_servers():
        try:
            # No token and no password, ahem...
            if srv['token'] == '' and not srv['password']:
                req = urllib.request.urlopen(srv['url'] + 'api/sessions')
            else:
                req = urllib.request.urlopen(
                    srv['url'] + 'api/sessions?token=' + srv['token'])
            sessions = json.load(req)
            for sess in sessions:
                if sess['kernel']['id'] == kernel_id:
                    return sess['notebook']['path']
        except:
            pass  # There may be stale entries in the runtime directory
    return None


def get_next_notebook():
    _id = int(notebook_name()[0]) + 1
    return glob.glob(f"{_id}*.ipynb")[0]


def get_previous_notebook():
    _id = int(notebook_name()[0]) - 1
    return glob.glob(f"{_id}*.ipynb")[0]


def get_notebook_by_number(_id):
    return glob.glob(f"{_id}*.ipynb")[0]
