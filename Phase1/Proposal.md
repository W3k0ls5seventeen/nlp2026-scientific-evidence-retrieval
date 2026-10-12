# Scientific Evidence Retrieval with Lexical and Semantic Search

**NLP Course Project 2026 | Track B Demonstration | Phase 1 Project Proposal**

## 1 Team Members and Responsibilities

Tianhang Wang (Student ID 2311601) will complete the project independently and be responsible for literature review and data preparation, retrieval implementation, interface development, experimental evaluation, report writing, and the final demonstration. A weekly contribution log will record completed tasks, code changes, and experimental artifacts.

## 2 Background and Motivation

Students reading scientific literature need to locate abstracts relevant to a claim before judging its evidence. Keyword retrieval can miss paraphrases, while semantic retrieval can rank topically similar documents that do not address the claim. SciFact provides scientific claims with annotated evidence abstracts [1], making it suitable for a small, measurable retrieval demonstration. BEIR offers a common retrieval evaluation setting and shows that dense retrieval does not consistently outperform strong lexical baselines [2]. These findings motivate a direct comparison rather than an assumed advantage for neural methods.

The project will develop a local application that exposes the retrieved abstracts and the ranking process. Its purpose is to help a reader inspect candidate evidence and understand differences between lexical and semantic matching. Retrieved relevance will not be presented as proof that a claim is true. Automatic support/refute classification, generated answers, and full-text literature search are outside the core scope.

## 3 Problem Definition and Project Questions

Given an English scientific claim q and a fixed corpus D of scientific abstracts, the system will return the top k abstracts ranked by relevance to q. A document will consist of its title and abstract and retain its original identifier. The project will address three practical questions: (1) How do BM25 and a pretrained sentence encoder differ in evidence retrieval quality? (2) Does combining their rankings improve coverage or ranking quality? (3) What quality, latency, and interpretability trade-offs appear in a usable local demo?

The target users are students exploring literature evidence. The working collection will be the BEIR version of SciFact, with approximately 5,000 abstracts and 300 test queries [2, 7]. Evaluation concerns abstract retrieval only; it does not reproduce the complete claim-verification task of SciFact [1].

## 4 System Functions and Technical Architecture

The offline pipeline will validate the corpus, preserve document IDs, and build lexical statistics and cached document embeddings. The online pipeline will validate a query, run the selected retriever, rank or fuse candidates, and display results. A separate batch evaluator will use the same retrieval interface to export rankings and compute metrics. Python, NumPy, Sentence Transformers, and Streamlit are the planned tools; a GPU will be optional.

**Lexical retrieval.** I will implement an inverted index and BM25 scoring using term frequencies, document frequencies, and length normalization [3]. Text normalization will lowercase and tokenize words while preserving scientific numbers and negation terms. Initial parameters will be k1 = 1.2 and b = 0.75.

**Semantic retrieval.** I will use the existing sentence-transformers/all-MiniLM-L6-v2 encoder as a fixed external component [4, 6]. Queries and documents will be encoded, normalized, and compared with cosine similarity using exact search over cached embeddings. The model's 256-wordpiece input limit will be respected, and the fraction of truncated documents will be recorded. No model fine-tuning is required.

**Hybrid retrieval and interface.** I will implement reciprocal rank fusion [5], summing 1 / (c + rank) over the BM25 and dense top-100 lists with initial c = 60; a document absent from a list contributes zero. The demo will allow method selection and side-by-side top-10 results, showing document IDs, titles, abstracts, lexical matches, component ranks, and elapsed query time. Match highlights will indicate lexical overlap rather than a validated explanation of semantic relevance. Empty and invalid inputs will receive clear feedback.

<!-- PAGE BREAK -->

## 5 Implementation Plan and Independent Work

I will implement the corpus loader, lexical index, dense cache and search, fusion, evaluator, and interface. Libraries will supply numerical operations, the pretrained encoder, and UI widgets. BEIR utilities may load data and check metrics; its example retrievers will not replace the self-implemented core. Component checks will cover document-ID alignment, deterministic rankings, BM25 calculations, fusion with missing candidates, and metrics on manually checked cases.

## 6 Experimental and Evaluation Plan

**Data separation.** Development queries will be drawn deterministically from the BEIR SciFact training split using seed 42. No retriever will be trained; parameters will be selected by development nDCG@10 only. The full corpus will be indexed, including documents relevant to test queries, as required for corpus retrieval. Test queries and labels will not guide tuning. Configurations will be frozen before evaluating all 300 BEIR test queries. BEIR split names will be retained because they differ from the original SciFact splits.

**Comparison and metrics.** BM25, dense retrieval, and fusion will use the same title-plus-abstract corpus. Primary metrics will be nDCG@10 and Recall@10, supplemented by MRR@10 and Recall@100. Recall uses all judged relevant documents per query as its denominator. Warm-query latency includes query encoding, retrieval, and fusion, excluding indexing and browser rendering. Median and 95th-percentile latency, indexing time, cache size, and hardware will be reported. The target is median warm-query latency below two seconds, subject to measurement.

**Analysis.** Fusion will be compared with both individual systems. Development-only checks will vary c over {20, 60, 100} and candidate depth over {50, 100}. Paired bootstrap intervals with 1,000 resamples will summarize uncertainty. Twenty test queries sampled before inspecting outcomes will support analysis of paraphrases, negation, numerical conditions, and misleading topical similarity. Unjudged abstracts may still be relevant. Improvements are questions to test, not promised results.

## 7 Expected Outcomes and Completion Criteria

Deliverables will include a runnable demo, documented source code, dependency and model-version records, saved rankings and metrics, contributions, slides, and an eight-page English final report using the official ACL LaTeX template. Completion requires all three methods on the same corpus, exportable and reproducible test metrics, functioning result inspection and input handling, and a comparison discussing limitations even if fusion gives no improvement. The midterm will provide a working framework, lexical and dense modules, and genuine development results.

## 8 Project Timeline

| Period | Planned work and verifiable output |
| --- | --- |
| October 6 to 12 2026 | Finalize scope, references, and evaluation protocol; submit Phase 1 proposal by October 12. |
| Week 1 after proposal | Validate data and split IDs; implement and check BM25; save development rankings. |
| Week 2 | Build dense cache and fusion; compare development metrics and record runtime. |
| Week 3 | Integrate demo and input handling; prepare a midterm report and at most five progress slides. |
| Week 4 | Freeze configurations; evaluate the test set; analyze fixed cases and uncertainty. |
| Week 5 and final preparation | Complete reproducibility checks, ACL report, contributions, demo recording, and final slides. |

The weeks are planning targets; the midterm, presentation, and final submission dates will follow the instructor's announced schedule. Final slides will be submitted by 23:59 on the day before the assigned presentation.

## 9 Feasibility and Responsible Use

The small corpus and cached embeddings make exact retrieval feasible without large-model training. Resources will be cached early to reduce download risk; truncation and domain mismatch will be analyzed. Schedule pressure will reduce visual refinements while preserving the retrievers and evaluation. External data, algorithms, weights, and reused code will be cited. AI assistance was used to organize and draft this proposal. Any implementation assistance will also be disclosed; the student will verify outputs and explain the code. No experimental outcomes are claimed here.

<!-- REFERENCES PAGE -->

## References

[1] David Wadden, Shanchuan Lin, Kyle Lo, Lucy Lu Wang, Madeleine van Zuylen, Arman Cohan, and Hannaneh Hajishirzi. 2020. Fact or Fiction: Verifying Scientific Claims. In Proceedings of EMNLP, pages 7534-7550. https://aclanthology.org/2020.emnlp-main.609/

[2] Nandan Thakur, Nils Reimers, Andreas Rücklé, Abhishek Srivastava, and Iryna Gurevych. 2021. BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models. NeurIPS Datasets and Benchmarks. https://arxiv.org/abs/2104.08663

[3] Stephen Robertson and Hugo Zaragoza. 2009. The Probabilistic Relevance Framework: BM25 and Beyond. Foundations and Trends in Information Retrieval, 3(4):333-389. https://doi.org/10.1561/1500000019

[4] Nils Reimers and Iryna Gurevych. 2019. Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks. In Proceedings of EMNLP-IJCNLP, pages 3982-3992. https://aclanthology.org/D19-1410/

[5] Gordon V. Cormack, Charles L. A. Clarke, and Stefan Buettcher. 2009. Reciprocal Rank Fusion Outperforms Condorcet and Individual Rank Learning Methods. In Proceedings of SIGIR, pages 758-759. https://research.google/pubs/reciprocal-rank-fusion-outperforms-condorcet-and-individual-rank-learning-methods/

[6] Sentence Transformers. all-MiniLM-L6-v2 model card. Model resource accessed October 6, 2026. https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2

[7] BEIR maintainers. Official BEIR repository and dataset information. Data resource accessed October 6, 2026. https://github.com/beir-cellar/beir
