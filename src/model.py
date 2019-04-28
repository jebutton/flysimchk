"""Module containing classes that represent data objects.

Copyright 2019 Jacqueline Button.

"""
from typing import List
from typing import Dict


class ChecklistStep():
    """Contains the data used in each step.

    Right now it is limited to just the text of the step title and text.

    Attributes:
        step_number: The number of the step.
        step_title: The title of the step.
        step_text: the step of the text.

    Args:
        step_number (int): The number of the step.
        step_title (str): The title of the step.
        step_text (str): The title of the step.

    """

    def __init__(self, step_number: int, step_title: str, step_text: str):
        """Class Constructor."""
        self.step_number = step_number
        self.step_title = step_title
        self.step_text = step_text

    def __str__(self):
        """Turn class into a str.

        Returns:
            A str representation of the ChecklistStep.

        """
        output = '{ step_number: ' + str(self.step_number) + ' | step_title: '
        output += self.step_title + ' | step_text: ' + self.step_text + ' }'
        return output

    def __repr__(self):
        """Turn a class into a str for debugging purposes.

        Returns:
            A str representation of the Plane.

        """
        output = '{ ChecklistStep Object: step_number: '
        output += str(self.step_number)
        output += ' | step_title: ' + self.step_title
        output += ' | step_text: ' + self.step_text + ' }'
        return output


class Checklist():
    """This is a class to represent a checklist.

    Attributes:
        message (str): The message to use when displaying the checklist.
        name (str): The name of the checklist, also used as an ID in some
        operations.
        steps (list of ChecklistStep): The steps of the Checklist.

    Args:
        name: The name of the check list. Should be stored in the plane file.
        message: The message to use when displaying the checklist.
        Should be stored in the plane file.
        steps (Optional): The steps of the checklist. Should be stored in the
        plane file.

    """

    def __init__(self, name: str,
                 message: str,
                 steps: List[ChecklistStep] = None):
        """Class constructor."""
        self.message = message
        self.name = name
        self.steps = steps
        if self.steps is None:
            self.steps = []

    def __str__(self):
        """Turn class into a str.

        Returns:
            A str representation of the Checklist.

        """
        step_count = len(self.steps)
        counter = 1
        output = '{ name: ' + self.name + ' | message: ' + self.message
        output += ' | steps: ['
        for step in self.steps:
            if counter < step_count:
                if step is not None:
                    output += str(step) + ', '
                counter += 1
            else:
                output += str(step) + ']'
        output += ' }'
        return output

    def __repr__(self):
        """Turn a class into a str for debugging purposes.

        Returns:
            A str representation of the Checklist.

        """
        step_count = len(self.steps)
        counter = 1
        output = '{ Checklist Object: name: ' + self.name
        output += ' | message: ' + self.message
        output += ' | count_of_steps: ' + str(step_count)
        output += ' | step numbers: ['
        for step in self.steps:
            if counter < step_count:
                if step is not None:
                    output += str(step.step_number) + ', '
                counter += 1
            else:
                output += str(step.step_number) + '] '
        counter = 1
        output += ' | steps: ['
        for step in self.steps:
            if counter < step_count:
                if step is not None:
                    output += str(step) + ', '
                counter += 1
            else:
                output += str(step) + ']'
        output = output + ' }'
        return output

    def sort_checklist(self):
        """Sort the checklist."""
        self.steps = sorted(self.steps, key=lambda step: step.step_number)


class Plane():
    """This is class to represent a plane and all of its data.

    Attributes:
        plane_name (str): The name of the plane.
        plane_info (List of str): The additional information used in the plane.
        It will be expanded in a future releas.
        checklists (list of Checklist): The list containing all of the
        checklists for the plane.

    Args:
        plane_name: The name of the plane.
        plane_info: The additional info from the plane.
        checklists: The list of Checklists for the plane.

    """

    def __init__(self, plane_name: str,
                 plane_info: List[Dict[str, str]] = None,
                 checklists: List[Checklist] = None):
        """Class Constructor."""
        self.plane_name = plane_name
        self.plane_info = plane_info
        self.checklists = checklists
        if self.plane_info is None:
            self.plane_info = []
        if self.checklists is None:
            self.checklists = []
            self.checklists.append(Checklist('blank_list',
                                             'There are no checklists for '
                                             'this plane'))

    def __str__(self):
        """Turn class into a str.

        Returns:
            A str representation of the Plane.

        """
        checklist_count = len(self.checklists)
        counter = 1
        output = '{ plane_name: ' + self.plane_name + ' | plane_info: '
        output += str(self.plane_info)
        output += ' | checklists: [' + '\n'
        for checklist in self.checklists:
            if counter < checklist_count:
                output += str(checklist) + ',\n'
                counter += 1
            else:
                output += str(checklist) + '\n]'
        output += ' }'
        return output

    def __repr__(self):
        """Turn a class into a str for debugging purposes.

        Returns:
            A str representation of the Plane.

        """
        checklist_count = len(self.checklists)
        plane_info_count = len(self.plane_info)
        counter = 1
        output = '{ Plane Object: plane_name: ' + self.plane_name
        output += ' | # of Plane Info Pairs: ' + str(plane_info_count)
        output += ' | plane_info: ' + str(self.plane_info)
        output += ' | # of Checklists: ' + str(checklist_count)
        output += ' | checklists: [\n'
        for checklist in self.checklists:
            if counter < checklist_count:
                output += repr(checklist) + ',\n'
                counter += 1
            else:
                output += repr(checklist) + '\n]'
        output += ' }'
        return output
