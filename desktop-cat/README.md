# Desktop Cat

## What It Is

Desktop Cat is a Windows desktop companion built with Python and PyQt5. It renders an animated cat as a transparent, always-on-top overlay and simulates falling, walking, sitting, running, sleeping, grooming, stretching, itching, and meowing.

## Features

- Transparent frameless overlay without a taskbar entry.
- Animated sprite sheets with configurable sprite frame rate and scale.
- Gravity, ground collision, falling, walking, and running behavior.
- State-machine driven idle and activity animations.
- Window and screen geometry integration for desktop-aware behavior.
- Configurable frame rate, physics values, cat dimensions, movement speed, and state timings.
- Optional debug output for state and position tracking.

## Usage

Requirements: Windows, Python 3.10+ recommended, and the bundled sprite assets.

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python main.py
```

On Windows, `start_cat.bat` starts the application with `pythonw`. Edit `cat_config.json` for intended runtime settings, but note that the current implementation reads many gameplay constants from `core/config.py`; not every JSON setting is wired into the runtime yet.

## Technology

- Python
- PyQt5 for the transparent overlay, rendering, timers, and application loop
- `pywinctl` for visible-window geometry
- Local PNG sprite assets
- No network service is required

## Privacy and Safety

Desktop Cat runs locally and does not upload data. It reads screen dimensions and visible window geometry so the cat can interact with the desktop. The overlay stays above other windows and is mouse-transparent; close it with the normal process controls if needed. Review third-party assets and dependencies before redistribution.

## Distribution

Desktop Cat is distributed as a paid digital product through Gumroad. The product page may contain the current package, releases, and commercial purchase terms.

## License

No license is currently specified for this project. Obtain permission before redistributing or commercially reusing the source or bundled assets outside the applicable Gumroad terms.

## Status

Version is not declared. The current implementation targets Windows and uses the primary screen for the overlay.