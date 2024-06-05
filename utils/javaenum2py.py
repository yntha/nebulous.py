import re
import sys
from enum import Enum
from tkinter import *
from tkinter.scrolledtext import ScrolledText


def extract_enum_data():
    enum_class_def = st.get(1.0, END)
    class_name_pattern = r"\benum\s+([A-Za-z_]\w*)"
    enum_member_pattern = r"^\s*(\w+)\s*(?:\(([^)]*)\))?\s*(?:,|;)?\s*$"

    # find class name
    class_name_match = re.search(class_name_pattern, enum_class_def)

    if class_name_match:
        class_name = class_name_match.group(1)
    else:
        class_name = None

    # extract enum members and ctor args
    enum_members = []
    inside_enum = False

    for line in enum_class_def.split("\n"):
        line = line.strip()

        if "{" in line:
            inside_enum = True
        if "}" in line:
            inside_enum = False

        if inside_enum and line and not line.startswith("public") and not line.startswith("private"):
            match = re.match(enum_member_pattern, line)

            if match:
                enum_member = match.group(1)
                constructor_args = match.group(2)

                if constructor_args:
                    args_list = [arg.strip() for arg in constructor_args.split(",")]
                    enum_members.append((enum_member, args_list))
                else:
                    enum_members.append((enum_member, None))

    # generate python enum class
    python_enum_class = f"class {class_name}(enum.Enum):\n"
    for idx, item in enumerate(enum_members):
        member, args = item

        python_enum_class += f"    {member} = {idx}"

        if args:
            python_enum_class += f"  # {', '.join(args)}\n"
        else:
            python_enum_class += "\n"

    # print to stdout and exit
    print(python_enum_class)
    sys.exit()


mainwin = Tk()
Label(mainwin, text="Enter Java Enum Class:").grid(row=0, column=0)
st = ScrolledText(mainwin, height=20, width=60)
st.grid(row=1, column=0, columnspan=3)

Button(mainwin, text="Extract Data", command=extract_enum_data).grid(row=2, column=0, sticky="EW")
Button(mainwin, text="Exit", command=sys.exit).grid(row=2, column=1, columnspan=2, sticky="EW")

mainwin.mainloop()
