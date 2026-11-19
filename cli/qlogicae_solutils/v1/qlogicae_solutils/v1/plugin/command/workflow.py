__all__ = (
    "export"
)

_data = None


from qlogicae_cor.v3.library.value_cache_storage_manager import (
    ValueCacheStorageManager
)
from qlogicae_cor.v3.library.script_process_manager import (
    ScriptProcessManager
)
from qlogicae_cliq.v1.library.cli_command_manager import (
    CliCommandManager
)
_ValueCacheStorageManager = (
    ValueCacheStorageManager()
)
_CliCommandManager = (
    CliCommandManager()
)
_ScriptProcessManager = (
    ScriptProcessManager()
)


def run_workflow_run_command(arguments):
    selections = (
        (getattr(arguments, "selections", tuple())
        if not isinstance(arguments, tuple)
        else arguments.get("selections", tuple())) or tuple()
    )

    if not selections:
        return True


    workflow_selections = (
        _ValueCacheStorageManager
            .get_singleton()
            .get_one_item(
                keys=("qlogicae", "solutils", "v1", "workflow", "selection")
            )
    )

    for selection in selections:
        if not selection:
            continue
    
        if selection not in workflow_selections:
            continue

        workflow_selection_data = (
            workflow_selections
                .get(
                    selection,
                    {}
                ) or {}
        )

        run_workflow(
            workflow_selection_data
        )    

    return True



def run_workflow(data):
    if not data:
        return True

    workflow_jobs = (
        data.get(
            "jobs",
            ()
        ) or ()
    )
    workflow_selections = (
        _ValueCacheStorageManager
            .get_singleton()
            .get_one_item(
                keys=("qlogicae", "solutils", "v1", "workflow", "selection")
            )
    )
    cli_command_collection = (
        _CliCommandManager
            .get_singleton()
            .command_collection
    )

    if not workflow_jobs:
        return True

    result = True
    for workflow_job in workflow_jobs:
        if not workflow_job:
            continue

        workflow_job_run = (
            workflow_job
                .get(
                    "run",
                    ""
                ) or ""
        )
        if not workflow_job_run:
            continue

        if callable(workflow_job_run):
            workflow_job_arguments = (
                workflow_job
                    .get(
                        "argument",
                        {}
                    ) or {}
            )

            workflow_job_args = (
                workflow_job_arguments
                    .get(
                        "args",
                        ()
                    ) or ()
            )
            workflow_job_kwargs = (
                workflow_job_arguments
                    .get(
                        "kwargs",
                        {}
                    ) or {}
            )

            temp_result = workflow_job_run(
                *workflow_job_args,
                **workflow_job_kwargs,
            )
            if temp_result is not None:
                result = (
                    temp_result and result
                )

        elif workflow_job_run in cli_command_collection:
            cli_command = (
                cli_command_collection.get(
                    workflow_job_run,
                    None  
                ) or None
            )
            if not cli_command:
                continue

            workflow_job_arguments = (
                workflow_job
                    .get(
                        "argument",
                        {}
                    ) or {}
            )

            result = cli_command(
                workflow_job_arguments
            ) and result


        elif workflow_job_run in workflow_selections:
            result = run_workflow(
                workflow_selections.get(
                    workflow_job_run,
                    {}
                ) or {}
            ) and result

        else:
            result = (
                _ScriptProcessManager
                    .get_singleton()
                    .execute_command(
                        workflow_job_run,
                    ) and result
            )

        if not result:
            return False


    return result


def run_workflow_list_command(arguments):
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


def print_message_1():
    print("print_message_1")


def print_message_2(*args):
    print(args)

    return True


def print_message_3(**kwargs):
    print(kwargs)

    return True


def print_message_4(*args, **kwargs):
    print(args, kwargs)

    return True



def _allocate():
    global _allocate
    global _data

    _data = {
        "object_merge": {
            "level": 1
        },
        "qlogicae": {
            "solutils": {
                "v1": {
                    "workflow": {
                        "selection": {
                            "sub-workflow": {
                                "jobs": [
                                    {
                                        "run": "echo 'sub workflow'",
                                    },
                                ]
                            },
                            "main-workflow": {
                                "jobs": [
                                    {
                                        "run": "echo 'main workflow'",
                                    },
                                    {
                                        "run": "sub-workflow",
                                    },
                                    {
                                        "run": "about-show-version",
                                    },
                                    {
                                        "run": print_message_1,
                                    },
                                    {
                                        "run": print_message_2,
                                        "argument": {
                                            "args": (
                                                "Hello",
                                            ),
                                        }
                                    },
                                    {
                                        "run": print_message_3,
                                        "argument": {
                                            "kwargs": {
                                                "text": "World"
                                            }
                                        }
                                    },
                                    {
                                        "run": print_message_4,
                                        "argument": {
                                            "args": (
                                                "Hello",
                                            ),
                                            "kwargs": {
                                                "text": "World"
                                            }
                                        }
                                    },
                                ]
                            },
                        }
                    }
                }
            },
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
                                                run_workflow_run_command
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
                                                run_workflow_list_command
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

    _allocate = lambda: None


def export():
    if _data is None:
        _allocate()

    return _data

