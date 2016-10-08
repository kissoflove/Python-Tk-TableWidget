Python-Tk-TableWidget
====================================

Python-Tk-TableWidget is a Python 3 Tk widget for building and presenting data in a flexible, powerful way. It supports standard table features, like headers, columns, rows, and scrolling/resizing.

The table was designed to handle thousands of rows/columns of data without sacrificing performance. Scrolling smoothly is a first-class goal of Python-Tk-TableWidget and it's architected in a way to allow for flexibility and extensibility.

Features of Python-Tk-TableWidget:
* Fixed headers
* Performant scrolling/resizing
* Handling huge amounts of data only limited by memory
* Column/row resizing
* Customizable styling - font/align/color/size
* Key-binding for easy navigation
* Jumping to a row or column

Getting started
---------------

### Basic Example

```python
    root = tk.Tk()
    table = TableFrame(root)
    
    table.set_data(large_data, data_rows=2000, data_cols=2000, offset_x=50, offset_y=40)
    
    table.set_table_default(bg='#ffffff', fg='#000000')
    table.set_row_default(justify="center", fg="#0000ff", bg='#00ffff')
    table.set_col_default(justify="center", fg="#0000ff", bg='#00ffff')

    table.col_header.set_col_defaults(56, width=12)
    
    table.table.set_data_attrs(45, 54, fg="#ff0000")
    table.table.set_data_attrs(45, 55, fg="#00ff00")
    table.table.set_data_attrs(45, 56, fg="#0000ff")
    table.table.set_data_value(45, 56, "testtesttesttesttest")
    
    root.mainloop()
```

Contributions
------------

Use [GitHub issues](https://github.com/michaelben/Python-Tk-TableWidget/issues) for requests.

Changelog
---------

Changes are tracked as [GitHub releases](https://github.com/michaelben/Python-Tk-TableWidget/releases).

Todos
-----
* Customize Entry Wiget to accommodate multilines and font/size change. Entry Widget only for one line and does not contain font change. Text Widget is too heavy and not compatible with Entry Widget.
* Fixed and grouped columns
* layout reflow
* sorting/filting
* import/export different formats

License
-------

MIT-license
