#!/usr/bin/env python

# example helloworld.py

import pygtk
pygtk.require('2.0')
import gtk,pango,vte
import os

class PTE:
    def add_icon_to_button(self,button):
        iconBox = gtk.HBox(False, 0)        
        image = gtk.Image()
        image.set_from_stock(gtk.STOCK_CLOSE,gtk.ICON_SIZE_MENU)
        gtk.Button.set_relief(button,gtk.RELIEF_NONE)
        #gtk.Button.set_focus_on_click(button,False)
        settings = gtk.Widget.get_settings (button);
        (w,h) = gtk.icon_size_lookup_for_settings(settings,gtk.ICON_SIZE_MENU);
        gtk.Widget.set_size_request (button, w + 4, h + 4);
        image.show()
        iconBox.pack_start(image, True, False, 0)
        button.add(iconBox)
        iconBox.show()

    def remove_book(self, button, notebook):
        if notebook.get_n_pages() == 1:
            print "closing last page?"
            self.destroy(button)
        page = notebook.page_num(button)
        notebook.remove_page(page)
        notebook.queue_draw_area(0,0,-1,-1)
        
    def create_custom_tab(self, text, notebook):
        eventBox = gtk.EventBox()
        tabBox = gtk.HBox(False, 2)
        tabLabel = gtk.Label(text)

        tabButton=gtk.Button()
        tabButton.connect('clicked',self.remove_book, notebook)

        #Add a picture on a button
        self.add_icon_to_button(tabButton)
        iconBox = gtk.HBox(False, 0)
        
        eventBox.show()
        tabButton.show()
        tabLabel.show()

        tabBox.pack_start(tabLabel, False)       
        tabBox.pack_start(tabButton, False)

        tabBox.show_all()
        eventBox.add(tabBox)
        return eventBox

    def delete_event(self, widget, event, data=None):
        print "delete event occurred"
        # Change FALSE to TRUE and the main window will not be destroyed
        # with a "delete_event".
        return False

    def destroy(self, widget, data=None):
        print "destroy signal occurred"
        gtk.main_quit()

    def child_exited(self, control):
        self.remove_book(control,self.nb)

    def create_tabs(self, parent):
        eventBox = self.create_custom_tab("Term",parent)
        term = vte.Terminal()
        term.set_font(pango.FontDescription("monospace"))
        term.fork_command(os.environ['SHELL'],['-i','-l'],None,os.environ['HOME'],True,True,True)
        term.connect("child-exited",self.child_exited)
        term.show()
        self.terms += [ term ]
        parent.append_page(term, eventBox)
                                 
    def key_press(self, sender, event):
        if event.keyval == gtk.keysyms.F12:
            return True
        return False

    def __init__(self):
        self.terms = []
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.connect("delete_event", self.delete_event)
        self.window.connect("destroy", self.destroy)
        self.window.connect("key-press-event", self.key_press)
        self.window.set_border_width(4)
        self.nb = gtk.Notebook()
        self.create_tabs(self.nb)
        self.window.add(self.nb)
        self.nb.show()
        self.window.set_focus(self.terms[0])
        self.window.show()

    def main(self):
        gtk.main()

if __name__ == "__main__":
    pte = PTE()
    pte.main()


