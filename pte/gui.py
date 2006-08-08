### Copyright (C) 2002-2006 Eli Yukelzon <reflog@gmail.com>

### This program is free software; you can redistribute it and/or modify
### it under the terms of the GNU General Public License as published by
### the Free Software Foundation; either version 2 of the License, or
### (at your option) any later version.

### This program is distributed in the hope that it will be useful,
### but WITHOUT ANY WARRANTY; without even the implied warranty of
### MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
### GNU General Public License for more details.

### You should have received a copy of the GNU General Public License
### along with this program; if not, write to the Free Software
### Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA


# GTK/Gnome imports
import pygtk
pygtk.require('2.0')
import gtk,pango,vte,gconf

# Python imports
import os, sys

# Local imports
from settings import conf
import commands

def add_icon_to_button(button, icon_id):
    iconBox = gtk.HBox(False, 0)
    image = gtk.Image()
    image.set_from_stock(icon_id,gtk.ICON_SIZE_MENU)
    gtk.Button.set_relief(button,gtk.RELIEF_NONE)
    settings = gtk.Widget.get_settings (button);
    (w,h) = gtk.icon_size_lookup_for_settings(settings,gtk.ICON_SIZE_MENU);
    gtk.Widget.set_size_request (button, w + 4, h + 4);
    image.show()
    iconBox.pack_start(image, True, False, 0)
    button.add(iconBox)

def input_dialog(parent,title,message,previous_text=""):
    dlg = gtk.Dialog(title,parent,0,
               buttons=(   gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                           gtk.STOCK_APPLY, gtk.RESPONSE_YES
                       )
                    )
    hbox = gtk.HBox(False,8)
    dlg.vbox.pack_start(hbox, False, False, 0)
    label = gtk.Label(message)
    hbox.pack_start(label, False, False, 0)
    e = gtk.Entry()
    e.set_text(previous_text)
    hbox.pack_start(e, False, False, 0)
    dlg.show_all()
    ret = dlg.run()
    if ret == gtk.RESPONSE_YES:
        result = e.get_text()
    else:
        result = None
    dlg.destroy()
    return result

def create_custom_tab(notebook, title, profile, close_event):
    if not title: title = profile['title']
    eventBox = gtk.EventBox()
    tabBox = gtk.HBox(False, 2)
    tabLabel = gtk.Label(title)

    tabButton=gtk.Button()
    tabButton.connect('clicked',close_event, notebook)

    #Add a picture on a button
    add_icon_to_button(tabButton,gtk.STOCK_CLOSE)
    iconBox = gtk.HBox(False, 0)
    
    eventBox.connect('button-press-event',tab_button_press)
    eventBox.show()
    tabButton.show()
    tabLabel.show()
    
    if profile['icon']:
        iconImg = gtk.Image()
        iconImg.set_from_stock(profile['icon'],gtk.ICON_SIZE_MENU)
        tabBox.pack_start(iconImg, True, False, 0)

    tabBox.pack_start(tabLabel, False)       
    tabBox.pack_start(tabButton, False)

    tabBox.show_all()
    eventBox.add(tabBox)
    return eventBox

def tab_button_press(obj,event):
    if event.type == gtk.gdk._2BUTTON_PRESS and event.button == 1:
        term = commands.get_action_term(conf().main, obj)
        lab = conf().main.nb.get_tab_label(term)
        children = [c for c in lab.get_child().get_children()]
        label = children[0]
        ret = input_dialog(conf().main.window,_('Tab renaming'),_('Please enter new title for the tab:'),label.get_text())
        if ret:
            commands.tab_rename(conf().main, obj, ret)
        conf().main.window.set_focus(term)
    if event.type == gtk.gdk.BUTTON_PRESS and event.button == 3:
        menu = gtk.Menu()
        items = [ 
                (gtk.STOCK_CLOSE,_("_Close Tab"),  lambda x: commands.tab_close(conf().main, obj, None) ),
                (gtk.STOCK_DIALOG_AUTHENTICATION,_("_Lock Tab"), lambda x: commands.tab_lock(conf().main, obj, None)),
                (gtk.STOCK_COPY,_("_Duplicate Tab"), lambda x: commands.tab_duplicate(conf().main, obj, None) )
                ]

        for stockid,label,command in items:
            ni = gtk.ImageMenuItem(label)
            ni.connect("activate",command)
            img = gtk.Image ()
            img.set_from_stock(stockid, gtk.ICON_SIZE_MENU)
            ni.set_image(img)
            menu.add(ni)
            ni.show()
        menu.popup(None,None,None,event.button,event.time)


class ConfigCheckButton(gtk.CheckButton):
    def __init__(self, label, path):
        gtk.CheckButton.__init__(self, label)
        self.conf = gconf.client_get_default()
        self.set_active(self.conf.get_bool(path))
        self.connect('toggled', ConfigCheckButton.__toggled, path)
    
    def __toggled(self, path):
        self.conf.set_bool(path, bool(self.get_active()))

