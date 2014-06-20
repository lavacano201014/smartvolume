import svcore_except
import svcore_config

try:
    import mpd
except ImportError:
    raise svcore_except.SVDependencyError("python-mpd2 (https://github.com/Mic92/python-mpd2)")

try:
    configuration = svcore_config.get_module_configuration("vol", "mpdpy")

    try:
        # Port should be an integer
        configuration["port"] = int(configuration["port"])
    except ValueError:
        # Though the user might be an idiot and put something goofy in, we'll just use 6600 and bitch about it
        print("bad mpd port, using 6600")
except svcore_except.SVMissingConfigError:
    # Normally we'd throw a fit, but mpd defaults are straightforward and people rarely use anything else
    configuration = {}
    configuration["host"] = "localhost"
    configuration["port"] = 6600

mpdcli = mpd.MPDClient()

def should_adjust_volume():
    try:
        mpdcli.connect(configuration["host"], configuration["port"])
        mpdstatus = mpdcli.status()
        if mpdstatus["state"] == "play":
            return True
        else:
            return False
    except mpd.ConnectionError as exc:
        if str(exc) == "Already connected":
            pass # Nothing to worry about
        else:
            return False
    except:
        return False # Not connected for some reason, just return false

def adjust_volume(direction, amount):
    # We need to get the initial volume first
    try:
        mpdstatus = mpdcli.status() # Should probably make this global, oh well
        curvolume = int(mpdstatus["volume"])

        if direction == "+":
            curvolume += amount
        elif direction == "-":
            curvolume -= amount

        mpdcli.setvol(curvolume)

        return True
    except:
        return False
