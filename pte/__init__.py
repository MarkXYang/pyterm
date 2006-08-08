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
import gui
from settings import conf

# Main Class
class PTE:
    def remove_book_by_n(self, page):
        if self.nb.get_n_pages() == 1:
            self.window.destroy()
            self.exit()

        self.nb.remove_page(page)
        self.nb.queue_draw_area(0,0,-1,-1)
 
    def remove_book(self, button, *args):
        page = self.nb.page_num(button)
        self.remove_book_by_n(page)

    def exit(self):
        conf().sessions=self.terms
        print _("Thank you for using PyTerm by Reflog")
 
    def delete_event(self, widget, event, data=None):
        self.exit()
        return False

    def child_exited(self, control):
        self.remove_book(control)

    def title_changed(self, term):
        if term == self.nb.get_nth_page(self.nb.get_current_page()):
            self.window.set_title(term.get_window_title())

    def new_tab(self, profile=settings.default_profile, title=None):
        eventBox = gui.create_custom_tab(self.nb, title, profile, self.remove_book)
        term = vte.Terminal()
        term.set_font(profile['font'])
        term.fork_command(profile['cmd'],None,None,profile['cwd'],True,True,True)
        term.connect("child-exited",self.child_exited)
        term.connect("window-title-changed",self.title_changed)
        self.nb.append_page(term, eventBox)
        self.nb.show_all()
        #s.set_tab_reorderable(self.nb.get_nth_page(self.nb.page_num(term)), True) # TODO: make storeable
        return (term,profile)
 
    def create_tabs(self):
        for t in self.terms:
            (t['widget'],z) = self.new_tab(t['profile'], t['title'])

    def key_press(self, sender, event):
        if commands.handle_key_press(self,sender,event):
            return True
        return False

    def __init__(self, share_path):
        self.settings_dlg=gtk.glade.XML(share_path+"/glade/settings.glade").get_widget("dlgSettings")
        self.terms = conf().sessions
        self.profiles = conf().profiles
        self.conf = conf()
        if not self.terms: 
            self.terms += [ dict ( title=None, profile=settings.default_profile, widget=None )  ]
 
     
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.connect("delete_event", self.delete_event)
        self.window.connect("destroy", lambda w:  gtk.main_quit())
        self.window.connect("key-press-event", self.key_press)
        self.nb = gtk.Notebook()
        self.window.add(self.nb)
        self.nb.set_scrollable(True) # TODO: make settings
        self.create_tabs()
        
        self.window.show_all()
        self.window.set_focus(self.terms[0]['widget'])
        conf().main = self

    def main(self):
        try:
            gtk.main()
        except KeyboardInterrupt,e:
            pass

__all__ = [ PTE ]


