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
| 2 | Study in the USA — “Making the Right Housing Choice: Tips for Success” | Explains common U.S. housing options for international students, including dorms, apartments, homestays, and student housing communities. | Making the Right Housing Choice_ Tips for Success.pdf |
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

**Chunk size:**

**Overlap:**

**Reasoning:**

---

## Retrieval Approach

<!-- Which embedding model are you using (e.g., all-MiniLM-L6-v2 via sentence-transformers)?
     How many chunks will you retrieve per query (top-k)?
     If you were deploying this for real users and cost wasn't a constraint, what tradeoffs
     would you weigh in choosing a different embedding model — context length, multilingual
     support, accuracy on domain-specific text, latency? -->

**Embedding model:**

**Top-k:**

**Production tradeoff reflection:**

---

## Evaluation Plan

<!-- List your 5 test questions with their expected correct answers.
     Questions should be specific enough that you can judge whether the system's response
     is right or wrong. "What are good dining halls?" is too vague.
     "What do students say about wait times at [dining hall name] during lunch?" is testable. -->

| # | Question | Expected answer |
|---|----------|-----------------|
| 1 | | |
| 2 | | |
| 3 | | |
| 4 | | |
| 5 | | |

---

## Anticipated Challenges

<!-- What could go wrong? Name at least two specific risks with reasoning.
     Consider: noisy or inconsistent documents, missing source attribution, off-topic
     retrieval, chunks that split key information across boundaries. -->

1.

2.

---

## Architecture

<!-- Draw a diagram of your pipeline showing the five stages:
     Document Ingestion → Chunking → Embedding + Vector Store → Retrieval → Generation
     Label each stage with the tool or library you're using.
     You can use ASCII art, a Mermaid diagram, or embed a sketch as an image.
     You'll use this diagram as context when prompting AI tools to implement each stage. -->

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

**Milestone 3 — Ingestion and chunking:**

**Milestone 4 — Embedding and retrieval:**

**Milestone 5 — Generation and interface:**
