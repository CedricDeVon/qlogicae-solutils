
def main():    
    from qlogicae_cor.v3.library.plugin_manager import (
        PluginManager
    )
    from qlogicae_cor.v3.library.value_cache_storage_manager import (
        ValueCacheStorageManager
    )
    from qlogicae_cor.v3.library.external_dependency_manager import (
        ExternalDependencyManager
    )


    from qlogicae_cor.v3.library.hardware_plugin_manager import (
        HardwarePluginManager
    )
    from qlogicae_cor.v3.library.console_navigation_plugin_manager import (
        ConsoleNavigationPluginManager
    )
    from qlogicae_cor.v3.library.console_navigation_manager import (
        ConsoleNavigationManager
    )
    from qlogicae_cor.v3.library.build_plugin_manager import (
        BuildPluginManager
    )
    from qlogicae_cor.v3.library.time_zone_plugin_manager import (
        TimeZonePluginManager
    )
    from qlogicae_cor.v3.library.timestamp_plugin_manager import (
        TimestampPluginManager
    )
    from qlogicae_cor.v3.library.script_process_plugin_manager import (
        ScriptProcessPluginManager
    )
    from qlogicae_cor.v3.library.placeholder_plugin_manager import (
        PlaceholderPluginManager
    )
    from qlogicae_cor.v3.library.text_encoding_plugin_manager import (
        TextEncodingPluginManager
    )
    from qlogicae_cor.v3.library.macros_plugin_manager import (
        MacrosPluginManager
    )
    from qlogicae_cor.v3.library.json_io_plugin_manager import (
        JsonIoPluginManager
    )
    from qlogicae_cor.v3.library.text_io_plugin_manager import (
        TextIoPluginManager
    )
    from qlogicae_cor.v3.library.command_plugin_manager import (
        CommandPluginManager
    )

    from qlogicae_cor.v3.library.time_zone_data_manager import (
        TimeZoneDataManager
    )

    PluginManager().get_singleton().run({
        "internal_objects": (
            HardwarePluginManager().get_singleton(),
            ConsoleNavigationPluginManager().get_singleton(),
            BuildPluginManager().get_singleton(),
            TimestampPluginManager().get_singleton(),
            TimeZonePluginManager().get_singleton(),
            PlaceholderPluginManager().get_singleton(),
            TextEncodingPluginManager().get_singleton(),
            ScriptProcessPluginManager().get_singleton(),
            MacrosPluginManager().get_singleton(),
            JsonIoPluginManager().get_singleton(),
            TextIoPluginManager().get_singleton(),
            CommandPluginManager().get_singleton(),
        )
    })

    ValueCacheStorageManager().get_singleton().display_all_data()
    for item in (
        ExternalDependencyManager()
            .get_singleton()
            .import_targets
    ):
        print(item)


if __name__ == "__main__":
    raise SystemExit(main())



