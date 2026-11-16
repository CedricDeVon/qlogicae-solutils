__all__ = (
    "export"
)

_data = None

def print_message(*args, **kwargs):
    print(*args, **kwargs)

def _allocate():
    global _allocate
    global _data

    _data = {
        "qlogicae": {
            "solutils": {
                "v1": {
                    "workflow": {
                        "selection": {
                            "qlogicae-project-stage-release": {
                                "filesystem-path": "",
                                "scripts": [
                                    {
                                        "run": "echo 'qlogicae-project-stage-release'",
                                    },
                                    {
                                        "run": "qlogicae-project-build",
                                    },
                                    {
                                        "run": print_message,
                                        "args": [
                                            "Hello"
                                        ],
                                        "kwargs": {
                                            "key": "value"
                                        },
                                    },
                                    {
                                        "run": "filesystem-create",
                                        "kwargs": {
                                            "target_filesystem_paths": [
                                                "output",
                                            ],
                                        },
                                        "is-enabled": True,
                                        "is-failure-optional": True,
                                        "platforms-included": set(), # "Linux-x86_64"
                                        "platforms-excluded": set(),
                                        "return-codes-successful": set(), # 0
                                        "return-codes-unsuccessful": set(), # 1, -1
                                        "delay": 1,
                                        "delay-time-unit": "ms",
                                        "is-asynchronous": True,
                                    },
                                ],
                                "is-enabled": True,
                                "is-failure-optional": True,
                                "platforms-included": set(), # "Linux-x86_64"
                                "platforms-excluded": set(),
                                "return-codes-successful": set(), # 0
                                "return-codes-unsuccessful": set(), # 1, -1
                                "delay": 1,
                                "delay-time-unit": "ms",
                                "is-asynchronous": True,
                            },
                            "qlogicae-project-build": {
                                "filesystem-path": "",
                                "scripts": [
                                    {
                                        "run": {
                                            "value": "echo 'qlogicae-project-build'",
                                        },
                                    },
                                ],
                            },
                        },
                    },
                }
            }
        }
    }

    print(
        __file__
    )

    _allocate = lambda: None


def export():
    if not _data:
        _allocate()

    return _data



# "configuration": {
#     "workspace": {
#         "targets": [
#             "target.yml"
#         ]
#     },
#     "dotenv": {
#         "targets": [
#             ".env"
#         ]
#     }
# },
# "cache": {
#     "clear": {
#         "before": {
#             "is-enabled": {
#                 "value": False
#             },
#         },
#         "after": {
#             "is-enabled": {
#                 "value": False
#             },
#         },
#     },
# },
# "time": {
#     "zone": {
#         "value": "local"
#     }
# },
# "operating-system": {
#     "name": {
#         "value": "Linux"
#     },
#     "architecture": {
#         "value": "x86_64"
#     },
# },
# "log": {
#     "is-enabled": {
#         "value": True,
#         "override": False
#     },
#     "is-verbose": {
#         "value": True,
#         "override": False
#     },
#     "default": {
#         "file": {
#             "output": {
#                 "is-enabled": {
#                     "value": True
#                 }
#             }
#         }
#     },
#     "file": {
#         "is-enabled": {
#             "value": True
#         },
#         "is-verbose": {
#             "value": True
#         }            
#     },
#     "console": {
#         "is-enabled": {
#             "value": True
#         },
#         "is-verbose": {
#             "value": True
#         }
#     }
# },
# "plugin": {
#     "import": {
#         "is-enabled": {
#             "value": True
#         }
#     }
# },
# "display": {
#     "console": {
#         "is-enabled": {
#             "value": True
#         },
#         "style": {
#             "reset": {
#                 "value": "reset"
#             },
#             "base-1": {
#                 "value": "none"
#             },
#             "base-2": {
#                 "value": "grey"
#             },
#             "highlight-1": {
#                 "value": "green"
#             },
#             "highlight-2": {
#                 "value": "green"
#             },
#             "maximum-depth": {
#                 "value": 8
#             },
#             "is-skipped": {
#                 "value": True
#             },
#             "indent-count": {
#                 "value": 4
#             },
#             "vertical-count": {
#                 "value": 0
#             }
#         }
#     }
# },



# "workspace": {
#     "project": {
#         "selection": {
#             "qlogicae-project-root": {
#                 "filesystem-path": {
#                     "value": "selection/qlogicae-project-root"
#                 }
#             },
#             "qlogicae-project-cli": {
#                 "filesystem-path": {
#                     "value": "selection/qlogicae-project-root/cli"
#                 }
#             },
#         }
#     },
#     "group": {
#         "selection": {
#             "qlogicae-project": {
#                 "targets": [
#                     "qlogicae-project-root",
#                     "qlogicae-project-cli",
#                 ]
#             }
#         }
#     }
# },

# "workflow": {
#     "selection": {
#         "qlogicae-project-cli": {
#             "filesystem-path": {
#                 "value": ""
#             },
#             "scripts": {
#                 "run": {
#                     "value": ""
#                 }
#             }
#         },
#         "qlogicae-project-root": {
#             "filesystem-path": {
#                 "value": ""
#             },
#             "scripts": {
#                 "run": {
#                     "value": ""
#                 }
#             }
#         },
#     }
# },
# "macros": {
#     "static": {
#         "targets": {
#             "qlogicae-project-name": {
#                 "value": "qlogicae-project-name"
#             }
#         }
#     },
#     "dynamic": {
#         "targets": {
#             "time-now": {
#                 "value": lambda: 1
#             }
#         }
#     }
# }
