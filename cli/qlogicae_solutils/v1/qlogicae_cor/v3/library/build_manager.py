__all__ = (
    "BuildManager",
)

_BuildManager = None


def _allocate():
    global _allocate
    global _BuildManager

    class __BuildManager:
        __slots__ = (
            "_collection"
        )

        _singleton = None

        def __init__(self):
            self.construct()

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_value, traceback):
            self.shutdown()

        @property
        def collection(self):
            return self._collection

        @collection.setter
        def collection(self, value):
            if not isinstance(value, dict):
                raise TypeError("")

            self._collection = (
                self.setup_write_all_items_kwargs({})
            )

        @classmethod
        def get_singleton(cls):
            if cls._singleton is None:
                cls._singleton = cls()

            return cls._singleton

        def construct(self):
            self._collection = (
                self.setup_write_all_items_kwargs({})
            )

            return True

        def setup(self, **kwargs):
            if not kwargs:
                return True
                
            return True

        def shutdown(self):
            return True

        def read_one_item(self, key):
            if not isinstance(key, (str)):
                raise TypeError("")

            if key not in self._collection:
                raise ValueError("")

            return (
                self._collection.get(
                    key,
                    ""
                ) or ""
            )

        def read_all_items(self):
            return (
                self._collection
            )

        def write_one_item(self, key, value):
            if not isinstance(key, (str)):
                raise TypeError("")

            self._collection[key] = value

            return True

        def write_all_items(self, value):
            if not isinstance(value, dict):
                raise TypeError("")

            self._collection = (
                self.setup_write_all_items_kwargs(
                    value
                )
            )

            return True

        def remove_one_item(self, key):
            if not isinstance(key, (str)):
                raise TypeError("")

            if key not in self._collection:
                raise ValueError("")

            del self._collection[key]

            return True

        def remove_all_items(self):
            self._collection = {}

            return True
        
        def setup_write_all_items_kwargs(self, kwargs):
            if not isinstance(value, dict):
                raise TypeError("")

            if "company_name" not in kwargs:
                kwargs["company_name"] = ""

            if "project_name" not in kwargs:
                kwargs["project_name"] = ""

            if "project_description" not in kwargs:
                kwargs["project_description"] = ""

            if "brand_base_name" not in kwargs:
                kwargs["brand_base_name"] = ""

            if "brand_source_name" not in kwargs:
                kwargs["brand_source_name"] = ""


            if "current_version_label" not in kwargs:
                kwargs["current_version_label"] = ""

            if "current_active_major_version_label" not in kwargs:
                kwargs["current_active_major_version_label"] = ""

            return kwargs


    _BuildManager = __BuildManager
    _allocate = lambda: None


def BuildManager():
    if _BuildManager is None:
        _allocate()

    return _BuildManager



# if "is_runtime_checkpoint_enabled" not in kwargs:
#     kwargs["is_runtime_checkpoint_enabled"] = True

# if "is_runtime_checkpoint_logging_enabled" not in kwargs:
#     kwargs["is_runtime_checkpoint_logging_enabled"] = False

# if "is_runtime_checkpoint_error_handling_enabled" not in kwargs:
#     kwargs["is_runtime_checkpoint_error_handling_enabled"] = True


# if "error_message" not in kwargs:
#     kwargs["error_message"] = "something went wrong"

# def handle_runtime_checkpoint(self, condition):
#     is_runtime_checkpoint_enabled = (
#         self._build_manager.read_one_item(
#             "is_runtime_checkpoint_enabled"
#         )
#     )

#     if not is_runtime_checkpoint_enabled:
#         return condition

#     is_runtime_checkpoint_error_handling_enabled = (
#         self._build_manager.read_one_item(
#             "is_runtime_checkpoint_error_handling_enabled"
#         )
#     )
#     if is_runtime_checkpoint_error_handling_enabled:
#         if not condition:
#             is_runtime_checkpoint_error_handling_enabled = (
#                 self._build_manager.read_one_item(
#                     "is_runtime_checkpoint_error_handling_enabled"
#                 )
#             )    

#     return condition

# if not isinstance(kwargs, (dict)):
#     raise ValueError("")
