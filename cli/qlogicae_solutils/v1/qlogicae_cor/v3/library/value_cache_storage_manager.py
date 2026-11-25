
__all__ = (
    "ValueCacheStorageManager",
)


_ValueCacheStorageManager = None
_ExternalDependencyManager = None


def _allocate():
    global _allocate
    global _ValueCacheStorageManager

    class __ValueCacheStorageManager:
        __slots__ = (
            "_values",
            "_defaults",
        )

        _singleton = None

        def __init__(self):
            self.construct()

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_value, traceback):
            self.shutdown()

        def construct(self):
            global _ExternalDependencyManager

            from .external_dependency_manager import ExternalDependencyManager

            _ExternalDependencyManager = ExternalDependencyManager()

            self._values = {}
            self._defaults = {}

            return True

        def setup(self, kwargs):
            values = (
                kwargs.get("values", {}) or {}
            )
            defaults = (
                kwargs.get("defaults", {}) or {}
            )

            if values is None:
                values = {}

            if defaults is None:
                defaults = {}

            if not isinstance(values, dict):
                raise ValueError("'values' must be a dictionary")

            if not isinstance(defaults, dict):
                raise ValueError("'defaults' must be a dictionary")

            self._values = values
            self._defaults = defaults

            return True

        def shutdown(self):
            return True

        @classmethod
        def read_singleton(cls):
            if cls._singleton is None:
                cls._singleton = cls()

            return cls._singleton

        @property
        def values(self):
            return self._values

        @values.setter
        def values(self, value):
            if not isinstance(value, dict):
                raise ValueError("'values' must be a dictionary")

            self._values = value

        @property
        def defaults(self):
            return self._defaults

        @defaults.setter
        def defaults(self, value):
            if not isinstance(value, dict):
                raise ValueError("'defaults' must be a dictionary")

            self._defaults = value

        def _normalize_keys(self, key_path):
            if isinstance(key_path, str):
                return (key_path,)

            if isinstance(key_path, (tuple, list)):
                if not key_path:
                    raise ValueError("'key_path' cannot be empty")

                return tuple(key_path)

            raise ValueError(
                "'key_path' must be a string, tuple, or list"
            )

        def _normalize_typename(self, typename="values"):
            if typename not in ("values", "defaults"):
                raise ValueError("")

            return typename

        def read_specified_cache(self, typename="values"):
            if not isinstance(typename, (str)) or not typename:
                raise TypeError("")
                
            typename = self._normalize_typename(typename)

            if typename == "values":
                return self._values

            return self._defaults

        def _get_item_from_cache(self, key_path, typename):
            if not isinstance(key_path, (tuple, list)):
                raise TypeError("")

            if not isinstance(typename, (str)) or not typename:
                raise TypeError("")

            cache = self.read_specified_cache(typename)

            for key in key_path:
                if isinstance(cache, dict):
                    if key not in cache:
                        return False, None

                elif isinstance(cache, (list, tuple)):
                    if not isinstance(key, int):
                        return False, None

                    if key < 0 or key >= len(cache):
                        return False, None

                else:
                    return False, None

                cache = cache[key]

            return True, cache

        def _get_item(self, key_path, typename="values"):
            if not isinstance(key_path, (tuple, list)):
                raise TypeError("")

            if not isinstance(typename, (str)) or not typename:
                raise TypeError("")

            key_path = self._normalize_keys(key_path)
            typename = self._normalize_typename(typename)

            found, item = self._get_item_from_cache(
                key_path,
                typename,
            )

            if found or typename == "defaults":
                return found, item

            return self._get_item_from_cache(
                key_path,
                "defaults",
            )

        def is_key_found(self, key_path, typename="values"):
            if not isinstance(key_path, (tuple, list)):
                raise TypeError("")

            if not isinstance(typename, (str)) or not typename:
                raise TypeError("")

            found, _ = self._get_item(
                key_path,
                typename,
            )

            return found

        def read_one_data(self, key_path, typename="values"):
            if not isinstance(key_path, (tuple, list)):
                raise TypeError("")

            if not isinstance(typename, (str)) or not typename:
                raise TypeError("")

            found, item = self._get_item(
                key_path,
                typename,
            )

            return item if found else None

        def _get_parent(
            self,
            key_path,
            typename="values",
            create_missing=True,
        ):
            if not isinstance(key_path, (tuple, list)):
                raise TypeError("")

            if not isinstance(typename, (str)) or not typename:
                raise TypeError("")

            if not isinstance(create_missing, (bool)):
                raise TypeError("")

            key_path = self._normalize_keys(key_path)
            typename = self._normalize_typename(typename)

            cache = self.read_specified_cache(typename)

            for key in key_path[:-1]:
                if isinstance(cache, dict):
                    if key not in cache:
                        if not create_missing:
                            return None, None

                        cache[key] = {}

                    elif not isinstance(cache[key], (dict, list)):
                        return None, None

                    cache = cache[key]

                elif isinstance(cache, list):
                    if not isinstance(key, int):
                        raise TypeError(
                            f"expected an index, got "
                            f"'{type(key).__name__}'"
                        )

                    if key < 0 or key >= len(cache):
                        raise IndexError(
                            f"Index '{key}' is out of range"
                        )

                    cache = cache[key]

                else:
                    return None, None

            return cache, key_path[-1]

        def write_one_data(
            self,
            key_path,
            value=None,
            typename="values",
            create_missing=True,
        ):
            if not isinstance(key_path, (tuple, list)):
                raise TypeError("")

            if not isinstance(typename, (str)) or not typename:
                raise TypeError("")

            if not isinstance(create_missing, (bool)):
                raise TypeError("")

            typename = self._normalize_typename(typename)

            parent, key = self._get_parent(
                key_path,
                typename,
                create_missing,
            )

            if parent is None:
                return False

            if isinstance(parent, dict):
                parent[key] = value

            elif isinstance(parent, list):
                if not isinstance(key, int):
                    raise TypeError(
                        f"expected an index, got "
                        f"'{type(key).__name__}'"
                    )

                if key < 0 or key >= len(parent):
                    raise IndexError(
                        f"Index '{key}' is out of range"
                    )

                parent[key] = value

            else:
                return False

            return True

        def read_all_data(self):
            return self._values or {}

        def write_all_data(self, values=None):
            value = values or {}

            if not isinstance(value, dict):
                raise TypeError(
                    "'values' must be a dictionary"
                )

            self._values = value

            return True

        def remove_one_data(self, key_path, typename="values"):
            if not isinstance(key_path, (tuple, list)):
                raise TypeError("")

            if not isinstance(typename, (str)) or not typename:
                raise TypeError("")

            typename = self._normalize_typename(typename)

            parent, key = self._get_parent(
                key_path,
                typename,
                False,
            )

            if parent is None:
                return False

            if isinstance(parent, dict):
                if key not in parent:
                    return False

                del parent[key]

            elif isinstance(parent, list):
                if not isinstance(key, int):
                    raise TypeError(
                        f"expected an index, got "
                        f"'{type(key).__name__}'"
                    )

                if key < 0 or key >= len(parent):
                    return False

                del parent[key]

            else:
                return False

            return True

        def remove_all_data(self, typename="values"):
            if not isinstance(typename, (str)) or not typename:
                raise TypeError("")

            cache = self.read_specified_cache(typename)

            cache.clear()

            return True

        def display_one_data(self, key_path, typename="values"):
            if not isinstance(key_path, (tuple, list)):
                raise TypeError("")
                
            if not isinstance(typename, (str)) or not typename:
                raise TypeError("")

            found, item = self._get_item(
                key_path,
                typename,
            )

            if not found:
                return False

            _json = (
                _ExternalDependencyManager().read_singleton()
                .import_module(path="json")
            )

            print(
                _json().dumps(
                    item,
                    indent=2,
                    sort_keys=False,
                    ensure_ascii=False,
                    default=str,
                )
            )

            return True

        def display_all_data(self, typename="values"):
            if not isinstance(typename, (str)) or not typename:
                raise TypeError("")

            cache = self.read_specified_cache(typename)

            _json = (
                _ExternalDependencyManager().read_singleton()
                .import_module(path="json")
            )

            print(
                _json().dumps(
                    cache,
                    indent=2,
                    sort_keys=False,
                    ensure_ascii=False,
                    default=str,
                )
            )

            return True

    _ValueCacheStorageManager = __ValueCacheStorageManager
    _allocate = lambda: None


def ValueCacheStorageManager():
    if _ValueCacheStorageManager is None:
        _allocate()

    return _ValueCacheStorageManager
