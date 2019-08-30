"""
Example of using py_cui to create a simple git control

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
        self.add_files_menu = self.root.add_scroll_menu('Add Files', 0, 0, row_span=4, column_span=2)
        self.add_files_menu.help_text = 'Enter - git add, Space - see diff, Arrows - scroll, Esc - exit'

        self.branch_menu = self.root.add_scroll_menu('Git Branches', 4, 0, row_span=3, column_span=2, pady=1)

        self.refresh_git_status()

        self.diff_text_block = self.root.add_text_block('Git Info', 0, 2, row_span=8, column_span=6)
        self.diff_text_block.add_text_color_rule(['+'], py_cui.GREEN_ON_BLACK, 'startswith')
        self.diff_text_block.add_text_color_rule(['-'], py_cui.RED_ON_BLACK, 'startswith')
        self.diff_text_block.add_text_color_rule(['commit'], py_cui.YELLOW_ON_BLACK, 'startswith')

        #self.tag_textbox = self.root.add_text_box('New Tag', 9, 5, column_span=3)
        self.new_branch_textbox = self.root.add_text_box('New Branch', 8, 0, column_span=2)
        self.commit_message_box = self.root.add_text_box('Commit Message', 8, 2, column_span=6)


        self.refresh_button = self.root.add_button('Refresh', 7, 0, command=self.refresh_git_status)
        self.log_button = self.root.add_button('Git Log', 7, 1, command=self.show_log)
        

        self.add_files_menu.add_key_command(py_cui.keys.KEY_ENTER, self.add_revert_file)
        self.add_files_menu.add_key_command(py_cui.keys.KEY_SPACE, self.open_git_diff)
        self.branch_menu.add_key_command(py_cui.keys.KEY_ENTER, self.checkout_branch)
        self.new_branch_textbox.add_key_command(py_cui.keys.KEY_ENTER, self.create_new_branch)
        self.commit_message_box.add_key_command(py_cui.keys.KEY_ENTER, self.commit_changes)
        #self.tag_textbox.add_key_command(py_cui.keys.KEY_ENTER, self.create_new_tag)


    """
    def create_new_tag(self):
        tagname = self.tag_textbox.get()
        try:
            proc = Popen(['git', 'tag', tagname], stdout=PIPE, stderr=PIPE)
            out, err = proc.communicate()
            res = proc.returncode
            if res != 0:
                self.root.show_error_popup('Tag Failed', '{}'.format(err))
        except:
            self.root.show_warning_popup('Git Failed', 'Unable to reset file, please check git installation')
    """


    def show_log(self):
        proc = Popen(['git', '--no-pager', 'log'], stdout=PIPE, stderr=PIPE)
        out, err = proc.communicate()
        out = out.decode()
        self.diff_text_block.title='Git Log'
        self.diff_text_block.set_text(out)


    def create_new_branch(self):
        new_branch_name = self.new_branch_textbox.get()
        if len(new_branch_name) == 0:
            self.root.show_error_popup('Invalid Name', 'Please enter a new branch name')
            return
        try:
            proc = Popen(['git', 'checkout', '-b', new_branch_name])
            out, err = proc.communicate()
            res = proc.returncode
            if res != 0:
                self.root.show_error_popup('Create Branch Failed Failed', '{}'.format(err))
                return
            self.refresh_git_status(preserve_selected=True)
            self.new_branch_textbox.clear()
            self.root.show_message_popup('Success', 'Checked out branch {}'.format(new_branch_name))
        except:
            self.root.show_warning_popup('Git Failed', 'Unable to checkout branch, please check git installation')


    def commit_changes(self):
        message = self.commit_message_box.get()
        if len(message) == 0:
            self.root.show_error_popup('Invalid Commit Message', 'Please enter a commit message')
            return
        proc = Popen(['git', 'commit', '-m', '"{}"'.format(message)])
        out, err = proc.communicate()
        res = proc.returncode
        if res != 0:
            self.root.show_error_popup('Create Branch Failed Failed', '{}'.format(err))
            return
        self.refresh_git_status(preserve_selected=True)
        self.commit_message_box.clear()
        self.root.show_message_popup('Success', 'Commited: {}'.format(message))


    def checkout_branch(self):
        try:
            target = self.branch_menu.get()[2:]
            proc = Popen(['git', 'checkout', target])
            out, err = proc.communicate()
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
            proc = Popen(['git', 'reset', 'HEAD', target])
            self.refresh_git_status(preserve_selected=True)
        except:
            self.root.show_warning_popup('Git Failed', 'Unable to reset file, please check git installation')


    def open_git_diff(self):
        target = self.add_files_menu.get()[3:]
        self.diff_text_block.title = '{} File Diff'.format(target)
        proc = Popen(['git', 'diff', target], stdout=PIPE, stderr=PIPE)
        out, err = proc.communicate()
        out = out.decode()
        self.diff_text_block.set_text(out)


    def add_revert_file(self):
        try:
            target = self.add_files_menu.get()
            if target.startswith(' ') or target.startswith('?'):
                target = target[3:]
                proc = Popen(['git', 'add', target], stdout=PIPE, stderr=PIPE)
                self.refresh_git_status(preserve_selected=True)
            else:
                self.revert_changes()
        except:
            self.root.show_warning_popup('Git Failed', 'Unable to reset file, please check git installation')


    def refresh_git_status(self, preserve_selected=False):

        try:
            selected_branch = self.branch_menu.selected_item
            proc = Popen(['git', 'branch'], stdout=PIPE, stderr=PIPE)
            out, err = proc.communicate()
            out = out.decode().splitlines()
            self.branch_menu.clear()
            self.branch_menu.add_item_list(out)

            selected_file = self.add_files_menu.selected_item
            proc = Popen(['git', 'status', '-s'], stdout=PIPE, stderr=PIPE)
            out, err = proc.communicate()
            out = out.decode().splitlines()
            self.add_files_menu.clear()
            self.add_files_menu.add_item_list(out)
            if preserve_selected:
                if len(self.branch_menu.get_item_list()) > selected_branch:
                    self.branch_menu.selected_item = selected_branch
                if len(self.add_files_menu.get_item_list()) > selected_file:
                    self.add_files_menu.selected_item = selected_file

        except:
            self.root.show_warning_popup('Git Failed', 'Unable to get git status, please check git installation')



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
frame = AutoGitCUI(root, dir)
root.start()
