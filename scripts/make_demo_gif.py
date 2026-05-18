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
        Path("C:/Windows/Fonts/msyhbd.ttc" if bold else "C:/Windows/Fonts/msyh.ttc"),
        Path("C:/Windows/Fonts/simhei.ttf"),
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

    draw.text((172, 56), "Codex Cleaner Skill demo", font=FONT_TITLE, fill=PALETTE["text"])

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
                ("> Use codex-cleaner to scan my archived conversations", "green"),
                ("", "text"),
                ("Scanning local archived Codex sessions ...", "muted"),
                ("Reading conversation titles and matching project folders ...", "muted"),
                ("No files are deleted during scan.", "yellow"),
            ],
            "Step 1: scan first, delete nothing. / 第一步：先扫描，不删除。",
        )
    )

    frames.append(
        draw_terminal(
            [
                ("> codex-cleaner scan", "green"),
                ("", "text"),
                ("#   Title                         Session   Size      Workspace", "blue"),
                ("--  ----------------------------  --------  --------  ------------------------------", "muted"),
                ("1   Build sales image analyzer    019e25e9  242.2 MB  ...\\2026-05-14\\windows", "text"),
                ("2   Summarize PPE agencies        019e24a6  10.6 KB   ...\\2026-05-14\\demo-export", "yellow"),
                ("3   Product director workflow     019dce27  17.7 KB   ...\\2026-04-27\\new-chat", "text"),
                ("", "text"),
                ("User replies: 2", "green"),
            ],
            "Step 2: choose by readable title or row number. / 第二步：按编号选择。",
        )
    )

    frames.append(
        draw_terminal(
            [
                ("Codex asks: What should I clean?", "blue"),
                ("", "text"),
                ("1. Delete archived conversation only - keep project files", "text"),
                ("2. Delete local project files only - keep the conversation", "text"),
                ("3. Delete both - move to Codex_Trash", "text"),
                ("4. Permanently delete everything - cannot be restored", "red"),
                ("", "text"),
                ("用户也会看到：只删对话 / 只删项目 / 两者都清理 / 彻底删除", "yellow"),
            ],
            "Step 3: choose the cleanup mode from one menu. / 第三步：选择清理方式。",
        )
    )

    frames.append(
        draw_terminal(
            [
                ("User chooses: 1. Conversation only", "green"),
                ("", "text"),
                ("Selected: [2] Summarize PPE agencies", "blue"),
                ("Conversation-only mode. Project files will be kept.", "yellow"),
                ("Dry run only. Reply confirm to apply.", "yellow"),
                ("dry-run: would move archived log to Codex_Trash:", "muted"),
                ("  C:\\Users\\you\\.codex\\archived_sessions\\rollout-019e24a6.jsonl", "text"),
                ("", "text"),
                ("Kept: C:\\Users\\you\\Documents\\Codex\\2026-05-14\\demo-export", "green"),
            ],
            "Step 4: preview exact paths before cleanup. / 第四步：先预览路径。",
        )
    )

    frames.append(
        draw_terminal(
            [
                ("User confirms: confirm", "green"),
                ("", "text"),
                ("Selected: [2] Summarize PPE agencies", "blue"),
                ("Conversation-only mode. Project files will be kept.", "yellow"),
                ("moved:", "green"),
                ("  ...\\archived_sessions\\rollout-019e24a6.jsonl", "text"),
                ("  -> C:\\Users\\you\\Documents\\Codex_Trash\\20260518_archive_rollout.jsonl", "muted"),
                ("", "text"),
                ("Local cleanup complete. Project files were kept.", "green"),
                ("Cloud-side ChatGPT/Codex history is not changed.", "muted"),
            ],
            "Done: safe local cleanup with clear choices. / 完成：选择清楚，默认安全。",
        )
    )

    frames.append(
        draw_terminal(
            [
                ("Permanent delete is available, but separated.", "red"),
                ("", "text"),
                ("If the user picks option 4:", "blue"),
                ("  - Codex dry-runs first", "text"),
                ("  - Codex warns it will not go to Codex_Trash", "text"),
                ("  - Codex asks for explicit final confirmation", "text"),
                ("", "text"),
                ("普通用户不用记命令，只按编号选择。", "green"),
            ],
            "Option 4 is deliberately treated as dangerous. / 第 4 项会明确提示风险。",
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
        duration=[1400, 2200, 2600, 2600, 2400, 2400],
        loop=0,
        optimize=True,
    )
    print(OUT)


if __name__ == "__main__":
    main()
