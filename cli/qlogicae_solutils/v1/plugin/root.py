__all__ = (
    "export"
)

_data = None


def on_pre_setup():
    pass


def on_post_setup():
    pass


def on_pre_run():
    pass


def on_post_run():
    pass


def _allocate():
    global _allocate
    global _data

    from configuration import qlogicae

    qlogicae_exports = qlogicae.export()

    _data = {
        "object_merge": {
            "level": 0
        },
        "command": {
            "options": {
                "kwargs": {
                    "prog": (
                        (qlogicae_exports
                            .get("brand-base-name", {}) or {})
                            .get("value", "") or ""
                    ),
                    "description": (
                        (qlogicae_exports
                            .get("project-description", {}) or {})
                            .get("value", "") or ""
                    )
                },
                "commands": [],
            },
            "callbacks": {
                "on_pre_setup": on_pre_setup,
                "on_post_setup": on_post_setup,
                "on_pre_run": on_pre_run,
                "on_post_run": on_post_run,
            },
        },
    }

    _allocate = lambda: None


def export():
    if not _data:
        _allocate()

    return _data
