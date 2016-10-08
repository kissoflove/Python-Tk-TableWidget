import tkinter as tk
from tkinter import ttk

class TableFrame(tk.Frame):
    """A spreadsheet-like widget having a row header, a column header
    and a table with thousands of rows and columns.
    """

    def __init__(self, container, data=None, data_rows=None, data_cols=None, offset_x=0, offset_y=0, default=None):


        tk.Frame.__init__(self, container)
        self.container = container
        self.data = data
        self.offset_x = offset_x
        self.offset_y = offset_y

        self.row_header = row_header = Cells(master=self, data="row_header")
        self.col_header = col_header = Cells(master=self, data="col_header")
        self.table = table = Cells(master=self, data=data)

        row_header.insert_col(0)
        col_header.insert_row(0)

        self.vsb = vsb = tk.Scrollbar(self, orient="vertical", command=self.on_vsb_scroll)
        self.hsb = hsb = tk.Scrollbar(self, orient="horizontal", command=self.on_hsb_scroll)

        # Frame does not support ScrollBar but Canvas does.
        # So, embed frame in canvas to use ScrollBar.
        self.canvas = canvas = MyCanvas(master=self, borderwidth=0, background="#d4d4d4")
        self.rh_canvas = rh_canvas = MyCanvas(master=self, borderwidth=0,
                                               width=40, background="#d4d4d4")
        self.ch_canvas = ch_canvas = MyCanvas(master=self, borderwidth=0,
                                               height=20, background="#d4d4d4")

        rh_canvas.grid(column=0, row=1, sticky='nsew')
        ch_canvas.grid(column=1, row=0, sticky='nsew')

        canvas.grid(column=1, row=1, sticky='nsew')
        vsb.grid(column=2, row=1, sticky='ns')
        hsb.grid(column=1, row=2, sticky='ew')

        canvas.create_window((0, 0), window=self.table, anchor="nw", tags="self.table")
        rh_canvas.create_window((0, 0), window=self.row_header, anchor="nw", tags="self.row_header")
        ch_canvas.create_window((0, 0), window=self.col_header, anchor="nw", tags="self.col_header")

        self.rowconfigure(0, weight=0)      # row header
        self.columnconfigure(0, weight=0)   # col header
        self.rowconfigure(1, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(2, weight=0)
        self.columnconfigure(2, weight=0)

        self.canvas.bind("<Configure>", self.on_frame_configure)
        self.canvas.bind("<MouseWheel>", self.on_mouse_scroll)
        self.canvas.bind_all("<Key>", self.on_key_scroll)

        # self.auto_extend = auto_extend

        self.table.data = data
        self.canvas.data = data
        self.default = self.cell_options_default()
        if default:
            self.default.update(default)
        self.default = self.get_ikeysdict(self.default)
        
        self.row_default = self.get_ikeysdict(self.cell_options_default())
        self.col_default = self.get_ikeysdict(self.cell_options_default())
        self.data_rows = 0
        self.data_cols = 0
        self.visible_rows = 0
        self.visible_cols = 0

    keys = ['value', 'font', 'justify', 'bg', 'fg', 'width', 'height', 'state'] # tk keys
    ikeys = ['v', 'ft', 'a', 'b', 'f', 'w', 'h', 's'] # internal saved format
    keysdict = dict(zip(keys, ikeys))
    ikeysdict = dict(zip(ikeys, keys))

    def get_ikeysdict(self, d):
        '''Convert from tk keys to internal format'''
        di = {}
        for key in d:
            ikey = self.keysdict.get(key)
            if ikey:
                di[ikey] = d[key]
            else:
                di[key] = d[key]

        return di

    def get_keysdict(self, d):
        '''Convert from internal format to tk keys'''
        di = {}
        for ikey in d:
            key = self.ikeysdict.get(ikey)
            if key:
                di[key] = d[ikey]
            else:
                di[ikey] = d[ikey]

        return di

    def set_table_default(self, default={}, **kwargs):
        """set default cell value and cell attributes, for table.
            {value:value, font:font, align:align, bgcolor:bgcolor,
            fgcolor:fgcolor, width:width, height:height}

            This default is used when no cell values, row_defaults, 
            col_defaults are set.
        """
        d = {}
        d.update(default, **kwargs)
        di = self.get_ikeysdict(d)

        self.default.update(di)

    def set_row_default(self, default={}, **kwargs):
        """set default cell attributes, for row header.
            {font:font, align:align, bgcolor:bgcolor, fgcolor:fgcolor, 
            width:width, height:height}

            The row header attributes are set from this default and 
            row_defaults
        """
        d = {}
        d.update(default, **kwargs)
        di = self.get_ikeysdict(d)

        self.row_default.update(di)

    def set_col_default(self, default={}, **kwargs):
        """set default cell attributes, for column header.
            {font:font, align:align, bgcolor:bgcolor, fgcolor:fgcolor, 
            width:width, height:height}

            The column header attributes are set from this default and 
            col_defaults
        """
        d = {}
        d.update(default, **kwargs)
        di = self.get_ikeysdict(d)

        self.col_default.update(di)

    def set_value(self, row, col, value):
        self.table.set_value(row, col, value)

    def set_row_header(self, row, value):
        self.row_header.set_value(row, 0, value)

    def set_col_header(self, col, value):
        self.col_header.set_value(0, col, value)

    def on_vsb_scroll(self, *args):
        self.canvas.yview(*args)
        self.rh_canvas.yview(*args)

    def on_hsb_scroll(self, *args):
        self.canvas.xview(*args)
        self.ch_canvas.xview(*args)

    def on_mouse_scroll(self, event):
        if event.delta > 0:
            self.on_vsb_scroll("scroll", "-3", "units")
        else:
            self.on_vsb_scroll("scroll", "3", "units")

    unit = 1
    def set_key_scroll_size(self, unit=1):
        self.unit = unit

    def on_key_scroll(self, event):
        if event.keysym == 'Up':
            self.on_vsb_scroll("scroll", "-"+str(self.unit), "units")
        if event.keysym == 'Down':
            self.on_vsb_scroll("scroll", str(self.unit), "units")
        if event.keysym == 'Left':
            self.on_hsb_scroll("scroll", "-"+str(self.unit), "units")
        if event.keysym == 'Right':
            self.on_hsb_scroll("scroll", str(self.unit), "units")
        if event.keysym == 'Prior': #PageUp
            self.on_vsb_scroll("scroll", "-1", "pages")
        if event.keysym == 'Next':  #PageDown
            self.on_vsb_scroll("scroll", "1", "pages")
        if event.keysym == 'Home':
            if self.offset_x > 0 or self.offset_y > 0:
                self.hsb.set(0, min(self.visible_cols/self.data_cols, 1))
                self.vsb.set(0, min(self.visible_rows/self.data_rows, 1))
                self.offset_x = 0
                self.offset_y = 0
                self.row_header.redraw()
                self.col_header.redraw()
                self.table.redraw()
        if event.keysym == 'End':
            rs = max(0, self.data_rows - self.visible_rows)
            cs = max(0, self.data_cols - self.visible_cols)
            if self.offset_x < cs or self.offset_y < rs:
                self.hsb.set(cs/self.data_cols, 1)
                self.vsb.set(rs/self.data_rows, 1)
                self.offset_x = cs
                self.offset_y = rs
                self.row_header.redraw()
                self.col_header.redraw()
                self.table.redraw()

    def reset_scrollbars(self):
        """reset scrollbars based on new data/offsets and visible area.
        """
        ystart = self.offset_x / self.data_rows
        yend = (self.visible_rows + self.offset_x) / self.data_rows
        xstart = self.offset_y / self.data_cols
        xend = (self.visible_cols + self.offset_y) / self.data_cols
        self.vsb.set(ystart, yend)
        self.hsb.set(xstart, xend)

    def _resync(self):
        """resync visible area to the backing store, when either visible
        area changes size or the backing store changes size.

        Invariant: all visible area always reflects some part in the 
        backing store so that the backing store is at least large in size
        as visible area.
        
        1. Insert/delete rows/columns as visible area increases/decreases;
        2. When reaching the last backing rows/columns, adjusting offset 
        instead; 
        3. When the backing store is smaller than visible area, 
        filling empty cells/values to visible area/the backing store.
        """

        rows = self.visible_rows
        cols = self.visible_cols

        if cols + self.offset_x > len(self.data[0]):
            if len(self.data[0]) - cols >= 0:
                self.offset_x = len(self.data[0]) - cols
            else:
                #self.col_header.set_col_count(cols)
                for i in range(len(self.data)):
                    if self.data[i]:
                        self.data[i].extend([None]*(cols - len(self.data[i])))

        if rows + self.offset_y > len(self.data):
            if len(self.data) - rows >= 0:
                self.offset_y = len(self.data) - rows
            else:
                #self.row_header.set_row_count(rows)
                self.data.extend([None]*(rows - len(self.data)))

        self.resize_row(rows)
        self.resize_col(cols)
        self.reset_scrollbars()

    def on_frame_configure(self, event):
        """Reset the scroll region to encompass the inner frame"""
        self.table.lower(self.rh_canvas)
        self.table.lower(self.ch_canvas)
        self.table.lift(self.canvas)
        self.row_header.lift(self.rh_canvas)
        self.col_header.lift(self.ch_canvas)
        self.canvas.lower(self.vsb)
        self.canvas.lower(self.hsb)

        cell_w, cell_h = self.cell_geometry()
        self.visible_cols = int(event.width / cell_w) + 1
        self.visible_rows = int(event.height / cell_h) + 1

        if self.data:
            self.data_rows = len(self.data)
        if self.data and self.data[0]:
            self.data_cols = len(self.data[0])

        self._resync()

        self.rh_canvas.grid(column=0, row=1, sticky='nsew')
        self.ch_canvas.grid(column=1, row=0, sticky='nsew')

        self.canvas.grid(column=1, row=1, sticky='nsew')
        self.vsb.grid(column=2, row=1, sticky='ns')
        self.hsb.grid(column=1, row=2, sticky='ew')
        self.table.configure(width=event.width, height=event.height)

        self.table.grid_propagate(0) # force the widget size regardless of its content
        self.after_idle(self.release_grab) # release grab in case locked

    def release_grab(self, *args):
        w = self.grab_current()
        if w:
            w.grab_release()

    current_cell = None
    def set_current_cell(self, event):
        """set current cell when the mouse moves in"""

        if self.current_cell:
            self.current_cell.configure(highlightthickness=0)

        self.current_cell = event.widget
        self.current_cell.configure(highlightthickness=1)
        self.current_cell.configure(highlightcolor="#00ffff")

    # selected region in rows and columns
    selected_row = None
    selected_col = None
    selected_row2 = None
    selected_col2 = None

    def clear_selection():
        if selected_row and selected_col and selected_row2 and selected_col2:
            for row in range(self.selected_row, self.selected_row2 + 1):
                for col in range(self.selected_col, self.selected_col2 + 1):
                    self.table.cells[row][col].configure(highlightthickness=0)
                    self.table.cells[row][col].configure(highlightcolor="#00ffff")

    def set_selection(self, x1, y1, x2, y2):
        """make cells selected within area (x1, y1, x2, y2) in pixels"""

        self.clear_selection()

        row, col = self.table.grid_location(x1, y1)
        row2, col2 = self.table.grid_location(x2, y2)
        self.selected_row = row
        self.selected_col = col
        self.selected_row2 = row2
        self.selected_col2 = col2

        for row in range(self.selected_row, self.selected_row2 + 1):
            for col in range(self.selected_col, self.selected_col2 + 1):
                self.table.cells[row][col].configure(highlightthickness=1)
                self.table.cells[row][col].configure(highlightcolor="#ff0000")

    def insert_row(self, pos, count=1, text=None):

        if not count > 0:
            return

        self.row_header.insert_row(pos, count)
        self.table.insert_row(pos, count, text)


    def insert_col(self, pos, count=1, text=None):

        if not count > 0:
            return

        self.col_header.insert_col(pos, count)
        self.table.insert_col(pos, count, text)

    def delete_row(self, pos, count):
        self.row_header.delete_row(pos, count)
        self.table.delete_col(pos, count)

    def delete_col(self, pos, count):
        self.col_header.delete_col(pos, count)
        self.table.delete_col(pos, count)

    def clear_all(self):
        self.row_header.clear_all()
        self.col_header.clear_all()
        self.table.clear_all()

    def resize_row(self, count):
        curr_count = self.count_row()

        if count > curr_count:
            self.insert_row(curr_count, count - curr_count)
        elif count < curr_count:
            self.delete_row(count, curr_count - count)
        else:   # count == curr_count
            pass    # Do nothing.

    def resize_col(self, count):
        curr_count = self.count_col()

        if count > curr_count:
            self.insert_col(curr_count, count - curr_count)
        elif count < curr_count:
            self.delete_col(count, curr_count - count)
        else:   # count == curr_count
            pass    # Do nothing.

    def count_row(self):
        return self.row_header.count_row()

    def count_col(self):
        return self.col_header.count_col()

    def set_data(self, data, data_rows=0, data_cols=0, offset_x=0, offset_y=0):
        """set backing store for the table.

        data format:
        data is a list of rows, each of rows is a list of cells, each cell
        is either a value or a dict which contains cell value and cell
        attributes. A row or a cell could be None. The trailing Nones 
        could be omitted for columns or rows, in which case data_rows and/
        or data_cols should be specified. This is a trade-off for space and
        time efficiency for daily use-cases.

        Cell dict has the following keys which have internal keys to save
        space for large data set:

        keys = ['value', 'font', 'align', 'bg', 'fg', 'width', 'height',
                'state', 'background', 'foreground', 'justify']
        ikeys = ['v', 'ft', 'a', 'b', 'f', 'w', 'h',
                 's', 'b', 'f', 'a']

        Other keys supported by Entry Widget or Text Widget are transferred
        to the cell widget. However width/height are pixels which would be
        transformed to characters/lines for Entry Widget/Text Widget.

        offset_x: the starting row offset to be displayed
        offset_y: the starting column offset to be displayed
        """

        self.data_rows = max(data_rows, len(data)) if data else data_rows

        self.data_cols = max([len(data[i]) for i in range(self.data_rows) if data[i]])
        self.data_cols = max(self.data_cols, data_cols)

        if offset_x < 0:
            offset_x = 0
        if offset_y < 0:
            offset_y = 0
        if offset_y >= self.data_rows:
            offset_y = self.data_rows - 1
        if offset_x >= self.data_cols:
            offset_x = self.data_cols - 1

        self.data = data
        self.table.data = data
        self.canvas.data = data

        self.offset_x = offset_x
        self.offset_y = offset_y

        if not self.table.cells:
            for i in range(self.visible_cols):
                self.insert_col(i)

            for j in range(self.visible_rows):
                self.insert_row(j)

            for i in range(self.visible_rows):
                for j in range(self.visible_cols):
                    ix = i + self.offset_x
                    iy = j + self.offset_y
                    if self.data and self.data[ix] and self.data[ix][iy]:
                        self.set_value(i, j, self.data[ix][iy])

            for i in range(self.visible_rows):
                self.set_row_header(i, i+self.offset_y)

            for j in range(self.visible_cols):
                self.set_col_header(j, j+self.offset_x)

            self.reset_scrollbars()
        else:
            self._resync()

        self.table.redraw()
        self.row_header.redraw()
        self.col_header.redraw()

    #The following methods operate on backing store

    def insert_data_row(self, pos, count=1, text=None):
        pass

    def insert_data_col(self, pos, count=1, text=None):
        pass

    def delete_data_row(self, pos, count):
        pass

    def delete_data_col(self, pos, count):
        pass

    def clear_data_all(self):
        pass

    def resize_data_row(self, count):
        pass

    def resize_data_col(self, count):
        pass

    def count_data_row(self):
        pass

    def count_data_col(self):
        pass

    dummy_cell = None
    CELL_WIDTH = 5 # 5 characters
    def _dummy_cell(self):
        if self.dummy_cell == None:
            self.dummy_cell = tk.Entry(self,
                        readonlybackground="#bbbbbb",
                        width=self.CELL_WIDTH,
                        state="readonly",
                        highlightcolor="#ff0000",
                        cursor="left_ptr",
                        relief="flat")

    def cell_geometry(self):
        self._dummy_cell()

        return (self.dummy_cell.winfo_reqwidth(), self.dummy_cell.winfo_reqheight())

    def cell_options_default(self):
        self._dummy_cell()
        options_default = self.dummy_cell.configure()
        bg = options_default.pop('background', None)
        options_default['bg'] = bg
        fg = options_default.pop('foreground', None)
        options_default['fg'] = fg
        keys = self.keys + ['readonlybackground', 'highlightcolor', 'cursor', 'relief']
        return {k:options_default[k][-1] for k in options_default if len(options_default[k]) == 5 and k in keys}


class MyCanvas(tk.Canvas):
    """Special canvas with large backstore, dynamically inserting/deleting
    row/column when scrolling/resizing.
    """

    def __init__(self, master, **args):

        tk.Canvas.__init__(self, master, **args)

        self.master = master
        self.data = self.master.data

    def yview(self, event, value, unit=None):
        if event == "moveto":
            self.set_row_offset(int(len(self.master.data) * float(value) + 0.5))
            ystart = float(value)
        elif event == "scroll":
            if unit == "units":
                self.set_row_offset(self.master.offset_y + int(value))
                ystart = (self.master.offset_y + int(value)) / len(self.master.data)
            elif unit == "pages":
                page_size = self.master.count_row()
                self.set_row_offset(self.master.offset_y + int(value) * page_size)
                ystart = (self.master.offset_y + int(value) * page_size) / len(self.master.data)

        yend = ystart + self.master.count_row()/len(self.master.data)
        self.master.vsb.set(ystart, yend)

    def xview(self, event, value, unit=None):
        if event == "moveto":
            self.set_col_offset(int(len(self.master.data[0]) * float(value) + 0.5))
            xstart = float(value)
        elif event == "scroll":
            if unit == "units":
                self.set_col_offset(self.master.offset_x + int(value))
                xstart = (self.master.offset_x + int(value)) / len(self.master.data[0])
            elif unit == "pages":
                page_size = self.master.count_col()
                self.set_col_offset(self.master.offset_x + int(value) * page_size)
                xstart = (self.master.offset_x + int(value) * page_size) / len(self.master.data[0])

        xend = xstart + self.master.count_col()/len(self.master.data[0])
        self.master.hsb.set(xstart, xend)

    def set_row_offset(self, offset):
        # clamp first index
        page_size = self.master.count_row()
        if offset < 0 or len(self.master.data) <= page_size:
            offset = 0
        elif offset >= len(self.master.data) - page_size:
            offset = len(self.master.data)-page_size
        if offset != self.master.offset_y:
            # redraw widget
            self.master.offset_y = offset
            self.master.row_header.redraw()
            self.master.col_header.redraw()
            self.master.table.redraw()


    def set_col_offset(self, offset):
        # clamp first index
        page_size = self.master.count_col()
        if offset < 0 or len(self.master.data[0]) <= page_size:
            offset = 0
        elif offset >= len(self.master.data[0]) - page_size:
            offset = len(self.master.data[0])-page_size
        if offset != self.master.offset_x:
            # redraw widget
            self.master.offset_x = offset
            self.master.row_header.redraw()
            self.master.col_header.redraw()
            self.master.table.redraw()


    def get_visible_region(self):
        x1, y1 = self.canvasx(0), self.canvasy(0)
        self.update_idletasks() # make sure winfo_reqwidth/height up to date
        w, h = self.winfo_reqwidth(), self.winfo_reqheight()
        x2, y2 = self.canvasx(w), self.canvasy(h)
        return (x1, y1, x2, y2)


class Cells(tk.Frame):

    def __init__(self, master, data=None):

        tk.Frame.__init__(self, master)
        self.master = master
        self.data = data
        self.cells = []  # list of rows of nodes
    
        self.configure(background="#d4d4d4")  # Boader color: slightly darker than default
        self._row_count = 0
        self._col_count = 0

        self.bind('<MouseWheel>', master.on_mouse_scroll)

        self.row_defaults = self.col_defaults = []

    def count_row(self):
        """Count rows or nodes"""
        return self._row_count

    def count_col(self):
        """Count rows or nodes"""
        return self._col_count

    def set_row_count(self, count):
        self._row_count = count

    def set_col_count(self, count):
        self._col_count = count

    def set_row_defaults(self, row, default={}, **kwargs):
        """set default cell vaule and cell attributes, 
        for <row> in row_header.

        row_defaults are looked up when the cell values/attrs are not 
        found.  <row> is relative to the backing store data origin.
        """
        if row < self.master.data_rows:
            d = {}
            d.update(default, **kwargs)
            di = self.master.get_ikeysdict(d)

            if not self.row_defaults:
                self.row_defaults = [[None] for i in range(row + 1)]

            if len(self.row_defaults) < row:
                self.row_defaults.extend([[None] for i in range(row-len(self.row_defaults)+1)])

            if not self.row_defaults[row][0]:
                self.row_defaults[row][0] = {}

            self.row_defaults[row][0].update(di)

    def set_col_defaults(self, col, default={}, **kwargs):
        """set default cell vaule and cell attributes, 
        for <col> in col_header.

        col_defaults are looked up when the cell values/attrs are not 
        found.  <col> is relative to the backing store data origin.
        """
        if col < self.master.data_cols:
            d = {}
            d.update(default, **kwargs)
            di = self.master.get_ikeysdict(d)

            if not self.col_defaults:
                self.col_defaults = [None] * (col + 1)
     
            if len(self.col_defaults) < col:
                self.col_defaults.extend([None]*(col-len(self.col_defaults)+1))

            if not self.col_defaults[col]:
                self.col_defaults[col] = {}

            self.col_defaults[col].update(di)

    def _set_cell_value(self, cell, value):
        last_state = cell.cget("state")
        cell.config(state="normal")
        cell.delete(0, tk.END)
        cell.insert(0, value)
        cell.config(state=last_state)

    def _set_value(self, row, col, value):
        """Set value to an on-screen grid cell.

        (row, col) are relative to the on-screen grid left-top corner.
        """
        cell = self.cells[row][col]
        self._set_cell_value(cell, value)

    def get_nchars(self, width):
        """get the number of chars for the width in pixels"""

    def get_nlines(self, height):
        """get the number of lines for the height in pixels"""

    def _set_attrs(self, row, col, attrs):
        """Set attrs to an on-screen grid cell.

        (row, col) are relative to the on-screen grid left-top corner.
        """
        bg = attrs.get('bg')
        
        if bg:
            cell = self.cells[row][col]
            state = cell.cget("state")
            if state == 'readonly':
                attrs['readonlybackground'] = bg
            elif state == 'disabled':
                attrs['disabledbackground'] = bg

        self._config(self.cells[row][col], attrs, mode='tk')

    def _fill_empty(self, row, col):
        if not self.data:
            self.data.extend([[None]] * (row - len(self.data) + 1))
            self.data[row].extend([None] * (col-len(self.data[row])+1))
        elif not self.data[row]:
            self.data.extend([[None]] * (row - len(self.data) + 1))
        elif not self.data[row][col]:
            self.data[row].extend([None] * (col-len(self.data[row])+1))

    def _set_data_value(self, row, col, value):
        """Set value to a cell at the backing store.

        (row, col) are relative to the backing store origin.
        """
        self._fill_empty(row, col)
        c = self.data[row][col]
        if isinstance(c, dict):
            c.update(v=value)
            self.data[row][col] = c
        else:
            self.data[row][col] = value

    def _set_data_attrs(self, row, col, attrs):
        """Set attrs to a cell at the backing store.

        (row, col) are relative to the backing store origin.
        """
        self._fill_empty(row, col)
        c = self.data[row][col]
        if isinstance(c, dict):
            c.update(**attrs)
            self.data[row][col] = c
        elif c == None:
            if attrs:
                self.data[row][col] = attrs
        else:
            if attrs:
                attrs.update({'v':c})
                self.data[row][col] = attrs

    def set_value(self, row, col, value):
        """Set value to an on-screen grid cell and the backing store.

        (row, col) are relative to the on-screen grid left-top corner.
        """

        if row < self.count_row()  \
            and col < self.count_col() \
            and self.cells \
            and self.cells[row] \
            and self.cells[row][col]:

            self._set_value(row, col, value)

        if not isinstance(self.data, str):
            row += self.master.offset_y
            col += self.master.offset_x

            if row < self.master.data_rows \
                and col < self.master.data_cols:

                self._set_data_value(row, col, value)

    def set_data_value(self, row, col, value):
        """Set value to a cell at the backing store.

        (row, col) are relative to the backing store origin.
        """

        if not isinstance(self.data, str):

            if row < self.master.data_rows \
                and col < self.master.data_cols:

                self._set_data_value(row, col, value)

    def set_row_value(self, row, value):
        """Set value to a row of cells"""

    def set_col_value(self, col, value):
        """Set value to a column of cells"""

    def set_region_value(self, start_row, end_row, start_col, end_col, value):
        """Set value to a region of cells"""

    def set_font(self, row, col, font):
        """Set font to a cell"""
        self.set_attrs(row, col, font=font)

    def set_align(self, row, col, align):
        """Set alignment to a cell

            tk.LEFT(default), tk.CENTER, tk.RIGHT
        """
        self.set_attrs(row, col, justify=align)

    def set_background(self, row, col, bg):
        """Set bg to a cell"""
        self.set_attrs(row, col, bg=bg)

    def set_foreground(self, row, col, fg):
        """Set fg to a cell"""
        self.set_attrs(row, col, fg=fg)

    def set_width(self, row, col, width):
        """Set width in pixel to a cell"""
        self.set_attrs(row, col, width=width)

    def set_height(self, row, col, height):
        """Set height in pixel to a cell"""
        self.set_attrs(row, col, height=height)

    def set_attrs(self, row, col, attrs={}, **kwargs):
        """set attributes to an on-screen grid cell and the backing store.

        (row, col) are relative to the on-screen grid left-top corner.

        """

        d = {}
        d.update(attrs, **kwargs)

        if d:
            di = self.master.get_ikeysdict(d)

            if row < self.count_row()  \
                and col < self.count_col() \
                and self.cells \
                and self.cells[row] \
                and self.cells[row][col]:

                self._set_attrs(row, col, d)

            #row += self.master.offset_y
            #col += self.master.offset_x

            #if not isinstance(self.data, str):
            #    if row < self.master.data_rows \
            #        and col < self.master.data_cols:

            #        self._set_data_attrs(row, col, di)

    def set_data_attrs(self, row, col, attrs={}, **kwargs):
        """set attributes to the backing store.

        (row, col) are relative to the backing store origin.

        """

        d = {}
        d.update(attrs, **kwargs)

        if d:
            di = self.master.get_ikeysdict(d)

            if not isinstance(self.data, str):
                if row < self.master.data_rows \
                    and col < self.master.data_cols:

                    self._set_data_attrs(row, col, di)

    def set_value_attrs(self, row, col, attrs={}, **kwargs):
        """set value and attributes to an on-screen grid cell and the 
        backing store.

        (row, col) are relative to the on-screen grid left-top corner.

        """

        d = di = {}
        d.update(attrs, **kwargs)
        value = d.pop('value', None)

        if value or value == 0:
            self.set_value(row, col, value)

        self.set_attrs(row, col, d)

    def set_data_value_attrs(self, row, col, attrs={}, **kwargs):
        """set value and attributes to an on-screen grid cell and the 
        backing store.

        (row, col) are relative to the backing store origin.

        """

        d = di = {}
        d.update(attrs, **kwargs)
        value = d.pop('value', None)

        if value:
            self.set_data_value(row, col, value)

        self.set_data_attrs(row, col, d)

    def insert_row(self, pos, count=1, text=None):
        """Insert empty rows or nodes"""
        if count < 1:
            raise ValueError

        pos = max(min(pos, self._row_count), 0)

        for r in range(count):
            col = []    # col is empty if self._col_count == 0
            for c in range(self._col_count):
                col.append(self._new_cell(text))

            self.cells.insert(pos, col)

        self._row_count += count

        self.redraw()

    def insert_col(self, pos, count=1, text=None):
        """Insert empty rows or nodes"""
        if count < 1:
            raise ValueError

        pos = max(min(pos, self._col_count), 0)

        if self._row_count == 0:
            pass
        else:
            for row in self.cells:
                for col in range(count):
                    row.insert(pos, self._new_cell(text))

        self._col_count += count

        self.redraw()

    def _config(self, cell, conf, mode='internal'):
        #if isinstance(cell, tk.Entry):
        #    conf.pop('height', None) #TclError: unknown option 'height' for Entry
        #    conf.pop('h', None) #TclError: unknown option 'height' for Entry
        #if isinstance(cell, tk.Text):
        #    conf.pop('justify', None) #TclError: unknown option 'justify' for Text
        #    conf.pop('a', None) #TclError: unknown option 'justify' for Text

        if mode == 'internal':
            cell.configure(**self.master.get_keysdict(conf))
        else:
            cell.configure(**conf)

    def _new_cell(self, text=None, mode='singleline'):
        if mode == 'singleline':
            cell = tk.Entry(self)
        else:
            cell = tk.Text(self)

        self._config(cell, self.master.default)
        cell.grid(padx=(0, 1), pady=(0, 1))
        if text:
            _set_cell_value(cell, value)

        # Force the widget size regardless of its content. 
        # TODO: make a customized Entry widget to accomodate multilines
        # and font/size chanages.
        # grid_propagate(0) does not contain font changes.
        cell.grid_propagate(0)

        cell.bind("<MouseWheel>", self.master.on_mouse_scroll)
        cell.tk_focusFollowsMouse()

        return cell

    def redraw(self):
        for row in range(self.count_row()):
            for col in range(self.count_col()):
                iy = col + self.master.offset_x
                ix = row + self.master.offset_y
                if self.data == "row_header":
                    self.set_value(row, col, ix)

                    cd = self.master.row_default.copy()
                    row_defaults = self.row_defaults
                    if row_defaults and ix < len(row_defaults) and row_defaults[ix][0]:
                        cd.update(row_defaults[ix][0])

                    cd = self.master.get_keysdict(cd)
                    self._set_attrs(row, col, cd)
                elif self.data == "col_header":
                    self.set_value(row, col, iy)

                    cd = self.master.col_default.copy()
                    col_defaults = self.col_defaults
                    if col_defaults and iy < len(col_defaults) and col_defaults[iy]:
                        cd.update(col_defaults[iy])

                    cd = self.master.get_keysdict(cd)
                    self._set_attrs(row, col, cd)
                else:
                    if ix < len(self.data) and iy < len(self.data[0]):
                        c = {}
                        if self.data and self.data[ix]:
                            c = self.data[ix][iy]
                            if c == None:
                                c = {}
                            elif not isinstance(c, dict): # cell is a value
                                c = {'v': c}

                        cd = self.master.default.copy()
                        row_defaults = self.master.row_header.row_defaults
                        if row_defaults and ix < len(row_defaults) and row_defaults[ix][0]:
                            cd.update(row_defaults[ix][0])
                        col_defaults = self.master.col_header.col_defaults
                        if col_defaults and iy < len(col_defaults) and col_defaults[iy]:
                            cd.update(col_defaults[iy])
                        cd.update(c)
                        c = self.master.get_keysdict(cd)

                        if self.data[ix] == None:
                            self.clear_cell(row, col)
                        elif self.data[ix][iy] == None:
                            self.clear_cell(row, col)
                        else:
                            self.set_value_attrs(row, col, c)

                self.cells[row][col].grid(row=row, column=col)

    def delete_row(self, pos, count=1):

        if count <= 0:
            return

        row_count = self.count_row()

        if not pos < row_count:
                return  # Do nothing.

        count = min(count, row_count - pos)

        for i in range(count):
            deleted_row = self.cells[pos]
            self.cells.pop(pos)

            for j in range(len(deleted_row)):
                deleted_row[j].grid_remove()
                deleted_row[j].destroy()

        self._row_count -= count

        self.redraw()

    def delete_col(self, pos, count=1):

        if count <= 0:
            return

        col_count = self.count_col()

        if not pos < col_count:
            return  # Do nothing.

        count = min(count, col_count - pos)

        for row in self.cells:
            for i in range(count):
                deleted_cell = row[pos]
                row.pop(pos)
                deleted_cell.grid_remove()
                deleted_cell.destroy()

        self._col_count -= count

        self.redraw()

    def clear_cell(self, row, col):
        cell = self.cells[row][col]
        last_state = cell.cget("state")
        cell.config(state="normal")
        cell.delete(0, tk.END)
        cell.config(state=last_state)

    def clear_all(self):
        for row in range(self.count_row()):
            for col in range(self.count_col()):
                self.clear_cell(row, col)


def test_table_frame(data_size='small'):

    LARGE = 2000
    SMALL = 5

    # initialize large data
    large_data = []
    for i in range(LARGE):
        large_data.append([])
        for j in range(LARGE):
            large_data[i].append(i*LARGE+j)

    # initialize small data
    small_data = []
    for i in range(SMALL):
        small_data.append([])
        for j in range(SMALL):
            small_data[i].append(i*SMALL+j)

    root = tk.Tk()
    table_frame = TableFrame(root)
    table_frame.pack(side="top", fill="both", expand=True)

    table_frame.set_data(large_data, data_rows=LARGE, data_cols=LARGE, offset_x=50, offset_y=40)

    import tkinter.font as tkFont

    header_font = tkFont.Font(weight="bold")

    table_frame.set_table_default({})
    #table_frame.set_row_default(font=header_font, justify="center", fg="#0000ff", bg='#00ffff')
    #table_frame.set_col_default(font=header_font, justify="center", fg="#0000ff", bg='#00ffff')
    table_frame.set_row_default(justify="center", fg="#0000ff", bg='#00ffff')
    table_frame.set_col_default(justify="center", fg="#0000ff", bg='#00ffff')

    table_frame.col_header.set_col_defaults(56, width=12)
    #table_frame.row_header.set_row_defaults(45, height=2)

    table_frame.table.set_data_attrs(45, 54, fg="#ff0000")
    table_frame.table.set_data_attrs(45, 55, fg="#00ff00")
    table_frame.table.set_data_attrs(45, 56, fg="#0000ff")
    table_frame.table.set_data_value(45, 56, "testtesttesttesttest")

    def _on_mouse_press():
        large = False

        def _switch_data(event):
            nonlocal large
            large = not large
            if large:
                table_frame.set_data(large_data, data_rows=LARGE, data_cols=LARGE, offset_x=50, offset_y=40)
            else:
                table_frame.set_data(small_data, data_rows=SMALL, data_cols=SMALL)

        return _switch_data

    on_mouse_press = _on_mouse_press()

    switch_data_frame = tk.Frame(table_frame)
    switch_data_frame.grid(column=0, row=0, sticky='nsew')
    switch_data_frame.bind("<Button>", on_mouse_press)

    root.mainloop()


def sortby(tree, col, descending):
    """Sort tree contents when a column is clicked on."""
    # grab values to sort
    data = [(tree.set(child, col), child) for child in tree.get_children('')]

    # reorder data
    data.sort(reverse=descending)
    for indx, item in enumerate(data):
        tree.move(item[1], '', indx)

    # switch the heading so that it will sort in the opposite direction
    tree.heading(col,
                 command=lambda col=col: sortby(tree, col, int(not descending)))

def autoscroll(sbar, first, last):
    """Hide and show scrollbar as needed."""
    first, last = float(first), float(last)
    if first <= 0 and last >= 1:
        sbar.grid_remove()
    else:
        sbar.grid()
    sbar.set(first, last)


if __name__ == '__main__':
    test_table_frame('small')
