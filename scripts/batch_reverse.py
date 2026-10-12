#!/usr/bin/env python3
"""batch_reverse.py - 批量图片反推提示词（OpenAI 兼容 API，任何视觉模型可用）

用法:
    export OPENAI_API_KEY=xxx
    export OPENAI_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1   # 可选，默认官方
    python batch_reverse.py ./imgs/ --model qwen3-vl-plus --dialect gpt-image -o prompts.md

依赖: pip install openai
"""
import argparse
import base64
import sys
from pathlib import Path

try:
    from openai import OpenAI
except ImportError:
    sys.exit("缺少依赖: pip install openai")

IMG_EXTS = {".png", ".jpg", ".jpeg", ".webp", ".gif"}

DIALECT_HINTS = {
    "gpt-image": "自然语言散文式整段描述（适配 GPT Image 2.x / Nano Banana / 豆包），图中文字用中文引号逐字包裹并注明位置层级",
    "jimeng": "中文结构化：图片类型+主体+排版布局+文案（引号包裹）+风格氛围（适配即梦 Seedream 等国产模型）",
    "midjourney": "Midjourney 格式：英文短语逗号分隔，末尾带 --ar --s --v 参数",
    "sd": "SD/Flux 格式：逗号分隔 tags，另附一行 Negative prompt",
}

PROMPT_TMPL = """你是图片反推专家。把这张图片逆向成一条可直接用于 AI 生图的提示词。

要求：
1. 按八个维度拆解：主体/场景/构图/光影/色彩/风格媒介/图中文字与字体/情绪氛围
2. 图中所有文字逐字转写并标注位置、层级、字体特征；读不清标 [看不清]，禁止编造
3. 没看到的细节禁止脑补，拿不准标 [不确定]
4. 最终提示词使用以下方言：{dialect}

输出格式：
## 完整提示词
（可直接复制的最终 prompt）
## 八维拆解
（逐项列出观察结果）
## 可替换锚点
（哪些部分可安全替换、哪些动了会破坏风格）"""


def to_data_url(path: Path) -> str:
    mime = "image/png" if path.suffix.lower() == ".png" else "image/jpeg"
    b64 = base64.b64encode(path.read_bytes()).decode()
    return f"data:{mime};base64,{b64}"


def main():
    ap = argparse.ArgumentParser(description="批量图片反推提示词")
    ap.add_argument("input_dir", help="图片目录")
    ap.add_argument("--model", default="qwen3-vl-plus", help="视觉模型名")
    ap.add_argument("--dialect", default="gpt-image",
                    choices=list(DIALECT_HINTS), help="目标生图模型方言")
    ap.add_argument("-o", "--output", default="prompts.md", help="输出 markdown 文件")
    args = ap.parse_args()

    imgs = sorted(p for p in Path(args.input_dir).iterdir()
                  if p.suffix.lower() in IMG_EXTS)
    if not imgs:
        sys.exit(f"{args.input_dir} 里没有图片")

    client = OpenAI()  # 读 OPENAI_API_KEY / OPENAI_BASE_URL
    prompt = PROMPT_TMPL.format(dialect=DIALECT_HINTS[args.dialect])

    out = Path(args.output)
    with out.open("w", encoding="utf-8") as f:
        f.write(f"# 批量反推结果（模型: {args.model} / 方言: {args.dialect}）\n\n")
        for i, img in enumerate(imgs, 1):
            print(f"[{i}/{len(imgs)}] {img.name} ...", flush=True)
            try:
                resp = client.chat.completions.create(
                    model=args.model,
                    messages=[{"role": "user", "content": [
                        {"type": "text", "text": prompt},
                        {"type": "image_url",
                         "image_url": {"url": to_data_url(img)}},
                    ]}],
                )
                result = resp.choices[0].message.content
            except Exception as e:
                result = f"**反推失败: {e}**"
            f.write(f"---\n\n# {img.name}\n\n{result}\n\n")
    print(f"完成 → {out}")


if __name__ == "__main__":
    main()
