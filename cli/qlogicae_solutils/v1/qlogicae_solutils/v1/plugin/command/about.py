__all__ = (
    "export"
)

_data = None


def run_about_show_version_command(arguments):
    from qlogicae_solutils.v1.plugin import qlogicae

    qlogicae_exports = qlogicae.export()

    print(
        ((((qlogicae_exports
            .get("qlogicae", {}) or {})
            .get("solutils", {}) or {})
            .get("v1", {}) or {})
            .get("current-version-label", {}) or {})
    )

    return True


def _allocate():
    global _allocate
    global _data

    _data = {
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
                                    "name": "about",
                                    "args": (),
                                    "kwargs": { "help": "Manage application build operations.", },
                                    "subcommands": [
                                        {
                                            "name": "show",
                                            "args": (),
                                            "kwargs": { "help": "Display operations.", },
                                            "subcommands": [
                                                {
                                                    "name": "version",
                                                    "args": (),
                                                    "kwargs": { "help": "Show version label.", },
                                                    "command_handler": (
                                                        run_about_show_version_command
                                                    ),
                                                },
                                            ],
                                        },
                                    ],
                                },
                            ],
                        },
                    },
                }
            }
        }
    }

    _allocate = lambda: None


def export():
    if _data is None:
        _allocate()

    return _data
