#!/usr/bin/env bash
# Import downloaded Survival Field Encyclopedia artifacts without modifying main.
# Usage: bash import_survival_downloads.sh --dry-run [folder]
#        bash import_survival_downloads.sh --push [folder]
set -Eeuo pipefail

MODE="${1:---dry-run}"
SOURCE="${2:-$HOME/Downloads}"
REPO_URL="https://github.com/Davisjxxxx/Survival_Guide.git"
BRANCH="review/b013-b014-field-drafts-20261122"

case "$MODE" in
  --dry-run|--push) ;;
  *) printf 'Usage: %s [--dry-run|--push] [folder]\n' "$0" >&2; exit 2 ;;
esac
[[ -d "$SOURCE" ]] || { printf 'Directory not found: %s\n' "$SOURCE" >&2; exit 1; }
SOURCE="$(cd "$SOURCE" && pwd -P)"

# Select only known project-named files or items inside named project folders.
# Do not scan unrelated downloads into a public repository.
files=()
while IFS= read -r -d '' file; do
  rel="${file#"$SOURCE"/}"
  lower="${rel,,}"
  case "/$lower" in
    */.git/*|*/.ssh/*|*/.env|*/.env.*|*/id_rsa*|*/id_ed25519*|*.pem|*.p12|*.pfx|*.key|*.crdownload|*.part)
      continue ;;
  esac
  # A project code must be B followed by exactly three digits and a separator.
  # In particular, filenames like b4199cca.css are unrelated browser assets.
  # Dedicated Survival_Guide folders may contain non-B-named supporting files.
  case "$lower" in
    survival_guide/*|*/survival_guide/*|survival_field_encyclopedia/*|*/survival_field_encyclopedia/*)
      files+=("$file"); continue ;;
  esac
  base="${lower##*/}"
  case "$base" in
    b[0-9][0-9][0-9]_*|b[0-9][0-9][0-9]-*|b[0-9][0-9][0-9]\ *|b[0-9][0-9][0-9]–*|survival_field_encyclopedia_*|north_woods_scope_amendment*|original_preparedness_reference_*|*_home_resilience_field_manual*|*_small_acreage_self_reliance*|*_thirty_day_outage_operations*|research\ and\ production\ blueprint\ for\ an\ original\ comprehensive\ survival\ manual*)
      files+=("$file") ;;
  esac
done < <(find "$SOURCE" -type f -print0 | sort -z)

printf 'Source: %s\nTarget: %s (%s)\nMatching files: %d\n' "$SOURCE" "$REPO_URL" "$BRANCH" "${#files[@]}"
for file in "${files[@]}"; do
  printf '  %s (%s bytes)\n' "${file#"$SOURCE"/}" "$(stat -c %s "$file")"
done

if [[ "$MODE" == --dry-run ]]; then
  printf '\nPreview only. Inspect this list, then rerun with --push.\n'
  exit 0
fi
if (( ${#files[@]} == 0 )); then
  printf 'Nothing matched; no commit or push performed.\n'
  exit 0
fi
command -v git >/dev/null || { echo 'git is required.' >&2; exit 1; }

work="$(mktemp -d "${TMPDIR:-/tmp}/survival-import.XXXXXXXX")"
cleanup() {
  rc=$?
  if (( rc == 0 )); then rm -rf -- "$work";
  else printf 'Import interrupted. Local Git clone retained at: %s/repo\n' "$work" >&2; fi
}
trap cleanup EXIT

git clone --quiet --single-branch --branch "$BRANCH" "$REPO_URL" "$work/repo"
[[ -n "$(git -C "$work/repo" config user.name || :)" && -n "$(git -C "$work/repo" config user.email || :)" ]] || {
  echo 'Configure git user.name and user.email first.' >&2; exit 1;
}

declare -A existing=()
while IFS= read -r sha; do [[ -n "$sha" ]] && existing["$sha"]=1; done < <(
  git -C "$work/repo" ls-tree -r HEAD | awk '$2=="blob" {print $3}'
)

batch="imports/local-downloads/$(date -u +%Y%m%dT%H%M%SZ)-$$"
manifest="$work/repo/$batch/IMPORT_MANIFEST.tsv"
mkdir -p -- "$(dirname "$manifest")"
printf 'sha256\tsource_relative_path\trepository_path\n' > "$manifest"
added=0
skipped=0
for file in "${files[@]}"; do
  rel="${file#"$SOURCE"/}"
  bytes="$(stat -c %s "$file")"
  if (( bytes >= 95000000 )); then
    printf 'SKIP (>95MB; review Git LFS): %s\n' "$rel" >&2
    ((skipped+=1)); continue
  fi
  blob="$(git -C "$work/repo" hash-object -- "$file")"
  if [[ -n "${existing[$blob]:-}" ]]; then
    printf 'SKIP (already stored, identical bytes): %s\n' "$rel"
    ((skipped+=1)); continue
  fi
  dest="$batch/$rel"
  mkdir -p -- "$(dirname "$work/repo/$dest")"
  cp -- "$file" "$work/repo/$dest"
  sha256="$(sha256sum "$file" | cut -d ' ' -f 1)"
  test "$sha256" = "$(sha256sum "$work/repo/$dest" | cut -d ' ' -f 1)" || {
    printf 'Hash mismatch copying %s\n' "$rel" >&2; exit 1;
  }
  printf '%s\t%s\t%s\n' "$sha256" "$rel" "$dest" >> "$manifest"
  existing["$blob"]=1
  ((added+=1))
done

if (( added == 0 )); then
  printf 'No new files. Skipped %d duplicates/oversize. Nothing pushed.\n' "$skipped"
  exit 0
fi

git -C "$work/repo" add -- "$batch"
# Check our generated manifest only: original PDFs/ZIPs and other research files
# may be binary or contain intentional trailing bytes. Their content is preserved.
git -C "$work/repo" diff --cached --check -- "$batch/IMPORT_MANIFEST.tsv"
git -C "$work/repo" commit --quiet -m "Archive $added downloaded survival guide artifacts (no overwrites)"
git -C "$work/repo" push origin "HEAD:refs/heads/$BRANCH"
local_sha="$(git -C "$work/repo" rev-parse HEAD)"
remote_sha="$(git -C "$work/repo" ls-remote origin "refs/heads/$BRANCH" | cut -f 1)"
[[ "$local_sha" == "$remote_sha" ]] || { echo 'Remote verification failed.' >&2; exit 1; }
printf '\nSUCCESS: %d new file(s), %d skipped. Verified GitHub commit: %s\n' "$added" "$skipped" "$local_sha"
printf 'Review: https://github.com/Davisjxxxx/Survival_Guide/tree/%s\n' "$BRANCH"
