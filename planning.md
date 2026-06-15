# Project 1 Planning: The Unofficial Guide

> Write this document before you write any pipeline code.
> Your spec and architecture diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Update the Retrieval Approach and Chunking Strategy sections if you change your approach during implementation.
> Update this file before starting any stretch features.

---

## Domain

<!-- What domain did you choose? Why is this knowledge valuable and hard to find through official channels? -->

My domain is housing options for undergraduate students at U.S. universities.

This domain focuses on helping students understand and compare common housing choices, such as traditional residence halls, suite-style housing, apartment-style campus housing, living-learning communities, Greek housing, off-campus apartments, homestays, and commuter options. This knowledge can be hard to find because every university explains housing differently, and practical advice is often scattered across housing office pages, student handbooks, Reddit threads, review sites, and student videos.

---

## Documents

<!-- List your specific sources: URLs, subreddit names, forum threads, or file descriptions.
     Aim for at least 10 sources that together cover different subtopics or perspectives within your domain. -->

| # | Source | Description | URL or location |
|---|--------|-------------|-----------------|
| 1 |Reddit thread: “What’s university accommodation like in the US?” | This thread gives informal explanations of what university housing is like in the U.S., including dorms, roommates, shared facilities, and differences between American university accommodation and other countries’ systems. It is useful for understanding practical student experiences rather than only official university policies. | https://www.reddit.com/r/AskAnAmerican/comments/1h8wkwa/whats_university_accommodation_like_in_the_us/ |
| 2 | Study in the USA — “Making the Right Housing Choice: Tips for Success” | Explains common U.S. housing options for international students, including dorms, apartments, homestays, and student housing communities. | https://www.studyusa.com/en/article/housing-options-for-international-college-students-in-the-us |
| 3 | IEFA — “Finding Student Housing in the U.S. for International Students” | Guide to finding safe and affordable student housing, with advice on location, leases, roommates, commute, scams, and deposits. | https://www.iefa.org/resources/finding-student-housing-in-the-us-for-international-students |
| 4 | Times Higher Education — “Six essential tips for finding student housing in the US” | Gives practical tips on choosing housing type, location, budget, social environment, fees, furnishings, and safety. | https://www.timeshighereducation.com/student/advice/six-essential-tips-finding-student-housing-us |
| 5 | College Raptor — “6 Types of Student Housing Options for College Students” | Explains common on-campus and off-campus housing types, including dorms, apartment-style housing, Greek housing, apartments, houses, and living at home. | https://www.collegeraptor.com/find-colleges/articles/college-search/types-of-student-housing/ |
| 6 | OnlineMacha forum — “What are the accommodation options available in the US?” | Forum discussion about U.S. accommodation options, including on-campus housing, off-campus apartments, homestays, temporary housing, leases, utilities, and apartment search tips. | https://onlinemacha.com/forum/study-in-usa/what-are-the-accommodation-options-available-in-the-us/#google_vignette |
| 7 | U.S. News — “College Student Housing: Should I Live On Campus or Off?” | Compares on-campus and off-campus housing, including cost, hidden expenses, independence, campus resources, financial aid, lease length, and safety. | https://www.usnews.com/education/best-colleges/paying-for-college/articles/what-to-know-about-choosing-between-housing-on-or-off-campus |
| 8 | Futurense — “Finding the Best Student Accommodation in the USA: Complete Guide” | Guide to U.S. student accommodation options, including on-campus housing, shared apartments, homestays, private housing, budget, location, safety, reviews, and lease terms. | https://futurense.com/blog/best-student-accommodation-in-the-usa |
| 9 | Keystone Sports — “University Accommodation Options in the US” | Explains four U.S. university housing options: residence halls, student apartments, off-campus apartments, and homestays, with pros and cons for each. | https://keystonesports.uk/university-accommodation-options-in-the-us/ |
| 10 | Illustrarch — “Complete Guide to Student Housing in the USA” | Guide to student housing in the U.S., including dorms, off-campus housing, homestays, shared apartments, budgeting, location, amenities, leases, and roommate agreements. | https://illustrarch.com/schooling/41550-complete-guide-to-student-housing-in-the-usa.html |

---

## Chunking Strategy

<!-- How will you split documents into chunks?
     State your chunk size (in tokens or characters), overlap size, and explain why those
     numbers fit the structure of your documents.
     A review-heavy corpus warrants different chunking than a long FAQ. -->

My documents are mostly long guide articles and forum discussions, not short 1–3 sentence reviews. Many of them have clear headings such as on-campus housing, off-campus housing, homestays, cost, lease terms, roommates, safety, and commute. Because of that, I will split the documents by section/topic first, then keep each chunk around the same size.

I will use a chunk size of about 400 tokens with about 75 tokens of overlap. This size should be large enough to keep one full housing idea together, such as the pros and cons of dorms or the explanation of lease terms. It is also small enough to avoid mixing too many different topics in one chunk.

The overlap is useful because some important information may continue from one paragraph into the next. For example, a source might explain off-campus housing in one paragraph and then list hidden costs in the next paragraph. With overlap, the retriever is less likely to lose important context.

I would know my chunks are too small if the system retrieves text that mentions a topic but does not have enough detail to answer the question. For example, a tiny chunk might only say “off-campus housing gives students more independence” but not explain costs, leases, or commute. I would know my chunks are too large if the retrieved chunk contains too many topics at once, such as dorms, homestays, leases, and scams together, making the answer less focused.

---

## Retrieval Approach

<!-- Which embedding model are you using (e.g., all-MiniLM-L6-v2 via sentence-transformers)?
     How many chunks will you retrieve per query (top-k)?
     If you were deploying this for real users and cost wasn't a constraint, what tradeoffs
     would you weigh in choosing a different embedding model — context length, multilingual
     support, accuracy on domain-specific text, latency? -->

I plan to use all-MiniLM-L6-v2 through sentence-transformers as my embedding model. This model is small, fast, and good enough for semantic search over short guide-style chunks.

I will retrieve the top 4 chunks for each user question. If I retrieve too few chunks, the LLM may not have enough context to answer comparison questions. If I retrieve too many chunks, the answer may become noisy or include unrelated information. Top 4 is a reasonable starting point because it gives enough context without overwhelming the prompt.

Semantic search is useful because users may ask questions using different words from the documents. For example, a user might ask “Should I live in a dorm?” while the documents may say “on-campus housing,” “residence halls,” or “university dormitories.” Embeddings can still connect these similar meanings even when the exact words are different.

If I were deploying this for real users and cost was not a constraint, I would consider a stronger embedding model with better accuracy and longer context length. I would also consider multilingual support because international students may ask questions in different languages. However, stronger models may be slower or more expensive, so I would need to balance accuracy, latency, and cost.

---

## Evaluation Plan

<!-- List your 5 test questions with their expected correct answers.
     Questions should be specific enough that you can judge whether the system's response
     is right or wrong. "What are good dining halls?" is too vague.
     "What do students say about wait times at [dining hall name] during lunch?" is testable. -->

| # | Question | Expected answer |
|---|----------|-----------------|
| 1 | What are the main housing options for students at U.S. universities? | Common options include on-campus dorms, apartment-style housing, off-campus apartments or houses, shared housing, homestays, Greek housing, private student housing, and living at home if possible. |
| 2 | What are the main benefits of living on campus? | On-campus housing is close to classes and campus facilities, helps students meet people, may include meal plans, and often has campus support, security, or residence staff. |
| 3 | What extra costs should students consider before choosing off-campus housing? | Students should consider utilities, internet, groceries, furniture, transportation, parking, security deposits, application fees, and longer lease terms. |
| 4 | Why might an international student choose a homestay? | A homestay can provide cultural experience, English practice, meals, a furnished room, a supportive family environment, and help adjusting to life in the U.S. |
| 5 | What should students compare before choosing a housing option? | Students should compare budget, location, commute, safety, privacy, roommates, lease terms, furniture, meal plans, social environment, and lifestyle needs. |

---

## Anticipated Challenges

<!-- What could go wrong? Name at least two specific risks with reasoning.
     Consider: noisy or inconsistent documents, missing source attribution, off-topic
     retrieval, chunks that split key information across boundaries. -->

1. Many sources repeat similar information about dorms, apartments, and homestays. This could make the system retrieve repetitive chunks instead of giving different useful perspectives.

2. Some sources are informal, such as Reddit or forum threads. These can be useful for student experience, but they may be subjective or inconsistent, so the system should not treat them as official policy.

3. Some housing information depends on the university or city. Cost, housing rules, lease terms, and availability can vary a lot, so the system should avoid making claims that sound true for every school.

---

## Architecture

<!-- Draw a diagram of your pipeline showing the five stages:
     Document Ingestion → Chunking → Embedding + Vector Store → Retrieval → Generation
     Label each stage with the tool or library you're using.
     You can use ASCII art, a Mermaid diagram, or embed a sketch as an image.
     You'll use this diagram as context when prompting AI tools to implement each stage. -->

## Architecture

```mermaid
flowchart LR
    A[Document Ingestion<br/>Sources: PDFs, URLs, Reddit/forum threads<br/>Tools: Python loaders / manual collection]
    --> B[Chunking<br/>Split by topic/section<br/>~400 tokens, 75-token overlap<br/>Tool: custom Python chunk_text()]

    B --> C[Embedding + Vector Store<br/>Embedding model: all-MiniLM-L6-v2<br/>Library: sentence-transformers<br/>Vector DB: ChromaDB]

    C --> D[Retrieval<br/>Embed user query<br/>Retrieve top 4 relevant chunks<br/>Tool: ChromaDB similarity search]

    D --> E[Generation<br/>Send question + retrieved chunks to LLM<br/>Tool: ChatGPT / LLM for final answer]

This pipeline starts with document ingestion, where I collect housing-related sources from PDFs, websites, and forum threads. Then I clean and split the text into topic-based chunks. After that, I create embeddings with all-MiniLM-L6-v2 and store them in ChromaDB. When a user asks a question, the system retrieves the top 4 most relevant chunks and sends them to the LLM to generate the final answer.
---

## AI Tool Plan

<!-- For each part of the pipeline below, describe:
     - Which AI tool you plan to use (Claude, Copilot, ChatGPT, etc.)
     - What you'll give it as input (which sections of this planning.md, which requirements)
     - What you expect it to produce
     - How you'll verify the output matches your spec

     "I'll use AI to help me code" is not a plan.
     "I'll give Claude my Chunking Strategy section and ask it to implement chunk_text()
     with my specified chunk size and overlap" is a plan. -->

I will use ChatGPT to help with the planning and implementation of the RAG pipeline.

First, I will give ChatGPT my Domain, Documents, and Chunking Strategy sections and ask it to help design a chunk_text() function. I expect it to produce Python code that splits documents by headings and then applies a 400-token chunk size with 75-token overlap.

Second, I will use ChatGPT or Copilot to help write the document loading code. I will give it the list of PDF files and URLs from my Documents section and ask for code that can load the text, clean it, and store source metadata.

Third, I will ask ChatGPT to help implement the embedding and retrieval part. I will provide the Retrieval Approach section and ask for Python code using sentence-transformers, all-MiniLM-L6-v2, and ChromaDB.

Fourth, I will use ChatGPT to help test the system with my five evaluation questions. I will give it the Evaluation Plan and ask it to compare the system’s answers with the expected answers.

Finally, I will use AI tools for debugging. If the retriever returns bad chunks, I will show ChatGPT the query, retrieved chunks, and expected answer, then ask how to improve chunking, metadata, or top-k retrieval.

**Milestone 3 — Ingestion and chunking:**

After running the ingestion and chunking script, I generated 62 final chunks from 10 sources after removing noisy chunks that mainly contained promotional text, footer content, unrelated links, or keyword lists.


**Milestone 4 — Embedding and retrieval:**

**Milestone 5 — Generation and interface:**
