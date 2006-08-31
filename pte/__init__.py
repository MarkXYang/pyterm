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
import gtk,pango,vte
import gtk.glade

# Python imports
import os, sys

# Local imports
import gui,settings
from settings import conf
from settings_window import SettingsWindow

# Main Class
class PTE:
    def exit(self):
        conf().sessions=[s['session'] for s in self.nb.terminals]
        print _("Thank you for using PyTerm by Reflog")
 
    def delete_event(self, widget, event, data=None):
        self.exit()
        return False

    def key_press(self, sender, event):
        print 'key press'
        if commands.handle_key_press(self,sender,event):
            return True
        return False

    def __init__(self, share_path):
        #FIXME: self.settings_dlg=gtk.glade.XML(share_path+"/glade/settings.glade").get_widget("dlgSettings")
        self.settings_dlg=SettingsWindow()
        self.profiles = conf().profiles
        self.conf = conf()

     
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.connect("delete_event", self.delete_event)
        self.window.connect("destroy", lambda w:  gtk.main_quit())
        self.window.connect("key-press-event", self.key_press)
        self.nb = gui.TerminalNotebook(self)
        self.window.add(self.nb)
        self.nb.create_tabs(conf().sessions)
        self.nb.set_scrollable(True) # TODO: make settings
        
        self.window.show_all()
        self.window.set_focus(self.nb.terminals[0]['term'])
        conf().main = self
        self.update_ui()

    def update_ui(self):
        """ Should be called on every configuration change """
        self.nb.set_tab_pos(settings.tab_pos_map[self.conf.tab_position])
        

    def main(self):
        try:
            gtk.main()
        except KeyboardInterrupt,e:
            pass

__all__ = [ PTE ]


