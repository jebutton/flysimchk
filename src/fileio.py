"""Handles the Reading and Writing to files for the program.

Copyright 2019 Jacqueline Button.

"""
import json
#from json import JSONDecodeError
from os import listdir

from model import Checklist
from model import ChecklistStep
from model import Plane


def load_plane_file(filename: str):
    """Handle the loading of a plane data file.

    Args:
        filename: the name of the file. It will be validated to make sure it
        is a JSON file

    """
    checklists = []
    new_plane = Plane('blank')
    if validate_plane_file(filename):
        with open(filename) as plane_data_file:
            try:
                plane_data = json.load(plane_data_file)
                # All other data in the file is not handled yet.
                # Currently only concerned about the checklists.
                for individual_checklist in plane_data['checklists']:
                    steps = []
                    for checklist_step in individual_checklist['checklist_steps']:
                        temp_checklist_step = ChecklistStep(
                            int(checklist_step['step_number']),
                            checklist_step['step_title'],
                            checklist_step['step_text']
                        )
                        steps.append(temp_checklist_step)
                    checklists.append(Checklist(
                        individual_checklist['checklist_name'],
                        individual_checklist['checklist_message'],
                        steps
                    ))
                    checklists[-1].sort_checklist()
                new_plane.plane_name = plane_data['plane_name']
                new_plane.checklists = checklists
            except json.JSONDecodeError:
                new_plane = Plane("Plane with filename: " + str(filename) + " Failed to load correctly.", None, None)
            
    else:
        raise Exception('Parameter filename Passed to load_plane_file method \
            was not a JSON file.')
    return new_plane


def search_directory_for_planes(directory: str):
    """Search a directory for plane JSON files.

    Args:
        directory: The directory to search in.

    """
    planes = []
    directory_list = listdir(str(directory))
    for plane_file in directory_list:
        if validate_plane_file(plane_file):
            planes.append(
                load_plane_file(
                    str(directory) + '/' + str(plane_file)
                )
                )
    return planes


def validate_plane_file(plane_file: str):
    """Handle the validation of plane files. Will be expanded greatly later.

    Args:
        plane_file: the name of the plane file to load.

    """
    valid = True
    if not plane_file.endswith('.json'):
        valid = False
    return valid
