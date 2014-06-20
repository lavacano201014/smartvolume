import re

security_warnings = ["open\(", "(import|from) importlib", "(import|from) os", "(from|import) sys", "(import|from) socket", "(from|import) urllib", "subprocess\.call\(", "Popen\(", "(from|import) subprocess"]

@ArgumentFunction(name="audit",description="Checks a module to make sure it's safe to use.",args="[<type_module>]")
def audit(module=None):
    if module:
        modules = [module]
    else:
        print("No module specified, auditing all modules loaded in config")
        print("..or at least i would if i actually got around to implementing that.")
        return 0

    for module in modules:
        try:
            with open("modules/sv" + module + ".py") as modulefile:
                current_line = 1
                for unstrippedline in modulefile:
                    line = unstrippedline.strip()
                    for regex in security_warnings:
                        if re.match("(^|[\s([])" + regex):
                            print("%s \033[1;31mSECURITY:\033[0m %s used in line %d" % module, regex, current_line)
                    current_line = current_line + 1
        except IOError:
            print("%s does not exist" % module)
