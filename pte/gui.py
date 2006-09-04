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
import commands,settings

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

class TerminalNotebookTablLabel(gtk.EventBox):# (notebook, title, profile, close_event):
    def __init__(self, parent, profile, title, close_callback):
        self.profile = None
        self.title = None
        self.owner = parent
        gtk.EventBox.__init__(self)

        self.tabBox = gtk.HBox(False, 2)
        self.tabLabel = gtk.Label()
        #self.tabLabel = gtk.Entry()
        #self.tabLabel.set_editable(False)
        #self.tabLabel.set_has_frame(False)
        #self.tabLabel.set_sensitive(False)
        #self.tabLabel.modify_base(gtk.STATE_INSENSITIVE, self.get_style().bg[gtk.STATE_PRELIGHT])
        #self.tabLabel.modify_text(gtk.STATE_INSENSITIVE, self.get_style().fg[gtk.STATE_PRELIGHT])

        self.tabButton=gtk.Button()
        self.tabButton.connect('clicked',close_callback, parent)

        self.add_icon_to_button(self.tabButton,gtk.STOCK_CLOSE)
        
        self.connect('button-press-event',self.tab_button_press)
        
        self.iconImg = gtk.Image()
        if profile['icon']:
            self.tabBox.pack_start(self.iconImg, True, False, 0)

        self.tabBox.pack_start(self.tabLabel, False)       
        self.tabBox.pack_start(self.tabButton, False)

        self.add(self.tabBox)
        
        self.set_profile(profile)
        self.set_title(title)

        self.show_all()

    def add_icon_to_button(self, button, icon):
        iconBox = gtk.HBox(False, 0)
        image = gtk.Image()
        image.set_from_stock(icon,gtk.ICON_SIZE_MENU)
        gtk.Button.set_relief(button,gtk.RELIEF_NONE)
        settings = gtk.Widget.get_settings (button);
        (w,h) = gtk.icon_size_lookup_for_settings(settings,gtk.ICON_SIZE_MENU);
        gtk.Widget.set_size_request (button, w + 4, h + 4);
        image.show()
        iconBox.pack_start(image, True, False, 0)
        button.add(iconBox)


    def set_title(self, title):
        if not title: 
            title = self.profile['title']
        if title != self.title:
            self.title = title
            self.tabLabel.set_text(self.title)
            self.owner.label_updated(self)

    def set_profile(self, profile):
        if profile != self.profile:
            self.profile = profile
            if profile['icon']:
                pixbuf = gtk.gdk.pixbuf_new_from_file(self.profile['icon'])
                settings = gtk.Widget.get_settings (self.tabButton);
                (w,h) = gtk.icon_size_lookup_for_settings(settings,gtk.ICON_SIZE_MENU);

                scaled_buf = pixbuf.scale_simple(w,h,gtk.gdk.INTERP_BILINEAR)
                self.iconImg.set_from_pixbuf(scaled_buf)
           
    def tab_button_press(self,obj,event):
        if event.type == gtk.gdk._2BUTTON_PRESS and event.button == 1:
            ret = input_dialog(conf().main.window,_('Tab renaming'),_('Please enter new title for the tab:'),self.title)
            if ret:
                self.set_title(ret)
            conf().main.window.set_focus(self.owner.term_by_label(self))
        if event.type == gtk.gdk.BUTTON_PRESS and event.button == 3:
            menu = gtk.Menu()
            items = [ 
                    (gtk.STOCK_CLOSE,_("_Close Tab"),  lambda x: commands.tab_close(conf().main, self, None) ),
                    (gtk.STOCK_DIALOG_AUTHENTICATION,_("_Lock Tab"), lambda x: commands.tab_lock(conf().main, self, None)),
                    (gtk.STOCK_COPY,_("_Duplicate Tab"), lambda x: commands.tab_duplicate(conf().main, self, None) )
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


class TerminalNotebook(gtk.Notebook):
    def __init__(self, parent ):
        self.owner = parent
        self.terminals = []
        gtk.Notebook.__init__(self)

    def create_tabs(self, terms=None  ):
        if not terms:
            terms = [ dict ( title=None, profile=conf().get_default_profile()  )]
        for t in terms:
            self.add_terminal(t['profile'],t['title'],t)
 

    def label_updated(self, label):
        """ This event is fired when label's text was changed """
        for t in self.terminals:
            if t['label'] == label:
                t['session']['title'] = label.title
                break

    def refresh_profiles(self):
        """ This event is fired after the settings dialog is closed """
        np = conf().profiles
        for t in self.terminals:
            t['label'].set_profile(  np[ t['profile']['name'] ] )


    def add_terminal(self, profile=conf().get_default_profile(), custom_title=None, session=None):
        if not session:
            session = dict (title=None, profile=conf().get_default_profile())
        label = TerminalNotebookTablLabel(self, profile, custom_title, self.remove_tab_by_sender)
        term = vte.Terminal()
        term.set_font(profile['font'])
        term.fork_command(profile['cmd'],None,None,profile['cwd'],True,True,True)
        term.connect("child-exited",self.child_exited)
        term.connect("window-title-changed",self.title_changed)
        page_n = self.append_page(term, label)

        new_term = dict(page=self.get_nth_page(page_n),page_n=page_n,term=term,profile=profile,label=label,session=session)
        self.terminals += [ new_term ]
        self.show_all()
        return new_term

    def remove_tab_by_n(self, page_n):
        if self.get_n_pages() == 1:
            self.owner.window.destroy()
            self.owner.exit()

        self.remove_page(page_n)
        self.queue_draw_area(0,0,-1,-1)
 
    def child_exited(self, control):
        self.remove_tab_by_sender(control)

    def title_changed(self, term):
        if term == self.get_nth_page(self.get_current_page()):
            self.window.set_title(term.get_window_title())

    def term_by_label(self, label):
        for t in self.terminals:
            if t['label'] == label:
                return t['term']

    def remove_tab_by_sender(self, button, *args):
        page = self.page_num(button)
        self.remove_tab_by_n(page)



class ConfigCheckButton(gtk.CheckButton):
    def __init__(self, label, path):
        gtk.CheckButton.__init__(self, label)
        self.conf = gconf.client_get_default()
        self.set_active(self.conf.get_bool(path))
        self.connect('toggled', ConfigCheckButton.__toggled, path)
    
    def __toggled(self, path):
        self.conf.set_bool(path, bool(self.get_active()))

