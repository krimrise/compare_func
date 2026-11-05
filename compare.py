"""Сравнение двух структур данных (словарей/списков) в режимах add/update/delete.

Второй аргумент (`source`) — желаемое состояние.
Третий аргумент (`target`) — текущее состояние.
"""

import json

ADD = "add"
UPDATE = "update"
DELETE = "delete"

_MODES = (ADD, UPDATE, DELETE)


def compare(mode, source, target):
    """Сравнить `source` и `target` и вернуть/вывести изменения.

    mode:
        "add"    — что есть в `source`, но отсутствует в `target` (добавить в `target`);
        "update" — что есть в обоих, но различается (изменить в `target` на значение из `source`);
        "delete" — что есть в `target`, но отсутствует в `source` (удалить из `target`).
    """
    if mode not in _MODES:
        raise ValueError(
            f"Неизвестный тип сравнения: {mode!r}. Ожидается одно из {_MODES}."
        )

    if mode == ADD:
        result = _diff_add(source, target)
    elif mode == UPDATE:
        result = _diff_update(source, target)
    else:
        result = _diff_delete(source, target)

    print(f"[{mode}]")
    print(json.dumps(result, indent=2, ensure_ascii=False, default=str))
    return result


def _diff_add(source, target):
    if isinstance(source, dict) and isinstance(target, dict):
        added = {}
        for key, value in source.items():
            if key not in target:
                added[key] = value
            elif isinstance(value, (dict, list)):
                nested = _diff_add(value, target[key])
                if nested:
                    added[key] = nested
        return added

    if isinstance(source, list) and isinstance(target, list):
        return [item for item in source if item not in target]

    return source if source != target else None


def _diff_update(source, target):
    if isinstance(source, dict) and isinstance(target, dict):
        changes = {}
        for key, value in source.items():
            if key not in target:
                continue
            old = target[key]
            if isinstance(value, dict) and isinstance(old, dict):
                nested = _diff_update(value, old)
                if nested:
                    changes[key] = nested
            elif isinstance(value, list) and isinstance(old, list):
                nested = _diff_update(value, old)
                if nested:
                    changes[key] = nested
            elif value != old:
                changes[key] = {"from": old, "to": value}
        return changes

    if isinstance(source, list) and isinstance(target, list):
        changes = {}
        for index, (new, old) in enumerate(zip(source, target)):
            if isinstance(new, dict) and isinstance(old, dict):
                nested = _diff_update(new, old)
                if nested:
                    changes[index] = nested
            elif isinstance(new, list) and isinstance(old, list):
                nested = _diff_update(new, old)
                if nested:
                    changes[index] = nested
            elif new != old:
                changes[index] = {"from": old, "to": new}
        return changes

    return {"from": target, "to": source} if source != target else None


def _diff_delete(source, target):
    if isinstance(source, dict) and isinstance(target, dict):
        removed = {}
        for key, value in target.items():
            if key not in source:
                removed[key] = value
            elif isinstance(value, (dict, list)):
                nested = _diff_delete(source[key], value)
                if nested:
                    removed[key] = nested
        return removed

    if isinstance(source, list) and isinstance(target, list):
        return [item for item in target if item not in source]

    return None


if __name__ == "__main__":
    source = {"a": 1, "b": {"x": 1, "y": 2}, "c": 3}
    target = {"a": 1, "b": {"x": 1, "y": 5}, "d": 4}

    compare(ADD, source, target)
    compare(UPDATE, source, target)
    compare(DELETE, source, target)
