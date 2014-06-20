# Example volmodule for smartvolume

# This module contains exceptions built for smartvolume.
import svcore_except

# This module contains functions to load the config files for your module.
# If you need it for whatever reason (doubtful), get_global_configuration is
# also present and does precisely what it says on the tin
import svcore_config

# Lets say you needed a module that wasn't part of the Python standard library.
try:
    import your_buddy_daves_library
except ImportError:
    # Oh dear, looks like this system doesn't have this library installed.
    # Rather than let Python have its exception and break everything,
    # you can raise a dependency error so that smartvolume knows to
    # warn the user.
    raise svcore_except.SVDependencyError("My buddy Dave's really sweet library, you can get it at his website!")
    # smartvolume will output a line to stdout similar to this:
    # [yourmod] This module failed to load because the following dependencies are missing: My buddy Dave's really sweet library, (...)

# Now let's discuss configuration.
# First, lets load your critical configuration file.
# svcore_config has a nifty function: get_module_configuration
configuration = svcore_config.get_module_configuration("vol", "example")
# With a line like this, smartvolume will first read the "global" configuration file
# that lives at ${smartvolume_install_dir}/config/<type>/<config_name>, (this, with
# smartvolume installed by some package manager, would probably resolve to something
# like /usr/share/smartvolume/config/vol/example), and then read the "local" file,
# which lives in ~/.config/smartvolume/<type>/<config_name> (above example:
# ~/.config/smartvolume/vol/example). Then, it will assemble each config setting,
# with local (~/.config) taking precedence over global (/usr/share), and return a
# standard Python dictionary (above example, you would access the option "host" with
# configuration["host"]).

# You're going to want to check to make sure that actually loaded, by the way. If
# get_module_configuration has problems reading both global and local files, instead
# of a dictionary object it will just return False.
if not configuration:
    # This is a critical config file, so we're going to raise an exception so smartvolume
    # knows what's up.
    raise svcore_except.SVMissingConfigError

    # We're also going to return 0 so we don't continue and break things even more.
    return 0

# But what if you had a second, optional configuration file?
# Pretty much the same procedure
second_configuration = svcore_config.get_module_configuration("vol", "example_extras")

if not second_configuration:
    # Since this is an optional config, we don't have to raise any exceptions.
    say_to_yourself("well, darn.", snapping_fingers=True)
    # You might want to set some defaults for this configuration, but since this
    # is an example I have plenty of right to just put something silly down instead.

# Say you needed to give special treatment to a configuration option (e.g. you want
# "port" to be an integer). You have full Python 3 available to you (though running
# smartvolume's audit function will throw security warnings for various things), so
# you'd do it the usual way
configuration["port"] = int(configuration["port"])

# Now, each volmodule needs two functions: should_adjust_volume and adjust_volume.

# should_adjust_volume is the function smartvolume runs first, and takes no arguments.
def should_adjust_volume():
    # Pretty straightforward, just return True if smartvolume should use this module
    # and False if it shouldn't.
    # Since we're an example module, we can just return True. A media player module
    # might check to see if the player is running and playing, and return False if
    # it isn't.
    return True

# adjust_volume takes two arguments: direction, a string indicating whether we're turning
# the volume up or down ("+" and "-", respectively), and amount, a percentage.
# If the thing your module adjusts doesn't think in percentages, it's up to you to make
# the conversion. Here's the formula: your_program_max*amount/100
def adjust_volume(direction, volume):
    if direction == "+":
        change_your_volume("up", amount)
    elif direction == "-":
        change_your_volume("down", amount)
