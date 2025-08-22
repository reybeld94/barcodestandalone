import keyboard
import shared_flags

hook_listener = None

def start_hook(on_key_callback, suppress=True):
    global hook_listener
    if not hook_listener:
        hook_listener = keyboard.hook(on_key_callback, suppress=suppress)
        shared_flags.hook_enabled = True


def stop_hook():
    global hook_listener
    if hook_listener:
        keyboard.unhook(hook_listener)
        hook_listener = None
        shared_flags.hook_enabled = False
