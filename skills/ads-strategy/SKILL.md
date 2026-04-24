---
name: ads-strategy
description: Full Ad Strategy Orchestrator. Launches 5 parallel subagents to build a complete advertising strategy from a single URL — audience personas, creative concepts, funnel architecture, competitive intelligence, and budget allocation. Produces a composite Ad Readiness Score (0-100) with a unified, client-ready strategy report.
---

## Voice and Style

**Before generating any output, load `STYLE.md` at the repository root and apply every rule in it.**

`STYLE.md` defines the writing voice, acronym translation rules, glossary requirement, date and currency formatting (DD/MM/YYYY and R1,000.00), forbidden phrases, and visual palette that all Daily Discounts reports must follow. Rules in `STYLE.md` override any conflicting guidance in this file.

---

# Full Ad Strategy Orchestrator

## Skill Purpose

Perform a comprehensive, end-to-end advertising strategy build for any business from a single URL. This is the flagship command of the AI Ads Strategist — it launches 5 parallel subagents simultaneously to analyze every dimension of ad readiness, then synthesizes all findings into a unified strategy document with a composite Ad Readiness Score (0-100).

The output is a client-ready deliverable that covers audience research, creative strategy, funnel architecture, competitive positioning, and budget allocation — the kind of document an agency would charge $3,000-$10,000 to produce.

## When to Use

- User runs `/ads strategy <url>`
- User asks for a "full ad strategy", "complete advertising plan", or "ad audit"
- User wants everything in one command without running individual ad skills separately
- User needs a single deliverable covering all advertising dimensions
- User is preparing to launch paid ads and wants a complete roadmap

## Input Requirements

- **Required:** A business URL to analyze
- **Optional:** Monthly budget, target geography, industry context, specific platforms of interest

---

## How to Execute

This skill runs 3 phases. Phase 1 gathers intelligence. Phase 2 launches 5 parallel subagents. Phase 3 synthesizes all results into the final report.

Display progress to the user:

```
================================================================
  ADS STRATEGY BUILD: [Company Name]
================================================================

  Phase 1: Discovery & Business Intelligence ......... [running]
  Phase 2: Parallel Agent Analysis ................... [pending]
    - Audience Research Agent (25%) .................. [pending]
    - Creative Strategy Agent (20%) .................. [pending]
    - Funnel Architecture Agent (20%) ................ [pending]
    - Competitive Intelligence Agent (15%) ........... [pending]
    - Budget & ROI Agent (20%) ...................... [pending]
  Phase 3: Synthesis & Report Generation ............. [pending]

================================================================
```

Update each status as work progresses:
- `[running]` -- Currently executing
- `[complete]` -- Finished successfully
- `[limited]` -- Completed with limited data
- `[pending]` -- Not yet started

---

## Phase 1: Discovery & Business Intelligence

**Objective:** Fetch the target URL, extract all available business intelligence, detect business type, and prepare the context package that all 5 subagents will receive.

### Step 1: Fetch and Analyze the Homepage

Use `WebFetch` to retrieve the homepage at the provided URL. Extract:

| Data Point | Where to Find |
|---|---|
| Company name | Page title, logo, footer, about page |
| Tagline / Value proposition | Hero section, H1, meta description |
| Products or services | Navigation menu, service pages, pricing page |
| Pricing model | Pricing page, CTAs ("free trial", "get quote", "add to cart") |
| Target market signals | Copy language, imagery, testimonials, case studies |
| Trust signals | Client logos, certifications, review counts, media mentions |
| Current CTAs | Buttons, forms, phone numbers, chat widgets |
| Contact info | Phone, email, address, social links |
| Tech stack signals | Meta tags, scripts, platform indicators |
| Content assets | Blog, resources, videos, podcasts, lead magnets |

### Step 2: Detect Business Type

Classify the business into one of these categories based on homepage signals:

| Business Type | Detection Signals | Ad Strategy Implications |
|---|---|---|
| **SaaS / Software** | Pricing page, "Sign up" / "Free trial" / "Book demo" CTAs, feature lists, integration pages, app subdomain | Focus on demo/trial conversions, long sales cycles, retargeting heavy |
| **E-commerce** | Product listings, shopping cart, "Add to cart" buttons, product categories, price displays | Focus on ROAS, product catalog ads, shopping campaigns, impulse triggers |
| **Local Business** | Physical address, Google Maps embed, service area mentions, phone number prominent, "Near me" language | Focus on call extensions, local targeting, Google LSAs, radius targeting |
| **Agency / Services** | Case studies, portfolio, "Our Work", client logos, consultation CTAs, team page | Focus on lead gen, authority building, LinkedIn, long nurture sequences |
| **Creator / Course** | Course listings, "Enroll now", instructor bio, curriculum, testimonials from students, community mentions | Focus on webinar funnels, transformation messaging, urgency/scarcity |
| **Restaurant / Hospitality** | Menu, reservations, location hours, food imagery, delivery links | Focus on Instagram/TikTok visuals, local targeting, seasonal promotions |

### Step 3: Identify Industry and Competitive Context

Use `WebSearch` to gather additional intelligence:

```
"[Company Name]" competitors
"[Company Name]" reviews
"[Company Name]" pricing
[industry] + [location] market size
[industry] advertising benchmarks [current year]
```

### Step 4: Detect Recommended Platforms

Based on business type, determine the optimal platform mix:

| Business Type | Primary Platforms | Secondary Platforms | Avoid |
|---|---|---|---|
| SaaS / Software | Google Ads (Search), LinkedIn | Facebook/Instagram (retargeting), YouTube (demos) | TikTok (unless B2C SaaS) |
| E-commerce | Meta (FB/IG), Google Shopping | TikTok, Pinterest, YouTube | LinkedIn |
| Local Business | Google Ads (Search + LSA), Facebook/IG | Nextdoor, Yelp Ads | LinkedIn, Pinterest |
| Agency / Services | LinkedIn, Google Ads (Search) | Facebook (retargeting), YouTube | TikTok, Pinterest |
| Creator / Course | YouTube Ads, Instagram, Facebook | TikTok, Google (search) | LinkedIn (unless B2B) |
| Restaurant / Hospitality | Instagram, Facebook, Google (local) | TikTok, Yelp | LinkedIn |

### Step 5: Build the Context Package

Compile all Phase 1 findings into a structured context package. This exact package is passed to every subagent so they all operate from the same intelligence:

```
CONTEXT PACKAGE:
- Company: [Name]
- URL: [URL]
- Business Type: [Type]
- Industry: [Industry]
- Products/Services: [List]
- Pricing Model: [Model]
- Value Proposition: [Tagline]
- Target Geography: [Location or "National/Global"]
- Current CTAs: [List]
- Trust Signals: [List]
- Recommended Platforms: [Platform list]
- Monthly Budget: [If provided, else "Not specified"]
- Key Competitors: [List from search]
```

---

## Phase 2: Parallel Agent Launch

**Objective:** Launch 5 specialized subagents simultaneously using the `Agent` tool. Each agent receives the full context package from Phase 1 and produces a category score (0-100) plus detailed findings.

**CRITICAL:** All 5 agents MUST be launched in parallel (not sequentially) to minimize execution time. Use 5 separate `Agent` tool calls in the same response.

---

### Agent 1: Audience Research Agent

**Weight in composite score: 25%**
**Corresponding skill:** `ads-audience`

Launch this agent with the following prompt:

```
You are the Audience Research Agent for an ad strategy build. Using the context below, build a complete audience analysis.

CONTEXT:
[Insert full context package from Phase 1]

YOUR TASK:
1. Build 5-7 detailed audience personas for this business. For each persona include:
   - Persona name and archetype (e.g., "Budget-Conscious Buyer", "Overwhelmed Executive")
   - Demographics: age range, gender split, income level, education, job title, location
   - Psychographics: values, lifestyle, aspirations, fears, daily frustrations
   - Pain points: top 3 problems this business solves for them
   - Buying triggers: what specific events or moments push them to buy
   - Objections: top 3 reasons they hesitate or say no
   - Content consumption: platforms they use, content formats they prefer, influencers they follow
   - Platform-specific targeting parameters:
     - Meta (Facebook/Instagram): interests, behaviors, lookalike seed suggestions
     - Google Ads: search intent keywords, in-market audiences, affinity audiences
     - LinkedIn: job titles, industries, company sizes, skills
     - TikTok: interest categories, creator affinities, hashtag communities
   - Persona relevance score (1-5): how valuable is this persona relative to others

2. Define negative audiences (who NOT to target):
   - Demographic exclusions
   - Interest-based exclusions
   - Behavioral exclusions
   - Why each exclusion matters (wasted spend reasons)

3. Identify the #1 highest-value persona and explain why they should receive the largest budget allocation.

4. Map personas to funnel stages — which personas are TOFU (cold), MOFU (warm), BOFU (hot)?

5. Provide an Audience Clarity Score (0-100) based on:
   - How well-defined the ICP is from the website (0-25)
   - How many distinct personas the business can viably target (0-25)
   - How precise the targeting parameters are on each platform (0-25)
   - How clearly the website speaks to specific audience segments (0-25)

OUTPUT FORMAT:
Return your findings as structured markdown with clear headers for each persona and section. End with:
- AUDIENCE_CLARITY_SCORE: [0-100]
- TOP_PERSONA: [Name]
- TOTAL_PERSONAS: [Count]
- KEY_INSIGHT: [One-sentence biggest finding about the audience]
```

---

### Agent 2: Creative Strategy Agent

**Weight in composite score: 20%**
**Corresponding skill:** `ads-creative`

Launch this agent with the following prompt:

```
You are the Creative Strategy Agent for an ad strategy build. Using the context below, develop a complete creative strategy.

CONTEXT:
[Insert full context package from Phase 1]

YOUR TASK:
1. Develop 3 core messaging angles for this business:
   - Pain-point angle: Lead with the problem the audience faces
   - Aspiration angle: Lead with the outcome/transformation
   - Social proof angle: Lead with results, reviews, or authority

2. Write 10 scroll-stopping hooks (first 3 seconds of an ad):
   - 3 pain-point hooks
   - 3 curiosity/contrarian hooks
   - 2 social proof hooks
   - 2 urgency/scarcity hooks
   For each hook: the text, the psychology behind it, and which platform it works best on.

3. Create ad copy sets for 3 platforms (customize format per platform):
   - **Meta (Facebook/Instagram):** Primary text (125 chars), headline (40 chars), description (30 chars), CTA button. Provide 3 variations using PAS, AIDA, and BAB frameworks.
   - **Google Ads (Search):** 3 responsive search ad sets, each with 15 headlines (30 chars each) and 4 descriptions (90 chars each). Include keyword insertion templates.
   - **LinkedIn:** Introductory text (150 words max), headline, CTA. 2 variations — one thought-leader style, one direct-response style.

4. Develop 3 creative concept briefs:
   - Static image ad concept (with visual description, text overlay, color direction)
   - Short video ad concept (15-second script with shot-by-shot breakdown)
   - UGC-style ad concept (script template for a creator to film)

5. Provide a Creative Quality Score (0-100) based on:
   - Hook strength and attention-grabbing potential (0-30)
   - Copy clarity and persuasion quality (0-30)
   - Visual concept variety and platform fit (0-20)
   - A/B test readiness (multiple variations provided) (0-20)

OUTPUT FORMAT:
Return your findings as structured markdown with clear headers. End with:
- CREATIVE_QUALITY_SCORE: [0-100]
- STRONGEST_HOOK: [The single best hook you wrote]
- RECOMMENDED_FIRST_AD: [Which ad concept to test first and why]
- KEY_INSIGHT: [One-sentence biggest creative opportunity]
```

---

### Agent 3: Funnel Architecture Agent

**Weight in composite score: 20%**
**Corresponding skill:** `ads-funnel`

Launch this agent with the following prompt:

```
You are the Funnel Architecture Agent for an ad strategy build. Using the context below, design a complete advertising funnel.

CONTEXT:
[Insert full context package from Phase 1]

YOUR TASK:
1. Design a complete 4-stage advertising funnel:

   **TOFU (Top of Funnel) — Awareness:**
   - Objective: brand awareness, video views, engagement
   - Audience: cold traffic, broad interests, lookalikes
   - Ad formats: video ads, carousel, boosted content
   - Platforms and campaign types per platform
   - KPIs: CPM, video view rate, engagement rate
   - Budget allocation: percentage of total spend

   **MOFU (Middle of Funnel) — Consideration:**
   - Objective: traffic, lead generation, content consumption
   - Audience: warm traffic (engaged with TOFU), website visitors, email subscribers
   - Ad formats: lead ads, content downloads, case studies, webinar registrations
   - Platforms and campaign types per platform
   - KPIs: CPC, CTR, cost per lead, landing page conversion rate
   - Budget allocation: percentage of total spend

   **BOFU (Bottom of Funnel) — Conversion:**
   - Objective: purchases, demos, consultations, sign-ups
   - Audience: hot traffic (MOFU engagers), cart abandoners, pricing page visitors
   - Ad formats: offer ads, testimonial ads, urgency/scarcity ads, dynamic product ads
   - Platforms and campaign types per platform
   - KPIs: CPA, ROAS, conversion rate
   - Budget allocation: percentage of total spend

   **Retargeting — Recovery & Loyalty:**
   - Retargeting windows (1-3 days, 3-7 days, 7-14 days, 14-30 days, 30-60 days)
   - Audience segmentation by engagement depth
   - Creative rotation strategy (avoid ad fatigue)
   - Frequency caps per platform
   - Cross-sell / upsell sequences for existing customers
   - Budget allocation: percentage of total spend

2. Map the conversion path:
   - Ad click -> Landing page -> [Micro-conversion] -> [Primary conversion]
   - Identify the primary conversion action (purchase, demo, call, form)
   - Define landing page requirements for each funnel stage

3. Define the retargeting pixel strategy:
   - What events to track (page views, add to cart, initiate checkout, form start, video watch %)
   - Custom audience definitions for each retargeting segment
   - Lookalike audience recommendations from each segment

4. Provide a Funnel Architecture Score (0-100) based on:
   - Funnel completeness (all 4 stages defined) (0-25)
   - Stage-to-stage flow logic and audience progression (0-25)
   - Retargeting sophistication and timing (0-25)
   - Platform-specific campaign structure quality (0-25)

OUTPUT FORMAT:
Return your findings as structured markdown with clear headers for each funnel stage. End with:
- FUNNEL_ARCHITECTURE_SCORE: [0-100]
- RECOMMENDED_FUNNEL_TYPE: [e.g., "Lead Gen Funnel", "Direct Purchase Funnel", "Webinar Funnel"]
- BUDGET_SPLIT: [TOFU: X% | MOFU: X% | BOFU: X% | Retargeting: X%]
- KEY_INSIGHT: [One-sentence biggest funnel opportunity]
```

---

### Agent 4: Competitive Intelligence Agent

**Weight in composite score: 15%**
**Corresponding skill:** `ads-competitors`

Launch this agent with the following prompt:

```
You are the Competitive Intelligence Agent for an ad strategy build. Using the context below, analyze the competitive advertising landscape.

CONTEXT:
[Insert full context package from Phase 1]

YOUR TASK:
1. Identify 3-5 direct competitors using web search:
   - Search: "[Company Name] competitors", "[Company Name] alternatives", "[Company Name] vs"
   - Search: "best [industry] [location]" or "top [product category] companies"
   - Fetch each competitor's homepage to analyze their positioning

2. For each competitor, analyze:
   - **Positioning:** How do they position themselves? What is their main value proposition?
   - **Offer structure:** What are they selling and at what price points? Free trials, discounts, bundles?
   - **Landing page quality:** CTA clarity, trust signals, page speed, mobile optimization
   - **Ad presence indicators:** Do they appear to run ads? (look for UTM parameters, retargeting pixels, ad library presence)
   - **Content strategy:** Blog, YouTube, podcast, social media activity
   - **Unique angles:** What messaging do they use that the target business does NOT?

3. Search for competitor ads:
   - Reference Meta Ad Library: "facebook.com/ads/library" searches for competitor names
   - Reference Google Ads Transparency Center mentions
   - Look for competitor ad copy patterns in search results (sponsored listings)

4. Build a competitive gap analysis:
   - What are competitors saying that this business should also say?
   - What are competitors NOT saying that this business could own?
   - What platforms are competitors absent from (opportunity for first-mover advantage)?
   - What audience segments are competitors ignoring?

5. Create a "Beat the Competition" strategy:
   - 3 specific positioning angles that differentiate from competitors
   - Ad copy hooks that directly counter competitor messaging
   - Platform opportunities where competitors are weak or absent
   - Pricing/offer strategies that create competitive advantage

6. Provide a Competitive Position Score (0-100) based on:
   - Market differentiation (how unique is the business positioning) (0-25)
   - Competitor ad sophistication (how hard is the competition) (0-25)
   - Gap opportunities identified (exploitable weaknesses) (0-25)
   - First-mover potential on underserved platforms/audiences (0-25)

OUTPUT FORMAT:
Return your findings as structured markdown with clear headers. End with:
- COMPETITIVE_POSITION_SCORE: [0-100]
- TOP_COMPETITOR: [Name of strongest competitor]
- BIGGEST_GAP: [Single most exploitable competitive gap]
- KEY_INSIGHT: [One-sentence competitive advantage summary]
```

---

### Agent 5: Budget & ROI Agent

**Weight in composite score: 20%**
**Corresponding skill:** `ads-budget`

Launch this agent with the following prompt:

```
You are the Budget & ROI Agent for an ad strategy build. Using the context below, build a complete budget allocation and ROI projection.

CONTEXT:
[Insert full context package from Phase 1]

YOUR TASK:
1. Determine estimated pricing benchmarks for this industry and business type:
   - Average CPM (cost per 1,000 impressions) by platform
   - Average CPC (cost per click) by platform
   - Average CPA (cost per acquisition/conversion) by platform
   - Average ROAS (return on ad spend) benchmarks
   - Average conversion rates by platform and funnel stage
   Use web search if needed: "[industry] advertising benchmarks [current year]"

2. Build 3 budget scenarios:

   **Starter Budget ($1,000-$2,000/month):**
   - Platform allocation (percentages and dollar amounts)
   - Campaign types to run at this budget
   - Expected impressions, clicks, and conversions
   - What to prioritize and what to skip
   - Timeline to meaningful data (statistical significance)

   **Growth Budget ($3,000-$5,000/month):**
   - Platform allocation with multi-platform strategy
   - Full funnel activation (TOFU through retargeting)
   - Expected metrics and projected ROAS
   - A/B testing budget allocation
   - Scaling triggers (when to increase spend)

   **Scale Budget ($7,000-$10,000+/month):**
   - Advanced platform mix with full optimization
   - Multi-channel attribution considerations
   - Creative testing velocity requirements
   - Team/agency resource requirements
   - Expected ROAS at scale and diminishing returns thresholds

3. Calculate break-even analysis:
   - Average order value (AOV) or customer lifetime value (CLV) — estimate from pricing page
   - Break-even CPA calculation
   - Break-even ROAS calculation
   - Months to profitability at each budget tier

4. Build a 90-day scaling roadmap:
   - Month 1: Testing phase — budget, platforms, campaigns, KPIs
   - Month 2: Optimization phase — what to cut, what to scale, new tests
   - Month 3: Scaling phase — budget increases, new platforms, automation

5. Provide a Budget Efficiency Score (0-100) based on:
   - Pricing clarity (can we estimate AOV/CLV from the website) (0-25)
   - Platform-market fit (are the recommended platforms right for this business) (0-25)
   - Scalability potential (room to grow ad spend profitably) (0-25)
   - ROI achievability (realistic conversion path and economics) (0-25)

OUTPUT FORMAT:
Return your findings as structured markdown with clear headers. End with:
- BUDGET_EFFICIENCY_SCORE: [0-100]
- RECOMMENDED_STARTING_BUDGET: [$X/month]
- PROJECTED_ROAS: [X.Xx at growth budget]
- BREAK_EVEN_CPA: [$X]
- KEY_INSIGHT: [One-sentence budget/ROI finding]
```

---

## Phase 3: Synthesis & Report Generation

**Objective:** Collect all 5 agent results, calculate the composite Ad Readiness Score, assign a grade, and generate the unified strategy report.

### Step 1: Extract Scores from Agent Results

Parse the closing metrics from each agent's output:

| Agent | Score Variable | Weight |
|---|---|---|
| Audience Research | AUDIENCE_CLARITY_SCORE | 25% |
| Creative Strategy | CREATIVE_QUALITY_SCORE | 20% |
| Funnel Architecture | FUNNEL_ARCHITECTURE_SCORE | 20% |
| Competitive Intelligence | COMPETITIVE_POSITION_SCORE | 15% |
| Budget & ROI | BUDGET_EFFICIENCY_SCORE | 20% |

### Step 2: Calculate Composite Ad Readiness Score

```
Ad_Readiness_Score = (Audience * 0.25) + (Creative * 0.20) + (Funnel * 0.20) + (Competitive * 0.15) + (Budget * 0.20)
```

### Step 3: Assign Grade

| Score Range | Grade | Interpretation |
|---|---|---|
| 95-100 | A+ | Exceptional ad readiness -- this business is primed to scale paid ads immediately |
| 90-94 | A | Excellent foundation -- minor refinements needed before aggressive scaling |
| 85-89 | A- | Strong position -- address 1-2 gaps before full budget deployment |
| 80-84 | B+ | Good readiness -- some strategic gaps to close before scaling |
| 75-79 | B | Solid base -- needs focused work on weaker categories before launch |
| 70-74 | B- | Above average -- several areas need improvement for consistent ROI |
| 65-69 | C+ | Moderate readiness -- significant work needed in 2-3 categories |
| 60-64 | C | Fair -- fundamental gaps exist that will limit ad performance |
| 55-59 | C- | Below average -- most categories need substantial improvement |
| 50-54 | D+ | Weak -- major strategic overhaul needed before spending on ads |
| 45-49 | D | Poor -- advertising spend will likely be wasted without foundational fixes |
| 40-44 | D- | Very poor -- critical issues across most categories |
| 0-39 | F | Not ad-ready -- business fundamentals must be addressed before paid advertising |

### Grade Interpretation and Recommendation

| Grade | Recommendation |
|---|---|
| A+ to A- | Start running ads immediately. Focus on testing and scaling. Use the Growth or Scale budget scenario. |
| B+ to B- | Address the 1-2 lowest-scoring categories first. Start with the Starter budget to test while improving. |
| C+ to C- | Significant prep work needed. Fix fundamentals (landing pages, offer clarity, tracking) before spending. Start with Starter budget on one platform only. |
| D+ to F | Do NOT run ads yet. Invest in website improvements, offer development, and brand positioning first. Revisit ads in 30-60 days after foundational work. |

---

## Output Report

**Before generating the report, load `STYLE.md` at the repository root.** Every rule in that file applies. In particular: translate every acronym on first use, include a glossary, use DD/MM/YYYY dates, use R1,000.00 for currency, never use em or en dashes, never use forbidden phrases listed in STYLE.md. Use South African English spelling throughout.

Generate a file called `ADS-STRATEGY-[CompanyName].md` where `[CompanyName]` is the cleaned company name (spaces replaced with hyphens, lowercase). Use the following template. Replace every `[X]` placeholder with real content. Write like a human, not like a template.

```markdown
# Advertising Strategy Report
## [Company Name]

**Report date:** [DD/MM/YYYY]
**URL:** [URL]
**Prepared for:** [Site owner / client name]

---

## Executive Summary

**Ad Readiness Score: [X]/100 ([Grade])**

[Write 2 to 4 short paragraphs, in plain English. Cover: what the business should do, why, what the numbers say, and the single most important thing to fix. A reader outside advertising should get the full picture in 30 seconds. No acronyms without explanation. No corporate filler.]

**Business type:** [Detected type]
**Industry:** [Industry]
**Recommended platforms:** [Platform list]
**Recommended starting budget:** R[X] per month
**Realistic target ROAS (month 3 and beyond):** [X.X]x

---

## Score Breakdown

The overall [X]/100 score is made up of five weighted categories.

| Category | Score | Rating | What this measures |
|---|---|---|---|
| Audience clarity | [X]/100 | [Strong/Adequate/Weak] | How well we know who we are selling to, and how clearly we can target them. |
| Creative quality | [X]/100 | [Rating] | The quality of the ad copy, hooks, and creative angles available. |
| Campaign architecture | [X]/100 | [Rating] | How well the ad plan moves a stranger from first contact to a purchase, then back for a second one. |
| Competitive position | [X]/100 | [Rating] | How the brand stacks up against competitors in the same market. |
| Budget efficiency | [X]/100 | [Rating] | How much work each rand of ad spend has to do. |

### Rating key
- **Excellent (90-100):** Best in class. No immediate action needed.
- **Strong (75-89):** Above average. Minor tweaks available.
- **Adequate (60-74):** Functional. Clear room for improvement.
- **Weak (40-59):** Below average. Needs focused attention.
- **Critical (0-39):** Major issues that will undermine ad performance.

---

## Critical Findings

The two or three biggest issues, with evidence. Each one is a named problem, not a vague concern.

### 1. [Name the issue in plain English]
[Short paragraph explaining the issue and why it matters. Include specific evidence: a percentage, a rand value, a date, a specific observation from the site or the data. End with one sentence on what to do about it.]

### 2. [Name the issue]
[Same structure.]

### 3. [Name the issue, if there is a third]
[Same structure.]

---

## Quick Wins (Start This Week)

Five actions that require minimal effort but lift performance quickly. None of them should take more than a day to set up.

| # | Action | Why it matters |
|---|---|---|
| 1 | [Specific action, in plain language] | [The concrete benefit, with numbers where possible] |
| 2 | [Action] | [Benefit] |
| 3 | [Action] | [Benefit] |
| 4 | [Action] | [Benefit] |
| 5 | [Action] | [Benefit] |

---

## Glossary

Plain-English explanations of the terms used in this report. Refer to this whenever a term trips you up.

| Term | What it means |
|---|---|
| ROAS (Return on Ad Spend) | What you get back in sales for every rand spent on ads. A 4x ROAS means you spent R1.00 and earned R4.00. |
| CPA (Cost Per Acquisition) | What it costs in ads to win one paying customer. |
| AOV (Average Order Value) | The average basket size across the shop. |
| LTV (Lifetime Value) | What a customer is worth across all their purchases, not just the first. |
| CPM (Cost Per 1,000 Impressions) | What it costs to show the ad to 1,000 people. |
| CPC (Cost Per Click) | What it costs each time someone clicks the ad. |
| CTR (Click Through Rate) | The percentage of people who see the ad and click it. |
| Quality Score | Google's 1 to 10 rating of your search ads. Higher scores mean cheaper clicks and better positions. |
| Funnel | The path a shopper takes from never hearing of you to buying. Three stages: Top (TOFU, strangers), Middle (MOFU, browsing), Bottom (BOFU, ready to buy). |
| Prospecting | Ads shown to people who have never seen the brand before. |
| Retargeting | Ads shown to people who already visited the site. |
| Lookalike audience | An audience built by Facebook or Google that looks similar to existing buyers. |
| Custom Audience / Customer Match | Uploading the customer list to a platform so you can target, exclude, or find similar people. |
| Performance Max (PMax) | A Google campaign that runs across Search, Shopping, YouTube and Gmail, automated. |
| Responsive Search Ads (RSA) | Google text ads where you supply headlines and descriptions and Google mixes and matches. |
| Dynamic Product Ads | Ads that automatically show a shopper the exact product they looked at. |
| UGC (User Generated Content) | Content that looks like a customer made it, not a brand. |
| Pixel / Conversions API (CAPI) | Tracking code on the site. The CAPI (server-side) version is more accurate than the old browser pixel. |
| BFCM | Black Friday and Cyber Monday. |
| BNPL | Buy Now Pay Later (PayJustNow, PayFlex, Mobicred, Payshap). |
| PAS / AIDA / BAB | Three copywriting structures. PAS is Problem, Agitate, Solution. AIDA is Attention, Interest, Desire, Action. BAB is Before, After, Bridge. |
| GTIN | The unique barcode number on every product. Required by Google Shopping. |

[Add any other terms that appear in this specific report. Follow the same plain-English pattern.]

---

## Company Profile

| Field | Detail |
|---|---|
| Company | [Name] |
| URL | [URL] |
| Business type | [Type] |
| Industry | [Industry] |
| Products or services | [List] |
| Pricing model | [Model] |
| Value proposition | [Tagline] |
| Target geography | [Location] |
| Primary conversion action | [Purchase/demo/call/form/sign-up] |

---

## Audience Analysis

**Audience clarity score: [X]/100**

[Short lead-in paragraph describing the audience in human terms. Who is the ideal customer and what are they trying to do?]

### The personas at a glance

| # | Persona | Who they are | Platform mix | Priority |
|---|---|---|---|---|
| 1 | [Name] | [Age, gender split, household income, location] | [Facebook 60% / Google 30% / TikTok 10%] | [1 to 5] |
| 2 | [Name] | [Details] | [Platform mix] | [1 to 5] |
| 3 | [Name] | [Details] | [Platform mix] | [1 to 5] |

### Top persona deep dive: [Name]

[2 to 3 short paragraphs explaining who this person is, what they need, and when they buy. Write in human terms, not bullet-point CV format.]

**What they care about:**
- [Pain point or goal 1]
- [Pain point or goal 2]
- [Pain point or goal 3]

**When they buy:** [Triggers — paydays, seasons, life events, stock-outs, etc.]

**Recommended budget share:** R[X] per month ([X]% of total)

### Who NOT to target

[Short list of audiences to exclude, with rationale. One sentence each.]

### Key audience insight
> [One sentence. The single biggest thing the reader should take from this section, written plainly.]

---

## Creative Direction

**Creative quality score: [X]/100**

[Short lead-in. What is the overall creative approach?]

### Three core messaging angles

| Angle | Territory | How to use it |
|---|---|---|
| Pain-point | [One-line framing] | [When and where to use it] |
| Aspiration | [Framing] | [Use] |
| Social proof | [Framing] | [Use] |

### Top 5 scroll-stopping hooks

A hook is the first line of the ad. If it does not stop the scroll, nothing else matters.

| # | Hook | Type | Best placement |
|---|---|---|---|
| 1 | "[Hook text]" | [Pain / curiosity / social proof / urgency] | [Platform and format] |
| 2 | "[Hook text]" | [Type] | [Placement] |
| 3 | "[Hook text]" | [Type] | [Placement] |
| 4 | "[Hook text]" | [Type] | [Placement] |
| 5 | "[Hook text]" | [Type] | [Placement] |

### First creative to test

[Short paragraph explaining the single first creative the business should launch. Say which angle, which format, which platform, and why this one first.]

### What is ready to test on day one

[Brief bulleted summary of the copy frameworks, Google RSA sets, and creator angles available.]

### Key creative insight
> [One sentence in plain English.]

---

## Campaign Architecture

**Campaign architecture score: [X]/100**

[Short lead-in. The campaign architecture is how the ad plan moves a stranger from first contact to a purchase and back again. Explain the overall logic in one paragraph.]

### Budget split by buying stage

| Stage | Who this reaches | % of budget | R / month | Purpose |
|---|---|---|---|---|
| Top (TOFU) | Strangers who have never heard of the brand | [X]% | R[X] | Awareness, introduce the brand |
| Middle (MOFU) | People who know the brand but have not bought | [X]% | R[X] | Consideration, move them toward a purchase |
| Bottom (BOFU) | People ready to buy now | [X]% | R[X] | Close the sale |
| Retargeting | Recent visitors and existing customers | [X]% | R[X] | Bring back browsers, keep customers loyal |

### Campaign breakdown

| Campaign | What it does | Monthly |
|---|---|---|
| [Campaign name] | [Plain-English description, not just a platform name] | R[X] |
| [Campaign name] | [Description] | R[X] |
| [Campaign name] | [Description] | R[X] |
| **Total** | **All stages, all platforms** | **R[X]** |

### How the shopper moves from ad to purchase

[Plain-English description of the conversion path. What does the shopper see first, what do they click, where do they land, what do they do next? One short paragraph.]

### Tracking and audience setup

[What tracking needs to be in place: Meta Pixel plus Conversions API, Google Enhanced Conversions, TikTok Events API. What custom audiences and lookalikes to build. Written in full sentences, not jargon.]

### Key architecture insight
> [One sentence in plain English.]

---

## Competitive Positioning

**Competitive position score: [X]/100**

[Short lead-in. Where does the brand sit in the market, and what is the biggest competitive challenge?]

### The competitors

| Competitor | Threat level | Their strength | Their weakness |
|---|---|---|---|
| [Name] | [Critical / High / Medium] | [Strength in plain words] | [Weakness] |
| [Name] | [Level] | [Strength] | [Weakness] |
| [Name] | [Level] | [Strength] | [Weakness] |

### Where the gaps are

| Gap | What it means | How to exploit it |
|---|---|---|
| [Gap] | [Explanation] | [Specific action] |
| [Gap] | [Explanation] | [Specific action] |
| [Gap] | [Explanation] | [Specific action] |

### How to win

[2 to 3 short paragraphs on positioning angles, counter-messaging hooks, and offer strategies. Written as if explaining to the business owner, not writing a pitch deck.]

### Key competitive insight
> [One sentence in plain English.]

---

## Budget and Return on Investment

**Budget efficiency score: [X]/100**

### Platform split (R[X] per month)

| Platform | Share | Monthly |
|---|---|---|
| Google (Shopping + Performance Max + Search) | [X]% | R[X] |
| Facebook / Instagram (Advantage+, retargeting, prospecting) | [X]% | R[X] |
| TikTok (creator-led tests) | [X]% | R[X] |

### The underlying maths

This is where profitability depends on repeat customers and Black Friday, not on cheaper clicks.

| Metric | Value | What it means |
|---|---|---|
| Average order value (assumed) | R[X] | The typical basket size |
| Gross margin (assumed) | [X]% | Percentage of each sale left after the cost of the goods |
| Break-even CPA on first order only | R[X] | The most you can spend in ads to win a new customer and break even on their first order |
| Break-even ROAS on first order only | [X.X]x | Sales per R1.00 of ads needed to break even on the first sale alone |
| Break-even CPA including repeat custom | R[X] | Factoring in repeat purchases, what you can afford to spend per new customer |
| Break-even ROAS including repeat custom | [X.X]x | Factoring in repeat purchases, the break-even return |
| Realistic target ROAS (month 3 and beyond) | [X.X]x to [X.X]x | What a well-run account should deliver |
| Realistic target CPA (month 3 and beyond) | R[X] to R[X] | What it should cost to win a new customer by month 3 |

### Launch phase projection (first 90 days)

The account will not perform at target from day one. Month 1 is about getting the tracking right and learning what converts. Month 2 is about killing the losers. Month 3 is when the returns catch up.

| | Month 1 | Month 2 | Month 3 |
|---|---|---|---|
| Spend | R[X] | R[X] | R[X] |
| Blended ROAS | [X.X]x to [X.X]x | [X.X]x to [X.X]x | [X.X]x to [X.X]x |
| Blended CPA | R[X] to R[X] | R[X] to R[X] | R[X] to R[X] |
| Focus | Testing and tracking | Kill losers, scale winners | Scale and optimise |

### Key budget insight
> [One sentence. Usually the point that profitability depends on repeat custom, the email list, and BFCM, not on cheaper clicks.]

---

## Launch to Year-End Roadmap

Three distinct phases, not a single 90-day sprint. Phase 1 takes the business live. Phase 2 optimises what works and quietly builds the audience. Phase 3 executes on the biggest trading window of the year. Each phase has its own dates, priorities, and measures of success.

**IMPORTANT:** Use real calendar dates based on the report date. If the report date is in April 2026, Phase 1 Week 1 begins in the week of the report date. Never use abstract "Month 3" language that could drift across a calendar year. Be honest about when things actually happen.

### PHASE 1: Launch ([start date] to [end of month 3])

Get the tracking right, get the ads live, cut losers, scale winners, consolidate.

#### Week 1: Red zone — foundations ([dates])

Nothing works without this week. The tracking is the foundation.

- **Install tracking on every platform.** Meta Pixel plus Conversions API (server-side), GA4, Google Enhanced Conversions, TikTok Pixel plus Events API. The server-side versions are critical because iPhone changes have killed roughly 20% of the old browser pixel signals.
- **Install the WooCommerce Conversions API Gateway plugin** so server data feeds back to Facebook correctly.
- **Set up conversion events and custom audiences.** Tell each ad platform what counts as a purchase, a cart add, a product view. Upload the customer list.
- **Build the Google Shopping feed properly.** Every product needs its barcode number (GTIN). Fix anything flagged in the Google Merchant Center dashboard.
- **Launch the defensive brand campaign on Google.** Start bidding on the brand name immediately.
- **Spend R[X] in week 1** across Google Shopping, brand-name Google Search, and Facebook retargeting.

#### Weeks 2 to 4: Amber zone — launch and learn ([dates])

- **Launch Google Performance Max** as a retail asset group.
- **Launch Facebook Advantage+ Shopping** with four different creative versions so the platform has something to test.
- **Start A/B testing ad copy** using the PAS, AIDA and BAB frameworks (see glossary).
- **Add non-branded Google Search** targeting category-level queries, not just the brand name.
- **Launch 6 TikTok creator Spark Ads** using UGC-style content.
- **End of month 1: full review.** Add 20% budget to winners. Cut anything delivering under 50% of target return.

#### Month 2: Blue zone — cut and scale ([dates])

- **Cut underperforming Facebook ads** with a click-through rate under 0.6% after 10,000 impressions.
- **Cut weak Google Search keywords** with a Quality Score under 5 after 500 impressions.
- **Scale the top two Shopping product clusters +20%.**
- **Scale Facebook 3-day cart-abandonment retargeting +25%.**
- **Launch Facebook lookalike audiences** built from existing buyers, at 1%, 2% and 3% match tightness.
- **Run the first landing-page A/B test.** Product page versus a dedicated category landing page.

#### Month 3: Green zone — consolidate ([dates])

- **Scale the winners again (+20%).**
- **Deep search query report review.** Mine the last 60 days for new keywords worth bidding on and negatives worth blocking.
- **Roll out retargeting ladders on Facebook.** Different messages at 3, 7, 14 and 30 days since last visit.
- **Second Facebook creative refresh** (6 to 8 new assets) before fatigue sets in.
- **Begin in-house UGC production.** Staff filming real products in real homes, for BFCM pipeline.

### PHASE 2: Steady State ([dates — 3 months after launch])

Optimise what works. Grow the email and WhatsApp list. Lay the BFCM foundations.

#### [Month 4 name, e.g. "July 2026"]

- **Launch 3 to 5 creator partnerships** in the 20,000 to 100,000 follower tier. Measure direct sales plus halo effect on branded search.
- **Second landing page A/B test.** Product-specific landers versus category pages.
- **Start building the BFCM creative library.** Target 12 or more finished assets by the end of Phase 2.
- **Test vernacular creative** on a small budget for under-served audiences.
- **Review the retention stack.** Email list growth rate, WhatsApp opt-ins, loyalty credit uptake. Fix now, not in October.
- **First supplier conversations for BFCM stock.**

#### [Month 5]

- Continue creator partnership measurement.
- BFCM creative library build continues.
- Identify top underperforming product categories. Decide whether to reposition, re-price, or pull from Shopping.

#### [Month 6]

- **Finalise the BFCM campaign structure.** Separate campaign groups so BFCM spend does not contaminate regular-run learning.
- **Complete the BFCM creative library.** All assets finished, approved, ready to schedule.
- **Audit the tracking one more time.** Signal quality must be 95% or better before BFCM budgets hit.
- **Full-account efficiency review.** Cut structurally underperforming campaigns before budgets rise.
- **Pre-commit BFCM budget lifts with Finance.**

### PHASE 3: Black Friday Build ([October to December])

The year's biggest trading window. BFCM and the December clearance carry annual profitability. Under-spend or under-stock here and the year does not work.

#### October

- Last pre-BFCM creative refresh. Shift Facebook from 70/30 image-to-video to 30/70.
- Build dedicated BFCM landing pages with countdown timers.
- Launch warm-up teaser campaigns from mid-October at low spend.
- Stock confirmation locked by 20/10. No late changes.
- Final tracking audit.

#### November

- First half: normal run-rate with BFCM teaser creative rotated in.
- From 15/11: warm-up campaigns launch properly. Budgets up 25% to 30%.
- 21/11 to 26/11: budgets up another 40%. Cost per 1,000 impressions will double or quadruple. Plan for it.
- 27/11 (Black Friday) and 30/11 (Cyber Monday): peak execution. Well-run accounts can return R10.00 to R18.00 per R1.00 spent. Monitor hourly.

#### December

- 01/12 to 15/12: BFCM wind-down. Taper gradually, do not cut overnight.
- Mid-December: swap creative to gifting themes.
- 20/12 to 25/12: last-minute gifting push.
- 26/12 (Boxing Day): clearance peak.
- End of month: full review and plan next year.

---

## Critical Flags and Open Items

Things that must be resolved inside the first month, because they affect the accuracy of the whole plan.

| Open item | Why it matters |
|---|---|
| Confirm the real numbers: AOV, repeat rate, gross margin per category | The whole model runs on estimates. Pull the last 90 days of data and refine before full spend. |
| Install server-side tracking | Without it, roughly 20% of signals from iPhones alone are lost. |
| Stock availability feed to Google Shopping | Out-of-stock ads waste spend and drive customer complaints. |
| [Add business-specific flags here] | [Rationale] |

---

## Next Steps

| What to do next | Skill | Command |
|---|---|---|
| Deep-dive audience research | Audience Persona Builder | `/ads audience [url]` |
| Generate full ad copy sets | Ad Copy Generator | `/ads copy [platform]` |
| Get 20-plus scroll-stopping hooks | Hook Generator | `/ads hooks` |
| Build complete funnel blueprint | Funnel Architect | `/ads funnel [url]` |
| Full competitor ad analysis | Competitive Intelligence | `/ads competitors [url]` |
| Detailed budget projections | Budget Allocator | `/ads budget [amount]` |
| Video ad scripts | Video Script Generator | `/ads video [product]` |
| Landing page audit | Landing Page Auditor | `/ads landing [url]` |
| A/B testing plan | Testing Plan Builder | `/ads testing [campaign]` |
| Generate PDF report | PDF Report Generator | `/ads report-pdf` |
```

## Terminal Output

After the report is saved, display a comprehensive summary in the terminal:

```
================================================================
  AD STRATEGY COMPLETE: [Company Name]
================================================================

  Ad Readiness Score:  [XX]/100  ([Grade])

  Agent Results:
    1. Audience Research ........ COMPLETE  [XX]/100
    2. Creative Strategy ........ COMPLETE  [XX]/100
    3. Funnel Architecture ...... COMPLETE  [XX]/100
    4. Competitive Intelligence . COMPLETE  [XX]/100
    5. Budget & ROI ............. COMPLETE  [XX]/100

  Company Profile:
    Business Type:     [Type]
    Industry:          [Industry]
    Platforms:         [Platform list]
    Starting Budget:   $[X]/month
    Projected ROAS:    [X.Xx]

  Key Metrics:
    Total Personas:    [N] built
    Ad Copy Sets:      [N] variations across [N] platforms
    Hooks Written:     10 scroll-stopping hooks
    Competitors:       [N] analyzed
    Budget Scenarios:  3 (Starter / Growth / Scale)
    Break-Even CPA:    $[X]

  Top Finding:    [Most critical finding across all agents]
  Top Action:     [Single most impactful recommended action]

  Full report saved to: ADS-STRATEGY-[CompanyName].md

  Next steps:
    /ads copy [platform]    -- Generate full ad copy sets
    /ads hooks              -- Get 20+ hooks for testing
    /ads landing [url]      -- Audit the landing page
    /ads report-pdf         -- Generate client-ready PDF
================================================================
```

---

## Key Principles

- **This is the flagship skill.** The report should be thorough enough to justify a $5,000+ consulting engagement if presented as a client deliverable.
- **Parallel execution is mandatory.** All 5 agents MUST launch simultaneously to minimize total execution time. Never run them sequentially.
- **Context consistency matters.** All 5 agents receive the identical context package from Phase 1. This ensures consistency across all sections of the final report.
- **WebSearch is the data source.** Be transparent about what was found and what was estimated. Never fabricate metrics, but do provide industry benchmark ranges when exact data is unavailable.
- **Copy-paste ready.** All ad copy in the report should be ready to paste directly into the ad platform without editing. Character counts must comply with platform limits.
- **Actionable over theoretical.** Every section must end with specific actions, not vague advice. "Create a Meta campaign targeting HR managers at 500+ employee companies using lead gen objective" beats "Consider targeting your ideal audience on social media."
- **The 90-day plan must be specific.** Dates, platforms, budgets, and metrics should be concrete. The reader should know exactly what to do on Day 1, Day 7, Day 14, etc.
- **Grade honestly.** A business with a mediocre website, no tracking, and unclear pricing is NOT an A. The score must reflect reality so the action plan is credible.
- **Always end with next steps.** Guide the user to the specific individual skills that will help them execute on the strategy. The flagship report identifies what to do; the individual skills help them do it.
- **If data is limited, say so.** Mark sections as `[estimated from industry benchmarks]` or `[limited data -- verify before launch]` rather than guessing. Honest limitations build trust.
