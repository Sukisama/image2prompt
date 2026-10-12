# image2prompt

> 把任何成品图片，逆向成"能重新生成它"的 AI 生图提示词。
> Reverse-engineer any finished image into a reusable, model-specific AI image prompt.

一个 Agent Skill（兼容 Claude Code / Codex / WorkBuddy / Kimi 等支持 Skills 的客户端），也是一套可独立使用的方法论 + 批量脚本。

## 为什么做这个

看到一张好看的海报/封面/产品图，想复刻它的风格，但不知道怎么写提示词——这个 skill 解决的就是这件事。

和"随便描述一下这张图"不同，它有三条铁律：

1. **方言匹配**：先确认你要喂给哪个生图模型。GPT Image 要自然语言散文，SD/Flux 要逗号标签串，即梦要中文结构化，Midjourney 要参数后缀——给错方言等于白干。
2. **图中文字逐字转写**：海报的文案是核心资产，读不清就标 `[看不清]`，绝不编造。
3. **Round-trip 验证**：反推的 prompt 能重新生成出相似的图，才算有效。

## 包含什么

```
image2prompt/
├── SKILL.md                              # 触发规则 + 标准流程 + 翻车点
├── references/
│   ├── decomposition-template.md         # 八维拆解模板（主体/场景/构图/光影/色彩/风格/文字/情绪）
│   └── dialects.md                       # 四大目标模型方言 + 视觉模型选型
└── scripts/
    └── batch_reverse.py                  # 批量反推（OpenAI 兼容 API，任意视觉模型）
```

## 使用

**作为 Agent Skill**：把本目录放进你的 skills 目录（如 `~/.claude/skills/` 或 `~/.agents/skills/`），然后对 agent 说"反推这张图的提示词"即可触发。

**只用批量脚本**：

```bash
pip install openai
export OPENAI_API_KEY=xxx
export OPENAI_BASE_URL=<兼容端点>   # 可选
python scripts/batch_reverse.py ./imgs/ --model qwen3-vl-plus --dialect gpt-image -o prompts.md
```

支持四种方言：`gpt-image`（自然语言散文）/ `jimeng`（中文结构化）/ `midjourney` / `sd`。

## 视觉模型选型建议

| 场景 | 推荐 |
|---|---|
| 中文海报/图中大量文字 | Qwen3-VL 系列（中文 OCR 最强） |
| 单张精品分析 | GPT-5.5 / Gemini 旗舰 |
| 大批量省钱 | Qwen3-VL / GLM-4.5V API |
| 隐私/未发布素材 | 本地 JoyCaption / Ollama + Qwen3-VL |

## License

MIT
