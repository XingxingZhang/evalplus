"""Purpose of this file: Sanitize the code produced by LLMs for the following reasons.
1. Vicuna generated code could miss one white space. We fix the white space to make Vicuna more capable.
2. {Our fault lol.} We find more EOFs tokens afterwards and truncate some messy code afterwards.
"""

import os
from warnings import warn

from tqdm import tqdm

from evalplus.data import (
    get_human_eval_plus,
    get_mbpp_plus,
    load_solutions,
    write_directory,
    write_jsonl,
)
from tools.checker import syntax_check


def remove_unindented_lines(code, ok_starts):
    lines = code.splitlines()
    cut_idx = None
    for i, line in enumerate(lines):
        if any([line.startswith(t) for t in ok_starts]) or line.strip() == "":
            continue

        lspace = len(line) - len(line.lstrip())
        if lspace == 0:
            cut_idx = i
            break

    return "\n".join(lines[:cut_idx])


def to_four_space_indents(old_code):
    new_code = ""
    for line in old_code.splitlines():
        lspace = len(line) - len(line.lstrip())
        if lspace == 3:
            new_code += " "
        new_code += line + "\n"
    return new_code


if __name__ == "__main__":
    import argparse
    import pathlib

    parser = argparse.ArgumentParser()
    parser.add_argument("--samples", type=str, required=True)
    parser.add_argument("--eofs", nargs="+", type=str, default=[])
    parser.add_argument("--inplace", action="store_true")
    parser.add_argument(
        "--rm-prefix-lines", type=str, help="Remove lines starting with this"
    )
    parser.add_argument(
        "--dataset", required=True, type=str, choices=["humaneval", "mbpp"]
    )
    parser.add_argument(
        "--debug-task", type=str, help="Enter the task ID to only sanitize that task."
    )
    args = parser.parse_args()

    # task_id -> entry_point
    entry_point = {}
    prompts = {}

    if args.dataset == "humaneval":
        dataset = get_human_eval_plus()
    elif args.dataset == "mbpp":
        dataset = get_mbpp_plus()

    for task_id, problem in dataset.items():
        entry_point[task_id] = problem["entry_point"]
        prompts[task_id] = problem["prompt"]

    # make a new folder with "-sanitized" suffix
    is_folder = os.path.isdir(args.samples)
    target_path = pathlib.Path(args.samples)
    if not args.inplace:
        if is_folder:
            new_name = target_path.name + "-sanitized"
        else:
            new_name = target_path.name.replace(".jsonl", "-sanitized.jsonl")
        target_path = target_path.parent / new_name
    target_path = str(target_path)

    nsan = 0
    ntotal = 0

    new_solutions = []

    for solution in tqdm(load_solutions(args.samples)):
        task_id = solution["task_id"]
        dbg_identifier = solution["_identifier"]
        if args.debug_task is not None and task_id != args.debug_task:
            continue

        ntotal += 1
        if "solution" in solution:
            old_code = solution["solution"]
        else:
            assert "completion" in solution
            old_code = dataset[task_id] + "\n" + solution["completion"]

        if args.rm_prefix_lines is not None:
            old_code = "\n".join(
                [
                    line
                    for line in old_code.splitlines()
                    if not line.startswith(args.rm_prefix_lines)
                ]
            )

        old_code = "\n" + old_code
        # basic handling of chat output
        for blk in ["\n```python\n", "\n```\n"]:
            old_code = old_code.split(blk, maxsplit=1)[-1].split("\n```", maxsplit=1)[0]
            old_code = "\n" + old_code

        def_left = "def " + entry_point[task_id]
        if def_left not in old_code:
            warn(f"Cannot find {def_left} in {dbg_identifier}. Skipping.")

        if args.dataset == "humaneval":
            imports, def_right = prompts[task_id].split(def_left)
            new_code = imports + def_left + old_code.split(def_left)[-1]
        elif args.dataset == "mbpp":
            new_code = old_code

        chunks = new_code.split(def_left)  # imports + def_left + {def_right + impl}
        new_code = def_left + def_left.join(chunks[1:])  # fn + impl
        new_code = to_four_space_indents(new_code)

        for eof in args.eofs:
            new_code = new_code.split(eof)[0]

        # remove lines that are not indented
        new_code = remove_unindented_lines(new_code, ["def "])
        new_code = chunks[0] + new_code

        # cut off the last function if it is incomplete
        last_fn = "def " + new_code.split("\ndef ")[-1]
        if not syntax_check(last_fn):
            new_code = "\ndef ".join(new_code.split("\ndef ")[:-1])

        # if changed, print the message
        if new_code.strip() != old_code.strip():
            msg = "Sanitized: " + dbg_identifier
            if is_folder:
                msg += " -> " + dbg_identifier.replace(args.samples, target_path)
            print(msg)
            nsan += 1

        new_solutions.append(
            {
                "task_id": solution["task_id"],
                "solution": new_code.strip(),
            }
        )

    if is_folder:
        write_directory(target_path, new_solutions)
    else:
        write_jsonl(target_path, new_solutions)

    print(f"Sanitized {nsan} out of {ntotal} files.")
