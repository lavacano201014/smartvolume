from os.path import dirname, realpath
from os import environ

import svcore_except

globaldir = dirname(realpath(__file__)) + "/config/"

def _parse_configuration_file(filename):
    configuration = {}
    file_parsed = False
    try:
        global_file = open(globaldir + filename) # global file is wherever the script is installed
        for line in global_file:
            # comments shall start with #
            if not line[0] == "#":
                # split lines on the = character
                # example config line: "modules = mpd alsa"
                line_split = line.split("=")
                # use strip on the keys and values = ignore leading/trailing whitespace, also makes the space between = and the things they separate optional
                # people can make their config files as pretty as they want, idgaf
                configuration[line_split[0].strip()] = line_split[1].strip()
        global_file.close()
        file_parsed = True
    except IOError:
        print("Warn: global configuration file %s missing" % filename)

    try:
        local_file = open(environ["HOME"] + "/.config/smartvolume/" + filename)
        for line in local_file:
            # same as before except with local files in ~/.config (useful in case some distro package manager installs to /usr/share)
            # split lines on the = character
            # example config line: "modules = mpd alsa"
            line_split = line.split("=")
            # use strip on the keys and values = ignore leading/trailing whitespace, also makes the space between = and the things they separate optional
            # people can make their config files as pretty as they want, idgaf
            configuration[line_split[0].strip()] = line_split[1].strip()
        local_file.close()
        file_parsed = True
    except IOError:
        pass # Probably not needed, no point spamming console
    
    if file_parsed:
        return configuration
    else:
        return False

def get_global_configuration():
    configuration = _parse_configuration_file("config")
    if not configuration: # uh global config is pretty important
        raise svcore_except.SVMissingConfigError
    
    # the modules lines are pretty special lines
    # instead of just a string it should really be a list
    # first, volume modules
    volmodules_line = configuration["volmodules"]
    volmodules_list = volmodules_line.split(" ")
    configuration["volmodules"] = volmodules_list

    # TODO: in the future i intend to do other types of modules (eyecandy modules, for instance)
    # right this second just volume control modules will do

    return configuration

def get_module_configuration(modtype, configname):
    if modtype == "vol":
        filename = "modules/vol/" + configname
    else:
        return False # unknown type

    if "../" in filename:
        return False # exploit

    return _parse_configuration_file(filename) # already returns false if the file doesn't exist
