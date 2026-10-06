#!/usr/bin/env python3
"""蜜蜂小狗肿胀指数测试 —— 致敬 2026-10-03 "蜜蜂小狗" 热梗，善意玩梗。

问卷式 CLI：回答 7 个问题，按权重算出 0-100 的"蜜蜂小狗指数"，
分档给出毒舌但善意的评语。纯标准库。
"""
from __future__ import annotations

import argparse
import random
import sys

# 每题：(问题, [(选项文本, 权重), ...])；权重总和上限 100
QUESTIONS: list[tuple[str, list[tuple[str, int]]]] = [
    ("昨晚睡了几小时？", [
        ("不到 4 小时（修仙）", 25),
        ("4-6 小时（勉强续命）", 18),
        ("6-8 小时（正常人）", 8),
        ("8 小时以上（睡眠富翁）", 0),
    ]),
    ("昨晚哭了吗？", [
        ("嚎啕大哭，枕头都湿了", 20),
        ("默默流泪，be like 小狗", 12),
        ("眼眶湿润了一下", 6),
        ("没有，眼泪是珍珠不轻弹", 0),
    ]),
    ("昨晚吃咸了吗？", [
        ("重盐宵夜，快乐加倍", 15),
        ("有点咸，快乐减半", 8),
        ("清淡养生，快乐没被发现", 0),
    ]),
    ("过敏了吗？", [
        ("正在过敏，鼻子眼睛一起抗议", 12),
        ("有点痒，挠也不是不挠也不是", 6),
        ("没有，免疫系统很给面子", 0),
    ]),
    ("揉眼睛了吗？", [
        ("使劲揉，揉出了残影", 10),
        ("轻轻碰了一下", 4),
        ("没有，眼睛是用来看的不是揉的", 0),
    ]),
    ("熬夜刷手机了吗？", [
        ("刷到天亮，手机比我先睡", 8),
        ("刷到半夜，依依不舍", 5),
        ("早睡，手机都没我困", 0),
    ]),
    ("早上照镜子被自己吓到了吗？", [
        ("吓一跳，以为家里进了蜜蜂小狗", 10),
        ("还行，能见人", 3),
        ("美得很，镜子都害羞", 0),
    ]),
]

MAX_SCORE = sum(max(w for _, w in opts) for _, opts in QUESTIONS)
assert MAX_SCORE == 100, f"权重总和应为 100，实际 {MAX_SCORE}"


def compute_score(answers: list[int]) -> int:
    """answers[i] 是第 i 题选的选项下标；返回 0-100 的指数。"""
    if len(answers) != len(QUESTIONS):
        raise ValueError(f"需要回答 {len(QUESTIONS)} 题，实际 {len(answers)} 题")
    total = 0
    for i, a in enumerate(answers):
        opts = QUESTIONS[i][1]
        if not isinstance(a, int) or not 0 <= a < len(opts):
            raise ValueError(f"第 {i + 1} 题选项非法: {a!r}")
        total += opts[a][1]
    return min(total, 100)


def tier(score: int) -> tuple[str, str]:
    """返回 (档位名, 评语)。评语玩梗但保持善意。"""
    if not 0 <= score <= 100:
        raise ValueError(f"指数非法: {score}")
    if score <= 20:
        return ("清澈小狗",
                "眼睛清澈得像小狗刚睡醒，蜜蜂看了都自愧不如。"
                "继续保持，你是人间清醒本醒！")
    if score <= 40:
        return ("微肿小狗",
                "有点肿，但还能见人，属于\"用对了不\"的边缘试探。"
                "敷个眼膜，明天又是一条好汉。")
    if score <= 60:
        return ("蜜蜂小狗预备役",
                "肿胀得恰到好处，再努努力就能持证上岗当蜜蜂小狗了。"
                "建议今晚早睡，不然明天更蜜蜂了。")
    if score <= 80:
        return ("蜜蜂小狗本狗",
                "眼睛肿成表情包，出门记得带墨镜，不然容易被认成热搜本搜。"
                "别慌，冰勺敷一敷，你还是你妈最靓的崽。")
    return ("肿胀天花板",
            "建议直接报备蜜蜂小狗，用对了不！"
            "这肿胀程度，小沈阳看了都得给你递话筒。"
            "开个玩笑啦——好好休息，多喝水，眼睛会感谢你的。")


def describe_answers(answers: list[int]) -> str:
    lines = []
    for i, a in enumerate(answers):
        q, opts = QUESTIONS[i]
        lines.append(f"  Q{i + 1} {q} -> {opts[a][0]}（+{opts[a][1]}）")
    return "\n".join(lines)


def ask_interactive() -> list[int]:
    answers: list[int] = []
    print("=" * 46)
    print("🐝🐶 蜜蜂小狗肿胀指数测试")
    print("致敬 2026-10-03\"蜜蜂小狗\"热梗，善意玩梗，开心就好")
    print("=" * 46)
    for i, (q, opts) in enumerate(QUESTIONS):
        print(f"\nQ{i + 1}/{len(QUESTIONS)} {q}")
        for j, (text, _) in enumerate(opts):
            print(f"  {j + 1}. {text}")
        while True:
            raw = input("请选择 (1-{}): ".format(len(opts))).strip()
            if raw.isdigit() and 1 <= int(raw) <= len(opts):
                answers.append(int(raw) - 1)
                break
            print("  输入非法，请输入 1 到 {} 之间的数字~".format(len(opts)))
    return answers


def report(score: int, verbose: bool = False, answers: list[int] | None = None) -> None:
    name, comment = tier(score)
    print("-" * 46)
    print(f"你的蜜蜂小狗指数：{score} / 100")
    print(f"档位：{name}")
    print(f"评语：{comment}")
    if verbose and answers is not None:
        print("\n答题明细：")
        print(describe_answers(answers))
    print("-" * 46)


def run_auto(n: int, seed: int) -> list[int]:
    rng = random.Random(seed)
    scores: list[int] = []
    print(f"自动测试：随机生成 {n} 个虚拟用户（seed={seed}）")
    print("=" * 46)
    for k in range(n):
        answers = [rng.randrange(len(opts)) for _, opts in QUESTIONS]
        s = compute_score(answers)
        scores.append(s)
        name, _ = tier(s)
        print(f"用户{k + 1:>2}: 指数 {s:>3}  档位「{name}」")
    print("=" * 46)
    print(f"分布统计：最低 {min(scores)}，最高 {max(scores)}，"
          f"平均 {sum(scores) / len(scores):.1f}")
    # 直方图（10 分一档）
    buckets = [0] * 10
    for s in scores:
        buckets[min(s // 10, 9)] += 1
    print("指数分布直方图（每档 10 分）：")
    for i, c in enumerate(buckets):
        print(f"  {i * 10:>3}-{i * 10 + 9:>3}: {'█' * c} ({c})")
    return scores


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="蜜蜂小狗肿胀指数测试 —— 致敬 2026-10-03 热梗")
    parser.add_argument("--auto", action="store_true", help="随机生成虚拟用户自动测试")
    parser.add_argument("--games", type=int, default=10, help="--auto 的虚拟用户数（默认 10）")
    parser.add_argument("--seed", type=int, default=42, help="随机种子（默认 42）")
    parser.add_argument("--verbose", action="store_true", help="打印答题明细")
    args = parser.parse_args(argv)

    if args.auto:
        if args.games <= 0:
            print("games 必须为正整数", file=sys.stderr)
            return 2
        run_auto(args.games, args.seed)
        return 0

    if not sys.stdin.isatty():
        print("交互模式需要终端；非终端请使用 --auto 模式。", file=sys.stderr)
        return 2
    answers = ask_interactive()
    score = compute_score(answers)
    report(score, verbose=args.verbose, answers=answers)
    return 0


if __name__ == "__main__":
    sys.exit(main())
