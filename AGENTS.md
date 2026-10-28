# Lemo-Opuscar: instructions for agents

This repository is a library of film styles. Each style has a `styles/<slug>/STYLE.md` (what the style is) and one demo film made entirely in code (`DEMO.md` and `demo/`). People pick a style and ask for a film about **their own** topic. Your job is to direct and produce that film.

| The request | Go to |
|---|---|
| Any request: first see the user's own styles; no request yet: offer the ways in | **Start** below |
| A film about the user's topic (the normal case) | **Style and story**, **Workflow** below |
| "Which styles are there?" / no style chosen | **Finding the style** below |
| A math teaching film (dạy toán, mọi cấp) | [`MATH-VIDEOS.md`](MATH-VIDEOS.md) |
| Directing: story, sound, rhythm, camera, checks, delivery | [`DIRECTOR.md`](DIRECTOR.md) |
| Building: install, pages, voice, music, mix | [`TECHNIQUE.md`](TECHNIQUE.md) |
| Tool commands and flags | [`core/README.md`](core/README.md) |
| The user wants to change a style and keep it as their own, or make their own style from a blank page, or names a style in `~/lemo-my-styles/` | [`MY-STYLES.md`](MY-STYLES.md) |
| Adding a style to the library (owner only) | [`MAINTAINING.md`](MAINTAINING.md) |

**Films outside `styles/` are the user's: no LemoLab credit, no watermark.**

**Math films:** follow `MATH-VIDEOS.md`: fixed Minh Quân Pro voice, slow and thorough explanations, no background music or sound effects, no narration captions. These requirements override defaults in STYLE.md as well as demos. Preserve the user's selected style; audio and caption settings are independently configurable. Avoid white-paper/whiteboard layouts by default; follow an explicit user choice and assess the actual visuals rather than rejecting a style by name.

**QA for every film:** Read [FILM-QA.md](FILM-QA.md). For all film types, merge environment → `.env` per key; only math films overlay `.env.math` last. When the effective `AI_QA_REQUIRED=true`, style consultation, assets QA and final QA are mandatory before delivery. Use `tools/film_qa.py` for general films and `tools/film_qa.py --film-type math` (or `tools/math_qa.py`) for math. Missing configuration, failed QA or insufficient evidence blocks production at the relevant gate. Never silently skip enabled QA.

**Early math style consultation:** when `AI_QA_REQUIRED=true`, consult QA as soon as proposing/selecting a style, before finalizing the visual direction or producing images, TTS or animation. Use `tools/math_qa.py --stage style` with the original problem, grade/mode, full style specification and concrete design proposal. Resolve blocker/fix feedback before production and retain actual exchanges and agent decisions in qa.html. Planning approval does not replace later assets QA or final logo and delivery-cleanliness QA. See `MATH-VIDEOS.md`.

## Start

- **Their own styles first.** If `~/lemo-my-styles/README.md` exists, read it: it lists every style the user has saved, wherever it's kept, and their own styles ([`MY-STYLES.md`](MY-STYLES.md)) count like library styles. When they name a style, look there first, then in the library.
- **Their language.** Talk to them in the language they write in. When they started the skill without writing anything, your first question is always the language, even when their settings, memory or earlier messages suggest one: the `AskUserQuestion` tool, a question of its own headed "Language 语言" with two options, 中文 and English (the tool adds Other, where they type any other language). Use it from then on, and as the film's default language.
- **No request yet** (they only started the skill, or said hello): offer the ways in with one question, using the `AskUserQuestion` tool, in their language, with the first as the recommended one:
  1. a film in a library style (**Finding the style**);
  2. change a library style and keep it as their own ([`MY-STYLES.md`](MY-STYLES.md));
  3. make their own style from a blank page ([`MY-STYLES.md`](MY-STYLES.md));
  4. a film in one of their own styles, only when they have some (name them).

  When their request already says which, skip the question.

## Style and story

- **Production uses existing styles only.** Select an existing library style or an already-existing user style. Never create, register, fork, rename or code a new style during film production, including to bypass a QA rejection. Adapting an existing style's music, SFX, voice, narration captions, pacing or teaching layout to the brief is normal production, not creating a new style. Preserve a style explicitly chosen by the user. Neither the agent nor QA may authorize a replacement; explain a genuine unresolved visual conflict and obtain the user's decision before switching. New-style work requires a separate explicit user request; this production rule overrides the style-creation routes below.
- **Keep production bounded.** Follow `PRODUCTION-EFFICIENCY.md` for full command/output logging, short planning, targeted QA, tool-repair limits and actual timing. Do not turn a film request into tool development or repeatedly rebuild the production stack.

- **`STYLE.md` defines the visual identity, with configurable production settings.** Preserve its distinctive materials, rendering, colour logic, lettering, motion and camera grammar. Music, SFX, voice and narration captions may be disabled or replaced to meet the user's brief or math requirements, even when STYLE.md describes them as essential. Instructional text (problems, labels, numbers, formulas) is separate from narration captions. Crayon without music or captions is still Crayon: keep wax texture, paper tooth, hatching and hand-drawn motion. Record overrides in the film's treatment/proposal; do not edit the library style or register a variant. QA must evaluate this adapted contract, including fidelity to the user's chosen style.
- **Everything else is yours to direct** from the user's topic: story, structure, characters, settings, shots, timings, references, how data is charted. Never bend the topic toward the demo.
- **Treatment first, demo later.** Write your own `TREATMENT.md`, with three candidate structures and your choice (DIRECTOR.md §4), before you open `DEMO.md` or the demo code. Then use the demo only to learn techniques (a brush engine, a rig, a shader, a mix), never its story, arc, shots, props or timeline. One exception: a style cut from real material (Edit & Documentary) needs its material before the treatment, so the tools its `STYLE.md` names in `demo/tools/` for finding and logging material (`footage.py` and the like) may be used first, copied into the project folder and run there; still read `DEMO.md` and the rest of the demo only after the treatment is written.
- **Scene styles** (a set-up guide, a spec walkthrough, a museum plate, a trail guide) list use cases in their `STYLE.md`. Read them as grammar for the order in which information arrives and how long each part needs on screen, then build the user's content in your own structure. Swapping text into a demo's `content.json` is only a technical check, never the way to deliver.
- Never build inside `styles/`: copy what you need into the film's project folder.

## Finding the style

Users name a style by its gallery name in English or Chinese ("Impasto Oil Painting", "油画厚涂") or by its folder (`impasto`). Look it up in [`styles/README.md`](styles/README.md). If nothing matches clearly, show the closest two or three and ask.

If the user hasn't picked a style:
- Suggest two or three that fit their topic.
- If they have their own styles, list those first, under "My styles" (in their language).
- Show them the full list below in the chat, in the user's language only: English names (and English category names) for someone writing in English, Chinese names for someone writing in Chinese. Don't drop, merge or rename anything.
- Link the gallery, where every style has its demo film: https://lemomo-ai.github.io/lemo-opuscar/
- Then ask them to type the name. The list goes in your own message (a command's output isn't shown to them), and the question is plain text, not `AskUserQuestion`: its few options would hide the rest of the list.

<!-- style-list:start -->
All 59 styles · 全部风格:

- **剪辑与纪实 Edit & Documentary** (8): 字幕新闻 Caption News, 1920s 新闻影片 1920s Newsreel, 实时倒计时分屏 Live Countdown Split-screen, 延时交响 Time-lapse Symphony, 视觉调查 Visual Investigation, 构成主义蒙太奇 Constructivist Montage, 体育战术板 Sports Telestrator, 电视新闻包装 Broadcast News Package
- **实证影像 Evidence Films** (8): 卫星简报 Satellite Briefing, 工程简报板 Engineering Briefing Board, 点云测绘 LiDAR Survey, 白模投影 Projection on White Model, 数据实物化 Data Physicalization, 产品拆解 Exploded Teardown, 显微叙事 Microscope Story, 档案灯台 Archive Light Table
- **手绘与绘画 Hand-drawn & Painting** (7): 蜡笔儿童绘本 Crayon Picture Book, 水彩笔刷 Watercolor Brush, 中国水墨 Chinese Ink Wash, 油画厚涂 Impasto Oil Painting, 一笔画 One-line Drawing, 白板讲解 Whiteboard Explainer, 钢笔淡彩 Urban Sketch · Pen & Wash
- **东方传统 East Asian Traditions** (4): 皮影戏 Shadow Puppetry, 浮世绘 Ukiyo-e, 红色窗花剪纸 Red Paper-cut, 纸雕灯影 Paper-cut Lightbox
- **印刷与版画 Print & Printmaking** (5): Risograph 孔版印刷 Risograph Print, 复古半调案卷 Halftone Dossier, 木刻版画 Woodcut Print, 铜版画 Copperplate Engraving, 丝印旅行海报 Silkscreen Travel Poster
- **图形与排版 Graphic & Type** (7): 瑞士动态排版 Swiss Motion Graphics, 60s 间谍片头 60s Spy Title Sequence, 装饰艺术 Art Deco, 蓝图 / 工程制图 Blueprint, 彩色玻璃窗 Stained Glass, 象形运动图形 Pictogram Motion, ASCII / CRT 终端 ASCII / CRT Terminal
- **信息与发布 Information & Keynote** (5): 数据叙事 Data Storytelling, 等距信息图 Isometric Infographic, 暗色科技发布 Dark Tech Keynote, 活体实机录屏 Living Screencast, 科幻全息界面 Sci-fi Hologram HUD
- **卡通与动画 Cartoon & Anime** (4): 1930s 橡皮管卡通 1930s Rubber Hose Cartoon, 80 年代赛璐璐动画 80s Cel Anime, 科幻情景喜剧卡通 Sci-Fi Sitcom Toon, 50s 扁平卡通 Mid-century Cartoon
- **游戏 Games** (4): 16-bit 像素 RPG 16-bit Pixel RPG, HD-2D, 微游戏快闪 Microgame Frenzy, 综艺节奏扁平 Game Show Flat
- **电影与时代 Cinema & Eras** (2): 1920s 默片 1920s Silent Film, 后室 / 新怪谈 Liminal Found Footage
- **材质与 3D Materials & 3D** (5): 积木玩具 Brick Toy, 纸片立体书 Paper Pop-up Book, 移轴微缩 Tilt-Shift Miniature, 低多边形等距 Low-poly Isometric Island, 玻璃质感产品 Glass Product Render
<!-- style-list:end -->

## Workflow

1. **Brief.** Make sure the style and the topic are clear, then ask the user once, in a single message (DIRECTOR.md §1):
   - anything about the topic you can't decide yourself (facts; names, logos or products that must appear);
   - whether they have material of their own: a voice recording or a preferred voice, music, photos, logos, fonts, and for a style built from real material, their own data or scans;
   - the film's language, if it isn't obvious (default: the language they write in or chose, for voice and subtitles);
   - whether they want to review a storyboard first (default: no);
   - anything missing on their machine: first run `sh plugin/skills/lemo-opuscar/scripts/setup.sh deps` from the library root (core only) and include what it reports. Add the voice and music tiers later, only if the film needs them (TECHNIQUE.md §1).

   Skip what their request already answers. Wait for the reply, fill every other gap with a sensible default, sum up the brief in a few lines and start. Don't come back with more questions.
2. **Treatment.** Write `project/TREATMENT.md` in the film folder (DIRECTOR.md §4), before you open the demo (an Edit & Documentary style gathers its material first: **Treatment first** above).
3. **QA gates.** Follow FILM-QA.md: if enabled, pass style QA before images/TTS/animation, assets QA before full render, and final QA on the muxed MP4 before delivery. Retain actual exchanges in qa.html.
4. **Look.** Render style frames or a model sheet with the real drawing code and check them against `STYLE.md` (DIRECTOR.md §5).
5. **Storyboard, only if the user asked for it** (DIRECTOR.md §5). **Stop and wait for approval.** Otherwise don't stop.
6. **Produce.** Voice → check → score (can run in parallel) → animation → mix → render (TECHNIQUE.md).
7. **Self-check and deliver** (DIRECTOR.md §11).

Report progress in the user's language. If a step fails, read the error, fix the cause and retry; go back to the user only for a decision or something only they can provide.

## Where things go

- **Output folders are not a reference library.** During production, do not list, scan, search, read or index the output directory or other produced films, including completed films, to discover examples, code, scripts, assets, reports or QA history. Access only the exact current film folder; checking whether a proposed exact folder name exists is allowed without enumerating the output directory. Use repository documentation, shared tools and the selected style's permitted demo as technical references. Never copy or execute scripts from another produced film. An explicit user request to inspect a named film permits access to that film only; it does not authorize browsing neighboring films.

- **Output contract:** read [OUTPUT-STRUCTURE.md](OUTPUT-STRUCTURE.md). At the film root keep only cover.png, calendar.json, one final MP4, preview.html, report.html and qa.html. Put source, treatment, credits, upload text, audio, intermediate builds and QA evidence in subfolders (default project/). report.html must retain work history and the final summary; qa.html must retain actual QA exchanges. This overrides older flat-folder examples in all guides.
- **Calendar template:** Read and copy [`docs/templates/calendar.json`](docs/templates/calendar.json) into the current film's root, then populate it from upload.md and the final MP4's measured metadata. Never invent a shortened schema or copy another produced film. Preserve existing scheduling/publication data when repairing an existing file. Validate every template key/type, nonempty posting text, absence of placeholders, and real local media paths before delivery; write UTF-8 without BOM. See MATH-VIDEOS.md § Đăng ký vào lịch đăng for the field mapping. File existence alone is not completion.

- The film's project folder defaults to `<OUTPUT_DIR>/<name>/` (by default `films/<name>/`, configurable via `OUTPUT_DIR` in `.env`), or `<name>/` in the user's folder in skill mode (see the skill's `SKILL.md`). Wherever a guide says `films/<name>/`, read "the project folder". Work only there, unless the user asks you to work in their own project.
- Name the project folder `<yyyy-mm-dd>_<slug>/`: the date the folder is created, then `_`, then a short kebab-case slug of the film's topic — e.g. `films/2026-10-24_bai-toan-xe-buyt/`. If the name is already taken, append `-2`, `-3`… to the slug; keep the date prefix.
- Run `node core/…` and `sh tools/…` from the library root (`$LIB` in skill mode).
- `core/` has ready-made tools (rendering, TTS, speech check, sampler, sfx, mux). Use them or your own stack, but don't edit `core/` or `styles/` for a user's film.
- **Film-specific files stay with the film.** During film/video production, write every one-off script (Python, CMD/BAT, PowerShell, shell, JS/TS or any other language), temporary helper, diagnostic, restored HTML, backup and intermediate file inside the current film's output subfolders (default `project/scripts/` for scripts). If a temporary file cannot be stored there, use only `<library-root>/.scratch/<current-film-id>/`, with a separate folder for each film; never put loose files in the repository root, `tools/`, other films or another temporary directory. Do not browse or reuse other films' scratch folders. Preserve any scratch files needed for rebuilding or QA in the current film's `project/` before delivery and record their paths/reason in the report. Existing shared tools may be invoked unchanged with film-local outputs. If a shared tool needs modification to make the film work, inherit/wrap or copy it into the film output and modify that local version; do not patch the main project as part of production. Preserve provenance, dependencies and reproducible commands. In `report.html`, document the original file/version, local changes, reason, validation and a concrete proposed upstream fix for the user to review; do not apply that proposal without an explicit request to change the main project. See `OUTPUT-STRUCTURE.md`.
- Never kill processes you didn't start. Don't leave background processes running.

## Shared skill configuration and image generation

- For every skill, resolve configuration from its documented global sources first, then overlay the project configuration. Project values override global values per key; unspecified project values retain global defaults. Do not copy global secrets into the project.
- If required configuration is still missing or invalid after merging, stop and tell the user exactly which configuration fields to add or fix, without exposing secrets. Missing configuration is not a reason to skip a skill or provider and continue the fallback chain. Host-managed built-in tools require no invented API configuration.
- Read each installed SKILL.md before use. If its native loader does not implement this precedence, explicitly pass the merged configuration through supported parameters or the project adapter; do not assume it does.
- All film types use the image skill chain: **image-generate → api-image → muse-image**. Start with the host's built-in image tool through image-generate. Enter api-image once only when the built-in tool is absent, unsupported, or unavailable because of service, quota, or access errors.
- api-image owns its gateway chain through API_IMAGE_PROVIDER. Do not repeat gateways outside that skill. Enter muse-image only after the API chain exhausts its gateways due to eligible service errors, never due to missing configuration.
- Stop on invalid input, safety refusal, or uncertain job status. Preserve prompt, references, size, aspect ratio, and quality across tiers.
- tools/film_image.py implements API → Muse for new images only. The agent must handle the built-in tier first and supply --builtin-unavailable with a verified reason. Use the skills directly for reference images or editing.
- --dry-run makes no network calls and reports configuration issues. --cover normalizes output to PNG at 1280x720 under 2 MB. Inspect the actual image before accepting it.
- Keep code-native style artwork when required by STYLE.md.
- Shared project settings belong in .env. For math films, read MATH-VIDEOS.md; .env.math contains OUTPUT_DIR and optional AI_QA_* overrides. Follow FILM-QA.md for conditional vision QA on every film and MATH-VIDEOS.md for math-specific checks; only effective AI_QA_REQUIRED=true enables it. Pass output paths explicitly to core tools that do not load .env.math.
- tools/math_cover.py is a compatibility entry point with --cover and the same built-in prerequisite.

**Delivery cleanliness:** Keep logo safe zones as invisible coordinates/metadata. Debug overlays default off and must be off in QA previews and exports. Visible production labels, placeholders or alignment guides are blockers in assets and final QA, even without overlap. Final QA checks both logo placement and full-frame delivery cleanliness on actual MP4 frames; report only the scope actually inspected.
