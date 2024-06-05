import re

enum_class_definition = """
public enum SampleEnum {
    VALUE1,
    VALUE2,
    VALUE3,
    SOME_FIELD(123),
    ANOTHER_FIELD("example");

    private int exampleField;
    private String anotherExample;

    public int getExampleField() {
        return exampleField;
    }

    SampleEnum(int exampleField) {
        this.exampleField = exampleField;
    }

    SampleEnum(String anotherExample) {
        this.anotherExample = anotherExample;
    }
}
"""

class_name_pattern = r"\benum\s+([A-Za-z_]\w*)"

# find class name
class_name_match = re.search(class_name_pattern, enum_class_definition)
if class_name_match:
    class_name = class_name_match.group(1)
else:
    class_name = None

enum_member_pattern = r"^\s*(\w+)\s*(?:\(([^)]*)\))?\s*(?:,|;)?\s*$"

enum_members = []
inside_enum = False

# extract members
for line in enum_class_definition.split("\n"):
    line = line.strip()

    if "{" in line:
        inside_enum = True
    if "}" in line:
        inside_enum = False

    if inside_enum and line and not line.startswith("public") and not line.startswith("private"):
        match = re.match(enum_member_pattern, line)

        if match:
            enum_member = match.group(1)
            enum_members.append(enum_member)


print(f"class {class_name}(enum.Enum):")

for idx, member in enumerate(enum_members):
    print(f"    {member} = {idx}")
