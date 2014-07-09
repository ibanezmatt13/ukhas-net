import urllib2
from json import load
from Tkinter import *

# function called when new listbox item selected
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
window.configure(bg='lightgrey')
window.title("UKHASnet Node Manager")
window.geometry("700x500")

frame = Frame(window)
frame.place(x=20, y=40)

lbl1 = Label(window, text="Node List:", fg='black', bg='lightgrey', font=("Helvetica", 16, "bold"))
lbl2 = Label(window, text="Node Information:", fg='black', bg='lightgrey', font=("Helvetica", 16,"bold"))
lbl1.place(x=20, y=4)
lbl2.place(x=230, y=4)

listNodes = Listbox(frame, width=20, height=20, font=("Helvetica", 12))
listNodes.pack(side="left", fill="y")

scrollbar = Scrollbar(frame, orient="vertical")
scrollbar.config(command=listNodes.yview)
scrollbar.pack(side="right", fill="y")

listNodes.config(yscrollcommand=scrollbar.set)

listSelection = Listbox(window, width=50, height=4, font=("Helvetica", 12))
listSelection.place(x=230, y=40)

response = urllib2.urlopen(mapNodes)
data = load(response)

# function that returns array of parsed information for certain node
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
            
# populate listbox
for current_id in range(0, len(data)):
    listNodes.insert(END, data[current_id]["name"])

listNodes.bind('<<ListboxSelect>>', onselect)


mainloop()




