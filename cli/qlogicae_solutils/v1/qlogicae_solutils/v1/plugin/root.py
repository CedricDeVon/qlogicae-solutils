__all__ = (
    "export"
)


_data = None

def _allocate():
    global _allocate
    global _data

    description = (
        "A local, OS-independent, CI/CD workflow execution tool for QLogicae projects"
    )
    _data = {
        "object_merge": {
            "level": -1
        },
        "qlogicae": {
            "solutils": {
                "v1": {
                    "company-name": "qlogicae",
                    "project-name": "solutils",
                    "brand-base-name": "qlogicae-solutils",
                    "brand-source-name": "qlogicae_solutils",
                    "project-description": description,
                    "active-major-version-label": "v1",
                    "current-version-label": "v1.0.0a1",
                    "debug": {
                        "is-enabled": True
                    },
                }
            },
            "cliq": {
                "v1": {
                    "command": {
                        "options": {
                            "kwargs": {
                                "prog": (
                                    "qlogicae-solutils"
                                ),
                                "description": (
                                    description
                                )
                            },
                            "commands": [],
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
