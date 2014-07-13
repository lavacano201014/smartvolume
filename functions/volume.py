@ArgumentFunction(name="up",description="Adjust volume up.")
def volume_up(amount=None):
    if amount == None:
        PLACEHOLDER_get_value_from_config(and_fastly)

    PLACEHOLDER_adjust_volume(amount)

@ArgumentFunction(name="down",description="Adjust volume down.")
def volume_down(amount=None):
    if amount == None:
        PLACEHOLDER_get_value_from_config(and_fastly)

    PLACEHOLDER_adjust_volume(amount)

