import urllib2
from json import load
from Tkinter import *

def onselect(event):
    w = event.widget
    index = int(w.curselection()[0])
    value = w.get(index)
    info = find_info(value)
    listSelection.delete(0, END)
    listSelection.insert(END, "Node ID: " + info[0])
    listSelection.insert(END, "Owner/Description: " + info[1])
    listSelection.insert(END, "Last Latitude: " + info[2])
    listSelection.insert(END, "Last Longitude: " + info[3])
    


mapNodes = "http://ukhas.net/api/mapNodes"
nodeData = "http://ukhas.net/api/nodeData"
current_id = 0

window = Tk() # create window
window.title("UKHASnet Node Manager")

scrollbar = Scrollbar(window, orient="vertical")
listNodes = Listbox(window, width=20, height=20, yscrollcommand=scrollbar.set)
scrollbar.config(command=listNodes.yview)
scrollbar.pack(side="right", fill="y")

listSelection = Listbox(window, width=40, height=20)

# pack objects onto window
listNodes.pack(side="left", fill="both", expand=True)
listSelection.pack(side="left", fill="both", expand=True)

response = urllib2.urlopen(mapNodes)
data = load(response)
print data[0]

def find_info(name):
    index = 0
    for index in range(0, len(data)):
        if data[index]["name"] == name:
            node_id = str(data[index]["id"])
            owner = str(data[index]["owner"])
            lon = str(data[index]["lon"])
            lat = str(data[index]["lat"])
            break
    info = []
    info.append(node_id)
    info.append(owner)
    info.append(lat)
    info.append(lon)
    return info
    
            

for current_id in range(0, len(data)):
    listNodes.insert(END, data[current_id]["name"])

listNodes.bind('<<ListboxSelect>>', onselect)

    
mainloop()



