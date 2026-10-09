# d0m3n1c0x.github.io

The front page of my portfolio: three projects readable in two minutes, then the rest.
Live at **https://d0m3n1c0x.github.io/**.

One HTML file, no build step. The short loops in `media/` are recorded from the live project pages with
the Chrome already installed, so they show the tools as they are today:

```bash
python3 -m venv .venv && .venv/bin/pip install playwright pillow
.venv/bin/python tools/record.py          # all loops and the link preview
.venv/bin/python tools/record.py vimeo    # one loop
```

Each loop also has a still (`media/*.png`), shown instead of the animation to anyone who asks their
system for reduced motion.
