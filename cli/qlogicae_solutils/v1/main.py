
def main():
    from qlogicae_cor.v3.library.build_plugin_manager import BuildPluginManager
    from qlogicae_cor.v3.library.command_plugin_manager import CommandPluginManager
    from qlogicae_cor.v3.library.console_log_plugin_manager import (
        ConsoleLogPluginManager,
    )
    from qlogicae_cor.v3.library.console_navigation_plugin_manager import (
        ConsoleNavigationPluginManager,
    )
    from qlogicae_cor.v3.library.file_log_plugin_manager import (
        FileLogPluginManager,
    )
    from qlogicae_cor.v3.library.filesystem_compression_plugin_manager import (
        FilesystemCompressionPluginManager,
    )
    from qlogicae_cor.v3.library.filesystem_metadata_plugin_manager import (
        FilesystemMetadataPluginManager,
    )
    from qlogicae_cor.v3.library.filesystem_plugin_manager import (
        FilesystemPluginManager,
    )
    from qlogicae_cor.v3.library.hardware_plugin_manager import HardwarePluginManager
    from qlogicae_cor.v3.library.json_io_plugin_manager import JsonIoPluginManager
    from qlogicae_cor.v3.library.macros_plugin_manager import MacrosPluginManager
    from qlogicae_cor.v3.library.persistent_cache_storage_plugin_manager import (
        PersistentCacheStoragePluginManager,
    )
    from qlogicae_cor.v3.library.placeholder_plugin_manager import (
        PlaceholderPluginManager,
    )
    from qlogicae_cor.v3.library.plugin_manager import PluginManager
    from qlogicae_cor.v3.library.script_process_plugin_manager import (
        ScriptProcessPluginManager,
    )
    from qlogicae_cor.v3.library.text_encoding_plugin_manager import (
        TextEncodingPluginManager,
    )
    from qlogicae_cor.v3.library.text_io_plugin_manager import TextIoPluginManager
    from qlogicae_cor.v3.library.time_zone_plugin_manager import TimeZonePluginManager
    from qlogicae_cor.v3.library.timestamp_plugin_manager import TimestampPluginManager
    from qlogicae_cor.v3.library.value_cache_storage_manager import (
        ValueCacheStorageManager,
    )
    from qlogicae_cor.v3.library.workflow_plugin_manager import (
        WorkflowPluginManager,
    )

    PluginManager().read_singleton().run({
        "internal_objects": (
            HardwarePluginManager().read_singleton(),
            ConsoleNavigationPluginManager().read_singleton(),
            BuildPluginManager().read_singleton(),
            TimestampPluginManager().read_singleton(),
            TimeZonePluginManager().read_singleton(),
            PlaceholderPluginManager().read_singleton(),
            TextEncodingPluginManager().read_singleton(),
            ScriptProcessPluginManager().read_singleton(),
            MacrosPluginManager().read_singleton(),
            JsonIoPluginManager().read_singleton(),
            TextIoPluginManager().read_singleton(),
            FilesystemPluginManager().read_singleton(),
            FilesystemMetadataPluginManager().read_singleton(),
            FilesystemCompressionPluginManager().read_singleton(),
            PersistentCacheStoragePluginManager().read_singleton(),
            WorkflowPluginManager().read_singleton(),
            ConsoleLogPluginManager().read_singleton(),
            FileLogPluginManager().read_singleton(),
            CommandPluginManager().read_singleton(),
        ),
        "is_setup_enabled": False,
        "is_run_enabled": False,
        "is_shutdown_enabled": False,
    })

    ValueCacheStorageManager().read_singleton().display_all_data()
    # for item in (
    #     ExternalDependencyManager()
    #         .read_singleton()
    #         .import_targets
    # ):
    #     print(item)


if __name__ == "__main__":
    raise SystemExit(main())



