from PyPDF2 import PdfMerger
from tkinter import filedialog, messagebox
from tkinter import *
from tkinter import ttk
import webbrowser

FILES = []


def open_files():
    try:
        files = filedialog.askopenfilenames(initialdir="",
                                            title="Choose PDF Files",
                                            filetypes=[("PDF Files", "*.pdf")])

        if files:
            for file in files:
                FILES.append(file)

            update_treeview()

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while opening files: {str(e)}")


def remove_file():
    try:
        selected_items = treeview.selection()
        for item in selected_items:
            index = int(item.split(' ')[0]) - 1  # Extract index from the item ID
            del FILES[index]

        update_treeview()

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while removing file: {str(e)}")


def move_up():
    try:
        selected_items = treeview.selection()
        selected_indices = [int(item.split(' ')[0]) - 1 for item in selected_items]

        for index in selected_indices:
            if 0 < index < len(FILES):
                FILES[index], FILES[index - 1] = FILES[index - 1], FILES[index]

        update_treeview()
        reselect_items(selected_indices, move_up=True)

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while moving files up: {str(e)}")


def move_down():
    try:
        selected_items = reversed(treeview.selection())
        selected_indices = [int(item.split(' ')[0]) - 1 for item in selected_items]

        for index in selected_indices:
            if 0 <= index < len(FILES) - 1:
                FILES[index], FILES[index + 1] = FILES[index + 1], FILES[index]

        update_treeview()
        reselect_items(selected_indices, move_up=False)

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while moving files down: {str(e)}")


def clear_all():
    try:
        global FILES
        FILES = []
        update_treeview()

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while clearing files: {str(e)}")


def merge_files():
    try:
        if FILES:
            merger = PdfMerger()
            for pdf in FILES:
                merger.append(pdf, import_outline=False)

            location = filedialog.asksaveasfile(initialdir="",
                                                title="Merge Files",
                                                filetypes=[("PDF", "*.pdf")],
                                                defaultextension=".pdf")

            if location:
                merger.write(location.name)
                merger.close()
                webbrowser.open(location.name)

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while merging files: {str(e)}")


def update_treeview():
    try:
        treeview.delete(*treeview.get_children())

        for i, file in enumerate(FILES, start=1):
            iid = f"{i} {file}"
            treeview.insert("", "end", iid=iid, values=(file.split('/')[-1],))

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while updating the treeview: {str(e)}")


def reselect_items(selected_indices, move_up=True):
    try:
        for index in selected_indices:
            new_index = index - 1 if move_up else index + 1

            if 0 <= new_index < len(FILES):
                new_item = f"{new_index + 1} {FILES[new_index]}"
                treeview.selection_add(new_item)

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while reselecting items: {str(e)}")


if __name__ == '__main__':
    root = Tk()
    root.title("PDF Merger")
    root.resizable(width=False, height=False)

    clear = Button(root, text="Clear All", command=clear_all)
    open_button = Button(root, text="Open Files", command=open_files)
    remove_button = Button(root, text="Delete Selected", command=remove_file)
    merge_button = Button(root, text="Merge Files", command=merge_files)
    move_up_button = Button(root, text="Move Up", command=move_up)
    move_down_button = Button(root, text="Move Down", command=move_down)

    clear.grid(row=0, column=0, padx=10, pady=10, sticky=W + E + N + S)
    open_button.grid(row=0, column=1, padx=10, pady=10, sticky=W + E + N + S)
    remove_button.grid(row=0, column=2, padx=10, pady=10, sticky=W + E + N + S)
    merge_button.grid(row=0, column=3, padx=10, pady=10, sticky=W + E + N + S)
    move_up_button.grid(row=2, column=1, padx=10, pady=10, sticky=W + E + N + S)
    move_down_button.grid(row=2, column=2, padx=10, pady=10, sticky=W + E + N + S)

    treeview = ttk.Treeview(root, columns=("Files",), show="headings")
    treeview.heading("Files", text="Files")
    treeview.grid(row=1, column=0, columnspan=4, padx=10, pady=10, sticky=W + E + N + S)

    root.eval('tk::PlaceWindow . center')

    root.mainloop()
