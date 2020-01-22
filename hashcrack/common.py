
import os
import tempfile

class NamedTemporaryFile:
    def __init__(self, data=None, **kwargs):
        """Same as tempfile.NamedTemporaryFile, except closes the handle so that it works with Windows."""
        self.kwargs = kwargs
        self.kwargs['delete'] = False

        self._tempfile = tempfile.NamedTemporaryFile(**self.kwargs)
        
        if data is not None:
            self.file.write(data)

        self.close()

    def close(self):
        return self._tempfile.close()

    @property
    def file(self):
        return self._tempfile.file

    @property
    def name(self):
        return self._tempfile.name

    def __enter__(self):
        return self.name

    def __exit__(self, *args):
        os.unlink(self.name)
