"""
Various tiny functions that didn't fit anywhere else.
"""

import os
import re
import StringIO
import unicodedata

import glib
import gtk

SPLIT_KEYWORDS_REGEX = re.compile("[^\w/*!-]", re.UNICODE)
UI_FILES_DIRS = [
    ".",
    "src",
    "/usr/local/share/paperwork",
    "/usr/share/paperwork",
]


def load_uifile(filename):
    """
    Load a .glade file and return the corresponding widget tree

    Arguments:
        filename -- glade filename to load. Must not contain any directory
            name, just the filename. This function will (try to) figure out
            where it must be found.

    Returns:
        GTK Widget tree

    Throws:
        Exception -- If the file cannot be found
    """
    widget_tree = gtk.Builder()
    has_ui_file = False
    for ui_dir in UI_FILES_DIRS:
        ui_file = os.path.join(ui_dir, filename)
        try:
            widget_tree.add_from_file(ui_file)
        except glib.GError, exc:
            print "Try to used UI file %s but failed: %s" % (ui_file, str(exc))
            continue
        has_ui_file = True
        print "UI file used: " + ui_file
        break
    if not has_ui_file:
        raise Exception("Can't find ressource file. Aborting")
    return widget_tree


def strip_accents(string):
    """
    Strip all the accents from the string
    """
    return ''.join(
        (character for character in unicodedata.normalize('NFD', string)
         if unicodedata.category(character) != 'Mn'))


def gtk_refresh():
    """
    Force a refresh of all GTK windows.

    Warning: will also tell GTK to handle all events.
    """
    while gtk.events_pending():
        gtk.main_iteration()


def image2pixbuf(img):
    """
    Convert an image object to a gdk pixbuf
    """
    file_desc = StringIO.StringIO()
    try:
        img.save(file_desc, "ppm")
        contents = file_desc.getvalue()
    finally:
        file_desc.close()
    loader = gtk.gdk.PixbufLoader("pnm")
    try:
        loader.write(contents, len(contents))
        pixbuf = loader.get_pixbuf()
    finally:
        loader.close()
    return pixbuf


def dummy_progress_cb(progression, total, step=None, doc=None):
    """
    Dummy progression callback. Do nothing.
    """
    pass
