# Phase 1 Proposal

Track B Demonstration. Independent student: Tianhang Wang, 2311601.

- `Project_Proposal.pdf`: English submission document, two body pages followed by one references page.
- `Proposal.md`: editable source of all proposal content.
- `build_proposal.py`: PDF generator, not project implementation code.

## Regenerate

Edit `Proposal.md`, then run:

```powershell
python -m pip install reportlab==4.4.9 pypdf==6.10.0
python build_proposal.py
```

The script resolves paths relative to itself and overwrites `Project_Proposal.pdf`. Review the regenerated PDF after editing, especially page breaks. The current version was rendered with Poppler and every page was visually checked.

## Before submission

The proposal deadline is October 12, 2026. The supplied handout does not specify a deadline time for Phase 1. Confirm any additional submission instructions with the course announcement.

When the team number is assigned, rename the PDF to `TeamXX_Proposal.pdf`, replacing `XX` with that number. Place it in the Phase 1 section of the team's `NLP2026_TeamXX_Demo` folder in the course's designated Feishu location. No team number has been invented. Publishing to GitHub does not replace the required course-folder submission.

The proposal uses a simple academic layout. The handout requires the official ACL LaTeX template for the final report; it does not explicitly impose that template on Phase 1. Later milestone and final dates remain unannounced, so the proposal uses relative weeks.

Methods, implementation, experiments, and demo are planned future work. The PDF contains no fabricated experimental results. The references are verified original papers and official project/model resources. AI assistance in preparing the proposal is disclosed in the document.
