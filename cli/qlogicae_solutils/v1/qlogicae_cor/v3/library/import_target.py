__all__ = (
    "ImportTarget",
)

_importlib = None
_ImportTarget = None

def _allocate():
    global _allocate
    global _importlib
    global _ImportTarget
    
    import importlib

    _importlib = (
        importlib
    )
        
    class __ImportTarget:
        __slots__ = (
            "_name",
            "_path",
            "_member",
            "_package",
            "_is_package",
            "_is_optional",
            "_allocated_module",
            "_is_pre_allocated",
            "_is_member_callable",
        )

        def __init__(self, kwargs):
            self.construct(kwargs)

        def __enter__(self):
            self.allocate()
            return self

        def __exit__(self, exc_type, exc_value, traceback):
            self.shutdown()

        @property
        def name(self):
            return self._name

        @name.setter
        def name(self, value):
            if not value or not isinstance(value, str):
                raise TypeError("")

            self._name = value

        @property
        def path(self):
            return self._path

        @path.setter
        def path(self, value):
            if not value or not isinstance(value, str):
                raise TypeError("")

            self._path = value

        @property
        def package(self):
            return self._package

        @package.setter
        def package(self, value):
            if value is not None and not isinstance(value, str):
                raise TypeError("")

            self._package = value or None

        @property
        def is_optional(self):
            return self._is_optional

        @is_optional.setter
        def is_optional(self, value):
            if not isinstance(value, bool):
                raise TypeError("")

            self._is_package = value

        @property
        def is_package(self):
            return self._is_package

        @is_package.setter
        def is_package(self, value):
            if not isinstance(value, bool):
                raise TypeError("")

            self._is_package = value

        @property
        def is_member_callable(self):
            return self._is_member_callable

        @is_member_callable.setter
        def is_member_callable(self, value):
            if not isinstance(value, bool):
                raise TypeError("")

            self._is_member_callable = value

        @property
        def member(self):
            return self._member

        @member.setter
        def member(self, value):
            if value is not None and not isinstance(value, str):
                raise TypeError("")

            self._member = value or None

        @property
        def allocated_module(self):
            return self._allocated_module

        @allocated_module.setter
        def allocated_module(self, value):
            self._allocated_module = value

        @property
        def is_pre_allocated(self):
            return self._is_pre_allocated

        @is_pre_allocated.setter
        def is_pre_allocated(self, value):
            if not isinstance(value, bool):
                raise TypeError("")

            self._is_pre_allocated = value

        def construct(self, kwargs):
            if not isinstance(kwargs, dict) or not kwargs:
                raise TypeError("")

            path = kwargs.get("path")

            if not isinstance(path, str) or not path:
                raise TypeError("")

            self._path = path

            name = kwargs.get("name")

            if name is not None and not isinstance(name, str):
                raise TypeError("")

            self._name = name or path

            package = kwargs.get("package")

            if package is not None and not isinstance(package, str):
                raise TypeError("")

            self._package = package or None

            is_optional = kwargs.get("is_optional", False)

            if not isinstance(is_optional, bool):
                raise TypeError("")

            is_package = kwargs.get("is_package", False)

            if not isinstance(is_package, bool):
                raise TypeError("")

            is_pre_allocated = kwargs.get("is_pre_allocated", False)

            if not isinstance(is_pre_allocated, bool):
                raise TypeError("")

            member = kwargs.get("member")

            if member is not None and not isinstance(member, str):
                raise TypeError("")

            is_member_callable = kwargs.get("is_member_callable", False)

            if not isinstance(is_member_callable, bool):
                raise TypeError("")

            self._member = member or None
            self._is_package = is_package
            self._is_optional = is_optional
            self._is_member_callable = is_member_callable
            self._is_pre_allocated = is_pre_allocated
            self._allocated_module = None

            if self._is_pre_allocated:
                self.allocate()

            return True

        def setup(self, kwargs):
            if not kwargs:
                return True
                
            return True

        def shutdown(self):
            result = self.deallocate()
            return result

        def allocate(self):
            if self._allocated_module is not None:
                return self._allocated_module

            try:            
                if self._package:
                    allocated_module = _importlib.import_module(
                        self._path,
                        package=self._package,
                    )
                else:
                    allocated_module = _importlib.import_module(self._path)

                if self._is_package and not hasattr(allocated_module, "__path__"):
                    raise TypeError("")

                if self._member:
                    for name in self._member.split("."):
                        if not name:
                            continue

                        allocated_module = getattr(allocated_module, name)

                if self._is_member_callable:
                    self._allocated_module = allocated_module()
                else:
                    self._allocated_module = allocated_module

            except Exception as error:
                if self._is_optional:
                   self._allocated_module = {}

                else:
                    raise Exception("")
                    
            return self._allocated_module


        def pre_allocate(self):
            if self._allocated_module is None:
                self.allocate()

            return self._allocated_module

        def deallocate(self):
            self._allocated_module = None
            return self._allocated_module

        def reallocate(self):
            if self._allocated_module is not None:
                self.deallocate()

            self.allocate()
            return self._allocated_module


    _ImportTarget = __ImportTarget
    _allocate = lambda: None


def ImportTarget():
    if _ImportTarget is None:
        _allocate()

    return _ImportTarget

