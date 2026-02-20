#! /usr/bin/env python
"""Tool used to split commits into separate per tool commits."""

import os
import re
import subprocess
import sys
from typing import List


class RebaseExceptionError(Exception):
    """Exceptions used by this tool."""


class CommitEntry:
    """CommitEntry represents a commit."""

    sha: str
    short_message: str
    files: List[str]
    tools_touched: set[str]
    clean: bool

    def __init__(self, sha: str, short_message: str, files: List[str]) -> None:
        """Initializes the CommitEntry."""
        self.sha = sha
        self.short_message = short_message
        self.files = files
        self.tools_touched = set()
        for f in self.files:
            # Just take the two first folders
            # Good enough for a first iteration of the tool
            # Would be cool to make it work regardless of folders
            # which should be possible. Or just make it configurable
            tool_name = "/".join(f.split(os.sep)[:2])
            if tool_name not in self.tools_touched:
                self.tools_touched.add(tool_name)

        self.clean = len(self.tools_touched) <= 1


def gather_commit_state() -> List[CommitEntry]:
    """Gathers commit state for the repo in current working directory."""
    commits = []
    commit_one_line = re.compile("^(\\S*)\\s?(.*\\s*)$")
    all_commit_data_proc = subprocess.Popen(  # noqa: S603
        ["git", "log", "origin..HEAD", "--oneline"],  # noqa: S607, S607, S603
        stdout=subprocess.PIPE,
    )

    for line in all_commit_data_proc.stdout:
        match_groups = commit_one_line.match(line.decode().rstrip()).groups()

        if len(match_groups) != 2:
            raise RebaseExceptionError("Failed to match commit regex.")

        sha, short_message = match_groups

        commit_file_data_proc = subprocess.Popen(
            ["git", "diff", "--name-only", f"{sha}..{sha}~1"],  # noqa: S607, S607, S603
            stdout=subprocess.PIPE,
        )
        files = []
        for f in commit_file_data_proc.stdout:
            commit_file = f.decode().strip()
            files.append(commit_file)

        commits.append(CommitEntry(sha, short_message, files))

    return commits


def run_and_print(args: List[str] | None = None, env: dict | None = None) -> bool:
    """Executes the command and prints out stdout."""
    if args is None:
        args = []

    if env is None:
        env = {}

    print(f'🏃 \x1b[1;36mExecuting:\x1b[0m \x1b[36m{" ".join(args)}\x1b[0m')

    env = os.environ | env
    proc = subprocess.Popen(args, env=env, stdout=subprocess.PIPE)  # noqa: S603
    for line in proc.stdout:
        print(f"\x1b[37m{line.decode().strip()}\x1b[0m")

    return proc.wait() == 0


def split_commits(commits: List[CommitEntry]) -> bool:
    """Splits up the provided commits."""
    split_shas = [split.sha for split in commits]

    env = os.environ | {"SPLIT_COMMITS": " ".join(split_shas)}
    args = [
        "git",
        "-c",
        # As it is delivered with this script we can assume it's in path.
        'sequence.editor="split-commits-sequence-editor"',
        "rebase",
        "-i",
        "origin/main",
    ]
    if not run_and_print(args=args, env=env):
        raise RebaseExceptionError("Failed to run rebase!")

    # We are in an interactive rebase at this point.
    commits.reverse()  # Edits appear in opposite order
    for commit in commits:
        # Get full commit message
        try:
            message = (
                subprocess.check_output(
                    ["git", "log", '--pretty=format:"%B"', "-n", "1", commit.sha],  # noqa: S603, S607
                )
                .decode()
                .strip('"')
            )
        except subprocess.CalledProcessError as e:
            raise RebaseExceptionError(
                f'Getting commit message from commit "{commit.sha}"'
                f" failed with exit code {e.returncode}: {e.output}"
            ) from e

        print(
            f"\x1b[1;32mWorking on commit\x1b[0m"
            f' \x1b[37m"{commit.short_message}"\x1b[0m'
        )

        if not run_and_print(["git", "reset", "HEAD~"]):
            raise RebaseExceptionError("Failed to reset commit in edit!")

        for tool in commit.tools_touched:
            if not run_and_print(args=["git", "add", tool]):
                raise RebaseExceptionError(
                    f"Failed to add files to commit ({commit.sha})!"
                )

            if not run_and_print(
                args=["git", "commit", "-m", f"({tool}) {message}"],
                env=env,
            ):
                raise RebaseExceptionError(
                    f'Failed to commit new split commit for tool "{tool}".'
                )

        if not run_and_print(args=["git", "rebase", "--continue"]):
            print("\x1b[1;33mFailed to continue rebase.\x1b[0m")
            print(
                "Merge conflict? Please check previous"
                " output and fix before continuing."
            )
            print("A = Abort rebase")
            print("C = Continue rebase")
            print("N = Do nothing and exit")
            answer = sys.stdin.readline().rstrip().lower()

            if answer == "a":
                run_and_print(args=["git", "rebase", "--abort"])
                return False

            if answer == "c":
                if not run_and_print(args=["git", "rebase", "--continue"]):
                    raise RebaseExceptionError("Failed to continue rebase.")
            else:
                print("Doing nothing.")
                return True

    return True


if __name__ == "__main__":
    print(f"Working directory: {os.getcwd()}")
    commits = gather_commit_state()
    print("📃 Looking for commits to split!")
    commits_to_split = []
    for commit in commits:
        if commit.clean:
            print(f"🧼 \x1b[1;32mCommit {commit.sha} was clean!\x1b[0m")
            continue

        print(f"🪚 \x1b[1;33m{commit.short_message} ({commit.sha})\x1b[0m")
        print("Touches the following tools.")
        for tool in commit.tools_touched:
            print(f" - {tool}")

        print("\nWould you like to split up the commit for the different tools? (Y/N)")
        answer = sys.stdin.readline().rstrip().lower()
        if answer == "y" or answer == "yes":
            print(
                f"\x1b[32mAdding {commit.short_message} ({commit.sha})"
                " to list of commits to split.\x1b[0m"
            )
            commits_to_split.append(commit)
        else:
            print(f"\x1b[36mSkipping {commit.short_message} ({commit.sha})\x1b[0m")

    print("🪓 Splitting commits!")
    try:
        split_commits(commits_to_split)
    except RebaseExceptionError as e:
        print(f"😤 \x1b[31mRebase failed due to exception: {e}\x1b[0m")
        print("Your git repo is probably in a bad state. Sorry!")
        print("😥")
        sys.exit(1)
    except Exception as e:  # noqa: BLE001
        print(f"😡 \x1b[31mRebase failed due to generic exception: {e}\x1b[0m")
        print("Your git repo is probably in a bad state. Sorry!")
        print("😥")
        sys.exit(2)

    print("🎉 \x1b[1;32mDone!\x1b[0m")
    sys.exit(0)
