# Page Map

## README.md

English landing page for GitHub visitors. It explains the problem, target users, Skill install command, no-command workflow, CLI examples, safety model, privacy model, and promotion resources.

## README.zh-CN.md

Chinese landing page for GitHub visitors and social media traffic. It uses simpler wording for non-technical users and emphasizes the Codex Skill menu workflow.

## skills/codex-cleaner/SKILL.md

Runtime instructions for Codex. It tells Codex how to scan archived sessions, show a numbered list, ask which cleanup mode to use, dry-run first, require confirmation, and mirror Chinese or English user language.

## scripts/codex_cleaner.py

Main CLI implementation. It scans local archived sessions and performs dry-run or confirmed cleanup.

## skills/codex-cleaner/scripts/codex_cleaner.py

Bundled copy of the CLI used by the installed Codex Skill. Tests require this script to stay in sync with `scripts/codex_cleaner.py`.

## docs/promotion/xiaohongshu.md

Chinese Xiaohongshu post templates, title options, comment prompts, and cover image text ideas.

## docs/promotion/community-posts.md

Reusable community launch copy for GitHub Discussions, V2EX, Reddit, and X/Twitter.

## docs/promotion/share-with-friends.md

Short beginner-friendly instructions for helping a friend install and use the skill.

## docs/releases/

Release notes for published GitHub versions.

## assets/demo.gif

Animated demo used by the README files.
