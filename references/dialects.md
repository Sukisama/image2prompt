# 四大目标模型方言（dialects）

同一张图的八维拆解，组装成不同生图模型的"母语"。给错方言是反推失败的第一大原因。

---

## 方言 A：GPT Image 2.x / Nano Banana / 豆包 —— 自然语言散文式

**结构**：风格媒介 → 主体+场景 → 光影色彩 → 构图画幅 → 图中文字（引号逐字）→ 禁止项

**模板**：

```
一张【风格媒介】风格的【图片类型：海报/封面/产品图】。
画面主体是【主体+姿态+特征】，位于【场景描述】。
【光影描述】，【色彩：主色+点缀色+饱和度倾向】。
【构图：景别+机位+构图法则+留白位置】，画幅【比例】。
图中包含以下文字：主标题"XXX"（位置、字体特征、颜色），副标题"XXX"（…）。
不要出现水印、边框、【其他排除项】。
```

**要点**：
- 整段自然语言，像给设计师下 brief，不要逗号标签串
- 文字内容必须用中文引号逐字包裹，并指定位置层级
- 最重要的信息放前面（模型对前 50 词权重更高）
- 多轮改图话术单独给："只把标题改成'XX'，其他保持不变"

---

## 方言 B：即梦 Seedream / 国产模型 —— 中文结构化

**结构**：【图片类型】+【主体】+【排版布局】+【文案（引号包裹）】+【风格氛围】

**模板**：

```
【节日/活动名】海报，主体是【核心画面描述】。
顶部主标题"XXX"（字体特征），中部"XXX"，底部"时间/地点信息"，【二维码区域留白】。
整体【风格：暖色手绘/3D/国风】，色调【主色+点缀色】，文字清晰无错别字。
```

**要点**：中文提示词；文案一律引号包裹；明确写"文字清晰、无错别字"；可用"局部重绘"思路给出后续修改指令。

---

## 方言 C：Midjourney —— 短语 + 参数

**结构**：`subject, scene, style, lighting, color, composition --ar X:Y --s N --v X`

**示例**：

```
a braised meat platter on a wooden board, warm tungsten light from the left, dark moody food photography, shallow depth of field, rich amber and deep brown tones, centered composition --ar 3:4 --s 250 --v 7
```

**要点**：短语逗号分隔；画幅/风格化程度/版本放 `--` 参数；图中文字能力弱，海报类建议文字留到后期加。

---

## 方言 D：SD / Flux —— tags + negative

**结构**：`(quality tags), subject, scene, style, lighting, composition` + 独立 negative prompt

**示例**：

```
masterpiece, best quality, food photography, braised meat platter, wooden board, warm side lighting, dark background, shallow depth of field, amber tones
Negative: watermark, text, logo, blurry, deformed, oversaturated
```

**要点**：权重用 `(word:1.2)`；negative 必填；Flux 对自然语言容忍度高于 SD1.5，但仍以 tags 为主。

---

## 附录：反推用什么视觉模型（model routing）

| 场景 | 推荐模型 | 理由 |
|---|---|---|
| 中文海报/图中大量文字 | Qwen3-VL 系列 | 中文 OCR 最强，能逐字读出图中文字 |
| 单张精品、要"为什么好看"的分析 | GPT-5.5 / Gemini 旗舰 | 视觉推理最强，能分离内容与风格 |
| 批量几十上百张 | Qwen3-VL / GLM-4.5V API | 成本约 ¥1/百万 token 级 |
| 隐私/未发布素材 | 本地 JoyCaption / Ollama 跑 Qwen3-VL | 图不出门；JoyCaption 英文强中文弱 |

**交叉验证技巧**：重要图用两个模型各反推一次，取交集——两个模型一致的部分是可靠信号，分歧的部分人工裁决。
