
def export():
    description = (
        "A local, OS-independent, CI/CD workflow execution tool for QLogicae projects"
    )
    data = {
        "data": {
            "company-name": {
                "value": "qlogicae"
            },
            "project-name": {
                "value": "solutils"
            },
            "project-description": {
                "value": description
            },
            "active-major-version-label": {
                "value": "v1"
            },
            "debug": {
                "is-enabled": {
                    "value": True
                }
            },
        },
        "metadata": {

        },
    }

    return data
