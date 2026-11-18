__all__ = (
    "export"
)

_data = None


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
                                    "name": "",
                                    "args": (),
                                    "kwargs": { "help": "", },
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
