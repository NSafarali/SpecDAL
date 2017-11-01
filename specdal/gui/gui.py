import os
import sys
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
sys.path.insert(0, os.path.abspath("../.."))
import matplotlib
matplotlib.use('TkAgg')
from specdal.spectrum import Spectrum
from specdal.collection import Collection
from viewer import Viewer
from collections import OrderedDict

# ~/data/specdal/aidan_data2/PSR/

class SpecdalGui(tk.Tk):
    """GUI entry point for Specdal"""
    def __init__(self, collections=None):
        tk.Tk.__init__(self)

        # create menubar
        self.config(menu=Menubar(self))
        
        # create list
        self.collectionList = CollectionList(self, collections)
        self.collectionList.pack(side=tk.LEFT, fill=tk.Y)
        
        # create viewer
        self.viewer = Viewer(self, self.collectionList.currentCollection,
                             with_toolbar=False)
        self.viewer.pack(side=tk.LEFT, fill=tk.BOTH)
        
    def read_dir(self):
        directory = filedialog.askdirectory()
        if not directory:
            return
        self.collectionList.add_collection(
            Collection(name="collection" + str(self.collectionList.listbox.size()), directory=directory))

    def group_by(self, collection=None):
        if collection is None:
            collection = self.collectionList.currentCollection
        groups = collection.groupby(separator='_', indices=[0, 1], filler=None)
        for gname, gcoll in groups.items():
            gcoll.name = collection.name + " (" + gcoll.name + ")"
            self.collectionList.add_collection(gcoll)
    
class CollectionList(tk.Frame):
    """Stores and manages collections"""
    def __init__(self, parent, collections=None):
        tk.Frame.__init__(self, parent)
        self.collections = OrderedDict()
        self.currentCollection = None
        
        # gui
        self.scrollbar = ttk.Scrollbar(self)
        self.listbox = tk.Listbox(self, yscrollcommand=self.scrollbar.set,
                                  width=30)
        self.scrollbar.config(command=self.listbox.yview)
        self.listbox.pack(side=tk.LEFT, fill=tk.Y)
        self.scrollbar.pack(side=tk.LEFT, fill=tk.Y)
        self.listbox.bind('<Double-1>', lambda x:
                          self.master.viewer.set_collection(
                              self.set_cur(pos=self.get_selection()[0][0])))
        
        # load provided collections
        if collections:
            for c in collections:
                self.add_collection(c)
            self.set_cur()

    def set_cur(self, name=None, pos=0):
        if name is None:
            # TODO: check whether pos is valid
            name = self.listbox.get(pos) 
        self.currentCollection = self.get_collection(name)
        return self.currentCollection
            
    def add_collection(self, collection):
        assert isinstance(collection, Collection)
        self.collections[collection.name] = collection
        # add to listbox
        self.listbox.insert(tk.END, collection.name)

    def get_collection(self, name):
        if name in self.collections:
            return self.collections[name]

    def get_selection(self):
        ''' return indices (tuple) and names (list) '''
        idx = self.listbox.curselection()
        all_names = list(self.collections)
        names = [ all_names[i] for i in idx ]
        return idx, names
    
    def remove_selection(self):
        idx, names = self.get_selection()
        # remove from listbox
        for i in sorted(idx, reverse=True):
            self.listbox.delete(i)
        # remove from dict
        for name in names:
            if self.currentCollection.name == name:
                self.set_cur()
            self.collections.__delitem__(name)

class Menubar(tk.Menu):
    # parent is the SpecdalGui class
    def __init__(self, parent):
        tk.Menu.__init__(self, parent)
        # File
        fileMenu = tk.Menu(self, tearoff=0)
        fileMenu.add_command(label="open", command=lambda: print('Not Implemented'))
        fileMenu.add_command(label="read file", command=lambda: print('Not Implemented'))
        fileMenu.add_command(label="read directory", command=lambda: self.master.read_dir())
        fileMenu.add_command(label="read csv", command=lambda: print('Not Implemented'))
        fileMenu.add_command(label="save", command=lambda: print('Not Implemented'))
        fileMenu.add_command(label="save as", command=lambda: print('Not Implemented'))
        fileMenu.add_command(label="close", command=lambda: print('Not Implemented'))
        self.add_cascade(label="File", menu=fileMenu)
        
        # Edit
        editMenu = tk.Menu(self, tearoff=0)
        editMenu.add_command(label="mask/unmask", command=lambda: self.master.viewer.toggle_mask())
        editMenu.add_command(label="remove collection", command=lambda: self.master.collectionList.remove_selection())

        editMenu.add_command(label="setting", command=lambda: print('Not Implemented'))
        self.add_cascade(label="Edit", menu=editMenu)

        # View
        viewMenu = tk.Menu(self, tearoff=0)
        viewMenu.add_command(label="Collection/Spectra Mode", command=lambda: self.master.viewer.toggle_mode())
        viewMenu.add_command(label="Show/Hide Masked", command=lambda: self.master.viewer.toggle_show_masked())
        viewMenu.add_command(label="Mean", command=lambda: self.master.viewer.toggle_mean())
        viewMenu.add_command(label="Median", command=lambda: self.master.viewer.toggle_median())
        viewMenu.add_command(label="Min", command=lambda: print('Not Implemented'))
        viewMenu.add_command(label="Max", command=lambda: print('Not Implemented'))
        viewMenu.add_command(label="Std", command=lambda: self.master.viewer.toggle_std())
        self.add_cascade(label="View", menu=viewMenu)

        # Operators
        operatorMenu = tk.Menu(self, tearoff=0)
        operatorMenu.add_command(label="Groupby", command=lambda: self.master.group_by())
        operatorMenu.add_command(label="Stitch", command=lambda: self.master.viewer.stitch())
        operatorMenu.add_command(label="Jump Correct", command=lambda: self.master.viewer.jump_correct())
        self.add_cascade(label="Operator", menu=operatorMenu)


    
def read_test_data():
    path = '~/data/specdal/aidan_data2/ASD'
    c = Collection("Test Collection", directory=path)
    for i in range(30):
        c.mask(c.spectra[i].name)
    return c

def main():
    # root = tk.Tk()
    gui = SpecdalGui([read_test_data()])
    gui.mainloop()
    

if __name__ == "__main__":
    main()