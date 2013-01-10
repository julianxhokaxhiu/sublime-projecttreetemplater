# Project Tree Templater - Bring templates to your project!

## Introduction

This is a simple plugin for <code>Sublime Text 2</code> to create a template for your project. But what could a template for a project?
Imagine that you're creating your project literally from zero. You first have to create a folder called "css" where you will put all your CSS files in. Like before, you'll do a "js" folder, where you'll put your Javascript files in. And finally you'll create also an index.html where you will put your HTML inside of it.

Of course, this could be the probably not-common case of work, but in fact, sometimes happenes, from creating templates to starting little projects.

Today, with this plugin you can automate all your work, with only a few line of meta declarations, and everytime your project file will be saved, it will be reflected to your project folder. Simple as it should be.

## How it works

The only thing you have to do is creating a <code>.stprj</code> file wherever you want, remember than ANYTHING will be created in the same place where, that file, will be saved.

After that, what you have to do is declaring your project structure as likely you're used to do manually.
For example, the project mentioned in the <code>Introduction</code> before, could be written as the following:

    css/
    js/
    index.html

Yes, that's it. Pretty simple and clean! Didn't you remember something? Yeah, Unix path declaration. Nothing more, you have all the basis you would need to use this plugin. Nothing new.

## Reference

* To simply place a comment in your source script use the <code>#</code> character as the first character of your line. An example of use would be:

        # Example of comment

* To simply remove any file from your project everytime you save place the <code>-</code> character as the first character of your line. An example of use would be:

        -css/style.css

    but let we suppose we're going to remove all files inside the folder (and the folder itself), then we have to write:

        -css/*

* To place a *default* template for *every* file which will be created with that extension we will use the <code>?</code> character as the first character of your line. An example of use would be:

        ?css:path/to/tpl.css
        ...
        css/style.css

    remember that global templates MUST be declared before ANY path declaration.

* To place a single template for a single file, overriding also the global template (if it exists), we have to write the <code>:</code> character AFTER the path declaration. An example of use would be:

        css/style.css:path/to/tpl.css

### And remember!

If you place a <code>/</code> character at the beginning of any path (template or not), the path will be *always* considered RELATIVE to the project file.

## How to install

Soon it will be available to [Sublime Package Control](http://wbond.net/sublime_packages/package_control).
So what you have to do is: press code>Ctrl+Shift+P</code>, type <code>install</code>, press <code>Enter</code> then type <code>ProjectTreeTemplater</code> and finally press again the <code>Enter</code> key.

In the meanwhile, to install it you just have to download a copy of this folder, and copy it to the one of your already existing packages. To find it, simply open Sublime Text and then do
    
    Preferences -> Browse Packages...

and place it inside that folder.

### Only for Windows!

If you have package control enabled you have to specify it in your list. To do that you simply have to press <code>Ctrl+Shift+P</code> and type <code>Package Control Settings - User</code>, press the <code>Enter</code> key and then, in the list put this inside:
    
    "ProjectTreeTemplater"

## License

Project Tree Templater - Bring templates to your project!<br/>
Copyright (C) 2013 Julian Xhokaxhiu

This program is free software: you can redistribute it and/or modify<br/>
it under the terms of the GNU General Public License as published by<br/>
the Free Software Foundation, either version 3 of the License, or<br/>
(at your option) any later version.

This program is distributed in the hope that it will be useful,<br/>
but WITHOUT ANY WARRANTY; without even the implied warranty of<br/>
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the<br/>
GNU General Public License for more details.

You should have received a copy of the GNU General Public License<br/>
along with this program.  If not, see <http://www.gnu.org/licenses/>.

## Last but not least

This plugin is far from perfect, so if you find any bug you're free to contribute :)
