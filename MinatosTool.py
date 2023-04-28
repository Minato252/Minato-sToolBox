import tkinter as tk
import uuid
import customtkinter


class MinatosTool:
    def __init__(self):
        self.count = 0

        customtkinter.set_appearance_mode("dark")
        customtkinter.set_default_color_theme("green")
        self.root = customtkinter.CTk()
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        self.root.geometry("300x350")
        self.root.title("Minato‘sTool")
        # 绑定窗口拖动事件
        self.root.bind("<ButtonPress-1>", self.start_drag)
        self.root.bind("<B1-Motion>", self.drag)
        self.root.bind("<ButtonRelease-1>", self.stop_drag)

        self.previous_clipboard = None
        self.listen_clipboard = False
        self.fields = {}
        self.field_text_set = set()
        # Create a button to toggle the window on top
        self.window_button_frame = customtkinter.CTkFrame(self.root)
        self.topmost_button = customtkinter.CTkButton(self.window_button_frame, text="stick",
                                                      command=self.toggle_topmost, width=2,height=2, corner_radius=100,
                                                      fg_color=('green', '#2FA572'))
        # self.topmost_button.pack(anchor='center',padx=10)
        self.topmost_button.pack(side='left',padx=10)
        self.slider = customtkinter.CTkSlider(self.window_button_frame, from_=0, to=1, command=self.slider_event)
        self.slider.set(1)
        self.slider.pack(side='right',padx=10,)

        self.window_button_frame.grid(row=0,column=0,sticky="new",pady=(10,0),padx=10)

        self.tabview = customtkinter.CTkTabview(master=self.root)
        self.tabview.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        self.tabview.add("counter")  # add tab at the end
        self.tabview.add("notebook")  # add tab at the end
        self.tabview.add("todo")
        self.tabview.set("counter")  # set currently visible tab

        self.tab1 = self.tabview.tab("counter")
        self.tab2 = self.tabview.tab("notebook")
        self.tab3 = self.tabview.tab("todo")
        self.tab2.grid_columnconfigure(0, weight=1)
        self.tab2.grid_rowconfigure(1, weight=1)
        TodoList(master=self.tab3)
        # self.tab3.grid_columnconfigure(0, weight=1)
        # self.tab3.grid_rowconfigure(0, weight=1)
        # self.tab3frame.grid(row=0,column=0,sticky="nesw")


        # self.topmost_button.pack(anchor='nw', padx=5, pady=5)

        self.counter_label = customtkinter.CTkLabel(self.tab1, text=str(self.count), font=("Arial", 24))
        self.counter_label.pack(pady=10)

        self.counter_button = customtkinter.CTkButton(self.tab1, text="Add", command=self.increment_counter,
                                                      )
        # self.counter_button.pack(side="left", padx=30)
        self.counter_button.pack(pady=10)

        self.decrement_button = customtkinter.CTkButton(self.tab1, text="Decrement", command=self.decrement_counter)
        self.decrement_button.pack(pady=10)
        # self.decrement_button.pack(side="right", padx=30)

        self.buttonFram = customtkinter.CTkFrame(self.tab2)

        self.buttonFram.grid(row=0,column=0,padx=10,pady=10,sticky="new")
        # Create the initial button
        self.button = customtkinter.CTkButton(self.buttonFram, text="Null", command=self.add_text,width=2)
        self.button.pack(side='left', padx=10, pady=10)

        self.add_from_clipboard_button = customtkinter.CTkButton(self.buttonFram, text="Clipboard",width=2,
                                                                 command=self.add_text_from_clipBoard)
        self.add_from_clipboard_button.pack(side='left', padx=10, pady=10)
        self.swith_button = customtkinter.CTkButton(self.buttonFram,text="OFF",command=self.toggle_clipboard,width=2,fg_color=('green', '#2FA572'))
        self.swith_button.pack(side='right', padx=10, pady=10)

        self.crollable_frame = customtkinter.CTkScrollableFrame(self.tab2)
        self.crollable_frame.grid(row=1,column=0,padx=10,pady=10, sticky="nsew")
        self.check_clipboard()

        self.root.mainloop()
    def slider_event(self,value):
        self.root.attributes("-alpha", value)
    def toggle_clipboard(self):
        self.listen_clipboard = not self.listen_clipboard
        if self.listen_clipboard:
            self.swith_button.configure(text="AUTO")
            self.swith_button.configure(fg_color=('green', 'black'))
        else:
            self.swith_button.configure(text="OFF")
            self.swith_button.configure(fg_color = ('green', '#2FA572'))

    def start_drag(self, event):
        self._drag_start_x = event.x
        self._drag_start_y = event.y

    def drag(self, event):
        x = self.root.winfo_x() + event.x - self._drag_start_x
        y = self.root.winfo_y() + event.y - self._drag_start_y
        self.root.geometry(f"+{x}+{y}")

    def stop_drag(self, event):
        pass
    def check_clipboard(self):
        if self.listen_clipboard:
            try:
                clipboard = self.root.clipboard_get()
            except tk.TclError:
                clipboard = None

            if clipboard and clipboard != self.previous_clipboard:
                self.previous_clipboard = clipboard
                self.handle_clipboard_change(clipboard)

        # schedule the next clipboard check in 100 milliseconds
        self.root.after(100, self.check_clipboard)
    def handle_clipboard_change(self, text):
        self.add_text_from_clipBoard()
    def add_text_from_clipBoard(self):
        self.add_field(True)

    def add_text(self):
        # Replace the button with a text input field

        self.add_field(False)

    def add_field(self, isFromClipBoard=False):

        textt = ''
        if isFromClipBoard:
            text = self.root.clipboard_get()
            self.field_text_set = set()
            for eachkey in self.fields:
                self.field_text_set.add(self.fields[eachkey]["text"].get())
            if text not in self.field_text_set:
                self.field_text_set.add(text)
                textt=text
            else:
                return
        # Create a new input field and delete button
        self.field_frame = customtkinter.CTkFrame(self.crollable_frame)
        self.field_frame.grid_columnconfigure(1,weight=1)
        self.field_frame.grid_rowconfigure(0,weight=1)
        self.field = customtkinter.CTkEntry(self.field_frame)

        self.field.insert(tk.END, textt)

        index = uuid.uuid4()
        print("add " + str(index))
        self.fields[index] = {}
        self.fields[index]["frame"] = self.field_frame
        self.fields[index]["text"] = self.field
        self.delete_button=customtkinter.CTkButton(self.field_frame, text="X",
                                                     command=lambda: self.delete_field(index), width=2)
        self.copy_button = customtkinter.CTkButton(self.field_frame, text="C", command=lambda: self.copy_text(index),
                                                   width=2)
        # self.fields[self.delete_button]=self.field_frame
        # Add the field and delete button to the field frame

        self.copy_button.grid(row=0,column=0,sticky="e")
        self.field.grid(row=0,column=1,sticky="nsew")
        self.delete_button.grid(row=0,column=2,sticky="w")

        # Add the field frame to the GUI and keep track of it
        self.field_frame.pack(fill='both', expand=True,pady=5)
        # self.fields.append(self.field_frame)

        # Set the focus to the input field
        # field.focus_set()

    def copy_text(self, index):
        text = self.fields[index]["text"].get()
        self.root.clipboard_clear()
        self.root.clipboard_append(text)

    def delete_field(self, index):
        # Remove the specified field frame from the GUI and the fields list
        print("remove " + str(index))
        self.fields[index]["frame"].destroy()
        del self.fields[index]
        # self.fields.remove(field_frame)

    def toggle_topmost(self):
        if self.root.attributes("-topmost"):
            self.root.attributes("-topmost", False)
            self.topmost_button.configure(fg_color=('green', '#2FA572'),text='stick')
            self.root.overrideredirect(False)
        else:
            self.root.attributes("-topmost", True)
            self.topmost_button.configure(fg_color=('green', 'black'),text='sticked')
            self.root.overrideredirect(True)

    def increment_counter(self):
        self.count += 1
        self.counter_label.configure(text=str(self.count))

    def decrement_counter(self):
        self.count -= 1
        self.counter_label.configure(text=str(self.count))

class TodoList(customtkinter.CTkFrame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master

        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_rowconfigure(2,weight=1)
        self.create_widgets()

        # self.default_fg_color = customtkinter.CTkFrame(self.master)._fg_color

    def create_widgets(self):

        # Create a text box for adding new tasks
        self.add_entry = customtkinter.CTkEntry(self.master)
        self.add_entry.grid(row=0,column=0,columnspan=2,pady=5,sticky="new",)

        # Create a button to add new tasks
        self.add_button = customtkinter.CTkButton(self.master,width=1, text="Add Task", command=self.add_task)
        self.add_button.grid(row=1,column=0,pady=5,sticky="nw")
        # Create a button to remove completed tasks
        self.remove_button = customtkinter.CTkButton(self.master,width=1, text="Remove Completed Tasks", command=self.remove_task)
        self.remove_button.grid(row=1,column=1,pady=5,sticky="ne")
        # Create a frame to hold the task list
        self.task_frame = customtkinter.CTkFrame(self.master)
        self.task_frame.grid(row=2,column=0,columnspan=2,pady=5,sticky="nesw")



        # Create a list to store the tasks
        self.tasks = []

    def add_task(self):
        # Get the task from the add entry
        task_text = self.add_entry.get()

        # Create a frame for the task
        task_frame = customtkinter.CTkFrame(self.task_frame)
        task_frame.pack(fill=tk.X, padx=5, pady=5)

        # Create a Checkbutton for the task
        var = customtkinter.StringVar(value="off")
        task = customtkinter.CTkCheckBox(task_frame, text=task_text, variable=var, onvalue="on", offvalue="off")
        task.pack(side=tk.LEFT)

        # Create a button to delete the task
        delete_button = customtkinter.CTkButton(task_frame, width=1,text="D", command=lambda: self.delete_task(task_frame))
        delete_button.pack(side=tk.RIGHT)

        # Create a button to edit the task
        edit_button = customtkinter.CTkButton(task_frame, width=1,text="E", command=lambda: self.edit_task(task, task_text, task_frame))
        edit_button.pack(side=tk.RIGHT)

        # Create buttons to move the task up and down
        up_button = customtkinter.CTkButton(task_frame,width=1, text="↑", command=lambda: self.move_task(task_frame, -1))
        up_button.pack(side=tk.RIGHT)
        down_button = customtkinter.CTkButton(task_frame, width=1,text="↓", command=lambda: self.move_task(task_frame, 1))
        down_button.pack(side=tk.RIGHT)

        # Add the task and its components to the list of tasks
        self.tasks.append((task_text, var, task_frame))

        # Apply the special tag to the first task
        if len(self.tasks) == 1:
            self.bold_frame(task_frame)

        # Clear the add entry
        self.add_entry.delete(0, tk.END)

    def delete_task(self, task_frame):
        # Get the index of the task in the list of tasks
        for i, task in enumerate(self.tasks):
            if task[2] == task_frame:
                index = i

        # Remove the task from the list of tasks
        self.tasks.pop(index)

        # Remove the task frame from the task_frame container
        task_frame.pack_forget()

        # Apply the special tag to the new first task, if necessary
        if len(self.tasks) > 0 and index == 0:
            self.bold_frame(self.tasks[0][2])
    def bold_frame(self,frame):
        #TODO:换个样式
        frame.configure(fg_color='green')

    def off_bold_frame(self,frame):
        default = customtkinter.CTkFrame(self.master)._fg_color
        frame.configure(fg_color=default)
    def edit_task(self, task, task_text, task_frame):
        # Create a new window for editing the task
        edit_window = customtkinter.CTkToplevel(self.master)
        edit_window.focus()
        # Create a label and entry for editing the task text
        edit_label = customtkinter.CTkLabel(edit_window, text="Edit task:")
        edit_label.pack(pady=5)
        edit_entry = customtkinter.CTkEntry(edit_window, width=30)
        edit_entry.insert(0, task_text)
        edit_entry.pack(pady=5)

        # Create a button to save the edited task
        save_button = customtkinter.CTkButton(edit_window, text="Save", command=lambda: self.save_task(task, edit_entry.get(), task_frame, edit_window))
        save_button.pack(pady=5)

    def save_task(self, task, new_task_text, task_frame, edit_window):
        # Update the task text
        task.config(text=new_task_text)

        # Update the task in the list of tasks
        for i, t in enumerate(self.tasks):
            if t[2] == task_frame:
                self.tasks[i] = (new_task_text, t[1], t[2])

        # Close the edit window
        edit_window.destroy()

    def move_task(self, task_frame, direction):
        # Get the index of the task in the list of tasks
        for i, task in enumerate(self.tasks):
            if task[2] == task_frame:
                index = i

        # Calculate the new index of the task
        new_index = index + direction

        # Check that the new index is within the bounds of the task list
        if new_index < 0 or new_index >= len(self.tasks):
            return

        # Swap the task with the task at the new index in the list of tasks
        self.tasks[index], self.tasks[new_index] = self.tasks[new_index], self.tasks[index]

        # Update the position of the task frames in the task_frame container
        for i, task in enumerate(self.tasks):
            task_frame = task[2]
            task_frame.pack_forget()
            task_frame.pack(fill=tk.X, padx=5, pady=5)

            # Apply the special tag to the new first task
            if i == 0:
                self.bold_frame(task_frame)
            else:
                self.off_bold_frame(task_frame)

    def remove_task(self):
        # Remove completed tasks from the list of tasks
        for i, each in enumerate(self.tasks):
            print(str(i)+each[1].get())
        remove_tasks = [(task_text, var, task_frame) for task_text, var, task_frame in self.tasks if var.get()=="on"]
        self.tasks=[(task_text, var, task_frame) for task_text, var, task_frame in self.tasks if var.get()=="off"]
        # Destroy the task frames for completed tasks
        for task in remove_tasks:
            task_frame = task[2]
            task_frame.destroy()
        if len(self.tasks) != 0:
            self.bold_frame(self.tasks[0][2])


if __name__ == "__main__":
    MinatosTool()
