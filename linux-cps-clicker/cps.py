#!/usr/bin/env python3

import argparse
import selectors
import sys
import threading
import time

from evdev import InputDevice, UInput, ecodes as e, list_devices

TOGGLE_KEY = e.KEY_F4
QUIT_KEY = e.KEY_F8
PREFIX = "cps-virtual"

enabled = False
held = False
running = True
click_count = 0
active_ui = None
lock = threading.Lock()


def find_devices():
    keyboards, mice = [], []
    for path in list_devices():
        dev = InputDevice(path)
        if dev.name.startswith(PREFIX):
            dev.close()
            continue
        caps = dev.capabilities()
        keys = caps.get(e.EV_KEY, [])
        rel = caps.get(e.EV_REL, [])
        absolute = caps.get(e.EV_ABS, [])
        if TOGGLE_KEY in keys and QUIT_KEY in keys:
            keyboards.append(dev)
        elif e.BTN_LEFT in keys and e.REL_X in rel and not absolute:
            mice.append(dev)
        else:
            dev.close()
    return keyboards, mice


def click_loop(cps):
    global click_count
    period = 1.0 / cps
    next_time = time.perf_counter()
    while running:
        ui = active_ui
        if not (enabled and held and ui):
            time.sleep(0.005)
            next_time = time.perf_counter()
            continue

        with lock:
            ui.write(e.EV_KEY, e.BTN_LEFT, 1)
            ui.syn()
        time.sleep(0.008)
        with lock:
            ui.write(e.EV_KEY, e.BTN_LEFT, 0)
            ui.syn()
            click_count += 1

        next_time += period
        delay = next_time - time.perf_counter()
        if delay > 0:
            time.sleep(delay)
        else:
            next_time = time.perf_counter()


def main():
    global enabled, held, running, click_count, active_ui

    parser = argparse.ArgumentParser()
    parser.add_argument("--cps", type=float, default=10.0)
    parser.add_argument("--debug", action="store_true")
    args = parser.parse_args()
    if args.cps <= 0:
        sys.exit("--cps doit être > 0")

    try:
        keyboards, mice = find_devices()
    except PermissionError:
        sys.exit("Permission refusée : lance avec  sudo python3 cps.py")

    if not keyboards:
        sys.exit("Aucun clavier détecté (essaie avec sudo).")
    if not mice:
        sys.exit("Aucune souris détectée (essaie avec sudo).")

    mice_by_path = {m.path: m for m in mice}
    mouse_ui = {}
    forwarded = {}
    try:
        for m in mice:
            mouse_ui[m.path] = UInput.from_device(m, name=f"{PREFIX}-{m.name}")
            forwarded[m.path] = False
            m.grab()
    except OSError as err:
        sys.exit(f"Impossible de capturer la souris : {err}")
    
    print("AutoLinux - v1.0 (Linux)")
    print("par Walid22202")
    print("Discord: lecouscoussier42")
    print("Toggle: F4   Maintiens le clic gauche pour cliquer   Quitter: F8")
    print(f"CPS cible : {args.cps:.1f}")
    print("Claviers écoutés :")
    for k in keyboards:
        print(f"  - {k.name}  ({k.path})")
    print("Souris capturées :")
    for m in mice:
        print(f"  - {m.name}  ({m.path})")
    print()

    sel = selectors.DefaultSelector()
    for dev in keyboards + mice:
        sel.register(dev, selectors.EVENT_READ, data=dev.path)

    time.sleep(0.5)  
    threading.Thread(target=click_loop, args=(args.cps,), daemon=True).start()

    last_t = time.perf_counter()
    measured = 0.0
    try:
        while running:
            for key, _ in sel.select(timeout=0.2):
                dev = key.fileobj
                path = key.data
                try:
                    for ev in dev.read():
                        if path in mouse_ui:
                            ui = mouse_ui[path]
                            if ev.type == e.EV_KEY and ev.code == e.BTN_LEFT:
                                if ev.value == 1:
                                    held = True
                                    active_ui = ui
                                    forwarded[path] = not enabled
                                elif ev.value == 0:
                                    held = False
                                if not forwarded[path]:
                                    continue  
                                if ev.value == 0:
                                    forwarded[path] = False
                            with lock:
                                ui.write_event(ev)
                        elif ev.type == e.EV_KEY and ev.value == 1:
                            if args.debug:
                                print(f"\n[debug] touche {ev.code} ({dev.name})")
                            if ev.code == TOGGLE_KEY:
                                enabled = not enabled
                            elif ev.code == QUIT_KEY:
                                running = False
                except BlockingIOError:
                    pass
                except OSError:
                    sel.unregister(dev)
                    print(f"\n[!] Périphérique perdu : {dev.name}")

            now = time.perf_counter()
            if now - last_t >= 0.5:
                with lock:
                    count, click_count = click_count, 0
                measured = count / (now - last_t)
                last_t = now

            state = "\033[92m[ON] \033[0m" if enabled else "\033[91m[OFF]\033[0m"
            hold = "clic maintenu" if held else "             "
            print(f"\rState: {state}  CPS: {measured:5.2f}  {hold}   ", end="", flush=True)
    except KeyboardInterrupt:
        pass
    finally:
        running = False
        for path, ui in mouse_ui.items():
            try:
                mice_by_path[path].ungrab()
            except OSError:
                pass
            ui.close()
        print("\nBye.")


if __name__ == "__main__":
    main()
