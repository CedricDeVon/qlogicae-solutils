__all__ = (
    "WorkflowManager",
)

_WorkflowManager = None
_ExternalDependencyManager = None

_CommandDataManager = None
_HardwareDataManager = None
_WorkflowDataManager = None
_ScriptProcessManager = None
_ScriptProcessDelayManager = None


def _allocate():
    global _allocate
    global _WorkflowManager

    class __WorkflowManager:
        __slots__ = ()

        _singleton = None

        def __init__(self):
            self.construct()

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_value, traceback):
            self.shutdown()

        @classmethod
        def get_singleton(cls):
            if cls._singleton is None:
                cls._singleton = cls()

            return cls._singleton

        def construct(self):
            global _ExternalDependencyManager

            global _CommandDataManager
            global _HardwareDataManager
            global _WorkflowDataManager
            global _ScriptProcessManager
            global _ScriptProcessDelayManager

            from .external_dependency_manager import ExternalDependencyManager

            _ExternalDependencyManager = (
                ExternalDependencyManager()
            )
            _HardwareDataManager = (
                _ExternalDependencyManager()
                    .get_singleton()
                    .import_module(                    
                        path="qlogicae_cor.v3.library.hardware_data_manager",
                        member="HardwareDataManager",
                        is_member_callable=True,
                    )
            )
            _ScriptProcessManager = (
                _ExternalDependencyManager()
                    .get_singleton()
                    .import_module(                    
                        path="qlogicae_cor.v3.library.script_process_manager",
                        member="ScriptProcessManager",
                        is_member_callable=True,
                    )
            )
            _ScriptProcessDelayManager = (
                _ExternalDependencyManager()
                    .get_singleton()
                    .import_module(                    
                        path="qlogicae_cor.v3.library.script_process_delay_manager",
                        member="ScriptProcessDelayManager",
                        is_member_callable=True,
                    )
            )            
            _WorkflowDataManager = (
                _ExternalDependencyManager()
                    .get_singleton()
                    .import_module(                    
                        path="qlogicae_cor.v3.library.workflow_data_manager",
                        member="WorkflowDataManager",
                        is_member_callable=True,
                    )
            )
            _CommandDataManager = (
                _ExternalDependencyManager()
                    .get_singleton()
                    .import_module(                    
                        path="qlogicae_cor.v3.library.command_data_manager",
                        member="CommandDataManager",
                        is_member_callable=True,
                    )
            )

            return True

        def setup(self, kwargs):
            if not isinstance(kwargs, (dict)):
                raise TypeError("")

            return True

        def shutdown(self):
            return True

        def run_workflows(self, kwargs):
            if not isinstance(kwargs, (dict)):
                raise TypeError("")

            workflow_selection_targets = (
                kwargs.get(
                    "targets",
                    ()
                ) or ()
            )

            if not workflow_selection_targets:
                return True

            workflow_data_manager = (
                _WorkflowDataManager()
                    .get_singleton()
            )
            root_data = (
                workflow_data_manager
                    .read_all_data()
            )
            
            if not root_data:
                return True

            root_data_workflow_selection = (
                workflow_data_manager
                    .read_property(
                        root_data,
                        "selection"
                    )
            )
            if not root_data_workflow_selection:
                return True

            command_data_manager = (
                _CommandDataManager()
                    .get_singleton()
            )

            functions = (
                command_data_manager
                    .read_functions()
            )

            def run_workflow(workflow_selection_target):
                if (
                    not isinstance(workflow_selection_target, (str))
                    or not workflow_selection_target
                ):
                    raise ValueError("")

                if workflow_selection_target not in root_data_workflow_selection:
                    raise ValueError("")

                workflow_selection = (
                    root_data_workflow_selection.get(
                        workflow_selection_target,
                        {}
                    ) or {}
                )
                if not workflow_selection:
                    return True

                workflow_selection_is_enabled = (
                    workflow_data_manager
                        .read_property(
                            workflow_selection,
                            "is_enabled"
                        )
                )
                if not workflow_selection_is_enabled:
                    return True

                workflow_selection_platforms_included = (
                    workflow_data_manager
                        .read_property(
                            workflow_selection,
                            "platforms_included"
                        )
                )
                workflow_selection_platforms_excluded = (
                    workflow_data_manager
                        .read_property(
                            workflow_selection,
                            "platforms_excluded"
                        )
                )
                if (
                    workflow_selection_platforms_included or
                    workflow_selection_platforms_excluded
                ):
                    hardware_data_manager = (
                        _HardwareDataManager()
                            .get_singleton()
                    )
                    current_platform = (
                        hardware_data_manager.read_platform()
                    )

                    if (
                        workflow_selection_platforms_excluded and
                        current_platform in workflow_selection_platforms_excluded
                    ): 
                        return True

                    if (
                        workflow_selection_platforms_included and
                        current_platform not in workflow_selection_platforms_included
                    ): 
                        return True

                workflow_selection_jobs = (
                    workflow_data_manager
                        .read_property(
                            workflow_selection,
                            "jobs"
                        )
                )
                if not workflow_selection_jobs:
                    return True

                workflow_selection_is_failure_optional = (
                    workflow_data_manager
                        .read_property(
                            workflow_selection,
                            "is_failure_optional"
                        )
                )

                workflow_selection_delay = (
                    workflow_data_manager
                        .read_property(
                            workflow_selection,
                            "delay"
                        )
                )
                if workflow_selection_delay:
                    script_process_delay_manager = (
                        _ScriptProcessDelayManager()
                            .get_singleton()
                    )

                    script_process_delay_manager.delay_process(
                        workflow_selection_delay
                    )

                workflow_result = True
                for workflow_selection_job in workflow_selection_jobs:
                    if (not isinstance(workflow_selection_job, (dict))):
                        raise ValueError("")

                    workflow_selection_job_is_enabled = (
                        workflow_data_manager
                            .read_property(
                                workflow_selection_job,
                                "is_enabled"
                            )
                    )
                    if not workflow_selection_job_is_enabled:
                        continue

                    workflow_selection_job_platforms_included = (
                        workflow_data_manager
                            .read_property(
                                workflow_selection_job,
                                "platforms_included"
                            )
                    )
                    workflow_selection_job_platforms_excluded = (
                        workflow_data_manager
                            .read_property(
                                workflow_selection_job,
                                "platforms_excluded"
                            )
                    )
                    if (
                        workflow_selection_job_platforms_included or
                        workflow_selection_job_platforms_excluded
                    ):
                        hardware_data_manager = (
                            _HardwareDataManager()
                                .get_singleton()
                        )
                        current_platform (
                            hardware_data_manager.read_platform()
                        )

                        if (
                            workflow_selection_job_platforms_excluded and
                            current_platform in workflow_selection_job_platforms_excluded
                        ): 
                            return True

                        if (
                            workflow_selection_job_platforms_included and
                            current_platform not in workflow_selection_job_platforms_included
                        ): 
                            return True

                    workflow_selection_job_run = (
                        workflow_data_manager
                            .read_property(
                                workflow_selection_job,
                                "run"
                            )
                    )
                    if not workflow_selection_job_run:
                        continue
                                    
                    workflow_selection_job_is_failure_optional = (
                        workflow_data_manager
                            .read_property(
                                workflow_selection_job,
                                "is_failure_optional"
                            )
                    )
                    workflow_selection_job_delay = (
                        workflow_data_manager
                            .read_property(
                                workflow_selection_job,
                                "delay"
                            )
                    )
                    if workflow_selection_job_delay:
                        script_process_delay_manager = (
                            _ScriptProcessDelayManager()
                                .get_singleton()
                        )

                        script_process_delay_manager.delay_process(
                            workflow_selection_job_delay
                        )

                    if workflow_selection_job_run in root_data_workflow_selection:
                        workflow_result = (
                            run_workflow(workflow_selection_job_run)
                        ) and workflow_result
                
                    elif (
                        workflow_selection_job_run in functions or
                        callable(workflow_selection_job_run)
                    ):
                        workflow_selection_job_run_arguments = (
                            workflow_data_manager
                                .read_property(
                                    workflow_selection_job,
                                    "arguments"
                                )
                        )
                        workflow_selection_job_run_arguments_args = (
                            workflow_data_manager
                                .read_property(
                                    workflow_selection_job_run_arguments,
                                    "args"
                                )
                        )
                        workflow_selection_job_run_arguments_kwargs = (
                            workflow_data_manager
                                .read_property(
                                    workflow_selection_job_run_arguments,
                                    "kwargs"
                                )
                        )

                        if callable(workflow_selection_job_run):
                            workflow_result = (
                                workflow_selection_job_run(
                                    *workflow_selection_job_run_arguments_args,
                                    **workflow_selection_job_run_arguments_kwargs
                                ) and workflow_result
                            )
                        elif workflow_selection_job_run in functions:
                            command = (
                                functions.get(
                                    workflow_selection_job_run,
                                    None
                                ) or None
                            )
                            if not callable(command) or not command:
                                raise ValueError("")

                            workflow_result = (
                                command(
                                    *workflow_selection_job_run_arguments_args,
                                    **workflow_selection_job_run_arguments_kwargs
                                ) and workflow_result
                            )

                    else:                        
                        script_process_manager = (
                            _ScriptProcessManager()
                                .get_singleton()
                        )

                        workflow_selection_job_process = (
                            workflow_data_manager
                                .read_property(
                                    workflow_selection_job,
                                    "process"
                                )
                        )
                        workflow_selection_job_successful_return_codes = (
                            workflow_data_manager
                                .read_property(
                                    workflow_selection_job,
                                    "successful_return_codes"
                                )
                        )
                        workflow_selection_job_unsuccessful_return_codes = (
                            workflow_data_manager
                                .read_property(
                                    workflow_selection_job,
                                    "unsuccessful_return_codes"
                                )
                        )

                        script_process_result = (
                            script_process_manager.execute_command(
                                workflow_selection_job_run.
                                workflow_selection_job_process
                            )
                        )

                        if (
                            workflow_selection_job_successful_return_codes and
                            script_process_result not in
                                workflow_selection_job_successful_return_codes
                        ):
                            workflow_result = False

                        if (
                            workflow_selection_job_unsuccessful_return_codes and
                            script_process_result in
                                workflow_selection_job_unsuccessful_return_codes
                        ):
                            workflow_result = False

                    if (
                        not workflow_selection_is_failure_optional and
                        not workflow_selection_job_is_failure_optional and
                        not workflow_result
                    ):
                        return False

                return workflow_result


            result = True
            for workflow_selection_target in workflow_selection_targets:
                if (
                    not isinstance(workflow_selection_target, (str))
                    or not workflow_selection_target
                ):
                    raise ValueError("")

                result = run_workflow(
                    workflow_selection_target
                ) and result                  

            return result


    _WorkflowManager = __WorkflowManager
    _allocate = lambda: None


def WorkflowManager():
    if _WorkflowManager is None:
        _allocate()

    return _WorkflowManager

