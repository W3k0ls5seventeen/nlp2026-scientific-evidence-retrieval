# Scientific Evidence Retrieval with Lexical and Semantic Search

NLP Course Project 2026 · **Track B Demonstration**

Independent project by **Tianhang Wang**, Student ID **2311601**.

This project proposes a local scientific-evidence retrieval application. Given an English scientific claim, it will search a fixed collection of scientific abstracts and compare BM25, pretrained sentence embeddings, and reciprocal rank fusion. The planned demo will show the original abstracts, document identifiers, component ranks, lexical matches, and query latency.

## Current progress

**Phase 1 Project Proposal is complete.** The English PDF has two body pages and one references page. It includes the problem and motivation, responsibilities, system functions and architecture, independent implementation plan, evaluation protocol, expected outcomes, feasibility considerations, and project timeline.

| Stage | Status | Available artifacts |
| --- | --- | --- |
| Phase 1 Project Proposal | Complete | English PDF, editable Markdown, PDF generator, regeneration instructions |
| Phase 2 Midterm Milestone | Planned | Retrieval implementation, initial development results, report and progress slides |
| Final project | Planned | Runnable demo, experiments, ACL report, slides and contribution statement |

No retrieval system or experimental results have been completed at this stage. The Python file in this repository generates the proposal PDF; it is not the retrieval implementation.

## Phase 1 files

- [Read the English proposal PDF](Phase1/Project_Proposal.pdf)
- [Read or edit the proposal source](Phase1/Proposal.md)
- [PDF generation script](Phase1/build_proposal.py)
- [Regeneration and course submission instructions](Phase1/README.md)

## Regenerate the proposal

Use Python with the PDF-authoring dependencies:

```sh
python -m pip install -r requirements-proposal.txt
python Phase1/build_proposal.py
```

Edit `Phase1/Proposal.md` before rebuilding. The generator replaces `Phase1/Project_Proposal.pdf`. Check page layout after any change; the published PDF was rendered and visually checked page by page.

## Planned evaluation

The planned collection is the BEIR version of SciFact. Parameter selection will use development queries drawn from its training split; the 300 BEIR test queries will be evaluated after configurations are frozen. Primary metrics are nDCG@10 and Recall@10, with MRR@10, Recall@100, latency, and qualitative error analysis as supporting measures. The project evaluates evidence retrieval and does not infer claim truth from relevance scores.

## Sources and assistance

The proposal cites the original SciFact, BEIR, BM25, Sentence-BERT, and reciprocal rank fusion papers, together with official dataset and model resources. Full references are in the proposal. Pretrained encoders will be identified as external components; BM25, fusion, retrieval orchestration, evaluation integration, and the inspection interface are planned independent work.

AI assistance was used to organize and draft the proposal and prepare its PDF-generation script and repository documentation. Implementation and experiments remain future work. Any later assistance will be disclosed, and the student is responsible for verifying outputs and understanding the implementation.

GitHub publication is a project record. Course submission follows the instructor's designated submission location and naming rules. The team number has not yet been supplied.
