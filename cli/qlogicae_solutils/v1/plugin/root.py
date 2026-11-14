__all__ = (
    "export"
)

def command_about_version(arguments):
    print("Confirmed!")

    return True


def on_pre_setup():
    print("on_pre_setup")


def on_post_setup():
    print("on_post_setup")


def on_pre_run():
    print("on_pre_run")


def on_post_run():
    print("on_post_run")


def export():
    data = {
        "object_merge": {
            "level": -1
        },
        "command": {
            "options": {
                "commands": [
                    {
                        "name": "about",
                        "args": (),
                        "kwargs": {
                            "help": "about",
                        },
                        "subcommands": [
                            {
                                "name": "version",
                                "kwargs": {
                                    "help": "version",
                                },
                                "command_handler": command_about_version,
                                "arguments": [],
                            },
                        ],
                    },
                ],
            },
            "callbacks": {
                "on_pre_setup": on_pre_setup,
                "on_post_setup": on_post_setup,
                "on_pre_run": on_pre_run,
                "on_post_run": on_post_run,
            },
        },
    }

    return data


