#!/usr/bin/env bash
# Move the latest version tag (proposal/v* or thesis/v*) to HEAD in the local
# repository, keeping its message. Nothing is pushed.
#
# Usage: scripts/amend_latest_tag.sh
#   DRY_RUN=1   print the git command without running it
set -euo pipefail

run() {
	echo "+ $*"
	if [ "${DRY_RUN:-}" != "1" ]; then "$@"; fi
}

if [ -n "$(git status --porcelain --untracked-files=no)" ]; then
	echo "Error: tracked files have uncommitted changes. Commit them before tagging." >&2
	exit 1
fi

# Highest version number across both phases (proposal/v1, proposal/v2, thesis/v3, ...).
tag="$(git tag -l 'proposal/v*' 'thesis/v*' |
	awk -F'/v' '$2 ~ /^[0-9]+$/ { print $2 "\t" $0 }' |
	sort -n | tail -1 | cut -f2)"
if [ -z "$tag" ]; then
	echo "Error: no proposal/v* or thesis/v* tag found." >&2
	exit 1
fi

head="$(git rev-parse HEAD)"
old="$(git rev-parse "$tag^{commit}")"

if [ "$old" = "$head" ]; then
	echo "$tag already points to HEAD ($(git rev-parse --short "$head"))."
	exit 0
fi

echo "Moving $tag: $(git rev-parse --short "$old") -> $(git rev-parse --short "$head")"
if [ "$(git cat-file -t "$tag")" = "tag" ]; then
	run git tag -f -a "$tag" -m "$(git tag -l --format='%(contents)' "$tag")" "$head"
else
	run git tag -f "$tag" "$head"
fi
