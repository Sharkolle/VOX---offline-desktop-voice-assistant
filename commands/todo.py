# commands/todo.py


from core.memory import get_active_user, get_user_file, load_memory, save_memory

KEY = "todo"

def _load():
    user = get_active_user()
    f = get_user_file(user)
    mem = load_memory(f) if f else {}
    if KEY not in mem:
        mem[KEY] = []
    return mem, f

def add_item(item: str):
    mem, f = _load()
    item = item.strip()
    if not item:
        return {"text": "What should I add?", "speak": "What should I add?"}
    mem[KEY].append(item)
    save_memory(mem, f)
    return {"text": f"Added to your list: {item}", "speak": f"Added {item} to your list."}

def list_items():
    mem, _ = _load()
    if not mem[KEY]:
        return {"text": "Your to-do list is empty.", "speak": "Your to-do list is empty."}
    lines = [f"{i+1}. {t}" for i, t in enumerate(mem[KEY])]
    return {"text": "Your to-do list:\n" + "\n".join(lines), "speak": f"You have {len(mem[KEY])} items."}

def remove_item(item: str):
    mem, f = _load()
    item = item.strip().lower()
    for i, t in enumerate(mem[KEY]):
        if t.lower() == item:
            mem[KEY].pop(i)
            save_memory(mem, f)
            return {"text": f"Removed: {t}", "speak": f"Removed {t}."}
    return {"text": f"Couldn't find '{item}' on your list.", "speak": "I couldn't find that item."}

def clear_list():
    mem, f = _load()
    mem[KEY] = []
    save_memory(mem, f)
    return {"text": "Cleared your to-do list.", "speak": "Cleared your to-do list."}
