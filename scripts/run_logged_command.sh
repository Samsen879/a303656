#!/usr/bin/env bash
set -euo pipefail

if (( $# < 4 )); then
  echo "usage: $0 LOG_DIR TAG -- COMMAND [ARG ...]" >&2
  exit 2
fi

log_dir=$1
tag=$2
shift 2
if [[ $1 != -- ]]; then
  echo "missing -- before command" >&2
  exit 2
fi
shift
if (( $# == 0 )); then
  echo "missing command" >&2
  exit 2
fi
if [[ ! $tag =~ ^[A-Za-z0-9_.-]+$ ]]; then
  echo "invalid log tag: $tag" >&2
  exit 2
fi

record_dir="$log_dir/$tag"
mkdir -p "$log_dir"
if ! mkdir "$record_dir"; then
  echo "refusing to overwrite existing command log: $record_dir" >&2
  exit 2
fi

{
  printf 'working_directory=%q\n' "$PWD"
  printf 'command='
  printf '%q ' "$@"
  printf '\n'
  printf 'started_utc=%s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
} > "$record_dir/command.txt"

set +e
/usr/bin/time -v -o "$record_dir/time.txt" -- "$@" \
  > "$record_dir/stdout.log" \
  2> "$record_dir/stderr.log"
rc=$?
set -e

printf '%s\n' "$rc" > "$record_dir/return_code.txt"
printf 'finished_utc=%s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
  >> "$record_dir/command.txt"
exit "$rc"
