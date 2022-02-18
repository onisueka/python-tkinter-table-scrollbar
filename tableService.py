import tkinter as tk

class tableService(object):

    def __init__(self, container, data, scrollable = True):
        self.data = data
        self.frame = container
        self.header_bg = '#3d3d3d'
        self.header_color = '#ffffff'
        self.body_bg = '#ffffff'
        self.body_color = '#141414'
        if(scrollable == True):
            self.scroll_height = 350
            self.set_scrollbar()
        else:
            self._frame = self.frame

    def set_scrollbar(self):
        self.table_box = tk.Canvas(self.frame)
        self._frame = tk.Frame(self.table_box)
        scrollbar = tk.Scrollbar(self.frame, orient="vertical", command = self.table_box.yview)
        scrollbar.pack( side = tk.RIGHT, fill = tk.Y )
        self.table_box.config(yscrollcommand=scrollbar.set)
        self.table_box.pack()

        self.table_box.create_window((0,0), window=self._frame, anchor= tk.NW)
        self._frame.bind("<Configure>", lambda x: self.table_box.configure(scrollregion=self.table_box.bbox("all"), width=self._frame.winfo_width(), height=self.scroll_height))
        # with Windows OS (120/-120)
        self.table_box.bind_all("<MouseWheel>", lambda event: self.table_box.yview_scroll(int(5 * (event.delta / 120)), "units"))
        # with Linux OS (4/5)
        self.table_box.bind_all("<Button-4>", lambda event: self.table_box.yview_scroll(int(-100 * (event.num / 120)), "units"))
        self.table_box.bind_all("<Button-5>", lambda event: self.table_box.yview_scroll(int(100 * (event.num / 120)), "units"))

    def set_column(self, widths = []):
        self.column_width = widths

    def set_header(self, headers = ()):
        frame = tk.Frame(self._frame)
        frame.pack(anchor = tk.NW)
        for index, item in enumerate(headers):
            tk.Label(frame, text=item['text'], borderwidth=2, relief="groove", padx=10, background=self.header_bg, foreground=self.header_color, width=self.column_width[index]).pack(side = tk.LEFT)

    def set_body(self, bodies = ()):
        frame = tk.Frame(self._frame)
        frame.pack(anchor = tk.NW)

        for index, item in enumerate(bodies):
            if(item['type'] == 'checkbox'):
                row = tk.IntVar()
                module_checkbox_name = 'checkbox' + str(index)
                command = lambda _item = row: self.data.binding_event({ 'module': module_checkbox_name, 'id': bodies[0]['text'], 'value': _item.get() })
                tk.Checkbutton(frame, text='', borderwidth=2, relief="groove", padx=12, pady=5, variable=row, onvalue=1, offvalue=0, background=self.body_bg, foreground=self.body_color, width=self.column_width[index] - 3, command=command).pack(side = tk.LEFT)
            elif(item['type'] == 'selectbox'):
                row = tk.StringVar(frame)
                row.set(item['text']) # initial value
                module_selectbox_name = 'selectbox' + str(index)
                command = lambda _item: self.data.binding_event({ 'module': module_selectbox_name, 'id': bodies[0]['text'], 'value': _item })
                optionmenu = tk.OptionMenu(frame, row, "pending", "complete", command=command)
                optionmenu.config(borderwidth=2, relief="groove", padx=8, pady=4, background=self.body_bg, foreground=self.body_color, width = self.column_width[index] - 3)
                optionmenu.pack(side = tk.LEFT)
            else:
                tk.Label(frame, text=item['text'], borderwidth=2, relief="groove", padx=10, pady=5, background=self.body_bg, foreground=self.body_color, width=self.column_width[index]).pack(side = tk.LEFT)       
