import os
import re
import sys
# Path to bbfetch repository
sys.path += [os.path.expanduser('~/Projects/bbfetch')]
import blackboard.grading


class Grading(blackboard.grading.Grading):
    # Username used to log in to Blackboard
    username = '201303589'
    # Blackboard course id (of the form '_NNNNN_1')
    course = '_124138_1'
    # Names of classes/groups of students to display
    # If you need to grade hand-ins of all students in the course,
    # put classes = all
    classes = ['Class 2']
    # Regex pattern and replacement text to abbreviate group names
    student_group_display_regex = (r'Class (\d+)', r'\1')
    # Regex pattern and replacement text to abbreviate handin names
    assignment_name_display_regex = (r'(\S+) compulsory assignment', r'\1')
    # Template indicating where to save each handin
    # attempt_directory_name = '~/Grading/W{assignment}-{class_name}/{group}_{id}'
    # Case-insensitive regex used to capture comments indicating a score of 0
    rehandin_regex = r'genaflevering|re-?handin'
    # Case-insensitive regex used to capture comments indicating a score of 1
    accept_regex = r'accepted|godkendt'

    def get_attempt_directory_name(self, attempt):
        """
        Return a path to the directory in which to store files
        relating to the given handin.
        """

        name = attempt.student.name
        attempt_id = attempt.id
        if attempt_id.startswith('_'):
            attempt_id = attempt_id[1:]
        if attempt_id.endswith('_1'):
            attempt_id = attempt_id[:-2]

        m = {'First': '1', 'Second': '2', 'Third': 3, 'Fourth': 4, 'Fifth': 5, 'Sixth': 6}
        assignment= "Handin " + m[self.get_assignment_name_display(attempt.assignment)]

        return '{base}/{assignment}/{name}_{id}'.format(
            base=os.path.expanduser('~/Grading'),
            assignment=assignment,
            name=name, id=attempt_id)


if __name__ == "__main__":
    Grading.execute_from_command_line()
