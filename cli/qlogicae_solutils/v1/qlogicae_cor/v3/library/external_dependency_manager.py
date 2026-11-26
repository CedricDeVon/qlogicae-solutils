__all__ = (
    "ExternalDependencyManager",
)

_ImportTarget = None
_ExternalDependencyManager = None

def _allocate():
    global _allocate    
    global _ExternalDependencyManager        

    from .abstract_manager import AbstractManager

    class __ExternalDependencyManager(AbstractManager()):
        __slots__ = (
            "_import_targets",
            "_is_pre_allocated",
        )

        def __init__(self):
            self.construct()

        def __exit__(self, exc_type, exc_value, traceback):
            self.shutdown()

        @property
        def is_pre_allocated(self):
            return self._is_pre_allocated

        @is_pre_allocated.setter
        def is_pre_allocated(self, value):
            if not isinstance(value, bool):
                raise TypeError("")

            self._is_pre_allocated = value

        @property
        def import_targets(self):
            return self._import_targets

        @import_targets.setter
        def import_targets(self, value):
            if not isinstance(value, dict) or not value:
                raise TypeError("")

            for name, target in value.items():
                if not isinstance(name, str) or not name:
                    raise TypeError("")

                if not isinstance(target, _ImportTarget):
                    raise TypeError("")

            self._import_targets = value

        def construct(self):
            global _ImportTarget

            if not _ImportTarget:
                from qlogicae_cor.v3.library.import_target import (
                    ImportTarget
                )

                _ImportTarget = (
                    ImportTarget()
                )

            self._import_targets = {}
            self._is_pre_allocated = False

            return True

        def setup(self, kwargs):
            if not isinstance(kwargs, (dict)):
                raise TypeError("")

            import_targets = kwargs.get("import_targets", ())

            if not isinstance(import_targets, (tuple, list)):
                raise TypeError("")

            is_pre_allocated = kwargs.get(
                "is_pre_allocated",
                self._is_pre_allocated,
            )

            if not isinstance(is_pre_allocated, bool):
                raise TypeError("")

            staged_targets = {}

            for target in import_targets:
                if not isinstance(target, dict) or not target:
                    raise TypeError("")

            try:
                for target_kwargs in import_targets:
                    target_kwargs = dict(target_kwargs)
                    target_kwargs["is_pre_allocated"] = is_pre_allocated

                    target = _ImportTarget(target_kwargs)

                    if target.name not in self._import_targets:
                        staged_targets.setdefault(target.name, target)
                    else:
                        target.deallocate()

            except Exception:
                for target in staged_targets.values():
                    target.deallocate()

                raise

            self._import_targets.update(staged_targets)
            self._is_pre_allocated = is_pre_allocated

            return True

        def shutdown(self):
            self.clear_modules()
            return True

        def import_modules(
            self,
            targets
        ):
            if not isinstance(targets, (tuple, list)):
                raise TypeError("")

            for target in targets:
                if not target or not isinstance(target, (dict)):
                    raise TypeError("")

                self.import_module(
                    **target
                )

            return True

        def import_module(
            self,
            **kwargs,
        ):
            if not isinstance(kwargs, (dict)) or not kwargs:
                raise TypeError("")

            target_key = (
                (kwargs.get("name", "") or "")
                if "name" in kwargs
                else (kwargs.get("path", "") or "")
            )
            if not isinstance(target_key, (str)):
                raise TypeError("")

            import_target = None
            if target_key not in self._import_targets:
                kwargs["is_pre_allocated"] = (
                    self._is_pre_allocated
                )

                import_target = _ImportTarget(
                    kwargs
                )
                if not import_target:
                    raise TypeError("")

                self._import_targets[target_key] = (
                    import_target
                )

            else:
                import_target = (
                    self._import_targets[target_key]
                )

            import_target_allocate = (
                getattr(
                    import_target,
                    "allocate",
                    None
                ) or None
            )

            return (
                import_target_allocate
            )

        def pre_load_modules(self):
            for _key, import_target in self._import_targets.items():
                import_target.pre_allocate()

            return True

        def unload_modules(
            self,
            names,
        ):
            if not isinstance(names, (tuple, list)):
                raise TypeError("")

            for name in names:
                if not name or not isinstance(name, (str)):
                    raise TypeError("")

                self.unload_module(
                    name
                )

            return True

        def unload_module(
            self,
            name,
        ):
            if not name or not isinstance(name, (str)):
                raise TypeError("")

            if name not in self._import_targets:
                raise TypeError("")

            self._import_targets[name].deallocate()

            del self._import_targets[name]

            return True

        def clear_modules(
            self,
        ):
            if not len(self._import_targets):
                return True

            self.unload_modules(
                tuple(self._import_targets.keys())
            )

            return True


    _ExternalDependencyManager = __ExternalDependencyManager
    _allocate = lambda: None


def ExternalDependencyManager():
    if _ExternalDependencyManager is None:
        _allocate()

    return _ExternalDependencyManager

