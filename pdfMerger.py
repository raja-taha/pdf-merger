from PyPDF2 import PdfMerger
from tkinter import filedialog
from tkinter import *
from tkinter import ttk
import webbrowser

FILES = []


def open_files():
    files = filedialog.askopenfilenames(initialdir="",
                                        title="Choose PDF Files",
                                        filetypes=[("PDF Files", "*.pdf")])
    for file in files:
        FILES.append(file)

    update_treeview()


def remove_file():
    selected_items = treeview.selection()
    for item in selected_items:
        index = int(item.split(' ')[0]) - 1  # Extract index from the item ID
        del FILES[index]

    update_treeview()


def move_up():
    selected_items = treeview.selection()
    selected_indices = [int(item.split(' ')[0]) - 1 for item in selected_items]

    for index in selected_indices:
        if 0 < index < len(FILES):
            FILES[index], FILES[index - 1] = FILES[index - 1], FILES[index]

    update_treeview()
    reselect_items(selected_indices, move_up=True)


def move_down():
    selected_items = reversed(treeview.selection())
    selected_indices = [int(item.split(' ')[0]) - 1 for item in selected_items]

    for index in selected_indices:
        if 0 <= index < len(FILES) - 1:
            FILES[index], FILES[index + 1] = FILES[index + 1], FILES[index]

    update_treeview()
    reselect_items(selected_indices, move_up=False)


def clear_all():
    global FILES
    FILES = []
    update_treeview()


def merge_files():
    if FILES != []:
        merger = PdfMerger()
        for pdf in FILES:
            merger.append(pdf, import_outline=False)
        location = filedialog.asksaveasfile(initialdir="",
                                            title="Merge Files",
                                            filetypes=[("PDF", "*.pdf")],
                                            defaultextension=".pdf")
        if location is not None:
            merger.write(location.name)
            merger.close()

            webbrowser.open(location.name)


def update_treeview():
    treeview.delete(*treeview.get_children())

    for i, file in enumerate(FILES, start=1):
        iid = f"{i} {file}"
        treeview.insert("", "end", iid=iid, values=(file.split('/')[-1],))


def reselect_items(selected_indices, move_up=True):
    for index in selected_indices:
        new_index = index - 1 if move_up else index + 1

        # Check if the new index is within the bounds of the updated FILES list
        if 0 <= new_index < len(FILES):
            new_item = f"{new_index + 1} {FILES[new_index]}"
            treeview.selection_add(new_item)


if __name__ == '__main__':
    root = Tk()
    root.title("PDF Merger")
    root.resizable(width=False, height=False)

    # Create entry + buttons
    clear = Button(root, text="Clear All", command=clear_all)
    open_button = Button(root, text="Open Files", command=open_files)
    remove_button = Button(root, text="Delete Selected", command=remove_file)
    merge_button = Button(root, text="Merge Files", command=merge_files)
    move_up_button = Button(root, text="Move Up", command=move_up)
    move_down_button = Button(root, text="Move Down", command=move_down)

    # Position entry + buttons
    clear.grid(row=0, column=0, padx=10, pady=10, sticky=W + E + N + S)
    open_button.grid(row=0, column=1, padx=10, pady=10, sticky=W + E + N + S)
    remove_button.grid(row=0, column=2, padx=10, pady=10, sticky=W + E + N + S)
    merge_button.grid(row=0, column=3, padx=10, pady=10, sticky=W + E + N + S)
    move_up_button.grid(row=2, column=1, padx=10, pady=10, sticky=W + E + N + S)
    move_down_button.grid(row=2, column=2, padx=10, pady=10, sticky=W + E + N + S)

    # Create Treeview for displaying selected files
    treeview = ttk.Treeview(root, columns=("Files",), show="headings")
    treeview.heading("Files", text="Files")
    treeview.grid(row=1, column=0, columnspan=4, padx=10, pady=10, sticky=W + E + N + S)

    # Center window
    root.eval('tk::PlaceWindow . center')

    root.mainloop()
