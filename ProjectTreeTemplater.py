#!/usr/bin/env python
# Copyright (c) 2013 Julian Xhokaxhiu.
# License: GPL (http://www.gnu.org/licenses/gpl.html)

import os
import shutil
import urllib
import sublime
import sublime_plugin

# *** GLOBAL VARS ****

# This will represent the current directory of this application
currentdir = None

# This is the dictionary that will contain the extension-path key-value pair
# Ex.:
#     pdf - /path/to/template.pdf
#     js - /path/to/template.js
templateslist = {}

# This will represent the parent folder for each path
groupDir = ''

# *** GENERIC METHODS ****

def noop(fake):
    pass

def raise_error(msg):
    sublime.error_message("ProjectTreeTemplater: An error happened. Please look at the statusbar for extended details.")
    sublime.status_message(msg)

# *** TEMPLATE METHODS ****

def new_template_file(fullpath):
    # If the file has no templates
    if not copy_template(fullpath):
        # Touch the file
        open(fullpath,'w').close()

def add_template_to_list(spath):
    # Remove the ? first character
    if spath[0] == '?':
        spath = spath.lstrip('?')

    global templateslist
    sx,sep,dx = spath.partition(':')
    # Remove the . before the name of the extension (if it is present)
    sx = sx.lstrip('.')
    # Remove the root if inserted
    dx = dx.lstrip('/')
    # Add the extension  to the template list
    templateslist[sx] = currentdir + '/' + dx

def copy_template(spath):
    bret = False

    # Get path to file, and its extension
    spath,ext = os.path.splitext(spath)
    ext = ext.lstrip('.') #Remove the . if present

    # if any template was defined before, let's copy it with the path the user chose
    if ext in templateslist:
        templatepath = templateslist[ext]
        fullpath = spath + '.' + ext
        if 'http://' in templatepath or 'https://' in templatepath:
            try:
                urllib.urlretrieve(templatepath,fullpath)
                bret = True
            except Exception:
                raise_error("The path of the template for the extension '" + ext + "' does not exists or isn't accessible. Will continue with an empty file.")
        else:
            try:
                shutil.copyfile(templatepath,fullpath)
                bret = True
            except Exception:
                raise_error("The path of the template for the extension '" + ext + "' does not exists or isn't accessible. Will continue with an empty file.")

    return bret

# *** PARSE METHODS ****

# Add the path if the path doesn't exists
def add_path(spath):

    templatepath = None
    if spath.find(':') > -1:
        spath,sep,templatepath = spath.partition(':')

    # Get the full path to the file we have to add
    fullpath = currentdir + '/' + groupDir + spath

    # Remove the / first character, avoid root paths
    if spath[0] == '/':
        spath = path.lstrip('/')

    if not os.path.exists(fullpath):
        # Add the path (if exists)
        dirs = os.path.dirname(spath)
        if len(dirs) > 0:
            fulldirspath = currentdir + '/' + dirs
            if not os.path.exists(fulldirspath):
                os.makedirs(fulldirspath)

        if len(os.path.basename(fullpath)) > 0:
            # If this file has his own template
            if not templatepath is None:
                if 'http://' in templatepath or 'https://' in templatepath:
                    try:
                        urllib.urlretrieve(templatepath,fullpath)
                    except Exception:
                        raise_error("The template for file '" + spath + "' does not exists or you do not have the rights to write in the specified path. Will continue with an empty file or generic template (if defined).")
                        new_template_file(fullpath)
                else:
                    try:
                        shutil.copyfile(templatepath,fullpath)
                    except Exception:
                        raise_error("The template for file '" + spath + "' does not exists or you do not have the rights to write in the specified path. Will continue with an empty file or generic template (if defined).")
                        new_template_file(fullpath)
            else:
                new_template_file(fullpath)

# Remove always the path, if it exists
def remove_path(spath):
    if spath.find(':') > -1:
        raise

    # Remove the - first character
    if spath[0] == '-':
        spath = spath.lstrip('-')

    # Remove the / first character, avoid root paths
    if spath[0] == '/':
        spath = spath.lstrip('/')

    filename = path.basename(spath)
    fullpath = currentdir + '/' + spath
    if filename == '*':
        # Remove all files in that dir
        clean_dir(path.dirname(fullpath))
    if path.exists(fullpath):
        if len(filename) > 0:
            # Remove the file
            os.unlink(fullpath)

# Add a global parent path and prepend it to each path contained inside this group
def set_group(spath):
    spath = spath.rstrip('(').strip()
    groupDir = spath + '/'

# Remove the parent path
def unset_group(spath):
    groupDir = ''

# *** CORE METHODS ***

def clean_dir(spath):
    if os.path.exists(spath):
        for filename in os.listdir(spath):
            filepath = spath+'/'+filename
            if os.path.exists(filepath):
                os.remove(filepath)
        os.rmdir(spath)

def update_project_tree(view):
# get the current dir
    global currentdir
    currentdir = '' if view.file_name() is None else view.file_name()

    # This will be the first character in every line which will tell us,
    # what to do for every line we will parse.
    # The default function, is 'add_path' if no line begins with any
    # of this characters.
    ptcMetaCommands = {
        '-':remove_path,
        '#':noop,
        '?':add_template_to_list
    }

    # This will be the last character for every line, and if matched
    # the relative function will be called.
    groupMetaCommands = {
        '(':set_group,
        ')':unset_group
    }

    if len(currentdir) == 0:
        # Error
        raise_error("The file must be saved before using this command and it has to be with a '.stprj' extension.")
    elif os.path.splitext(os.path.basename(currentdir))[1] == '.stprj':
        # Get the current directory
        currentdir = os.path.dirname(currentdir)

        # get non-empty selections
        regions = [s for s in view.sel() if not s.empty()]

        # if there's no non-empty selection, filter the whole document
        if len(regions) == 0:
            regions = [sublime.Region(0, view.size())]

        for region in reversed(regions):
            lines = view.split_by_newlines(region)

            for line in lines:
                spath = view.substr(line).strip()
                if len(spath) > 0:
                    try:
                        if spath[0] in ptcMetaCommands:
                            ptcMetaCommands[spath[0]](spath)
                        else if spath[-1:] in groupMetaCommands:
                            groupMetaCommands[spath[-1:]](spath)
                        else:
                            add_path(spath)
                    except Exception:
                        raise_error("Syntax Error. Please fix it and try again.")
                        raise
        sublime.status_message("All done! Project created :)")

# *** SUBLIME HOOKS ****

class ProjectTreeTemplaterCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        update_project_tree(self.view)

class ProjectTreeTemplaterEventListener(sublime_plugin.EventListener):
    # Execute the project creation after the user has saved the file
    def on_post_save(self, view):
        # Read the global settings for the plugin
        global_settings = sublime.load_settings(__name__ + '.sublime-settings')

        # Do we need to update the project tree? True if it is not defined
        should_update = view.settings().get('update_project_on_save', global_settings.get('update_project_on_save', True))

        if should_update:
            update_project_tree(view)