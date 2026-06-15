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

## Sample Chunks

Below are five representative chunks from the final chunk set. Each chunk is labeled with its source document name and chunk ID.

**Sample Chunk 1**
**Source:** `source8_futurense.txt`
**Chunk ID:** 0
**Content:**
This chunk explains several major student accommodation options in the U.S., including on-campus housing, off-campus shared houses or apartments, homestays, and private student housing. It also discusses why international students need to consider budget, safety, campus proximity, and lifestyle when choosing accommodation.

**Sample Chunk 2**
**Source:** `source2_study_in_usa.txt`
**Chunk ID:** 0
**Content:**
This chunk explains housing options for international students in the U.S., including on-campus university dormitories, private off-campus apartments, shared apartments, and homestays. It also lists advantages and disadvantages such as proximity, community, security, independence, commute, and roommate compatibility.

**Sample Chunk 3**
**Source:** `source7_us_news.txt`
**Chunk ID:** 0
**Content:**
This chunk compares living on campus and living off campus. It explains that on-campus housing can connect students with campus facilities, peers, faculty, and student programs, while off-campus housing may provide more independence.

**Sample Chunk 4**
**Source:** `source10_illustrarch.txt`
**Chunk ID:** 2
**Content:**
This chunk focuses on factors students should consider when choosing housing, such as cost, budget, location, accessibility, amenities, facilities, lease agreements, security deposits, utilities, and transportation.

**Sample Chunk 5**
**Source:** `source6_onlinemacha_forum.pdf`
**Chunk ID:** 1
**Content:**
This chunk discusses temporary accommodation and homestay options for international students. It explains that students may need short-term housing when they first arrive and that staying with a local family can help with adjustment and local orientation.

---

## Retrieval Test Results

I tested the vector store with five evaluation questions and inspected the top returned chunks. Below are three representative retrieval tests.

**Retrieval Test 1**
**Query:** What are the main housing options for students at U.S. universities?
**Top returned chunks:**

* `source8_futurense.txt`, chunk 0, distance 0.2205
* `source10_illustrarch.txt`, chunk 0, distance 0.2292
* `source2_study_in_usa.txt`, chunk 0, distance 0.2522

**Why the chunks are relevant:**
These chunks directly discuss major U.S. student housing options, including on-campus housing, off-campus housing, shared apartments, homestays, and private student housing. The returned chunks clearly match the query and provide enough context to answer the question.

**Retrieval Test 2**
**Query:** What are the main benefits of living on campus?
**Top returned chunks:**

* `source7_us_news.txt`, chunk 0, distance 0.3246
* `source7_us_news.txt`, chunk 1, distance 0.3447
* `source3_iefa.pdf`, chunk 1, distance 0.3546

**Why the chunks are relevant:**
The top chunks discuss how living on campus can connect students with campus facilities, peers, faculty, and programs. They also compare on-campus and off-campus living, including convenience, community, and all-inclusive costs such as utilities, Wi-Fi, furniture, and meal plans.

**Retrieval Test 3**
**Query:** What extra costs should students consider before choosing off-campus housing?
**Top returned chunks:**

* `source10_illustrarch.txt`, chunk 2, distance 0.1919
* `source10_illustrarch.txt`, chunk 1, distance 0.2169
* `source8_futurense.txt`, chunk 1, distance 0.2643

**Why the chunks are relevant:**
These chunks discuss costs connected to off-campus housing, including application fees, security deposits, utilities, internet, commuting, groceries, lease terms, and guarantor requirements. The low distance scores and matching content show that retrieval is working well for this query.


## Evaluation Report

<!-- Run your 5 test questions from planning.md through your system and record the results.
     Be honest — a partially accurate or inaccurate result that you explain well is more 
     valuable than a suspiciously perfect result. --> 

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | What are the main housing options for students at U.S. universities? | Common options include on-campus dorms, off-campus apartments, shared apartments, homestays, and private student housing. | The system retrieved chunks about on-campus housing, off-campus housing, shared apartments, homestays, and private student housing from multiple housing guide sources. | Relevant | Accurate |
| 2 | What are the main benefits of living on campus? | Living on campus can provide proximity to classes and campus facilities, stronger community, easier access to peers and faculty, included utilities or meal plans, and more campus support. | The system retrieved chunks explaining that on-campus living connects students with campus facilities, peers, faculty, programs, and residence hall communities. It also retrieved information about all-inclusive housing costs such as utilities, Wi-Fi, furniture, and meal plans. | Relevant | Accurate |
| 3 | What extra costs should students consider before choosing off-campus housing? | Students should consider utilities, groceries, internet, furniture, transportation, parking, application fees, security deposits, lease terms, and possible penalties. | The system retrieved chunks about application fees, security deposits, utilities, internet, commuting, groceries, lease terms, guarantors, and other costs connected to off-campus housing. | Relevant | Accurate |
| 4 | Why might an international student choose a homestay? | An international student might choose a homestay for cultural exchange, English practice, meals, local orientation, safety, and support from a host family. | The system retrieved chunks explaining that homestays provide a host family environment, cultural exchange, meals, local orientation, and support for international students adjusting to life in the U.S. | Relevant | Accurate |
| 5 | What should students compare before choosing a housing option? | Students should compare cost, location, commute, safety, privacy, roommates, lease terms, amenities, meal plans, social environment, and lifestyle needs. | The system retrieved chunks about comparing budget, lifestyle, location, lease terms, amenities, campus proximity, shared living, and the advantages and disadvantages of different housing options. | Relevant | Accurate |

**Retrieval quality:** Relevant / Partially relevant / Off-target  
**Response accuracy:** Accurate / Partially accurate / Inaccurate

---

## Failure Case Analysis

**Question that failed:**

What is the tuition at Denison University?

**What the system returned:**

The system correctly answered that the available documents do not provide enough information to answer the question. However, during testing, the interface still displayed one weakly related retrieved source from the housing documents with a relatively high distance score.

**Root cause (tied to a specific pipeline stage):**

The issue came from the retrieval and source attribution stage, not the generation stage. Vector search always returns the closest available chunks, even when the question is outside the document collection. Since the question asked about Denison tuition and my documents only cover general U.S. student housing options, the retrieved chunk was not actually useful. The LLM grounding instruction worked because the model refused to answer, but the interface still surfaced a weak retrieved source.

**What you would change to fix it:**

I would make the retrieval filter stricter by lowering the maximum distance threshold so weak matches are removed before generation. I would also update the interface so that when the model says the documents do not contain enough information, the sources box displays “No sources cited because the retrieved context was not sufficient.” This would make the system clearer and prevent users from thinking an irrelevant source supported the refusal.

---

## Spec Reflection

**One way the spec helped you during implementation:**

The spec helped me break the project into clear stages instead of trying to build the whole RAG system at once. The planning stage made me define my domain, documents, chunking strategy, retrieval approach, evaluation questions, and architecture before writing the code. This made the implementation easier because I already knew what documents to collect, how large my chunks should be, which embedding model to use, and what questions I would use to test the system.

**One way your implementation diverged from the spec, and why:**

My implementation diverged from the original plan because I had to do more manual cleaning and filtering than expected. Several sources, especially web pages saved as PDFs and the Reddit thread, contained boilerplate text such as ads, navigation text, footer links, promoted content, and unrelated keyword lists. After inspecting the generated chunks, I added a filtering step to remove noisy chunks and renumbered the remaining chunk IDs so the vector store would contain cleaner, more useful data.

---

## AI Usage

**Instance 1**

- *What I gave the AI:*  
I gave the AI my project domain, document list, and chunking plan from `planning.md`. I explained that my sources were long guide articles, PDFs, and forum threads about student housing options in the U.S.

- *What it produced:*  
The AI helped me design an ingestion and chunking script that loads PDF and text files, cleans the text, splits the documents into overlapping chunks, and saves the final chunks into `processed/chunks.json`.

- *What I changed or overrode:*  
I adjusted the cleaning process after inspecting the generated chunks. Some chunks still contained promotional text, footer content, Reddit interface text, or keyword lists, so I manually identified bad chunks and added a filtering step to remove them. I also renumbered chunk IDs after filtering so the metadata stayed organized.

**Instance 2**

- *What I gave the AI:*  
I gave the AI my retrieval approach, including the `all-MiniLM-L6-v2` embedding model, ChromaDB as the vector store, top-k retrieval, and the requirement that answers must be grounded in retrieved chunks only.

- *What it produced:*  
The AI helped me write the embedding, retrieval, generation, and Gradio interface code. The generated code embeds chunks, stores them in ChromaDB with source metadata, retrieves the most relevant chunks for a query, passes those chunks to a Groq LLM, and displays both the answer and the retrieved source chunks in the interface.

- *What I changed or overrode:*  
I made the grounding behavior stricter by adding a system prompt that tells the model to answer only from the retrieved context and to say when the documents do not contain enough information. I also added a maximum distance threshold so weak retrieval matches are filtered out, and I surfaced source attribution programmatically by showing the retrieved source file names, chunk IDs, and distance scores.

## Example Responses

**Example 1: Grounded housing answer**

**Question:** What are the main housing options for students at U.S. universities?

**System response:**
The main housing options for students at U.S. universities include on-campus housing such as dormitories or residence halls, off-campus shared houses or apartments, homestays with local families, private student housing, private off-campus apartments, and shared housing with roommates.

**Sources visible in output:**

* `source8_futurense.txt`, chunk 0
* `source10_illustrarch.txt`, chunk 0
* `source2_study_in_usa.txt`, chunk 0
* `source3_iefa.pdf`, chunk 1

**Why this is grounded:**
The answer only lists housing options that appeared in the retrieved chunks, and the interface displays the source document names, chunk IDs, and distance scores used to generate the response.

**Example 2: Grounded housing answer**

**Question:** What are the main benefits of living on campus?

**System response:**
The main benefits of living on campus include increased retention and engagement, easy access to campus programs and facilities, opportunities to connect with peers and faculty, all-inclusive costs such as utilities, furniture, Wi-Fi, and meal plans, and a supportive community environment.

**Sources visible in output:**

* `source7_us_news.txt`, chunk 0
* `source7_us_news.txt`, chunk 1
* `source3_iefa.pdf`, chunk 1
* `source2_study_in_usa.txt`, chunk 1

**Why this is grounded:**
The answer is based on retrieved chunks about on-campus living, campus community, student engagement, and cost structure. The response does not add unsupported information beyond the retrieved documents.

**Example 3: Out-of-scope refusal response**

**Question:** What is the tuition at Denison University?

**System response:**
The available documents do not provide enough information to answer that question.

**Why this is grounded:**
The document collection is about student housing options at U.S. universities, not Denison tuition. The system correctly refuses to answer instead of making up tuition information from outside knowledge.

---

## Query Interface

I built a Gradio web interface in `app.py`. The interface has one input field where the user enters a housing-related question, an “Ask” button, an answer box, and a sources box. The answer box displays the LLM-generated response, while the sources box displays the retrieved source file names, chunk IDs, and distance scores.

The interface is designed so a viewer can understand how to use it without narration. The user enters a question, clicks “Ask,” and receives both an answer and the retrieved sources used to support that answer.

**Sample interaction transcript:**

**User input:**
What are the main housing options for students at U.S. universities?

**System answer:**
The main housing options for students at U.S. universities include on-campus housing, off-campus shared houses or apartments, homestays, private student housing, private off-campus apartments, and shared housing.

**Sources used:**

* `source8_futurense.txt`, chunk 0, distance 0.2205
* `source10_illustrarch.txt`, chunk 0, distance 0.2292
* `source2_study_in_usa.txt`, chunk 0, distance 0.2522
* `source3_iefa.pdf`, chunk 1, distance 0.2643
