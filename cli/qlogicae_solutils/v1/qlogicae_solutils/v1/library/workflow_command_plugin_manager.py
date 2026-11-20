__all__ = (
    "WorkflowCommandPluginManager",
)

_ValueCacheStorageManager = None
_WorkflowCommandPluginManager = None
_ExternalDependencyManager = None


def _allocate():
    global _allocate
    global _WorkflowCommandPluginManager

    class __WorkflowCommandPluginManager:
        __slots__ = (
            "_plugin_exports",
        )

        _singleton = None

        def __init__(self):
            self.construct()

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_value, traceback):
            self.shutdown()

        @property
        def plugin_exports(self):
            return self._plugin_exports

        @plugin_exports.setter
        def plugin_exports(self, value):
            if not isinstance(value, dict):
                raise ValueError(
                    "'plugin_exports' must be a dictionary"
                )

            self._plugin_exports = value

        @classmethod
        def get_singleton(cls):
            if cls._singleton is None:
                cls._singleton = cls()

            return cls._singleton

        def construct(self):
            global _ExternalDependencyManager
            global _ValueCacheStorageManager

            from qlogicae_cor.v3.library.external_dependency_manager import (
                ExternalDependencyManager,
            )

            _ExternalDependencyManager = (
                ExternalDependencyManager()
            )
            _ValueCacheStorageManager = (
                _ExternalDependencyManager()
                    .get_singleton()
                    .import_module(                    
                        path="qlogicae_cor.v3.library.value_cache_storage_manager",
                        member="ValueCacheStorageManager",
                        is_member_callable=True,
                    )
            )

            self._plugin_exports = {
                "object_merge": {
                    "level": 1
                },
                "qlogicae": {
                    "cliq": {
                        "v1": {
                            "command": {
                                "options": {
                                    "commands": [
                                        {
                                            "name": "workflow",
                                            "args": (),
                                            "kwargs": { "help": "Manage workflow operations.", },
                                            "subcommands": [
                                                {
                                                    "name": "run",
                                                    "args": (),
                                                    "kwargs": { "help": "Run workflows.", },
                                                    "command_handler": (
                                                        self.run_workflow_run_command
                                                    ),
                                                    "arguments": [
                                                        {
                                                            "args": (
                                                                "--selections",
                                                                "-s"
                                                            ),
                                                            "kwargs": {
                                                                "dest": "selections",
                                                                "help": "Workflow selections.",
                                                                "required": True,
                                                                "default": (),
                                                                "type": str,
                                                                "nargs": "+",
                                                            }
                                                        }
                                                    ],
                                                },
                                                {
                                                    "name": "list",
                                                    "args": (),
                                                    "kwargs": { "help": "Show workflows.", },
                                                    "command_handler": (
                                                        self.run_workflow_list_command
                                                    ),
                                                },
                                            ],
                                        },
                                    ],
                                },
                            },
                        },
                    },            
                }
            }

            return True

        def setup(self, **kwargs):
            if not isinstance(kwargs, (dict)) or not kwargs:
                raise ValueError("'kwargs' must be a non-empty dictionary")

            return True

        def shutdown(self):
            return True

        def run_workflow_list_command(self, arguments):
            if not isinstance(arguments, object) or not arguments:
                raise ValueError("'arguments' must be defined")

            workflows = (
                _ValueCacheStorageManager
                    .get_singleton()
                    .get_one_item(
                        keys=("qlogicae", "solutils", "v1", "workflow", "selection")
                    )
            )
            for workflow in workflows:
                if not workflow:
                    continue

                print(workflow)


            return True

        def run_workflow_run_command(self, arguments):
            if not isinstance(arguments, object) or not arguments:
                raise ValueError("'arguments' must be defined")
                
            return True


    _WorkflowCommandPluginManager = __WorkflowCommandPluginManager
    _allocate = lambda: None


def WorkflowCommandPluginManager():
    if _WorkflowCommandPluginManager is None:
        _allocate()

    return _WorkflowCommandPluginManager







# def run_workflow_run_command(arguments):
#     selections = (
#         (getattr(arguments, "selections", tuple())
#         if not isinstance(arguments, tuple)
#         else arguments.get("selections", tuple())) or tuple()
#     )

#     if not selections:
#         return True


#     workflow_selections = (
#         _ValueCacheStorageManager
#             .get_singleton()
#             .get_one_item(
#                 keys=("qlogicae", "solutils", "v1", "workflow", "selection")
#             )
#     )

#     for selection in selections:
#         if not selection:
#             continue
    
#         if selection not in workflow_selections:
#             continue

#         workflow_selection_data = (
#             workflow_selections
#                 .get(
#                     selection,
#                     {}
#                 ) or {}
#         )

#         run_workflow(
#             workflow_selection_data
#         )    

#     return True



# def run_workflow(data):
#     if not data:
#         return True

#     workflow_jobs = (
#         data.get(
#             "jobs",
#             ()
#         ) or ()
#     )
#     workflow_selections = (
#         _ValueCacheStorageManager
#             .get_singleton()
#             .get_one_item(
#                 keys=("qlogicae", "solutils", "v1", "workflow", "selection")
#             )
#     )
#     cli_command_collection = (
#         _CliCommandManager
#             .get_singleton()
#             .command_collection
#     )

#     if not workflow_jobs:
#         return True

#     result = True
#     for workflow_job in workflow_jobs:
#         if not workflow_job:
#             continue

#         workflow_job_run = (
#             workflow_job
#                 .get(
#                     "run",
#                     ""
#                 ) or ""
#         )
#         if not workflow_job_run:
#             continue

#         if callable(workflow_job_run):
#             workflow_job_arguments = (
#                 workflow_job
#                     .get(
#                         "argument",
#                         {}
#                     ) or {}
#             )

#             workflow_job_args = (
#                 workflow_job_arguments
#                     .get(
#                         "args",
#                         ()
#                     ) or ()
#             )
#             workflow_job_kwargs = (
#                 workflow_job_arguments
#                     .get(
#                         "kwargs",
#                         {}
#                     ) or {}
#             )

#             temp_result = workflow_job_run(
#                 *workflow_job_args,
#                 **workflow_job_kwargs,
#             )
#             if temp_result is not None:
#                 result = (
#                     temp_result and result
#                 )

#         elif workflow_job_run in cli_command_collection:
#             cli_command = (
#                 cli_command_collection.get(
#                     workflow_job_run,
#                     None  
#                 ) or None
#             )
#             if not cli_command:
#                 continue

#             workflow_job_arguments = (
#                 workflow_job
#                     .get(
#                         "argument",
#                         {}
#                     ) or {}
#             )

#             result = cli_command(
#                 workflow_job_arguments
#             ) and result


#         elif workflow_job_run in workflow_selections:
#             result = run_workflow(
#                 workflow_selections.get(
#                     workflow_job_run,
#                     {}
#                 ) or {}
#             ) and result

#         else:
#             result = (
#                 _ScriptProcessManager
#                     .get_singleton()
#                     .execute_command(
#                         workflow_job_run,
#                     ) and result
#             )

#         if not result:
#             return False


#     return result
