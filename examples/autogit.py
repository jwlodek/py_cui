"""
Example of using py_cui to create a simple git control.
This example is expanded into a full application with https://github.com/jwlodek/pyautogit

@author:    Jakub Wlodek
@created:   27-Aug-2019
"""

import py_cui
import os
import argparse
import getpass
from subprocess import Popen, PIPE


__version__ = '0.0.1'


class AutoGitCUI:

    def __init__(self, root, dir):
        self.root = root
        self.dir = dir
        os.chdir(self.dir)
        proc = Popen(['git', 'status', '-s'], stdout=PIPE, stderr=PIPE)
        while proc.returncode is None:
            proc.wait()
        res = proc.returncode
        if res != 0:
            print(res)
            print('ERROR - fatal, {} is not a git repository.'.format(self.dir))
            exit()

        self.dir = os.path.abspath(self.dir)
        self.root.set_title('Autogit v{} - {}'.format(__version__, os.path.basename(self.dir)))

        # Keybindings when in overview mode, and set info bar
        self.root.add_key_command(py_cui.keys.KEY_R_LOWER, self.refresh_git_status)
        self.root.add_key_command(py_cui.keys.KEY_L_LOWER, self.show_log)
        self.root.add_key_command(py_cui.keys.KEY_A_LOWER, self.add_all)
        self.root.add_key_command(py_cui.keys.KEY_E_LOWER, self.open_editor)
        self.root.add_key_command(py_cui.keys.KEY_F_LOWER, self.fetch_branch)
        self.root.add_key_command(py_cui.keys.KEY_P_LOWER, self.push_branch)
        self.root.add_key_command(py_cui.keys.KEY_M_LOWER, self.show_menu)
        self.root.set_status_bar_text('Quit - q | Refresh - r | Add all - a | Git log - l | Open Editor - e | Pull Branch - f | Push Branch - p')

        # Create the add files menu. Add color rules to color first characters based on git status
        self.add_files_menu = self.root.add_scroll_menu('Add Files', 0, 0, row_span=2, column_span=2)
        self.add_files_menu.add_text_color_rule(' ', py_cui.RED_ON_BLACK, 'startswith', match_type='region', region=[0,3], include_whitespace=True)
        self.add_files_menu.add_text_color_rule('?', py_cui.RED_ON_BLACK, 'startswith', match_type='region', region=[0,3], include_whitespace=True)
        self.add_files_menu.add_text_color_rule(' ', py_cui.GREEN_ON_BLACK, 'notstartswith', match_type='region', region=[0,3], include_whitespace=True)
        self.add_files_menu.add_text_color_rule('?', py_cui.GREEN_ON_BLACK, 'notstartswith', match_type='region', region=[0,3], include_whitespace=True)

        # Remotes menu
        self.git_remotes_menu =self.root.add_scroll_menu('Git Remotes', 2, 0, row_span=2, column_span=2)

        # Branches menu
        self.branch_menu = self.root.add_scroll_menu('Git Branches', 4, 0, row_span=2, column_span=2)

        # Commits menu
        self.git_commits_menu = self.root.add_scroll_menu('Recent Commits', 6, 0, row_span=2, column_span=2)

        # Initialize the menus with current repo git info
        self.refresh_git_status()

        # Our text block for statuses etc.
        self.diff_text_block = self.root.add_text_block('Git Info', 0, 2, row_span=8, column_span=6)
        self.diff_text_block.add_text_color_rule('+', py_cui.GREEN_ON_BLACK, 'startswith')
        self.diff_text_block.add_text_color_rule('-', py_cui.RED_ON_BLACK, 'startswith')
        self.diff_text_block.add_text_color_rule('commit', py_cui.YELLOW_ON_BLACK, 'startswith')
        self.diff_text_block.add_text_color_rule('Copyright', py_cui.CYAN_ON_BLACK, 'startswith')
        self.diff_text_block.add_text_color_rule('@.*@', py_cui.CYAN_ON_BLACK, 'contains', match_type='regex')
        self.diff_text_block.set_text(self.get_logo())
        
        # Textboxes for new branches and commits
        self.new_branch_textbox = self.root.add_text_box('New Branch', 8, 0, column_span=2)
        self.commit_message_box = self.root.add_text_box('Commit Message', 8, 2, column_span=6)

        # Key commands for our file menus. Enter will git add, Space will show diff
        self.add_files_menu.add_key_command(py_cui.keys.KEY_ENTER, self.add_revert_file)
        self.add_files_menu.add_key_command(py_cui.keys.KEY_SPACE, self.open_git_diff)
        self.add_files_menu.set_help_text('Enter - git add, Space - see diff, Arrows - scroll, Esc - exit')

        # Enter will show remote info
        self.git_remotes_menu.add_key_command(py_cui.keys.KEY_ENTER, self.show_remote_info)

        # Enter will show commit diff
        self.git_commits_menu.add_key_command(py_cui.keys.KEY_ENTER, self.show_git_commit_diff)
        self.git_commits_menu.add_text_color_rule(' ', py_cui.GREEN_ON_BLACK, 'notstartswith', match_type='region', region=[0,7], include_whitespace=True)

        # Enter will checkout 
        self.branch_menu.add_key_command(py_cui.keys.KEY_ENTER, self.checkout_branch)
        self.branch_menu.add_key_command(py_cui.keys.KEY_SPACE, self.show_log)

        # Add commands for committing and branch checkout.
        self.new_branch_textbox.add_key_command(py_cui.keys.KEY_ENTER, self.create_new_branch)
        self.commit_message_box.add_key_command(py_cui.keys.KEY_ENTER, self.ask_to_commit)


    def get_logo(self):
        logo =         "         _    _ _______ ____   _____ _____ _______\n" 
        logo = logo +  "    /\\  | |  | |__   __/ __ \\ / ____|_   _|__   __|\n"
        logo = logo +  "   /  \\ | |  | |  | | | |  | | |  __  | |    | |   \n"
        logo = logo +  "  / /\\ \\| |  | |  | | | |  | | | |_ | | |    | |   \n"
        logo = logo +  " / ____ \\ |__| |  | | | |__| | |__| |_| |_   | |   \n"
        logo = logo +  "/_/    \\_\\____/   |_|  \\____/ \\_____|_____|  |_|   \n\n\n"
        logo = logo + "Powered by the py_cui Python Command Line UI Library:\n\n"
        logo = logo + "https://github.com/jwlodek/py_cui\n\n"
        logo = logo + "Documentation available online here: https://jwlodek.github.io/py_cui\n\n"
        logo = logo + "Star me on Github!\n\n"
        logo = logo + "Copyright (c) 2019-2020 Jakub Wlodek\n\n"
        return logo


    def process_menu_option(self, option):

        self.root.set_title(option)


    def show_menu(self):
        option_list = ['Add all', 'Push', 'Pull', 'Stash', 'Pop Stash', 'Set Editor']
        self.root.show_menu_popup('Autogit Menu', option_list, self.process_menu_option)

    def show_git_commit_diff(self):
        try:
            commit_val = self.git_commits_menu.get()[:7]
            proc = Popen(['git', 'diff', commit_val], stdout=PIPE, stderr=PIPE)
            out, _ = proc.communicate()
            out = out.decode()
            self.diff_text_block.set_title('Git Diff for {}'.format(commit_val))
            self.diff_text_block.set_text(out)
        except:
            self.root.show_warning_popup('Git Failed', 'Unable to read commit diff information')

    def add_all(self):
        try:
            proc = Popen(['git', 'add', '-A'], stdout=PIPE, stderr=PIPE)
            _, _ = proc.communicate()
            self.refresh_git_status(preserve_selected=True)
        except:
            self.root.show_warning_popup('Git Failed', 'Unable to reset file, please check git installation')


    def show_remote_info(self):
        try:
            remote = self.git_remotes_menu.get()
            proc = Popen(['git', 'remote', 'show', '-n', remote], stdout=PIPE, stderr=PIPE)
            out, _ = proc.communicate()
            out = out.decode()
            self.diff_text_block.set_title('Git Remote Info')
            self.diff_text_block.set_text(out)
        except:
            self.root.show_warning_popup('Git Error', 'Unable to open git remote info, please check git installation')


    def open_editor(self):
        try:
            _ = Popen(['code', '.'], stdout=PIPE, stderr=PIPE)
        except:
            self.root.show_warning_popup('Open Failed', 'Please install VSCode')

    def show_log(self):
        try:
            branch = self.branch_menu.get()[2:]
            proc = Popen(['git', '--no-pager', 'log', branch], stdout=PIPE, stderr=PIPE)
            out, _ = proc.communicate()
            out = out.decode()
            self.diff_text_block.set_title('Git Log')
            self.diff_text_block.set_text(out)
        except:
            self.root.show_warning_popup('Git Error', 'Unable to open git log, please check git installation')


    def create_new_branch(self):
        new_branch_name = self.new_branch_textbox.get()
        if len(new_branch_name) == 0:
            self.root.show_error_popup('Invalid Name', 'Please enter a new branch name')
            return
        try:
            proc = Popen(['git', 'checkout', '-b', new_branch_name])
            _, err = proc.communicate()
            res = proc.returncode
            if res != 0:
                self.root.show_error_popup('Create Branch Failed Failed', '{}'.format(err))
                return
            self.refresh_git_status(preserve_selected=True)
            self.new_branch_textbox.clear()
            self.root.show_message_popup('Success', 'Checked out branch {}'.format(new_branch_name))
        except:
            self.root.show_warning_popup('Git Failed', 'Unable to checkout branch, please check git installation')


    def ask_to_commit(self):
        self.root.show_yes_no_popup('Would you like to commit?', self.commit_changes)


    def commit_changes(self, commit):
        if(commit):
            message = self.commit_message_box.get()
            if len(message) == 0:
                self.root.show_error_popup('Invalid Commit Message', 'Please enter a commit message')
                return
            proc = Popen(['git', 'commit', '-m', message])
            _, err = proc.communicate()
            res = proc.returncode
            if res != 0:
                self.root.show_error_popup('Create Branch Failed Failed', '{}'.format(err))
                return
            self.refresh_git_status(preserve_selected=True)
            self.commit_message_box.clear()
            self.root.show_message_popup('Success', 'Commited: {}'.format(message))
        else:
            self.root.show_message_popup('Cancelled', 'Commit Operation cancelled')


    def checkout_branch(self):
        try:
            target = self.branch_menu.get()[2:]
            proc = Popen(['git', 'checkout', target])
            out, _ = proc.communicate()
            res = proc.returncode
            if res != 0:
                self.root.show_error_popup('Checkout Failed', '{}'.format(out))
                return
            self.refresh_git_status(preserve_selected=True)
            self.root.show_message_popup('Success', 'Checked out branch {}'.format(target))
        except:
            self.root.show_warning_popup('Git Failed', 'Unable to checkout branch, please check git installation')


    def revert_changes(self):
        try:
            target = self.add_files_menu.get()[3:]
            _ = Popen(['git', 'reset', 'HEAD', target])
            self.refresh_git_status(preserve_selected=True)
        except:
            self.root.show_warning_popup('Git Failed', 'Unable to reset file, please check git installation')


    def open_git_diff(self):
        target = self.add_files_menu.get()[3:]
        self.diff_text_block.title = '{} File Diff'.format(target)
        proc = Popen(['git', 'diff', target], stdout=PIPE, stderr=PIPE)
        out, _ = proc.communicate()
        out = out.decode()
        self.diff_text_block.set_text(out)


    def add_revert_file(self):
        try:
            target = self.add_files_menu.get()
            if target.startswith(' ') or target.startswith('?'):
                target = target[3:]
                _ = Popen(['git', 'add', target], stdout=PIPE, stderr=PIPE)
                self.refresh_git_status(preserve_selected=True)
            else:
                self.revert_changes()
        except:
            self.root.show_warning_popup('Git Failed', 'Unable to reset file, please check git installation')


    def refresh_git_status(self, preserve_selected=False):

        try:
            proc = Popen(['git', 'branch'], stdout=PIPE, stderr=PIPE)
            out, _ = proc.communicate()
            out = out.decode().splitlines()
            self.branch_menu.clear()
            self.branch_menu.add_item_list(out)
            selected_branch = 0
            for branch in self.branch_menu.get_item_list():
                if branch.startswith('*'):
                    break
                selected_branch = selected_branch + 1

            remote = self.git_remotes_menu.get_selected_item()
            proc = Popen(['git', 'remote'], stdout=PIPE, stderr=PIPE)
            out, _ = proc.communicate()
            out = out.decode().splitlines()
            self.git_remotes_menu.clear()
            self.git_remotes_menu.add_item_list(out)

            proc = Popen(['git', '--no-pager', 'log', self.branch_menu.get()[2:], '--oneline'], stdout=PIPE, stderr=PIPE)
            out, _ = proc.communicate()
            out = out.decode().splitlines()
            self.git_commits_menu.clear()
            self.git_commits_menu.add_item_list(out)

            selected_file = self.add_files_menu.get_selected_item()
            proc = Popen(['git', 'status', '-s'], stdout=PIPE, stderr=PIPE)
            out, _ = proc.communicate()
            out = out.decode().splitlines()
            self.add_files_menu.clear()
            self.add_files_menu.add_item_list(out)

            if preserve_selected:
                if len(self.branch_menu.get_item_list()) > selected_branch:
                    self.branch_menu.set_selected_item(selected_branch)
                if len(self.git_remotes_menu.get_item_list()) > remote:
                    self.git_remotes_menu.selected_item = remote
                if len(self.add_files_menu.get_item_list()) > selected_file:
                    self.add_files_menu.set_selected_item(selected_file)

        except:
            self.root.show_warning_popup('Git Failed', 'Unable to get git status, please check git installation')


    def fetch_branch(self):
        try:
            target = self.branch_menu.get()[2:]
            remote = self.remote_menu.get()
            proc = Popen(['git', 'pull', remote, target, target])
            out, _ = proc.communicate()
            res = proc.returncode
            if res != 0:
                self.root.show_error_popup('Checkout Failed', '{}'.format(out))
                return
            self.refresh_git_status(preserve_selected=True)
            self.root.show_message_popup('Success', 'Checked out branch {}'.format(target))
        except:
            self.root.show_warning_popup('Git Failed', 'Unable to checkout branch, please check git installation')

    def push_branch(self):
        self.root.show_warning_popup('Unsupported Error', 'The git push operation is not yet supported.')


def parse_args():
    parser = argparse.ArgumentParser(description='An extension on nano for editing directories in CLI.')
    parser.add_argument('directory', help='Target directory to edit.')
    args = vars(parser.parse_args())
    if 'directory' not in args.keys():
        return '.' 
    elif not os.path.exists(args['directory']):
        print('ERROR - {} path does not exist'.format(args['directory']))
        exit()
    elif not os.path.isdir(args['directory']):
        print('ERROR - {} is not a directory'.format(args['directory']))
        exit()
    return args['directory']


dir = parse_args()
root = py_cui.PyCUI(9, 8)
root.toggle_unicode_borders()
frame = AutoGitCUI(root, dir)
root.start()
