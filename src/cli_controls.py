"""Module containing classes and functions to generate command line output.

Copyright 2019 Jacqueline Button.

"""
from typing import List, Optional

from PyInquirer import style_from_dict, Token, prompt, Separator

from model import ChecklistStep
from model import Checklist
from model import Plane


class CliStyle():
    """Configurable Style Class for use with PyInquirer.

    Attributes:
        style_dict (dict of str: str): The dictionary containing the style's
        configuration.
        style (Style): The Style that controls the formatting of a PyInquirer
        prompt.

    """

    def __init__(self):
        """Class Constructor."""
        self.style_dict = {
            Token.Separator: '#cc5454',
            Token.QuestionMark: '#673ab7 bold',
            Token.Selected: '#cc5454',
            Token.Pointer: '#673ab7 bold',
            Token.Instruction: '',
            Token.Answer: '#f44336 bold',
            Token.Question: ''
        }
        self.style = None
        self.refresh_style()

    def refresh_style(self):
        """Refresh the actual style from the current style dictionary.

        Args:
            None

        """
        self.style = style_from_dict(self.style_dict)

    def set_style_dict_value(self, key: str, value: str):
        """Set a value in the style_dict class Attribute.

        Args:
            key (str): The key of the value to update.
            value (str): The value to set. It must start with a '#'

        """
        try:
            if str(value).startswith('#'):
                self.style_dict[key] = value
                self.refresh_style()
            else:
                raise ValueError('Invalid Style Value: ' + str(value))
        except ValueError as v_err:
            print('Invalid Parameter: ', v_err)
        except KeyError as k_err:
            print('Key Not Found in Style Dictionary: ', k_err)


class CliJSONObject():
    """Represents a generic menu JSON class for inheritance.

    Attributes:
        json_type (str): The type of the prompt to be created.
        name (str): The name of the prompt. It is used as a key by PyInquier
        message (str): The text displayed when the prompt is shown.

    """

    def __init__(self, json_type: str, name: str, message: str):
        """Class Constructor."""
        self.json_type = json_type
        self.name = name
        self.message = message

    def __str__(self):
        """Return the string representation of the JSON object."""
        return str(self.return_json_instructions())

    def return_json_instructions(self):
        """Return the formatted JSON instructions for a PyInquier prompt.

        Args:
            None

        Returns:
            A JSON structure that can be used to create a PyInquier prompt.

        """
        result = {}
        result['type'] = self.json_type
        result['message'] = self.message
        result['name'] = self.name
        return [result]


class ChecklistSelectPageJSONObject(CliJSONObject):
    """A subclass of a CliJSONObject that is for Checklist Select Pages.

    Attributes:
        plane (Plane): An instance of a Plane class that contains at least one
        checklist.
        choices (list of str): An list of str to contain the list of choices
        for the JSON.

    Args:
        plane (Plane): An instance of a Plane class that contains at least one
        checklist.

    """

    def __init__(self, plane: Plane):
        """Class Constructor."""
        self.plane = plane
        super().__init__('list',
                         'list_of_checklist',
                         'Checklists for the ' + str(self.plane.plane_name)
                         )
        self.choices = self.generate_choices_json()

    def generate_choices_json(self):
        """Generate the choices section of the JSON instructions.

        The choices are based based on the checklists of a plane.

        Returns:
            An list of str representing the choices part of the JSON object
            built by this class.

        """
        result = []
        for checklist in self.plane.checklists:
            result.append(checklist.name)
        result.append('RETURN TO PLANE SELECT')
        return result

    def return_json_instructions(self):
        """Build the JSON instructions for the PyInquirer prompt() command.

        Returns:
            list of list: A JSON structure to be sent to the CLI as display
            instructions.

        """
        result = {}
        result['type'] = self.json_type
        result['message'] = self.message
        result['name'] = self.name
        result['choices'] = self.choices
        return [result]


class PlaneSelectPageJSONObject(CliJSONObject):
    """A subclass of CLIJSONObject for Plane select pages.

    The class represents the information that will be sent to a PyInquirer
    command line prompt for the selection page for the list of known planes.

    Attributes:
        planes (list of Plane): The list of Plane objects to select from.
        choices (list of str): The choices part of the JSON data created by
        this object.

    Args:
        planes (list of Plane) The list of Plane objects to select from.

    """

    def __init__(self, planes: List[Plane]):
        """Class Constructor."""
        CliJSONObject.__init__(self, 'list', 'list_of_planes',
                               'Planes to Select:')
        self.planes = planes
        self.choices = self.generate_choices_json()

    def generate_choices_json(self):
        """Generate the choices section of the JSON instructions.

        The choices are based based on the names of each plane.

        Returns:
            An list of str representing the choices part of the JSON object
            built by this class.

        """
        result = []
        for plane in self.planes:
            result.append(plane.plane_name)
        result.append('EXIT')
        return result

    def return_json_instructions(self):
        """Build the JSON instructions for the PyInquirer prompt() command.

        Returns:
            list of list: A JSON structure to be sent to the CLI as display
            instructions.

        """
        result = {}
        result['type'] = self.json_type
        result['message'] = self.message
        result['name'] = self.name
        result['choices'] = self.choices
        return [result]


class ChecklistJSONObject(CliJSONObject):
    """A subclass of CLIJSONObject representing Checklist JSON instructions.

    The class represents the information that will be sent to a PyInquirer
    command line prompt for the selection page for a plane's Checklists.

    Attributes:
        qmark (str): the character to display as part of the prompt.
        step_count (int): the number of steps in the JSON object.
        choices (list of str): The choices part of the JSON data created by
        this object.

    Args:
        checklist (Checklist): An instance of a Checklist object.
        selected_items (list of str) (optional): An list of steps that are
        already selected.

    """

    def __init__(self, checklist: Checklist,
                 selected_items: List[str] = None):
        """Class Constructor."""
        CliJSONObject.__init__(self, 'checkbox', checklist.name,
                               checklist.message)
        self.qmark = '?'
        self.step_count = 0
        self.choices = self.generate_choices_json(checklist.steps,
                                                  selected_items)

    def generate_choices_json(self,
                              checklist_steps: Optional[List[ChecklistStep]],
                              selected_items: Optional[List[str]]):
        """Generate the choices section of the JSON instructions.

        The choices are based based on the ChecklistSteps in the Checklist.

        Args:
            checklist_steps (list of ChecklistStep): The list of the steps of
            a checklist.
            selected_items (list of str) (optional): An list of options that
            have already been selected.

        Returns:
            list: An list of str representing the choices part of the JSON
            object built by this class.

        """
        result = []
        if checklist_steps is not None and checklist_steps != []:
            for step in checklist_steps:
                self.step_count += 1
                result.append(Separator(str(step.step_number) + ': ' + step.step_title))
                if selected_items is not None:
                    if step.step_text in selected_items:
                        result.append({'name': step.step_text,
                                       'checked': True})
                    else:
                        name_to_append = str(step.step_number) + ': ' + str(step.step_text)
                        result.append({'name': name_to_append})
                else:
                    result.append({'name': step.step_text})
        else:
            result.append({'name': 'There are no Steps'})
        return result

    def return_json_instructions(self):
        """Build the JSON instructions for the PyInquirer prompt() command.

        Returns:
            list of lists: A JSON structure to be sent to the CLI as display
            instructions.

        """
        result = {}
        result['type'] = self.json_type
        result['qmark'] = self.qmark
        result['message'] = self.message
        result['name'] = self.name
        result['choices'] = self.choices
        nav_controls = {'type': 'list',
                        'name': 'nav_controls',
                        'message': 'NAVIGATION CONTROLS',
                        'choices': ['GO BACK', 'RETURN TO LIST SELECT', 'EXIT']
                        }
        return [result, nav_controls]


def show_checklist_selection_page(plane, cli_cont_style: CliStyle):
    """Display a prompt that has a list of possible checklists from a plane.

    Args:
        plane (Plane): The Plane object that contains the checklists to be
        displayed.
        cli_cont_style (CliStyle): A CliStyle object to use as styling.

    Returns:
        str: The str name of the checklist chosen.

    """
    chlst_sel_pg = ChecklistSelectPageJSONObject(plane)
    chlst_sel_json_res = chlst_sel_pg.return_json_instructions()
    sel_chlst = prompt(chlst_sel_json_res,
                       style=cli_cont_style.style)[chlst_sel_pg.name]
    return sel_chlst


def show_checklist(plane, checklist_name, cli_cont_style: CliStyle):
    """Display a prompt with a list of possible checklists from a plane.

    Args:
        plane (Plane): The Plane object that contains the checklist to be
        displayed.
        checklist_name (str): The string name of the checklist to be
        displayed.
        cli_cont_style (CliStyle): A CliStyle object to use as styling.

    Returns:
        str: The value returned by the prompt operation.

    """
    page_results = None
    page_json = [List]
    flag = False
    selected_items = list('')
    results = None
    checklist_obj = Checklist('none', 'none')
    for checklist in plane.checklists:
        if checklist.name == checklist_name:
            checklist_obj = checklist
    while not flag:
        checklist_json_obj = ChecklistJSONObject(checklist_obj, selected_items)
        page_json = checklist_json_obj.return_json_instructions()
        page_results = prompt(page_json, style=cli_cont_style.style)
        selected_items = page_results[checklist_obj.name]
        nav_results = page_results['nav_controls']
        if nav_results in (['EXIT', 'RETURN TO LIST SELECT']):
            results = nav_results
            flag = True
    return results


def show_plane_select_menu(planes, cli_cont_style: CliStyle):
    """Display a list of planes to select from.

    Args:
        planes (list of Plane): The list of Plane objects to use as a list.
        cli_cont_style (CliStyle): The style to use for the PyInquirer prompt.

    Returns:
        str: The name of the plane selected by the user.

    """
    selected_plane = None
    plane_lst_json = PlaneSelectPageJSONObject(planes)
    sel_plane_nm = prompt(plane_lst_json.return_json_instructions(),
                          style=cli_cont_style.style)[plane_lst_json.name]
    if sel_plane_nm != 'EXIT':
        for plane in planes:
            if plane.plane_name == sel_plane_nm:
                selected_plane = plane
    return selected_plane
