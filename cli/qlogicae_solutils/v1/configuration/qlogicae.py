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
        "company-name": {
            "value": "qlogicae"
        },
        "project-name": {
            "value": "solutils"
        },
        "brand-base-name": {
            "value": "qlogicae-solutils"
        },
        "brand-source-name": {
            "value": "qlogicae_solutils"
        },
        "project-description": {
            "value": description
        },
        "active-major-version-label": {
            "value": "v1"
        },
        "current-version-label": {
            "value": "v1.0.0a1"
        },
        "debug": {
            "is-enabled": {
                "value": True
            }
        },
    }

    _allocate = lambda: None


def export():
    if not _data:
        _allocate()

    return _data
