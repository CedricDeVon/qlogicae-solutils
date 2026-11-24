
def main():    
    from qlogicae_cor.v3.library.plugin_manager import (
        PluginManager
    )
    from qlogicae_cor.v3.library.value_cache_storage_manager import (
        ValueCacheStorageManager
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
    from qlogicae_cor.v3.library.text_encoding_plugin_manager import (
        TextEncodingPluginManager
    )
    from qlogicae_cor.v3.library.macros_plugin_manager import (
        MacrosPluginManager
    )
    from qlogicae_cor.v3.library.command_plugin_manager import (
        CommandPluginManager
    )

    PluginManager().get_singleton().run({
        "internal_objects": (
            HardwarePluginManager().get_singleton(),
            ConsoleNavigationPluginManager().get_singleton(),
            BuildPluginManager().get_singleton(),
            TextEncodingPluginManager().get_singleton(),
            MacrosPluginManager().get_singleton(),
            CommandPluginManager().get_singleton(),
        )
    })

    ValueCacheStorageManager().get_singleton().display_all_data()


if __name__ == "__main__":
    raise SystemExit(main())



