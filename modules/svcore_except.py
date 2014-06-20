class SVCoreError(Exception):
    """Base exception, to determine if the exception is something directly related to the program."""
    pass

class SVDependencyError(SVCoreError):
    """Exception called if a SV module has a missing dependency"""
    def __init__(self, missing_deps):
        self.value = str(missing_deps)

class SVMissingConfigError(SVCoreError):
    """Exception called if SV (or a module) is missing an important config file."""
    def __init__(self, missing_config):
        self.value = str(missing_config)
