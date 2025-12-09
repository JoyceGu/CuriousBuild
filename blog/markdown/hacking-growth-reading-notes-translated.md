---
title: 《Hacking Growth》 Reading Notes （translated)
date: 2025-09-11
tags: Data Science, Career, Reading
summary: The Growth Hacker Sean Ellis Morgan Brown I finally finished the HackingGrowth over the OOF time, and found quite a few really INSPIRING things about ...
language: English
filename: hacking-growth-reading-notes-translated
---

**The Growth Hacker**

 Sean Ellis Morgan Brown

I finally finished the HackingGrowth over the OOF time, and found quite a few really INSPIRING things about it because of the recent change in groups. As a powerless IC really wish LEADERSHIP had taken the time to read this book as well. 🫢

The following quotes are translated from Chinese version post.

**Chapter 2: Good Products Are Fundamental to Growth**

> **Pursuing growth prematurely incurs opportunity costs on two levels. First, you'll waste valuable time and money on the wrong thing, i.e., promoting an unpopular product. Second, when you pursue growth too early, instead of converting early customers into loyal fans, you'll disappoint them or even turn them into angry critics.** Remember, viral word-of-mouth is a double-edged sword; it can help your growth take off, or it can wipe you out.

 Strongly agree, otherwise you'll just see a steep increase in users but poor retention.

>  If your product trial users aren't big enough to provide that many responses, you should rely more on customer interviews because if there are only a couple dozen responses, you might get the wrong message.

 I wish the PM of one of my current projects could see this paragraph

>  Different types of businesses or products have different retention rates, so it's best to be able to benchmark against successful products that are comparable enough in the industry. If possible, it's best to take an average as a reference to determine how the product is performing. For example, according to data released by mobile analytics company Quettra, **most mobile apps retain only 10% of their users after a month of installation, while the best apps retain over 60% of their users**. ￼

 Shocked by this data set.

**Chapter 4: Fast-Paced Experiments**

>  Analysis of the results of the trial should be performed by an analyst or a growth leader with data analysis skills. The results of the analysis should be written up in a trial summary and include the following: - The name and description of the trial, including the variables used and the target customers. For example, is the trial targeting a particular marketing channel or just mobile users, or is it targeting paid subscribers? - Type of test. Was the test a product feature, a modification of marketing copy on a screen of a web page or app or a creative idea, or a new marketing strategy? - Features affected. This could include a screenshot of where the test ran on the website or in the app, or a copy of a creative on a billboard, TV or radio ad. - Key metrics. What are the metrics that you hope to improve through the trial? - The point in time of the trial, including the start and end dates, but also stating what day of the week it was. - Trial hypotheses and results, including the initial ICE score, sample size, confidence level and statistical efficacy. - Potential confounding factors. For example, the season in which the trial was run, or if there were other promotions that may have influenced visitor behavior.

This paragraph is a short summary of ABtesting, it is important to meet with the product team before the experimentation to establish some success metrics, especially north star metrics, primary metrics, secondary metrics, Guardrails metrics (metrics that can't be influenced).

> **Remove friction from the user experience**

> Patel recommends **asking no more than 5 questions**, not using open-ended questions, but using multiple choice questions and no more than 4 answer options per question. **Adding images and visuals may help improve user engagement**. He suggests focusing on three main aspects of gamification: meaningful rewards, creating surprise and fun by changing the way rewards are won and presented, and providing elements that bring instant gratification. Gamification expert Gabe Zicherman has found that the most effective rewards in gamification practices include status, access, power, and stuff (meaning monetary rewards or gifts). Reciprocity - People are more likely to do something because of a courtesy, regardless of what kind of help someone has given you before and you now need to give someone some kind of help. - Commitment and consistency - people who have already taken an action are more likely to do it again, regardless of the size or content of the action has changed. - Social identity - when feeling uncertain, people will look at what others are doing before making a decision themselves. - Authority - people refer to what authority figures do to decide what action they take. - Favorability - people are more likely to do business with a company or person they like than one they dislike or have no feelings for. - Scarcity - people take action when they fear they will miss out on an opportunity.

> **Offer tangible, experiential rewards**

>  Companies should consider having more products with limited but more specialized features, rather than having all possible features in one product.

 Cursor is a product that focuses on AI programming, but Copilot integrates too many TOOLS, making users sometimes call irrelevant TOOLS while using it. interestingly we can use Copilot to look up which files were used to build Copilot (open source repo:   ) can cause Copilot performance to degrade, here is Copilot's answer:

 "

**Common reasons for agent mode underperforming.**

-  Poor prompt construction-see `agentPrompt.tsx`, `agentInstructions.tsx`.
-  Tool orchestration errors or missing/incorrect tool selection-see `toolCallingLoop.ts`, `agentIntent.ts`.
-  Context window/summarization truncation-see `simpleSummarizedHistoryPrompt.tsx`.
-  Fallbacks for large histories or tool failures.
-  Overly aggressive file protection or missing context due to sensitive file restrictions.
-  Workspace AGENTS.md file that misguides the agent.
 "

**Chapter 8 Cashing in: Increasing Revenue Per User**

>  For SaaS companies, it's possible that analytics show that there is a pinch point between free trial signups and paid subscriptions. By analyzing the causes of churn in depth, the team finds that **users who do not use a particular feature during the free trial phase are half as likely to purchase a lucrative enterprise plan as those who do use the feature.** As a result, the team may decide to focus the trial on increasing the percentage of trialists who use the feature, which in turn increases the number of people who purchase a paid plan at the end of the trial period.

 How do we find this "certain" feature, from general to more granular?

>  Customers from educational institutions and non-profit organizations and college students are less likely than other types of users to purchase the professional paid version.

This is interesting, for an AI product, I wonder if student users pay at a higher rate than some other cohort?

>  The growth team could experiment with using different payment methods in different countries to increase realizations in each country.

Each country has different payment methods, does blocker of payment affect user retention?
