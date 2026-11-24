# epstopdf trace findings (session scratch, 2026-11-16) - evidence for RUN-002 continuation

Toolchain: TeX Live 2023 Debian, pdfTeX 1.40.25, graphics-def pdftex.def v1.2b (2022/09/22), epstopdf-base v2.11 (2020-01-24).
No other TeX tree on the machine (find / for pdftex.def / epstopdf-base.sty / epstopdf.sty -> only /usr/share/texlive/texmf-dist).
kpsewhich: shell_escape=p (restricted, system default), openin_any=a (env overrides to p), openout_any=p.
All builds below ran with `--no-shell-escape -recorder`; shell escape never enabled.

## 1. REAL pipeline specimen build (pinned toolchain, hardened flags)
- 170 files read (-recorder .fls); written: sfe.aux, sfe.log, sfe.pdf only.
- epstopdf*/EPS/PS files read: NONE. Converted artifacts: NONE. epstopdf lines in log: NONE.
- \Gin@extensions at \AtEndDocument = .pdf,.png,.jpg,.mps,.jpeg,.jbig2,.jb2,.PDF,.PNG,.JPG,.JPEG,.JBIG2 (no .eps)
- Relative inputs: main.tex, sfe.sty, sfe.aux. Absolute inputs all under /usr/share/texlive|texmf.
- Files read that mention "epstopdf": pdftex.def (11 mentions), l3backend-pdftex.def (1: `repstopdf` inside a shell command string, line 622, not a load), main.tex (the opt-out line).
- Release-style build with PNG+JPEG+PDF images: relative inputs = those + main.tex/sfe.sty/sfe.aux; no epstopdf.

## 2. Exact load path (pdftex.def lines 650-695)
\AtEndOfPackage{\AtBeginDocument{ \ifx\includegraphics\@undefined\else
  \@ifpackageloaded{pst-pdf}{}{\@ifpackageloaded{pdftricks}{}{\@ifpackageloaded{graphics}{
     \ifnum\pdfshellescape>0   % condition (b) in TL2023
        \edef\Gin@extensions{\Gin@extensions,.eps}
        \RequirePackage{epstopdf-base}[2009/07/12]
     \fi}{}}}\fi}}
guarded by: `\expandafter\ifx\csname DoNotLoadEpstopdf\endcsname\relax` (documented opt-out; comment lines 656-662 of the driver itself).
epstopdf-base.sty lines 211-215: \PackageWarningNoLine{epstopdf}{Shell escape feature is not enabled} at LOAD time when \pdf@shellescape is defined (pdftexcmds, loaded by hyperref) and <=0.
Driver ALSO pre-declares (line 607) \@namedef{Gin@rule@.eps}#1{{eps}{.eps}{#1}} with no include routine.
=> Under TL2023 + --no-shell-escape the loader is NEVER reached (condition (b)); the reported warning cannot come from this driver version.
=> The reviewer's toolchain is unknown; a driver without condition (b) (older behaviour) would load epstopdf-base under --no-shell-escape and print exactly the reported line. Not provable locally which TL generation lacks (b) (no changelog line in README.md of graphics-def, which only says Release 2022-09-22).

## 3. MODEL of an unconditionally-loading driver (TL2023 pdftex.def with `\ifnum\pdfshellescape>0 %` -> `\ifnum1>0 %`, local ./pdftex.def copy)
- no opt-out : epstopdf-base + epstopdf-sys.cfg read; log has "Package epstopdf Warning: Shell escape feature is not enabled." (exact reported line) and "Redefining graphics rule for `.eps'"; .eps appended to \Gin@extensions. Reproduces the reviewer's symptom.
- with opt-out: nothing epstopdf read; clean log.
- no opt-out + EPS referenced: `runsystem(repstopdf ...)...disabled.` then `! Package pdftex.def Error: File 'fig-eps-converted-to.pdf' not found` -> FATAL. EPS conversion cannot work without shell escape.
- with opt-out + EPS referenced: exit 0, NO warning, EPS silently DROPPED.

## 4. EPS probe on small docs (A..D), 285 dark pixels = only the letters "A"/"B", a drawn 100x100bp square would be ~4800
- A real driver, no opt-out : exit 0, silent drop
- B real driver, opt-out    : exit 0, silent drop  (A == B: opt-out is a no-op on TL2023)
- C model driver, no opt-out: exit 1, fatal (conversion disabled)
- D model driver, opt-out   : exit 0, silent drop
=> an .eps reference under --no-shell-escape never renders and is not reported by the log gate. The texgen extension allowlist is load-bearing, and the recorder shows `./fig.eps` read in A/B/D (an input audit would catch it).

## 5. Decisions taken from the evidence
- Primary fix = removal: \DoNotLoadEpstopdf before \documentclass (kept).
- Remove the narrow downgrade note (suppression) - user: "prefer removing unnecessary loading over warning suppression".
- Keep EPS impossible by construction (texgen allowlist) + add per-build input audit (-recorder) so a silent EPS drop or a conversion artifact fails loudly.
