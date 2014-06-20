import svcore_except, svcore_config
import subprocess

configuration = svcore_config.get_module_configuration("vol", "alsa")

if not configuration:
    configuration = {}
    configuration["scontrol"] = "'Master',0"

def should_adjust_volume():
    return True

def adjust_volume(direction, amount):
    volamount = amount + "%" + direction
    result = subprocess.call(["amixer", "sset", configuration["scontrol"], volamount)
    if result > 0:
        return False
    else:
        return True
