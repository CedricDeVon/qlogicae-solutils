# __all__ = (
#     "CliManager",
# )

# _CliManager = None
# _ExternalDependencyManager = None

# _CommandPluginManager = None
# _CommandParserManager = None


# def _allocate():
#     global _allocate
#     global _CliManager

#     class __CliManager:
#         __slots__ = (
#             "_data_path",
#         )

#         _singleton = None

#         def __init__(self):
#             self.construct()

#         def __enter__(self):
#             return self

#         def __exit__(self, exc_type, exc_value, traceback):
#             self.shutdown()

#         @classmethod
#         def get_singleton(cls):
#             if cls._singleton is None:
#                 cls._singleton = cls()

#             return cls._singleton

#         def construct(self):
#             global _ExternalDependencyManager

#             global _CommandPluginManager
#             global _CommandParserManager

#             from qlogicae_cor.v3.library.external_dependency_manager import (
#                 ExternalDependencyManager,
#             )

#             _ExternalDependencyManager = (
#                 ExternalDependencyManager()
#             )
#             _CommandPluginManager = (
#                 _ExternalDependencyManager()
#                     .get_singleton()
#                     .import_module(                    
#                         path="qlogicae_cor.v3.library.plugin_manager",
#                         member="CommandPluginManager",
#                         is_member_callable=True,
#                     )
#             )
#             _CommandParserManager = (
#                 _ExternalDependencyManager()
#                     .get_singleton()
#                     .import_module(
#                         path="qlogicae_cor.v3.library.command_parser_manager",
#                         member="CommandParserManager",
#                         is_member_callable=True,
#                     )
#             )

#             return True

#         def setup(self, **kwargs):
#             if not isinstance(kwargs, (dict)):
#                 raise ValueError("'kwargs' must be a dictionary")

#             return True

#         def shutdown(self):
#             return True


#     _CliManager = __CliManager
#     _allocate = lambda: None


# def CliManager():
#     if _CliManager is None:
#         _allocate()

#     return _CliManager

