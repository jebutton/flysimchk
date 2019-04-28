"""Main Control Script for the flisick demo project.

Copyright 2019 Jacqueline Button.

"""
from cli_controls import CliStyle
from cli_controls import show_checklist
from cli_controls import show_checklist_selection_page
from cli_controls import show_plane_select_menu
from fileio import search_directory_for_planes

def main_loop():
    """Main Loop of flisick demo program."""
    app_style = CliStyle()
    flag = False
    checklist_select_loop_flag = False
    checklist_loop_flag = False
    while not flag:
        list_of_planes = search_directory_for_planes('./data')
        selected_plane = show_plane_select_menu(list_of_planes, app_style)
        if selected_plane is None:
            break
        while not checklist_select_loop_flag:
            selected_checklist = show_checklist_selection_page(selected_plane, app_style)
            if selected_checklist == 'RETURN TO PLANE SELECT':
                break
            else:
                while not checklist_loop_flag:
                    checklist_result = show_checklist(selected_plane, selected_checklist, app_style)
                    if checklist_result == 'EXIT':
                        flag = True
                        checklist_select_loop_flag = True
                        checklist_loop_flag = True
                    elif checklist_result == 'RETURN TO LIST SELECT':
                        checklist_loop_flag = True
                        break

main_loop()
