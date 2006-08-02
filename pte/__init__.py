# GTK/Gnome imports
import pygtk
pygtk.require('2.0')
import gtk,pango,vte

# Python imports
import os, sys

# Local imports
import settings as conf
import gui

# Main Class
class PTE:

    def remove_book_by_n(self, page):
        self.nb.remove_page(page)
        self.nb.queue_draw_area(0,0,-1,-1)
 
    def remove_book(self, button):
        if self.nb.get_n_pages() == 1:
            self.window.destroy()
            self.exit()

        page = self.nb.page_num(button)
        self.remove_book_by_n(page)

    def exit(self):
        conf.save_tabs(self.terms)
        print "Thank you for using PyTerm by Reflog"
 
    def delete_event(self, widget, event, data=None):
        return False

    def child_exited(self, control):
        self.remove_book(control)

    def new_tab(self, profile=conf.get_default_profile(), title=None):
        eventBox = gui.create_custom_tab(self.nb, title, profile, self.remove_book)
        term = vte.Terminal()
        term.set_font(profile['font'])
        term.fork_command(profile['cmd'],None,None,profile['cwd'],True,True,True)
        term.connect("child-exited",self.child_exited)
        term.show()
        self.nb.append_page(term, eventBox)
        #s.set_tab_reorderable(self.nb.get_nth_page(self.nb.page_num(term)), True) # TODO: make storeable
        return term
 
    def create_tabs(self):
        for t in self.terms:
            t['widget'] = self.new_tab(t['profile'], t['title'])

    def key_press(self, sender, event):
        if commands.handle_key_press(self,sender,event):
            return True
        return False

    def __init__(self):
        self.terms = conf.get_saved_tabs()
        if not self.terms: 
            self.terms += [ dict ( title=None, profile=conf.get_default_profile(), widget=None )  ]
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.connect("delete_event", self.delete_event)
        self.window.connect("destroy", lambda w:  gtk.main_quit())
        self.window.connect("key-press-event", self.key_press)
        self.nb = gtk.Notebook()
        self.create_tabs()
        self.window.add(self.nb)
        self.nb.show()
        self.window.set_focus(self.terms[0]['widget'])
        self.nb.set_scrollable(True) # TODO: make settings
        self.window.show()

    def main(self):
        gtk.main()

__all__ = [ PTE ]


