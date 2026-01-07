class GHWrapperError(Exception):
    """Base exception for GH Wrapper"""
    pass

class GHCommandError(GHWrapperError):
    """Raised when a GH CLI command fails"""
    pass

class GHNotInstalledError(GHWrapperError):
    """Raised when GH CLI is not installed"""
    pass
