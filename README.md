# The Unofficial Guide — Project 1

> **How to use this template:**
> Complete each section *after* you've built and tested the corresponding part of your system.
> Do not write placeholder text — if a section isn't done yet, leave it blank and come back.
> Every section below is required for submission. One-liners will not receive full credit.

---

## Domain

<!-- What topic or category of knowledge does your system cover?
     Why is this knowledge valuable, and why is it hard to find through official channels?
     Example: "Student reviews of CS professors at [university] — useful because official
     course descriptions don't reflect teaching style, exam difficulty, or workload." -->

My system covers housing options for undergraduate and international students at U.S. universities. This knowledge is valuable because students need to compare different housing choices before deciding where to live, especially when they are new to the U.S. or unfamiliar with American university housing. Official university housing pages often explain only one school’s policies, while practical housing advice is scattered across guide articles, forums, Reddit threads, and student-focused websites.

---

## Document Sources

<!-- List every source you collected documents from.
     Be specific: include URLs, subreddit names, forum thread titles, or file names.
     Aim for variety — sources that together cover different subtopics or perspectives. -->

| # | Source | Type | URL or file path |
|---|--------|------|-----------------|
| 1 |Reddit thread: “What’s university accommodation like in the US?” | Reddit discussion thread | https://www.reddit.com/r/AskAnAmerican/comments/1h8wkwa/whats_university_accommodation_like_in_the_us/ |
| 2 | Study in the USA — “Making the Right Housing Choice: Tips for Success” | Student housing guide article | https://www.studyusa.com/en/article/housing-options-for-international-college-students-in-the-us |
| 3 | IEFA — “Finding Student Housing in the U.S. for International Students” | International student housing guide | https://www.iefa.org/resources/finding-student-housing-in-the-us-for-international-students |
| 4 | Times Higher Education — “Six essential tips for finding student housing in the US” | Student advice article | https://www.timeshighereducation.com/student/advice/six-essential-tips-finding-student-housing-us |
| 5 | College Raptor — “6 Types of Student Housing Options for College Students” | Housing options explainer article | https://www.collegeraptor.com/find-colleges/articles/college-search/types-of-student-housing/ |
| 6 | OnlineMacha forum — “What are the accommodation options available in the US?” | Study abroad forum thread | https://onlinemacha.com/forum/study-in-usa/what-are-the-accommodation-options-available-in-the-us/#google_vignette |
| 7 | U.S. News — “College Student Housing: Should I Live On Campus or Off?” | On-campus vs. off-campus advice article | https://www.usnews.com/education/best-colleges/paying-for-college/articles/what-to-know-about-choosing-between-housing-on-or-off-campus |
| 8 | Futurense — “Finding the Best Student Accommodation in the USA: Complete Guide” | Student accommodation guide article | https://futurense.com/blog/best-student-accommodation-in-the-usa |
| 9 | Keystone Sports — “University Accommodation Options in the US” | University accommodation guide article | https://keystonesports.uk/university-accommodation-options-in-the-us/ |
| 10 | Illustrarch — “Complete Guide to Student Housing in the USA” | Complete student housing guide | https://illustrarch.com/schooling/41550-complete-guide-to-student-housing-in-the-usa.html |

---

## Chunking Strategy

<!-- Describe your chunking approach with enough specificity that someone else could reproduce it.
     Include:
     - Chunk size (characters or tokens) and why that size fits your documents
     - Overlap size and why (or why not) you used overlap
     - Any preprocessing you did before chunking (e.g., stripping HTML, removing headers)
     - What your final chunk count was across all documents -->

Chunk size:
I used a chunk size of about 400 words/tokens. This size fits my documents because most of them are long guide-style articles with sections about housing types, cost, location, lease terms, roommates, and safety. A 400-token chunk is large enough to keep one housing idea together, but not so large that many unrelated topics are mixed into one chunk.

Overlap:
I used an overlap of about 75 words/tokens. The overlap helps preserve context when important information continues across chunk boundaries. For example, a section may introduce off-campus housing in one paragraph and then explain utilities, deposits, or commuting in the next paragraph.

Why these choices fit your documents:
My documents are mostly long articles and forum discussions rather than short reviews. I first cleaned the text by removing obvious web boilerplate such as promotional text, footer content, unrelated links, cookie/banner text, and keyword lists. After generating chunks, I inspected the output and filtered out noisy chunks that did not contain useful housing information.

Final chunk count:
After cleaning and filtering noisy chunks, I generated 62 final chunks from 10 sources. The remaining chunks mostly focus on useful student housing information such as housing types, on-campus and off-campus options, cost, lease terms, roommates, safety, location, and international student concerns.

---

## Embedding Model

<!-- Name the embedding model you used and explain your choice.
     Then answer: if you were deploying this system for real users and cost wasn't a constraint,
     what tradeoffs would you weigh in choosing a different model?
     Consider: context length limits, multilingual support, accuracy on domain-specific text,
     latency, and local vs. API-hosted. -->

Model used:
I used all-MiniLM-L6-v2 from sentence-transformers as my embedding model. I chose this model because it is lightweight, fast, easy to run locally, and strong enough for semantic search over short guide-style chunks.

Production tradeoff reflection:
If I were deploying this system for real users and cost was not a constraint, I would compare stronger embedding models based on retrieval accuracy, context length, multilingual support, latency, and cost. A stronger API-hosted model might perform better on vague or complex user questions, but it could be slower and more expensive. I would also consider multilingual support because international students may ask housing questions in different languages.

---

## Grounded Generation

<!-- Explain how your system enforces grounding — how does it prevent the LLM from answering
     beyond the retrieved documents?
     Describe both your system prompt (what instruction you gave the model) and any structural
     choices (e.g., how you formatted the context, whether you filtered low-relevance chunks).
     Do not just say "I told it to use the documents" — show the actual instruction or explain
     the mechanism. -->

System prompt grounding instruction:

My system instructs the LLM to answer only using the retrieved document chunks. The model is not supposed to use outside knowledge or make assumptions beyond the provided context. If the retrieved chunks do not contain enough information, the model should say that the sources do not provide enough evidence.

The grounding instruction I used is:

You are answering questions for an unofficial guide about student housing options at U.S. universities. Use only the retrieved context chunks provided below. Do not use outside knowledge. If the context does not contain enough information to answer the question, say that the available sources do not provide enough information. When possible, mention which source the information came from.

I also format the prompt so that the retrieved chunks are clearly separated from the user question. Each chunk includes the source file name and chunk ID before the text. This helps the model know exactly what information it is allowed to use.

Example context format:

Source: source3_iefa.pdf
Chunk ID: 2
Text: ...

Source: source7_us_news.txt
Chunk ID: 1
Text: ...

How source attribution is surfaced in the response:

Each chunk stores metadata, including the source file name and chunk ID. When the system retrieves relevant chunks, it passes that metadata into the prompt along with the chunk text. The final response can then mention the source names used, such as source3_iefa.pdf or source7_us_news.txt.

This does not fully guarantee perfect citation behavior, but it makes the response more grounded because the model sees both the evidence and the source label. I also filtered noisy chunks before retrieval so that the model is less likely to cite irrelevant promotional text, footer content, or navigation text.

---

## Evaluation Report

<!-- Run your 5 test questions from planning.md through your system and record the results.
     Be honest — a partially accurate or inaccurate result that you explain well is more 
     valuable than a suspiciously perfect result. --> 

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | | | | | |
| 2 | | | | | |
| 3 | | | | | |
| 4 | | | | | |
| 5 | | | | | |

**Retrieval quality:** Relevant / Partially relevant / Off-target  
**Response accuracy:** Accurate / Partially accurate / Inaccurate

---

## Failure Case Analysis

<!-- Identify at least one question where retrieval or generation did not work as expected.
     Write a specific explanation of *why* it failed, tied to a part of the pipeline.

     "The answer was wrong" is not an explanation.

     "The relevant information was split across a chunk boundary, so retrieval returned
     only half the context — the model didn't have enough to answer correctly" is an explanation.

     "The embedding model treated the professor's nickname as out-of-vocabulary and returned
     results from an unrelated review" is an explanation. -->

**Question that failed:**

**What the system returned:**

**Root cause (tied to a specific pipeline stage):**

**What you would change to fix it:**

---

## Spec Reflection

<!-- Reflect on how planning.md shaped your implementation.
     Answer both questions with at least 2–3 sentences each. -->

**One way the spec helped you during implementation:**

**One way your implementation diverged from the spec, and why:**

---

## AI Usage

<!-- Describe at least 2 specific instances where you used an AI tool during this project.
     For each: what did you give the AI as input, what did it produce, and what did you
     change, override, or direct differently?

     "I used Claude to help me code" is not sufficient.
     "I gave Claude my Chunking Strategy section from planning.md and asked it to implement
     chunk_text(). It returned a function using a fixed character split. I overrode the
     chunk size from 500 to 200 because my documents are short reviews, not long guides." -->

**Instance 1**

- *What I gave the AI:*
- *What it produced:*
- *What I changed or overrode:*

**Instance 2**

- *What I gave the AI:*
- *What it produced:*
- *What I changed or overrode:*
