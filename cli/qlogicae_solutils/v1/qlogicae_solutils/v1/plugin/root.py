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

    from qlogicae_solutils.v1.plugin import qlogicae

    qlogicae_exports = qlogicae.export()

    _data = {

        "object_merge": {
            "level": 0
        },
        "qlogicae": {
            "cliq": {
                "v1": {
                    "command": {
                        "options": {
                            "kwargs": {
                                "prog": (
                                    ((((qlogicae_exports
                                        .get("qlogicae", {}) or {})
                                        .get("solutils", {}) or {})
                                        .get("v1", {}) or {})
                                        .get("brand-base-name", "") or "")
                                ),
                                "description": (
                                    ((((qlogicae_exports
                                        .get("qlogicae", {}) or {})
                                        .get("solutils", {}) or {})
                                        .get("v1", {}) or {})
                                        .get("project-description", "") or "")
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
            }
        }
    }

    _allocate = lambda: None


def export():
    if _data is None:
        _allocate()

    return _data
