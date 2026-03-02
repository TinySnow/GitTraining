#!/usr/bin/env python3
# =============================================================================
# 学海计划 - 标题图片批量生成工具
# =============================================================================
#
# 【功能】
#   读取 XMind 思维导图或纯文本列表，为每个主题生成一张标题图片。
#   图片样式：纯白背景，第一行"学海计划"，第二行为具体主题，
#   高度固定 200px，宽度根据文字自适应（含左右留白）。
#
# 【依赖】
#   pip install Pillow
#
# 【用法】
#
#   ① 从 XMind 文件生成全部画布：
#         python3 generate_titles.py
#      （默认读取 ../学海计划.xmind，也可显式指定：--xmind 其他路径.xmind）
#      输出结构：
#         output/
#         ├── 医学/
#         │   ├── 药理学.png
#         │   └── 不良反应.png
#         ├── 文学/
#         │   └── 写作手法.png
#         └── ...
#
#   ② 只重新渲染某一个画布（XMind 源文件有改动时使用）：
#         python3 generate_titles.py --xmind 学海计划.xmind --sheet 医学
#      仅处理名为"医学"的画布，其他画布不受影响。
#      画布名称需与 XMind 中的标签页名称完全一致。
#
#   ③ 列出 XMind 中所有画布名称（不生成图片，用于确认 --sheet 的名称）：
#         python3 generate_titles.py --xmind 学海计划.xmind --list-sheets
#
#   ④ 生成单张图片（临时测试用）：
#         python3 generate_titles.py --topic "不良反应"
#      图片直接输出到 OUTPUT_DIR 根目录，不建子文件夹。
#
#   ⑤ 从纯文本文件批量生成（不使用 XMind 时）：
#         python3 generate_titles.py --list topics.txt
#      topics.txt 格式：每行一个主题，# 开头为注释，空行忽略。
#      若文件不存在，脚本会自动创建一个示例文件。
#
# 【配置】
#   修改下方"配置区"中的变量即可调整字体、尺寸、颜色等。
# =============================================================================

import os
import sys
import argparse
import zipfile
import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

# ─── 配置区（按需修改） ───────────────────────────────────────
FONT_PATH  = "../fonts/仓耳与墨W02.ttf"  # 字体文件路径（.ttf / .otf）
OUTPUT_DIR = "../covers"            # 图片输出根目录
FONT_SIZE  = 60                    # 字号（px）
IMG_HEIGHT = 400                   # 图片高度（px），固定不变
PADDING_X  = 200                    # 左右留白（px），图片宽度 = 最长文字宽 + PADDING_X * 2
LINE_GAP   = 12                    # 两行文字之间的间距（px）
TEXT_COLOR = "#3d3d3d"             # 文字颜色
BG_COLOR   = "#ffffff"             # 背景颜色
TITLE_LINE = "学海计划"            # 固定第一行文字
# ─────────────────────────────────────────────────────────────


def load_font(size: int) -> ImageFont.FreeTypeFont:
    """
    加载字体文件。
    若字体文件不存在，打印明确提示后退出，避免静默使用默认字体产生错误输出。
    """
    path = Path(FONT_PATH)
    if not path.exists():
        print(f"[ERROR] 字体文件未找到：{FONT_PATH}")
        print("        请将字体文件放到脚本同目录，或修改脚本顶部 FONT_PATH 变量。")
        sys.exit(1)
    return ImageFont.truetype(str(path), size)


def make_image(topic: str, font: ImageFont.FreeTypeFont) -> Image.Image:
    """
    生成单张标题图片。

    原理：
      1. 用 1x1 的临时画布预测量两行文字的宽高（避免真正绘图前不知道尺寸）。
      2. 图片宽度 = max(第一行宽, 第二行宽) + 左右留白；高度固定为 IMG_HEIGHT。
      3. 两行文字整体在垂直方向居中，每行在水平方向居中。
    """
    # ── 步骤 1：测量文字尺寸 ──
    tmp  = Image.new("RGB", (1, 1))
    draw = ImageDraw.Draw(tmp)

    def measure(text):
        # textbbox 返回 (left, top, right, bottom)，差值即为宽高
        bbox = draw.textbbox((0, 0), text, font=font)
        return bbox[2] - bbox[0], bbox[3] - bbox[1]

    w1, h1 = measure(TITLE_LINE)   # 第一行"学海计划"的宽高
    w2, h2 = measure(topic)        # 第二行主题文字的宽高

    # ── 步骤 2：计算图片尺寸和文字起始坐标 ──
    img_width    = max(w1, w2) + PADDING_X * 2
    total_text_h = h1 + LINE_GAP + h2
    y_start      = (IMG_HEIGHT - total_text_h) // 2   # 整体垂直居中的起点

    # ── 步骤 3：绘制 ──
    img  = Image.new("RGB", (img_width, IMG_HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(img)

    # 每行分别水平居中：x = (图片宽 - 文字宽) / 2
    draw.text(((img_width - w1) // 2, y_start),                   TITLE_LINE, font=font, fill=TEXT_COLOR)
    draw.text(((img_width - w2) // 2, y_start + h1 + LINE_GAP),   topic,      font=font, fill=TEXT_COLOR)

    return img


def sanitize(name: str) -> str:
    """
    将字符串中 Windows / Linux 文件系统不允许出现在文件名或目录名中的字符，
    替换为视觉相近的全角字符，确保文件名合法且显示内容基本不变。

    非法字符对照：
      /  →  ／      \\  →  ＼     :  →  ：
      *  →  ＊      ?  →  ？     "  →  ＂
      <  →  ＜      >  →  ＞     |  →  ｜
    """
    return (name
        .replace("/",  "／").replace("\\", "＼").replace(":",  "：")
        .replace("*",  "＊").replace("?",  "？").replace('"',  "＂")
        .replace("<",  "＜").replace(">",  "＞").replace("|",  "｜"))


def save_image(img: Image.Image, topic: str, subfolder: str = "") -> str:
    """
    将图片保存到指定位置。

    参数：
      img       - 已生成的 PIL Image 对象
      topic     - 主题文字，用作文件名（自动净化非法字符）
      subfolder - 子文件夹名（通常为画布名），为空则直接存入 OUTPUT_DIR

    返回保存后的完整路径。
    """
    # 若指定了子文件夹（画布名），则在 OUTPUT_DIR 下建对应子目录
    out_dir = os.path.join(OUTPUT_DIR, sanitize(subfolder)) if subfolder else OUTPUT_DIR
    os.makedirs(out_dir, exist_ok=True)

    filename = f"{sanitize(topic)}.png"
    out_path = os.path.join(out_dir, filename)
    img.save(out_path, "PNG")

    # 控制台输出带画布名前缀，方便追踪进度
    prefix = f"[{subfolder}] " if subfolder else ""
    print(f"  ✓ {prefix}{filename}")
    return out_path


def parse_xmind(xmind_path: str) -> list[tuple]:
    """
    解析 XMind ZEN 格式（.xmind）文件，提取所有画布中的主题节点。

    XMind .xmind 文件本质上是一个 ZIP 压缩包，其中 content.json 记录了
    所有画布（sheet）和节点（topic）的树形结构。

    返回值：[(画布名, 主题文字), ...] 按文件中原始顺序排列。

    跳过规则：
      - 根节点（每个画布的顶层节点，通常是画布标题本身）
      - 含有 'You are here' 的节点（路径标记，非内容节点）
      - 空标题节点
    """
    try:
        results = []

        def walk(node, sheet_name, is_root=False):
            """递归遍历节点树，将符合条件的节点追加到 results。"""
            title    = node.get("title", "").strip()
            children = node.get("children", {}).get("attached", [])

            # 根节点和标记节点不生成图片，其余均收录（含中间节点和叶节点）
            if not is_root and "You are here" not in title and title:
                results.append((sheet_name, title))

            for child in children:
                walk(child, sheet_name)

        with zipfile.ZipFile(xmind_path) as z:
            if "content.json" not in z.namelist():
                print("[WARN] 未找到 content.json，请确认使用的是 XMind ZEN（.xmind）格式。")
                return results

            data = json.loads(z.read("content.json"))

            for sheet in data:
                # 画布名取 XMind 标签页的 title，空时兜底为"未命名画布"
                sheet_name = sheet.get("title", "").strip() or "未命名画布"
                walk(sheet.get("rootTopic", {}), sheet_name, is_root=True)

        return results

    except zipfile.BadZipFile:
        print(f"[ERROR] 无法打开文件，请确认 {xmind_path} 是有效的 .xmind 文件。")
        sys.exit(1)
    except Exception as e:
        print(f"[ERROR] 解析 XMind 失败：{e}")
        sys.exit(1)


def read_topics_file(path: str) -> list[str]:
    """
    从纯文本文件逐行读取主题列表。
    格式规则：# 开头的行视为注释，空行忽略，其余每行作为一个主题。
    """
    with open(path, encoding="utf-8") as f:
        return [
            line.strip()
            for line in f
            if line.strip() and not line.strip().startswith("#")
        ]


# ─── 主流程 ───────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(
        description="学海计划标题图片批量生成工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "示例：\n"
            "  python3 generate_titles.py\n"
            "  python3 generate_titles.py --sheet 医学\n"
            "  python3 generate_titles.py --list-sheets\n"
            "  python3 generate_titles.py --xmind 其他路径.xmind\n"
            "  python3 generate_titles.py --topic \"不良反应\"\n"
            "  python3 generate_titles.py --list topics.txt\n"
        )
    )

    parser.add_argument("--xmind",       metavar="FILE", default="../学海计划.xmind",
                        help="指定 XMind 文件路径（默认：../学海计划.xmind）")
    parser.add_argument("--sheet",       metavar="NAME",
                        help="仅处理指定名称的画布（配合 --xmind 使用）")
    parser.add_argument("--list-sheets", action="store_true",
                        help="列出 XMind 中所有画布名称后退出，不生成图片（配合 --xmind 使用）")
    parser.add_argument("--topic",       metavar="TEXT",
                        help="生成单张图片，直接传入主题文字")
    parser.add_argument("--list",        metavar="FILE",  nargs="?", const="topics.txt",
                        help="从文本文件批量生成（默认 topics.txt）")

    args = parser.parse_args()

    # ── 模式一：列出画布名称 ──────────────────────────────────
    # 仅打印画布列表，方便用户确认 --sheet 参数应填写的名称，不生成任何图片
    if args.list_sheets:
        if not args.xmind:
            print("[ERROR] --list-sheets 需要配合 --xmind 使用。")
            sys.exit(1)
        items  = parse_xmind(args.xmind)
        # 用 dict.fromkeys 去重且保持原始顺序（Python 3.7+ 字典有序）
        sheets = list(dict.fromkeys(s for s, _ in items))
        print(f"共 {len(sheets)} 个画布：")
        for i, name in enumerate(sheets, 1):
            count = sum(1 for s, _ in items if s == name)
            print(f"  {i:>3}. {name}  ({count} 个主题)")
        return

    # ── 加载字体（所有生成模式共用） ─────────────────────────
    font = load_font(FONT_SIZE)
    print(f"字体加载成功：{FONT_PATH}")
    print(f"输出目录：{OUTPUT_DIR}/\n")

    # ── 模式二：从 XMind 文件生成 ────────────────────────────
    if args.xmind:
        all_items = parse_xmind(args.xmind)

        if args.sheet:
            # 过滤：只保留与 --sheet 完全匹配的画布条目
            items = [(s, t) for s, t in all_items if s == args.sheet]
            if not items:
                # 找不到时列出可用画布名，方便用户核对拼写
                all_sheets = list(dict.fromkeys(s for s, _ in all_items))
                print(f"[ERROR] 未找到名为「{args.sheet}」的画布。")
                print("        可用的画布名称（可用 --list-sheets 查看完整列表）：")
                for name in all_sheets:
                    print(f"          - {name}")
                sys.exit(1)
            print(f"仅处理画布「{args.sheet}」，共 {len(items)} 个主题\n")
        else:
            # 未指定 --sheet，处理全部画布
            items  = all_items
            sheets = list(dict.fromkeys(s for s, _ in items))
            print(f"处理全部 {len(sheets)} 个画布，共 {len(items)} 个主题\n")

        for sheet, topic in items:
            img = make_image(topic, font)
            save_image(img, topic, subfolder=sheet)

        print(f"\n全部完成，共生成 {len(items)} 张图片。")
        return

    # ── 模式三：生成单张 ──────────────────────────────────────
    if args.topic:
        img = make_image(args.topic, font)
        save_image(img, args.topic)
        print("\n完成。")
        return

    # ── 模式四：从文本文件批量生成 ───────────────────────────
    list_path = args.list or "topics.txt"
    if not Path(list_path).exists():
        # 自动创建示例文件，降低首次使用门槛
        Path(list_path).write_text(
            "# 每行一个主题，# 开头为注释，空行忽略\n"
            "不良反应\n药代动力学\n受体理论\n",
            encoding="utf-8"
        )
        print(f"已创建示例文件 {list_path}，请填写主题后重新运行。")
        return

    topics = read_topics_file(list_path)
    print(f"从 {list_path} 读取到 {len(topics)} 个主题\n")
    for topic in topics:
        img = make_image(topic, font)
        save_image(img, topic)
    print(f"\n全部完成，共生成 {len(topics)} 张图片。")


if __name__ == "__main__":
    main()
