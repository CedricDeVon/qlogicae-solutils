__all__ = (
    "ObjectMergeManager",
)

_ObjectMergeManager = None
_ExternalDependencyManager = None

_copy = None


def _allocate():
    global _allocate
    global _ObjectMergeManager

    class __ObjectMergeManager:
        _singleton = None

        def __init__(self):
            self.construct()

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_value, traceback):
            self.shutdown()

        @classmethod
        def read_singleton(cls):
            if cls._singleton is None:
                cls._singleton = cls()

            return cls._singleton

        def construct(self):
            global _ExternalDependencyManager
            
            global _copy

            from .external_dependency_manager import ExternalDependencyManager

            _ExternalDependencyManager = (
                ExternalDependencyManager()
            )
            _copy = (
                _ExternalDependencyManager().read_singleton()
                    .import_module(
                        path="copy"
                    )
            )

            return True

        def setup(self, kwargs):
            if not isinstance(kwargs, (dict)):
                return True

            return True

        def shutdown(self):
            return True

        def deep_merge(
            self,
            left_object,
            right_object,
        ):
            if not left_object:
                return _copy().deepcopy(right_object)

            if not right_object:
                return _copy().deepcopy(left_object)

            if isinstance(left_object, dict) and isinstance(right_object, dict):
                result = _copy().deepcopy(left_object)

                for key, value in right_object.items():
                    if key in result:
                        result[key] = self.deep_merge(
                            result[key],
                            value,
                        )
                    else:
                        result[key] = _copy().deepcopy(value)

                return result

            if isinstance(left_object, list) and isinstance(right_object, list):
                return _copy().deepcopy(left_object) + _copy().deepcopy(right_object)

            return _copy().deepcopy(right_object)

        def deep_merge_fragments(
            self,
            left_object,
            right_object,
        ):
            if not left_object:
                return _copy().deepcopy(right_object)

            if not right_object:
                return _copy().deepcopy(left_object)

            if isinstance(left_object, dict) and isinstance(right_object, dict):
                result = _copy().deepcopy(left_object)

                for key, value in right_object.items():
                    if key in result:
                        result[key] = self.deep_merge_fragments(
                            result[key],
                            value,
                        )
                    else:
                        result[key] = _copy().deepcopy(value)

                return result

            if isinstance(left_object, list) and isinstance(right_object, list):
                return _copy().deepcopy(right_object)

            return _copy().deepcopy(right_object)


    _ObjectMergeManager = __ObjectMergeManager
    _allocate = lambda: None


def ObjectMergeManager():
    if not _ObjectMergeManager:
        _allocate()

    return _ObjectMergeManager


# ObjectMergeManager()
