#!/usr/bin/env python3
"""Run a single skill/agent test end-to-end and write result.md.

Pipeline:

  1. Parse test.md (scenario, prompt, criteria, output expectations)
  2. Spawn an isolated workspace under $TMPDIR with vanilla CLAUDE_CONFIG_DIR
  3. Invoke `claude -p --plugin-dir <plugin>` with the test prompt
  4. Capture the result
  5. Invoke a second `claude -p` instance with judge-prompt.md as the system prompt,
     feeding it the criteria and captured output
  6. Parse the judge's JSON response
  7. Write result.md to the test directory

Designed to be portable — no turtlestack-specific paths or assumptions.
Downstream projects can vendor this script and use it against their own
plugin/test layout.

Exit codes:
  0  PASS (>= 80%)
  1  PARTIAL (>= 60%)
  2  FAIL (< 60%)
  3+ infrastructure error (workspace setup, claude invocation, judge failure)
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
import uuid
from dataclasses import dataclass, field
from pathlib import Path

EXIT_PASS = 0
EXIT_PARTIAL = 1
EXIT_FAIL = 2
EXIT_INFRA = 3


@dataclass
class TestCase:
    scenario: str
    prompt: str
    criteria: list[str]
    output_expectations: list[str]
    test_dir: Path

    @property
    def all_criteria(self) -> list[str]:
        return self.criteria + self.output_expectations


@dataclass
class TargetRun:
    result_text: str
    duration_ms: int
    cost_usd: float
    tool_uses: int
    permission_denials: list[dict]
    raw_json: dict
    artifacts: dict[str, str] = field(default_factory=dict)


@dataclass
class JudgeOutput:
    verdict: str
    score_points: float
    score_max: float
    score_pct: float
    criteria: list[dict]
    notes: str
    raw_text: str


@dataclass
class RunConfig:
    test_dir: Path
    plugin_dir: Path
    target_model: str
    judge_model: str
    judge_prompt_path: Path
    extra_env: dict[str, str] = field(default_factory=dict)
    workspace_root: Path | None = None
    keep_workspace: bool = False
    timeout_sec: int = 300
    isolate_config: bool = False


def parse_test_md(test_dir: Path) -> TestCase:
    test_path = test_dir / "test.md"
    if not test_path.exists():
        raise FileNotFoundError(f"test.md not found at {test_path}")
    text = test_path.read_text()

    sections: dict[str, str] = {}
    current = "_preamble"
    buf: list[str] = []
    for line in text.splitlines():
        m = re.match(r"^##\s+(.+?)\s*$", line)
        if m:
            sections[current] = "\n".join(buf).strip()
            current = m.group(1).strip().lower()
            buf = []
        else:
            buf.append(line)
    sections[current] = "\n".join(buf).strip()

    scenario = sections.get("_preamble", "").strip()
    scenario_lines = [l for l in scenario.splitlines() if l.strip() and not l.startswith("#")]
    scenario_text = " ".join(scenario_lines).strip()

    prompt = sections.get("prompt", "").strip()

    criteria = _extract_checkboxes(sections.get("criteria", ""))
    output_expectations = _extract_checkboxes(sections.get("output expectations", ""))

    if not prompt:
        raise ValueError(f"test.md at {test_path} is missing a ## Prompt section")
    if not (criteria or output_expectations):
        raise ValueError(
            f"test.md at {test_path} has no checkbox criteria under ## Criteria or ## Output expectations"
        )

    return TestCase(
        scenario=scenario_text,
        prompt=prompt,
        criteria=criteria,
        output_expectations=output_expectations,
        test_dir=test_dir,
    )


def _extract_checkboxes(section: str) -> list[str]:
    items: list[str] = []
    for line in section.splitlines():
        m = re.match(r"^\s*-\s*\[\s*[ xX~]?\s*\]\s*(.+?)\s*$", line)
        if m:
            items.append(m.group(1).strip())
    return items


def make_workspace(root: Path | None) -> Path:
    base = root or Path(os.environ.get("TMPDIR", "/tmp"))
    base.mkdir(parents=True, exist_ok=True)
    runid = f"eval-{int(time.time())}-{uuid.uuid4().hex[:8]}"
    ws = base / runid
    (ws / "work").mkdir(parents=True)
    (ws / "config").mkdir()
    (ws / "learnings").mkdir()
    (ws / "rules").mkdir()
    (ws / "global-learnings").mkdir()
    (ws / "global-rules").mkdir()
    (ws / "handoff").mkdir()

    work = ws / "work"
    subprocess.run(["git", "init", "-q"], cwd=work, check=True)
    (work / "README.md").write_text("# eval workspace\n")
    subprocess.run(["git", "add", "."], cwd=work, check=True)
    subprocess.run(
        ["git", "-c", "user.email=eval@local", "-c", "user.name=eval",
         "commit", "-qm", "initial"],
        cwd=work, check=True,
    )
    return ws


def env_for_run(workspace: Path, extra: dict[str, str], isolate_config: bool) -> dict[str, str]:
    env = os.environ.copy()
    # CLAUDE_CONFIG_DIR isolates the global ~/.claude state — but it also
    # isolates auth (keychain reads target the real path, the redirect breaks
    # auth resolution). Only enable when ANTHROPIC_API_KEY is set or the user
    # has explicitly opted in via --isolate-config.
    if isolate_config:
        env["CLAUDE_CONFIG_DIR"] = str(workspace / "config")
    env["LEARNINGS_DIR"] = str(workspace / "learnings")
    env["RULES_DIR"] = str(workspace / "rules")
    env["GLOBAL_LEARNINGS_DIR"] = str(workspace / "global-learnings")
    env["GLOBAL_RULES_DIR"] = str(workspace / "global-rules")
    env["HANDOFF_DIR"] = str(workspace / "handoff")
    env.update(extra)
    return env


def _resolve_plugin_dirs(cfg: RunConfig, test: TestCase) -> list[Path]:
    """Return the list of --plugin-dir paths to pass to claude.

    When cfg.plugin_dir is a root directory (no plugin.json), try to derive
    the specific plugin directory from the test path:
      examples/<category>/<plugin>/... -> cfg.plugin_dir/<category>/<plugin>

    Keeps the root as a fallback so marketplace.json / settings-based plugins
    still apply alongside the derived specific plugin.
    """
    plugin_json = cfg.plugin_dir / ".claude-plugin" / "plugin.json"
    if plugin_json.exists():
        return [cfg.plugin_dir]

    # Root-style path: try to find the specific plugin from test path
    parts = test.test_dir.parts
    for i, part in enumerate(parts):
        if part == "examples" and i + 2 < len(parts):
            candidate = cfg.plugin_dir / parts[i + 1] / parts[i + 2]
            if (candidate / ".claude-plugin" / "plugin.json").exists():
                return [cfg.plugin_dir, candidate]
            break

    return [cfg.plugin_dir]


def run_target(cfg: RunConfig, test: TestCase, workspace: Path) -> TargetRun:
    plugin_dirs = _resolve_plugin_dirs(cfg, test)
    plugin_dir_args: list[str] = []
    for pd in plugin_dirs:
        plugin_dir_args += ["--plugin-dir", str(pd)]

    cmd = [
        "claude", "-p",
        *plugin_dir_args,
        "--output-format", "json",
        "--dangerously-skip-permissions",
        "--add-dir", str(workspace / "handoff"),
        "--add-dir", str(workspace / "learnings"),
        "--add-dir", str(workspace / "rules"),
        "--model", cfg.target_model,
        test.prompt,
    ]
    work = workspace / "work"
    env = env_for_run(workspace, cfg.extra_env, cfg.isolate_config)

    proc = subprocess.run(
        cmd, cwd=work, env=env,
        capture_output=True, text=True, timeout=cfg.timeout_sec,
    )
    if proc.returncode != 0:
        raise RuntimeError(
            f"claude target invocation failed (exit {proc.returncode})\n"
            f"stderr: {proc.stderr[:2000]}"
        )
    try:
        data = json.loads(proc.stdout)
    except json.JSONDecodeError as e:
        raise RuntimeError(f"target returned non-JSON output: {e}\n{proc.stdout[:1000]}")

    artifacts = _snapshot_artifacts(workspace)

    return TargetRun(
        result_text=data.get("result", ""),
        duration_ms=int(data.get("duration_ms", 0)),
        cost_usd=float(data.get("total_cost_usd", 0.0)),
        tool_uses=int(data.get("num_turns", 0)),
        permission_denials=data.get("permission_denials", []),
        raw_json=data,
        artifacts=artifacts,
    )


def _snapshot_artifacts(workspace: Path) -> dict[str, str]:
    """Read every file the target wrote into the workspace's path-override dirs.

    The judge needs to see the actual artifacts the skill produced, not just the
    chat response. A skill that writes a 200-line handoff doc to disk and prints
    a one-line confirmation would otherwise be judged on the confirmation alone.
    """
    artifacts: dict[str, str] = {}
    for sub in ("handoff", "learnings", "rules", "global-learnings", "global-rules"):
        root = workspace / sub
        if not root.exists():
            continue
        for path in root.rglob("*"):
            if not path.is_file():
                continue
            rel = path.relative_to(workspace)
            try:
                text = path.read_text()
            except (UnicodeDecodeError, OSError):
                continue
            if len(text) > 50_000:
                text = text[:50_000] + "\n\n[truncated — over 50KB]"
            artifacts[str(rel)] = text
    _SKIP_DIRS = {".git", ".claude", ".venv", "venv", "node_modules", "__pycache__",
                  ".tox", ".pytest_cache", "dist", "build", ".mypy_cache",
                  "bin", "obj", ".nuget", "packages", ".gradle", "target"}
    work_files = (workspace / "work").rglob("*")
    for path in work_files:
        if not path.is_file():
            continue
        rel = path.relative_to(workspace)
        if any(p in rel.parts for p in _SKIP_DIRS):
            continue
        if rel.name == "README.md" and rel.parent.name == "work":
            continue
        try:
            text = path.read_text(errors="replace")
            text = text.replace("\x00", "")
        except (UnicodeDecodeError, OSError):
            continue
        if len(text) > 50_000:
            text = text[:50_000] + "\n\n[truncated]"
        artifacts[str(rel)] = text
    return artifacts


def run_judge(cfg: RunConfig, test: TestCase, target: TargetRun, workspace: Path) -> JudgeOutput:
    judge_system = cfg.judge_prompt_path.read_text()

    criteria_lines = []
    for i, c in enumerate(test.all_criteria, start=1):
        criteria_lines.append(f"c{i}. {c}")
    criteria_block = "\n".join(criteria_lines)

    artifacts_block = ""
    if target.artifacts:
        parts = ["## ARTIFACTS WRITTEN\n"]
        parts.append(
            "Files the target wrote to disk during execution. Judge against these "
            "where the criterion asks about file contents — not just the chat response.\n"
        )
        for path, text in target.artifacts.items():
            parts.append(f"\n### `{path}`\n\n```\n{text}\n```\n")
        artifacts_block = "\n".join(parts) + "\n"

    user_msg = (
        "## TEST\n\n"
        f"**Scenario:** {test.scenario}\n\n"
        f"**Prompt:**\n\n```\n{test.prompt}\n```\n\n"
        "## CAPTURED OUTPUT (chat response)\n\n"
        f"```\n{target.result_text}\n```\n\n"
        f"{artifacts_block}"
        "## CRITERIA TO SCORE\n\n"
        f"{criteria_block}\n\n"
        "Score every criterion. Return only the JSON object specified in your system prompt."
    )

    # We deliberately don't use --bare here — bare mode requires
    # ANTHROPIC_API_KEY/apiKeyHelper for auth and fails without them.
    # Plain headless mode keeps keychain auth and is enough for a single
    # judge call.
    cmd = [
        "claude", "-p",
        "--append-system-prompt", judge_system,
        "--output-format", "json",
        "--model", cfg.judge_model,
    ]
    judge_workspace = workspace / "judge"
    judge_workspace.mkdir(exist_ok=True)
    judge_env = os.environ.copy()
    if cfg.isolate_config:
        judge_env["CLAUDE_CONFIG_DIR"] = str(workspace / "config")

    proc = subprocess.run(
        cmd, cwd=judge_workspace, env=judge_env,
        input=user_msg,
        capture_output=True, text=True, timeout=cfg.timeout_sec,
    )
    if proc.returncode != 0:
        raise RuntimeError(
            f"judge invocation failed (exit {proc.returncode})\n"
            f"stderr: {proc.stderr[:2000]}"
        )
    try:
        outer = json.loads(proc.stdout)
    except json.JSONDecodeError as e:
        raise RuntimeError(f"judge returned non-JSON wrapper: {e}\n{proc.stdout[:500]}")

    raw_text = outer.get("result", "").strip()
    inner_json = _extract_json_block(raw_text)
    if inner_json is None:
        raise RuntimeError(f"judge response did not contain a JSON object:\n{raw_text[:1000]}")

    return JudgeOutput(
        verdict=inner_json["verdict"],
        score_points=float(inner_json["score_points"]),
        score_max=float(inner_json["score_max"]),
        score_pct=float(inner_json["score_pct"]),
        criteria=inner_json["criteria"],
        notes=inner_json.get("notes", ""),
        raw_text=raw_text,
    )


def _extract_json_block(text: str) -> dict | None:
    text = text.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*\n?", "", text)
        text = re.sub(r"\n?```\s*$", "", text)
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    m = re.search(r"\{.*\}", text, re.DOTALL)
    if m:
        try:
            return json.loads(m.group(0))
        except json.JSONDecodeError:
            return None
    return None


def write_result_md(test: TestCase, target: TargetRun, judge: JudgeOutput) -> Path:
    result_path = test.test_dir / "result.md"
    today = time.strftime("%Y-%m-%d")

    lines: list[str] = []
    title = test.test_dir.name.replace("-", " ").title()
    lines.append(f"# {title}")
    lines.append("")
    if test.scenario:
        lines.append(test.scenario)
        lines.append("")
    lines.append("## Prompt")
    lines.append("")
    lines.append("> " + test.prompt.replace("\n", "\n> "))
    lines.append("")
    lines.append("## Output")
    lines.append("")
    lines.append("Captured from a real headless invocation of the skill/agent.")
    lines.append("")
    lines.append("### Chat response")
    lines.append("")
    lines.append(target.result_text)
    lines.append("")
    if target.artifacts:
        lines.append("### Artifacts written")
        lines.append("")
        for path, text in target.artifacts.items():
            lines.append(f"#### `{path}`")
            lines.append("")
            lines.append("```")
            lines.append(text)
            lines.append("```")
            lines.append("")
    lines.append("## Evaluation")
    lines.append("")
    lines.append("| Field | Value |")
    lines.append("|---|---|")
    lines.append(f"| Verdict | {judge.verdict} |")
    lines.append(f"| Score | {judge.score_points}/{judge.score_max} ({judge.score_pct:.0f}%) |")
    lines.append(f"| Evaluated | {today} |")
    lines.append(f"| Target duration | {target.duration_ms} ms |")
    lines.append(f"| Target cost | ${target.cost_usd:.4f} |")
    lines.append(f"| Permission denials | {len(target.permission_denials)} |")
    lines.append("")
    lines.append("### Criteria")
    lines.append("")
    lines.append("| # | Criterion | Result | Evidence |")
    lines.append("|---|---|---|---|")
    for c in judge.criteria:
        crit_text = c.get("text", "").replace("|", "\\|")
        evidence = c.get("evidence", "").replace("|", "\\|").replace("\n", " ")
        lines.append(f"| {c.get('id', '')} | {crit_text} | {c.get('result', '')} | {evidence} |")
    lines.append("")
    if judge.notes:
        lines.append("### Notes")
        lines.append("")
        lines.append(judge.notes)
        lines.append("")

    result_path.write_text("\n".join(lines))
    return result_path


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    p.add_argument("--test-dir", required=True, type=Path,
                   help="Path to a test directory (containing test.md)")
    p.add_argument("--plugin-dir", required=True, type=Path,
                   help="Path to the plugin directory under test (contains .claude-plugin/plugin.json)")
    p.add_argument("--target-model", default="claude-haiku-4-5-20251001",
                   help="Model to invoke for the skill/agent under test")
    p.add_argument("--judge-model", default="claude-sonnet-4-6",
                   help="Model to invoke for scoring the captured output")
    p.add_argument("--judge-prompt", type=Path,
                   default=Path(__file__).resolve().parent / "judge-prompt.md",
                   help="Judge system prompt template")
    p.add_argument("--workspace-root", type=Path,
                   help="Override base directory for the per-run workspace")
    p.add_argument("--keep-workspace", action="store_true",
                   help="Don't delete the workspace after the run")
    p.add_argument("--env", action="append", default=[],
                   metavar="KEY=VALUE",
                   help="Extra environment variable for the target run (repeatable)")
    p.add_argument("--timeout", type=int, default=300,
                   help="Timeout in seconds for both target and judge invocations")
    p.add_argument("--isolate-config", action="store_true",
                   help="Set CLAUDE_CONFIG_DIR to the workspace (full vanilla global state). "
                        "Requires ANTHROPIC_API_KEY in the environment — keychain auth "
                        "will not resolve through the redirected config dir.")
    p.add_argument("--write-result", action="store_true", default=True,
                   help="Write result.md to the test directory (default: true)")
    p.add_argument("--no-write-result", dest="write_result", action="store_false",
                   help="Skip writing result.md (still emits JSON to stdout)")
    return p.parse_args()


def main() -> int:
    args = parse_args()

    extra_env = {}
    for kv in args.env:
        if "=" not in kv:
            print(f"Invalid --env value (expected KEY=VALUE): {kv}", file=sys.stderr)
            return EXIT_INFRA
        k, v = kv.split("=", 1)
        extra_env[k.strip()] = v

    cfg = RunConfig(
        test_dir=args.test_dir.resolve(),
        plugin_dir=args.plugin_dir.resolve(),
        target_model=args.target_model,
        judge_model=args.judge_model,
        judge_prompt_path=args.judge_prompt.resolve(),
        extra_env=extra_env,
        workspace_root=args.workspace_root.resolve() if args.workspace_root else None,
        keep_workspace=args.keep_workspace,
        timeout_sec=args.timeout,
        isolate_config=args.isolate_config,
    )

    print(f"[run-test] reading {cfg.test_dir}/test.md", file=sys.stderr)
    test = parse_test_md(cfg.test_dir)
    print(f"[run-test] {len(test.all_criteria)} criteria parsed", file=sys.stderr)

    workspace = make_workspace(cfg.workspace_root)
    print(f"[run-test] workspace: {workspace}", file=sys.stderr)

    try:
        print("[run-test] invoking target...", file=sys.stderr)
        target = run_target(cfg, test, workspace)
        print(f"[run-test] target done in {target.duration_ms}ms, "
              f"${target.cost_usd:.4f}, denials={len(target.permission_denials)}",
              file=sys.stderr)

        print("[run-test] invoking judge...", file=sys.stderr)
        judge = run_judge(cfg, test, target, workspace)
        print(f"[run-test] judge: {judge.verdict} {judge.score_points}/{judge.score_max} "
              f"({judge.score_pct:.0f}%)", file=sys.stderr)

        if args.write_result:
            result_path = write_result_md(test, target, judge)
            print(f"[run-test] wrote {result_path}", file=sys.stderr)

        summary = {
            "test_dir": str(cfg.test_dir),
            "verdict": judge.verdict,
            "score_points": judge.score_points,
            "score_max": judge.score_max,
            "score_pct": judge.score_pct,
            "target_duration_ms": target.duration_ms,
            "target_cost_usd": target.cost_usd,
            "target_denials": len(target.permission_denials),
            "result_md": str(cfg.test_dir / "result.md") if args.write_result else None,
        }
        print(json.dumps(summary, indent=2))
    finally:
        if not cfg.keep_workspace:
            shutil.rmtree(workspace, ignore_errors=True)
            print(f"[run-test] cleaned up {workspace}", file=sys.stderr)
        else:
            print(f"[run-test] kept workspace at {workspace}", file=sys.stderr)

    if judge.verdict == "PASS":
        return EXIT_PASS
    if judge.verdict == "PARTIAL":
        return EXIT_PARTIAL
    return EXIT_FAIL


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        print(f"[run-test] infrastructure error: {e}", file=sys.stderr)
        sys.exit(EXIT_INFRA)
