# GTK/Gnome imports
import pygtk
pygtk.require('2.0')
import gtk,pango,vte,gconf

# Python imports
import os, sys

# Local imports
import settings as conf
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
    if event.type == gtk.gdk.BUTTON_PRESS and event.button == 3:
        menu = gtk.Menu()
        items = [ 
                (gtk.STOCK_CLOSE,"_Close Tab",  lambda x: commands.tab_close(conf.get_main(), obj, None) ),
                (gtk.STOCK_DIALOG_AUTHENTICATION,"_Lock Tab", lambda x: commands.tab_lock(conf.get_main(), obj, None)),
                (gtk.STOCK_COPY,"_Duplicate Tab", lambda x: commands.tab_duplicate(conf.get_main(), obj, None) )
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


class ConfirmDialog(gtk.MessageDialog):
    def __init__(self, parent, text, path):
        gtk.MessageDialog.__init__(self, parent, gtk.DIALOG_MODAL, gtk.MESSAGE_QUESTION,message_format=text) 
        self.set_border_width(6)
        self.set_resizable(False)
        self.add_buttons(
                         gtk.STOCK_YES, gtk.RESPONSE_YES,
                         gtk.STOCK_NO, gtk.RESPONSE_NO,
                         gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL
                        )
        box = gtk.VBox(spacing=6)
        box.set_border_width(6)

        self.vbox.set_spacing(6)
        self.set_default_response(gtk.RESPONSE_YES)
        c = ConfigCheckButton("Don't ask this again", path)
        self.vbox.add(c)
        self.child.show_all()


class ConfigCheckButton(gtk.CheckButton):
    def __init__(self, label, path):
        gtk.CheckButton.__init__(self, label)
        self.conf = gconf.client_get_default()
        self.set_active(self.conf.get_bool(path))
        self.connect('toggled', ConfigCheckButton.__toggled, path)
    
    def __toggled(self, path):
        self.conf.set_bool(path, bool(self.get_active()))

