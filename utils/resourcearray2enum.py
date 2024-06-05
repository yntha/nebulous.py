import re
import sys
from tkinter import *
from tkinter.scrolledtext import ScrolledText


def extract_array_data():
    java_array_definition = st.get(1.0, END)
    array_pattern = r"public\s+static\s+final\s+int\[\]\s+(\w+)\s*=\s*\{([^}]*)\};"

    # find array name and elements
    array_match = re.search(array_pattern, java_array_definition)
    if array_match:
        array_name = array_match.group(1)
        array_elements = array_match.group(2).split(",")
        array_elements = [elem.strip() for elem in array_elements]
    else:
        array_name = None
        array_elements = []

    # generate enum class
    python_enum_class = f"class {array_name}(enum.Enum):\n"

    for idx, element in enumerate(array_elements):
        element_name = element.split(".")[-1].upper()
        python_enum_class += f"    {element_name} = 0x{idx:02X}\n"

    # print to stdout n exit
    print(python_enum_class)
    sys.exit()


mainwin = Tk()
Label(mainwin, text="Enter Java Array of Resource IDs:").grid(row=0, column=0)
st = ScrolledText(mainwin, height=20, width=60)
st.grid(row=1, column=0, columnspan=3)

Button(mainwin, text="Extract Data", command=extract_array_data).grid(row=2, column=0, sticky="EW")
Button(mainwin, text="Exit", command=sys.exit).grid(row=2, column=1, columnspan=2, sticky="EW")

mainwin.mainloop()
