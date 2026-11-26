__all__ = (
    "GroupSelectionManager",
)

_GroupSelectionManager = None

def _allocate():
    global _allocate
    global _GroupSelectionManager

    from .abstract_manager import AbstractManager

    class __GroupSelectionManager(AbstractManager()):
        def flatten_group(
            self,
            target,
            data,
        ):
            if not target:
                raise TypeError("")

            if not data:
                raise TypeError("")

            resolved = []
            visited = set()
            stack = [target]

            while stack:
                value = stack.pop()

                if value in visited:
                    continue

                visited.add(value)

                if value not in data:
                    resolved.append(value)
                    continue

                stack.extend(reversed(data[value]))

            return tuple(resolved)

    _GroupSelectionManager = __GroupSelectionManager
    _allocate = lambda: None


def GroupSelectionManager():
    if _GroupSelectionManager is None:
        _allocate()

    return _GroupSelectionManager


# GroupSelectionManager()

