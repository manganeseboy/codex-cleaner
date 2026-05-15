#!/usr/bin/env python3
"""Generate a public demo GIF for Codex Cleaner."""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "demo.gif"
WIDTH = 1200
HEIGHT = 720


PALETTE = {
    "bg": "#0d1117",
    "panel": "#111827",
    "panel_2": "#0b1220",
    "border": "#263241",
    "text": "#e5edf5",
    "muted": "#94a3b8",
    "green": "#22c55e",
    "blue": "#60a5fa",
    "yellow": "#facc15",
    "red": "#f87171",
}


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    candidates = [
        Path("C:/Windows/Fonts/consolab.ttf" if bold else "C:/Windows/Fonts/consola.ttf"),
        Path("C:/Windows/Fonts/CascadiaMono.ttf"),
        Path("C:/Windows/Fonts/arial.ttf"),
    ]
    for path in candidates:
        if path.exists():
            return ImageFont.truetype(str(path), size=size)
    return ImageFont.load_default()


FONT_TITLE = font(28, True)
FONT = font(21)
FONT_SMALL = font(18)


def draw_terminal(lines: list[tuple[str, str]], footer: str | None = None) -> Image.Image:
    image = Image.new("RGB", (WIDTH, HEIGHT), PALETTE["bg"])
    draw = ImageDraw.Draw(image)

    draw.rounded_rectangle((48, 42, WIDTH - 48, HEIGHT - 42), radius=16, fill=PALETTE["panel"], outline=PALETTE["border"], width=2)
    draw.rounded_rectangle((48, 42, WIDTH - 48, 92), radius=16, fill=PALETTE["panel_2"])
    draw.rectangle((48, 72, WIDTH - 48, 92), fill=PALETTE["panel_2"])

    for x, color in [(78, "#ef4444"), (108, "#f59e0b"), (138, "#22c55e")]:
        draw.ellipse((x, 60, x + 14, 74), fill=color)

    draw.text((172, 56), "Codex Cleaner demo", font=FONT_TITLE, fill=PALETTE["text"])

    y = 126
    for text, color in lines:
        draw.text((78, y), text, font=FONT, fill=PALETTE[color])
        y += 32

    if footer:
        draw.rounded_rectangle((78, HEIGHT - 108, WIDTH - 78, HEIGHT - 72), radius=8, fill="#10251a", outline="#1f7a3a")
        draw.text((96, HEIGHT - 101), footer, font=FONT_SMALL, fill=PALETTE["green"])

    return image


def make_frames() -> list[Image.Image]:
    frames: list[Image.Image] = []

    frames.append(
        draw_terminal(
            [
                ("> codex-cleaner scan", "green"),
                ("", "text"),
                ("Scanning ~/.codex/archived_sessions ...", "muted"),
                ("Mapping each session to its recorded workspace cwd ...", "muted"),
            ],
            "Step 1: scan first, delete nothing.",
        )
    )

    frames.append(
        draw_terminal(
            [
                ("> codex-cleaner scan", "green"),
                ("", "text"),
                ("#   Session   Exists  Size      Files  Shared  Workspace", "blue"),
                ("--  --------  ------  --------  -----  ------  ------------------------------", "muted"),
                ("1   019e25e9  yes     242.2 MB  2970   1       ...\\2026-05-14\\windows", "text"),
                ("2   019e24a6  yes     10.6 KB   2      1       ...\\2026-05-14\\demo-export", "yellow"),
                ("3   019dce27  yes     17.7 KB   1      1       ...\\2026-04-27\\new-chat", "text"),
            ],
            "Step 2: pick the session or project you no longer need.",
        )
    )

    frames.append(
        draw_terminal(
            [
                ("> codex-cleaner clean --session-id 019e24a6 --target both", "green"),
                ("", "text"),
                ("Dry run only. Re-run with --yes to apply.", "yellow"),
                ("dry-run: would move to trash:", "muted"),
                ("  C:\\Users\\you\\Documents\\Codex\\2026-05-14\\demo-export", "text"),
                ("dry-run: would move to trash:", "muted"),
                ("  C:\\Users\\you\\.codex\\archived_sessions\\rollout-019e24a6.jsonl", "text"),
            ],
            "Step 3: dry-run shows the exact paths before cleanup.",
        )
    )

    frames.append(
        draw_terminal(
            [
                ("> codex-cleaner clean --session-id 019e24a6 --target both --yes", "green"),
                ("", "text"),
                ("moved:", "green"),
                ("  ...\\2026-05-14\\demo-export", "text"),
                ("  -> C:\\Users\\you\\Documents\\Codex_Trash\\20260515-170000_project_demo-export", "muted"),
                ("moved:", "green"),
                ("  ...\\archived_sessions\\rollout-019e24a6.jsonl", "text"),
                ("  -> C:\\Users\\you\\Documents\\Codex_Trash\\20260515-170000_archive_rollout.jsonl", "muted"),
            ],
            "Step 4: cleanup moves files to Codex_Trash by default.",
        )
    )

    frames.append(
        draw_terminal(
            [
                ("> codex-cleaner scan", "green"),
                ("", "text"),
                ("#   Session   Exists  Size      Files  Shared  Workspace", "blue"),
                ("--  --------  ------  --------  -----  ------  ------------------------------", "muted"),
                ("1   019e25e9  yes     242.2 MB  2970   1       ...\\2026-05-14\\windows", "text"),
                ("2   019dce27  yes     17.7 KB   1      1       ...\\2026-04-27\\new-chat", "text"),
                ("", "text"),
                ("Local archived log and workspace output cleaned safely.", "green"),
                ("Cloud-side ChatGPT/Codex history is not changed.", "muted"),
            ],
            "Done: safer cleanup for archived Codex workspaces.",
        )
    )

    return frames


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    frames = make_frames()
    frames[0].save(
        OUT,
        save_all=True,
        append_images=frames[1:],
        duration=[1200, 1800, 2200, 2200, 2200],
        loop=0,
        optimize=True,
    )
    print(OUT)


if __name__ == "__main__":
    main()
