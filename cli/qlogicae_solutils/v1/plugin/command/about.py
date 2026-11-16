__all__ = (
    "export"
)

_data = None


def about_version_command_handler(arguments):
    from configuration import qlogicae

    qlogicae_exports = qlogicae.export()

    print(
        (qlogicae_exports
            .get("current-version-label", {}) or {})
            .get("value", None) or None
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
                                    "kwargs": { "help": "", },
                                    "subcommands": [
                                        {
                                            "name": "version",
                                            "kwargs": { "help": "", },
                                            "command_handler": (
                                                about_version_command_handler
                                            ),
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
    if not _data:
        _allocate()

    return _data
