# Created by: Claude
# Date: 2026-11-03
# Purpose: SEO and AEO layer for every calculator and scorecard page on syedcreates.com. Adds a direct answer
#          block, how to steps (HowTo schema), the formula, a worked example, question led FAQs merged into the
#          page's FAQPage schema, related tool links, keyword led titles and descriptions.
# Owner: Syed Hadi
#
# Worked examples are computed with the same formulas the tools use. No tax rates or prices that go stale.
import html as _h
import json
import re

E = _h.escape
DATE = "2026-11-03"

# slug: dict(title, desc, h2 (guide heading), kw (keyword line), answer, steps, formula, example, faqs, related)
PAGES = {
    "calculator": dict(
        title="Free Calculators India: EMI, SIP, FIRE, BMI, Mileage",
        desc="Free India calculators in one place: loan EMI and prepayment, SIP and mutual fund returns, FIRE, salary growth, BMI, car mileage, Khums and GTM scorecards.",
        h2="Which Calculator Should You Use?",
        answer="Pick by the decision you are making. Use the loan EMI calculator before you borrow, the SIP and mutual fund calculator before you invest, the FIRE calculator to set a retirement date, the salary growth calculator for a 45 year view, BMI for health, car mileage for running cost and Khums for the yearly Shia obligation.",
        steps=[("Name the decision", "Borrow, invest, retire, drive or stay healthy. Each calculator answers one money or health decision."),
               ("Enter your own numbers", "Every calculator starts with sensible Indian defaults. Replace them with your salary, loan or fuel price."),
               ("Read the summary first", "The top line gives the answer in one number. The tables below explain how it was reached."),
               ("Download the PDF", "Most calculators export a branded PDF report you can keep or share.")],
        formula=None, example=None,
        faqs=[("Are these calculators free?", "Yes. Every calculator and scorecard on syedcreates.com is free, needs no sign up and runs in your browser."),
              ("Do the calculators store my data?", "No. The money and health calculators run entirely in your browser. Nothing is saved on a server unless you choose to email yourself a PDF."),
              ("Which calculator helps me close my home loan faster?", "The loan EMI and prepayment planner. It shows how much interest a yearly prepayment or a small EMI increase saves and the month the loan closes."),
              ("Is there a calculator for running cost of a car in India?", "Yes. The car mileage calculator turns kilometres, mileage and your city's petrol price into litres, fuel cost per month and cost per km.")],
        related=[("/loan-calculator", "Loan EMI and prepayment"), ("/fire-calculator", "FIRE calculator"), ("/company-research", "Company research")]),

    "car-mileage-calculator": dict(
        title=None,
        desc="Car mileage calculator for India. Enter km per month, km per litre and petrol price to get litres, fuel cost per month, cost per km and yearly running cost.",
        h2="How Do You Calculate Fuel Cost Per Month?",
        answer="Divide the kilometres you drive in a month by your car's real mileage to get litres, then multiply by the petrol price. A car doing 1,000 km a month at 15 km per litre uses 66.7 litres. At ₹102 a litre that is ₹6,800 a month, or ₹6.80 per km in fuel.",
        steps=[("Enter kilometres per month", "Use your odometer or trip meter for a normal month, including weekend drives."),
               ("Enter your real mileage", "Fill the tank, reset the trip meter, drive, refill. Kilometres divided by litres is your true km per litre."),
               ("Pick your city's petrol price", "Use the price at your usual pump. State taxes make it differ from city to city."),
               ("Add service and wear", "Add yearly service, tyres and insurance to see the full running cost, then download the PDF.")],
        formula=["Litres per month = km per month ÷ km per litre", "Fuel cost per month = litres × price per litre", "Cost per km = running cost per month ÷ km per month"],
        example="Suzuki Fronx, 1,000 km a month, 15 km/L, petrol at ₹102: 66.7 litres and ₹6,800 a month in fuel, ₹81,600 a year. The same driving costs ₹7,767 a month at ₹116.50 a litre.",
        faqs=[("What is a good mileage for a petrol car in India?", "Most compact petrol hatchbacks and SUVs return 13 to 18 km per litre in mixed city and highway use. Real mileage is usually below the ARAI figure on the brochure."),
              ("How do I calculate my car's real mileage?", "Fill the tank to full, reset the trip meter, drive normally, then refill to full. Divide the kilometres on the trip meter by the litres you refilled."),
              ("How much does it cost to run a car per km in India?", "Fuel alone is petrol price divided by mileage, about ₹6 to ₹8 per km for a 15 km/L car. Service, tyres and insurance usually add ₹1 to ₹2 per km."),
              ("Does AC reduce car mileage?", "Yes, usually by a small amount, more in slow city traffic than at highway speed. Correct tyre pressure and smooth driving recover more than switching the AC off.")],
        related=[("/loan-calculator", "Car loan EMI"), ("/salary-calculator", "Salary growth"), ("/fire-calculator", "FIRE calculator")]),

    "loan-calculator": dict(
        title="EMI Calculator India: Home and Car Loan Prepayment Planner",
        desc="EMI calculator for home, car and personal loans in India. See EMI, total interest and how prepayments or a higher EMI close the loan years earlier.",
        h2="How Is Loan EMI Calculated?",
        answer="EMI = P × r × (1 + r)^n ÷ ((1 + r)^n − 1), where P is the loan amount, r the monthly interest rate and n the number of months. A ₹50 lakh home loan at 8.5% for 20 years has an EMI of about ₹43,391 and total interest of about ₹54 lakh.",
        steps=[("Choose the loan type", "Home, car or personal. The defaults change to typical tenures and rates for each."),
               ("Enter amount, rate and tenure", "Use the rate in your sanction letter and the tenure in years."),
               ("Add a prepayment plan", "Try a yearly lump sum, a monthly top up or a yearly EMI step up."),
               ("Compare strategies", "See interest saved and the new closing date for each, then export the PDF.")],
        formula=["EMI = P × r × (1 + r)^n ÷ ((1 + r)^n − 1)", "r = annual rate ÷ 12 ÷ 100, n = years × 12", "Total interest = EMI × n − P"],
        example="₹50,00,000 at 8.5% for 20 years: r = 0.00708, n = 240, EMI ≈ ₹43,391. You repay about ₹1.04 crore, so interest is about ₹54.1 lakh. Prepayments go straight to principal and cut that interest the fastest in the early years.",
        faqs=[("Is it better to prepay a home loan or invest?", "Prepaying gives a guaranteed return equal to your loan rate. Investing can earn more but carries risk. The planner shows both outcomes so you can compare them for your rate."),
              ("Should I reduce EMI or tenure after a prepayment?", "Reducing tenure saves more interest. Reducing EMI frees monthly cash flow. If the EMI is comfortable, keep it and let the tenure shrink."),
              ("Is there a penalty for prepaying a home loan in India?", "Banks and housing finance companies do not charge prepayment penalties on floating rate home loans taken by individuals. Fixed rate and business loans can carry charges, so check your loan agreement."),
              ("How much does a 1% lower interest rate save?", "On a ₹50 lakh, 20 year loan, moving from 8.5% to 7.5% lowers the EMI by about ₹3,100 a month and total interest by roughly ₹7.4 lakh.")],
        related=[("/salary-calculator", "Salary growth"), ("/fire-calculator", "FIRE calculator"), ("/car-mileage-calculator", "Car running cost")]),

    "bmi-calculator": dict(
        title="BMI Calculator India: Asian Cut Offs and Healthy Habits Plan",
        desc=None,
        h2="How Do You Calculate BMI for Indians?",
        answer="BMI is weight in kilograms divided by height in metres squared. For Asian Indian adults the healthy range is 18.5 to 22.9, 23 to 24.9 is overweight and 25 or more is obesity. These cut offs are lower than the global WHO scale because health risk starts at a lower BMI in Indians.",
        steps=[("Enter height and weight", "Height in centimetres and weight in kilograms, measured in the morning."),
               ("Add your waist", "Measure at the navel. Waist size flags belly fat that BMI can miss."),
               ("Fill your daily habits", "Steps, cardio, sleep, sitting time and food. These drive the start and stop table."),
               ("Get your plan", "Read the insights, track 8 habits for 7 days and download the PDF plan.")],
        formula=["BMI = weight (kg) ÷ height (m)²", "Waist to height ratio = waist (cm) ÷ height (cm)"],
        example="170 cm and 78 kg: 78 ÷ 1.70² = 27.0. On Indian cut offs that is in the obesity band, while the WHO global scale calls it overweight. The healthy weight for 170 cm on Indian cut offs is about 53 to 66 kg.",
        faqs=[("What is a normal BMI for Indian adults?", "18.5 to 22.9 on the Asian Indian cut offs used by Indian guidelines. The global WHO scale uses 18.5 to 24.9."),
              ("Why is the BMI cut off lower for Indians?", "At the same BMI, Indians tend to carry more body fat and belly fat, which raises the risk of diabetes and heart disease earlier. Lower cut offs catch that risk sooner."),
              ("Is waist size more important than BMI?", "Both matter. A waist of 90 cm or more for men, or 80 cm or more for women, or a waist to height ratio above 0.5, signals belly fat even when BMI looks normal."),
              ("How many steps a day should I walk?", "Around 7,000 to 10,000 steps a day is linked with lower health risk in large studies. Start from your current count and add about 1,000 a week.")],
        related=[("/salary-calculator", "Salary growth"), ("/fire-calculator", "FIRE calculator"), ("/car-mileage-calculator", "Car running cost")]),

    "fire-calculator": dict(
        title="FIRE Calculator India: Retire Early Number and SIP Needed",
        desc=None,
        h2="How Do You Calculate Your FIRE Number in India?",
        answer="Grow your yearly expenses by inflation to your retirement year, then divide by a safe withdrawal rate. At ₹6 lakh a year today, 6% inflation and retirement in 15 years, expenses become about ₹14.4 lakh. At a 3.5% withdrawal rate the FIRE number is about ₹4.1 crore.",
        steps=[("Enter age and expenses", "Your current age, target retirement age and yearly living costs today."),
               ("Set inflation and returns", "Use cautious numbers. The defaults are planning assumptions, not promises."),
               ("Add your current investments", "Mutual funds, stocks and other savings you already hold."),
               ("Read the gap", "See the SIP you need, your earliest retirement age and download the plan.")],
        formula=["Expenses at retirement = expenses today × (1 + inflation)^years", "FIRE number = expenses at retirement ÷ withdrawal rate", "At 3.5% the multiple is about 28.6 times yearly expenses"],
        example="₹50,000 a month today is ₹6 lakh a year. After 15 years at 6% inflation that is ₹14.38 lakh a year. Divided by 3.5% the FIRE number is about ₹4.11 crore.",
        faqs=[("How much money do I need to retire early in India?", "Roughly 28 to 33 times your yearly expenses at the time you retire, which matches a 3 to 3.5% withdrawal rate. The calculator works out the exact figure for your age and inflation."),
              ("What is Lean FIRE and Fat FIRE?", "Lean FIRE covers a frugal lifestyle with a smaller corpus. Fat FIRE funds a more comfortable lifestyle and needs a much larger corpus. Enter the expenses you actually expect to see each."),
              ("Can I retire at 45 in India?", "Yes, if your corpus at 45 can support your expenses for 40 or more years. Start early, step up your SIP every year and keep expenses steady to bring the date closer."),
              ("Does the FIRE calculator include inflation?", "Yes. Expenses are grown by your inflation rate every year to the retirement date, and the corpus needed is based on that future amount.")],
        related=[("/mutual-fund-returns-calculator", "Mutual fund and SIP returns"), ("/salary-calculator", "Salary growth"), ("/loan-calculator", "Loan prepayment")]),

    "mutual-fund-returns-calculator": dict(
        title=None, desc=None,
        h2="How Is SIP Return Calculated?",
        answer="A monthly SIP grows with the formula FV = P × ((1 + i)^n − 1) ÷ i × (1 + i), where P is the monthly amount, i the monthly return and n the number of months. ₹10,000 a month for 10 years at 12% a year grows to about ₹23.2 lakh on ₹12 lakh invested.",
        steps=[("Pick a fund or category", "Large, mid, small cap, index, hybrid or debt from the 50 fund list."),
               ("Check past CAGR", "See 1, 3, 5, 10, 15 and 20 year returns from public AMFI data."),
               ("Enter SIP or lump sum", "Your monthly SIP, a one time amount and the years you plan to stay invested."),
               ("Compare with FD", "See the projected value against a fixed deposit and download the PDF.")],
        formula=["SIP future value = P × ((1 + i)^n − 1) ÷ i × (1 + i)", "i = annual return ÷ 12 ÷ 100, n = years × 12", "Lump sum future value = amount × (1 + annual return)^years"],
        example="₹10,000 a month for 10 years at 12%: i = 0.01, n = 120. Future value ≈ ₹23,23,391 on ₹12,00,000 invested, a gain of about ₹11.2 lakh before tax.",
        faqs=[("What is a good SIP return in India?", "Diversified equity funds have historically returned around 10 to 14% a year over long periods, with big swings in between. Plan with a cautious figure such as 10 to 12%."),
              ("How much will ₹5,000 a month SIP give in 20 years?", "At 12% a year, about ₹50 lakh on ₹12 lakh invested. At 10% it is about ₹38 lakh."),
              ("SIP or lump sum, which is better?", "A lump sum invested early gains more time in the market. A SIP spreads the purchase price and suits monthly income. The calculator shows both side by side."),
              ("What is the difference between CAGR and XIRR?", "CAGR measures one investment from start to end. XIRR measures a series of investments made on different dates, such as a SIP, and is the right return figure for SIPs.")],
        related=[("/fire-calculator", "FIRE calculator"), ("/salary-calculator", "Salary growth"), ("/loan-calculator", "Prepay or invest")]),

    "salary-calculator": dict(
        title="Salary Growth Calculator India: Hike, Savings and Corpus",
        desc=None,
        h2="How Do You Project Salary Growth Over Time?",
        answer="Multiply your salary by (1 + yearly increment) for every year ahead. A ₹60,000 monthly in hand salary growing 10% a year becomes about ₹1.56 lakh a month in 10 years. The calculator does this for 45 years, subtracts growing expenses and invests the surplus.",
        steps=[("Enter in hand salary", "Monthly take home pay after tax and deductions."),
               ("Enter needs and wants", "Monthly spends, each with its own yearly growth rate."),
               ("Set your increment", "The average yearly hike you expect. Use a realistic long term number."),
               ("Read the 45 year table", "Salary, savings and corpus each year, in future and today's money, with a PDF.")],
        formula=["Salary in year t = salary today × (1 + increment)^t", "Surplus = salary − needs − wants", "Value in today's money = future value ÷ (1 + inflation)^t"],
        example="₹60,000 a month with a 10% yearly hike: 60,000 × 1.1^10 ≈ ₹1,55,625 a month in year 10. If spends grow at 6%, the gap between income and spends widens every year and that gap is what builds the corpus.",
        faqs=[("What is a good salary hike in India?", "Average yearly increments in India have run around 9 to 10% in recent surveys. A job change often brings a larger one time jump."),
              ("How do I calculate my salary after an increment?", "New salary = current salary × (1 + hike percentage ÷ 100). A 12% hike on ₹50,000 gives ₹56,000."),
              ("How much of my salary should I save?", "A common rule is to save at least 20% of take home pay and raise it with every hike. The calculator shows what each extra point saved does to your corpus."),
              ("What does corpus in today's money mean?", "It removes inflation so a future number can be compared with prices today. ₹2 crore in 25 years buys much less than ₹2 crore today.")],
        related=[("/pmm-salary-2026", "PMM salary benchmarks"), ("/fire-calculator", "FIRE calculator"), ("/mutual-fund-returns-calculator", "SIP returns")]),

    "pmm-salary-2026": dict(
        title=None, desc=None,
        h2="How Much Does a Product Marketing Manager Earn in India?",
        answer="Product marketing pay in India depends most on level, then city and company stage. Use the calculator on this page to pick your title, years of experience and city and see the low, typical and strong band for 2026, then download the PDF guide.",
        steps=[("Pick your title", "From associate PMM to head of product marketing."),
               ("Enter experience", "Total years in marketing, with product marketing years counted in full."),
               ("Choose your city", "Bengaluru, Mumbai, Delhi NCR, Hyderabad, Pune, Chennai or remote."),
               ("Read your band", "Low, typical and strong pay for your profile, plus the PDF guide.")],
        formula=None, example=None,
        faqs=[("Which city pays product marketers the most in India?", "Bengaluru and Delhi NCR usually pay the most because of the density of SaaS and funded startups, followed by Mumbai, Hyderabad and Pune."),
              ("Does SaaS pay product marketers more than other industries?", "Generally yes. B2B SaaS and cybersecurity companies selling to global buyers tend to pay above consumer and services companies at the same level."),
              ("How do I negotiate a PMM salary?", "Anchor on the band for your level and city, show pipeline or launch results in numbers and ask for the range before you share your current pay."),
              ("Is product marketing a good career in India?", "Yes. Demand has grown with Indian SaaS selling globally, and the role builds skills in positioning, pricing and go to market that lead to growth and leadership roles.")],
        related=[("/salary-calculator", "Salary growth"), ("/jobs", "PMM jobs"), ("/fire-calculator", "FIRE calculator")]),

    "qums": dict(
        title="Khums Calculator (Qums) for Shia Muslims: Free and Easy",
        desc=None,
        h2="How Do You Calculate Khums?",
        answer="Khums is 20% of your yearly surplus: income left after your own and your family's reasonable expenses for the year, minus money you already paid Khums on. Half is Sahm e Imam and half is Sahm e Sadat. On a surplus of ₹3,00,000, Khums is ₹60,000.",
        steps=[("Pick your Khums date", "Usually the anniversary of the day you first started earning."),
               ("Add savings and unused items", "Cash, bank balances, investments and items bought but not used this year."),
               ("Remove exempt money", "Money already Khums paid, mahr, inheritance and items in daily use."),
               ("See the split", "20% Khums with Sahm e Imam and Sahm e Sadat worked out, then download the PDF.")],
        formula=["Surplus = savings and unused items − exempt amounts", "Khums = surplus × 20%", "Sahm e Imam = Khums ÷ 2, Sahm e Sadat = Khums ÷ 2"],
        example="Surplus ₹3,00,000: Khums = ₹60,000. Sahm e Imam ₹30,000 and Sahm e Sadat ₹30,000.",
        faqs=[("Is Khums 20 percent?", "Yes. Khums means one fifth, so it is 20% of the yearly surplus that is liable."),
              ("Is Khums due on salary?", "Salary itself is not taxed when spent on reasonable yearly needs. What remains unspent on your Khums date is surplus, and Khums is due on that."),
              ("Is Khums due on gold jewellery?", "Jewellery worn in reasonable amounts for your status is usually treated as an item in use. Gold held as savings or investment is liable. Confirm with your marja's office."),
              ("Can I pay Khums online in India?", "Many marja offices and their authorised representatives accept bank transfers. Use only the official channels listed by your marja.")],
        related=[("/salary-calculator", "Salary growth"), ("/mutual-fund-returns-calculator", "Mutual fund returns"), ("/fire-calculator", "FIRE calculator")]),

    "seo-aeo-score": dict(
        title=None, desc=None,
        h2="How Is an SEO and AEO Score Calculated?",
        answer="The checker fetches your page like a crawler and scores 16 SEO signals out of 60 and 8 answer engine signals out of 40, for a total out of 100. It adds Domain Rating from OpenSEO and lists the fixes in priority order, so you know what blocks ranking and AI citation first.",
        steps=[("Paste your URL", "Start with the home page, then a product or comparison page."),
               ("Read the two scores", "SEO out of 60 for crawl and on page signals, AEO out of 40 for AI answer signals."),
               ("Check Domain Rating", "Authority from backlinks. Under 30 means links are the ceiling."),
               ("Fix high priority items first", "Work down the action list, then rerun the check.")],
        formula=["Total score = SEO score (out of 60) + AEO score (out of 40)", "Each check carries a weight, passed checks add their points"],
        example="A page with a missing meta description, no FAQ schema and no llms.txt might score 41 of 60 on SEO and 18 of 40 on AEO, so 59 overall. Fixing those three items adds up to 18 points.",
        faqs=[("What is a good SEO score?", "70 or more out of 100 on this checker means the basics are in place. Above 85 means only refinements are left."),
              ("What is answer engine optimisation?", "AEO is making your pages easy for ChatGPT, Gemini, Perplexity and Google AI Overviews to quote. It relies on clear entities, structured data, direct answers and crawl access for AI bots."),
              ("Does llms.txt help AI visibility?", "It gives AI crawlers a curated map of your best pages. It is cheap to add and is one of the AEO checks here."),
              ("How often should I check my SEO score?", "After every major page change and at least once a month for your top five pipeline pages.")],
        related=[("/ai-visibility-checker", "AI visibility checker"), ("/company-research", "Company research"), ("/aeo-seo-in-a-box", "AEO/SEO Ranking in a box")]),

    "company-research": dict(
        title=None, desc=None,
        h2="How Do You Research a Company Before a Sales Call?",
        answer="Start with the company's own site for category, claims and logos, then check filings, funding news, headcount profiles, reviews and job posts. Note size, competitors, why buyers choose them, growth pain points and missed revenue. This tool does all of it from one homepage URL and returns a one page PDF.",
        steps=[("Paste the homepage", "Any public company or startup domain, such as accuknox.com."),
               ("Let the agent research", "It reads the site and the open web for 1 to 4 minutes."),
               ("Check confidence labels", "HIGH, MEDIUM or UNVERIFIED on every figure, with its source."),
               ("Download the one pager", "Share it with sales, partners or leadership.")],
        formula=None,
        example="A typical report covers market cap or valuation, HQ, employee count, customers, ARR, five competitors, four differentiators, buyer reasons, must fix and nice to fix pain points and three to five missed revenue plays with fixes.",
        faqs=[("How do I find a private company's revenue?", "Private companies rarely publish revenue. Look for funding announcements, analyst estimates and press interviews, and treat any figure as an estimate. The tool marks these MEDIUM or UNVERIFIED."),
              ("How do I find a company's competitors?", "Check comparison pages, review sites such as G2 and Gartner Peer Insights, analyst reports and the vendors buyers mention in reviews. The tool lists the top five with where they overlap."),
              ("What is account research in B2B sales?", "Account research is gathering facts about a target company's size, priorities, buyers and pains before outreach, so the first message and call are specific to them."),
              ("Is this company research tool free?", "Yes, with a limit of three new companies per visitor per hour. Companies researched in the last seven days load instantly from cache.")],
        related=[("/seo-aeo-score", "SEO and AEO score"), ("/partner-readiness-score", "Partner readiness score"), ("/gtm-health-check", "GTM health check")]),

    "ai-visibility-checker": dict(
        title=None, desc=None,
        h2="How Do You Get Your Brand Cited by ChatGPT and Gemini?",
        answer="Answer engines cite brands they can identify and trust. Declare your organisation with schema, keep facts consistent across your site, LinkedIn and directories, answer buyer questions directly in the first lines of a page, allow AI crawlers and earn mentions on sites the models already read.",
        steps=[("Answer 10 questions", "About entity data, content, crawl access and third party mentions."),
               ("Get your score", "Out of 100, based on how many signals you already have in place."),
               ("Read the gaps", "Each unanswered signal is a concrete fix."),
               ("Verify with the SEO and AEO score", "Run your URL through the checker to confirm the technical items.")],
        formula=["Score = points earned ÷ (10 questions × 2 points) × 100"],
        example="Answering 6 questions with full marks and 4 with partial marks earns 16 of 20 points, a score of 80.",
        faqs=[("What is AI visibility?", "AI visibility is how often answer engines such as ChatGPT, Gemini, Perplexity and Google AI Overviews mention or cite your brand when buyers ask about your category."),
              ("How do I check if ChatGPT mentions my brand?", "Ask it the questions your buyers ask, such as best tools for your category, in a fresh chat and note whether and how you appear. Repeat monthly with the same prompts."),
              ("Does schema markup help AI visibility?", "Yes. Organization, Person, FAQ and Article schema give answer engines clean facts to quote and help them resolve your brand as an entity."),
              ("How long does it take to improve AI visibility?", "Technical fixes show up within weeks of a recrawl. Third party mentions and authority take months, which is why they are worth starting now.")],
        related=[("/seo-aeo-score", "SEO and AEO score"), ("/aeo-seo-case-study", "AEO case study"), ("/aeo-seo-in-a-box", "AEO/SEO Ranking in a box")]),

    "gtm-health-check": dict(
        title=None, desc=None,
        h2="How Do You Measure Go To Market Health?",
        answer="A healthy go to market has a written ICP, one positioning statement sales repeats, a pipeline target tied to revenue, tracked conversion by stage and a regular review that changes spend. This 10 question check scores each of those areas so you know where pipeline leaks first.",
        steps=[("Answer 10 questions", "ICP, positioning, pipeline targets, channels, tracking and review rhythm."),
               ("See your score", "Out of 100, with a label for where you stand."),
               ("Find the weakest area", "Low scoring answers point to the fix with the most leverage."),
               ("Book a review", "Walk through the result with Syed if you want a 90 day plan.")],
        formula=["Score = points earned ÷ (10 questions × 2 points) × 100"],
        example="8 strong answers and 2 weak ones earn 16 of 20 points, a score of 80. The two weak answers are where to start.",
        faqs=[("What is a GTM strategy?", "A go to market strategy defines who you sell to, what problem you solve for them, how you reach them and how you measure the pipeline it creates."),
              ("What are GTM metrics?", "Pipeline created, win rate, sales cycle length, customer acquisition cost, payback period and net revenue retention are the core set for B2B SaaS."),
              ("How often should a startup review its go to market?", "Pipeline weekly, channel spend monthly and ICP plus positioning every quarter or after a major product change."),
              ("What is an ICP?", "An ideal customer profile describes the companies most likely to buy, succeed and expand, by industry, size, region, tech stack and trigger events.")],
        related=[("/partner-readiness-score", "Partner readiness score"), ("/company-research", "Company research"), ("/gtm-in-a-box", "GTM in a box")]),

    "partner-readiness-score": dict(
        title=None, desc=None,
        h2="How Do You Know Your Partner Program Is Ready?",
        answer="A partner program is ready when you have a defined partner profile, clear margins, deal registration, enablement material, a named partner manager and pipeline targets per partner. This 10 question score checks each of those so you launch or fix the program before signing more partners.",
        steps=[("Answer 10 questions", "Partner profile, economics, deal registration, enablement and tracking."),
               ("See your score", "Out of 100, with a readiness label."),
               ("Fix the gaps", "Low scores show what partners will hit first."),
               ("Plan the launch", "Use the gaps as the first 90 day partner plan.")],
        formula=["Score = points earned ÷ (10 questions × 2 points) × 100"],
        example="Strong answers on profile and margins but none on deal registration and enablement might score 60. Those two gaps are the usual reason partners sign and never sell.",
        faqs=[("What makes a good channel partner program?", "Clear partner tiers, healthy margins, protected deal registration, fast enablement, co marketing funds and a partner manager who reviews pipeline every month."),
              ("What is deal registration?", "Deal registration lets a partner claim an opportunity so the vendor protects it from conflict and pays the agreed margin when it closes."),
              ("How many partners should a startup sign?", "Start with a few partners that match your partner profile and prove pipeline with them before adding more. Depth beats logo count."),
              ("How do you measure partner performance?", "Partner sourced pipeline, partner influenced revenue, win rate on registered deals and time to first deal after onboarding.")],
        related=[("/gtm-health-check", "GTM health check"), ("/company-research", "Company research"), ("/partner-revenue-in-a-box", "Partner Revenue in a box")]),
}

CSS = r'''
/* ===== 2026-11-03 calculator guide (SEO and AEO) ===== */
.sg{padding:10px 0 40px}
.sg-ans{border-radius:20px;padding:22px 24px;background:linear-gradient(120deg,var(--accent-soft),var(--card));border:1px solid var(--line);border-left:4px solid var(--accent)}
.sg-ans small{display:block;font:700 11px "JetBrains Mono",monospace;letter-spacing:.14em;text-transform:uppercase;color:var(--accent);margin-bottom:8px}
.sg-ans p{margin:0;font-size:17px;line-height:1.6;color:var(--ink)}
.sg-grid{display:grid;grid-template-columns:1.1fr .9fr;gap:16px;margin-top:16px}
.sg-box{border:1px solid var(--line);border-radius:18px;padding:20px 22px;background:var(--card)}
.sg-box h3{font-size:18px;margin:0 0 12px}
.sg-steps{list-style:none;margin:0;padding:0;display:grid;gap:12px;counter-reset:sg}
.sg-steps li{counter-increment:sg;position:relative;padding-left:40px}
.sg-steps li::before{content:counter(sg);position:absolute;left:0;top:0;width:28px;height:28px;border-radius:9px;background:var(--accent-soft);color:var(--accent);font-weight:800;display:grid;place-items:center;font-size:14px}
.sg-steps b{display:block;font-size:15.5px;color:var(--ink)}.sg-steps span{font-size:14.5px;color:var(--ink-2);line-height:1.5}
.sg-f{margin:0 0 12px;padding:12px 14px;border-radius:12px;background:var(--bg-soft);border:1px solid var(--line);font:500 14px/1.7 "JetBrains Mono",monospace;color:var(--ink);overflow-x:auto}
.sg-f div{white-space:nowrap}
.sg-ex{margin:0;font-size:15px;line-height:1.6;color:var(--ink-2)}.sg-ex b{color:var(--ink)}
.sg-faq{margin-top:16px}
.sg-faq h3{font-size:18px;margin:0 0 6px}
.sg-q{border-top:1px solid var(--line);padding:14px 0}
.sg-q h4{margin:0 0 6px;font-size:16px;color:var(--ink)}
.sg-q p{margin:0;color:var(--ink-2);line-height:1.6;font-size:15px}
.sg-rel{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin-top:14px;font-size:14px;color:var(--ink-3)}
.sg-rel a{padding:7px 12px;border-radius:999px;border:1px solid var(--line);background:var(--card);color:var(--ink);font-weight:600;text-decoration:none}
.sg-rel a:hover{border-color:var(--accent);color:var(--accent)}
@media (max-width:860px){.sg-grid{grid-template-columns:1fr}}
.qb-apply span{font-size:11px}
'''


def _section(slug, d):
    steps = "".join(f"<li><b>{E(t)}</b><span>{E(x)}</span></li>" for t, x in d["steps"])
    right = ""
    if d.get("formula"):
        right += '<h3>The formula</h3><div class="sg-f">' + "".join(f"<div>{E(l)}</div>" for l in d["formula"]) + "</div>"
    if d.get("example"):
        right += f'<h3>Worked example</h3><p class="sg-ex">{E(d["example"])}</p>'
    if not right:
        right = '<h3>What you get</h3><p class="sg-ex">' + E(d["answer"]) + "</p>"
    faqs = "".join(f'<div class="sg-q"><h4>{E(q)}</h4><p>{E(a)}</p></div>' for q, a in d["faqs"])
    rel = "".join(f'<a href="{h}">{E(t)}</a>' for h, t in d["related"])
    return (f'<section class="bx-sec sg" id="guide" aria-labelledby="sg-h"><div class="wrap">'
            f'<div class="sec-head reveal" style="text-align:left;margin-left:0"><span class="eyebrow">Guide</span><h2 class="display" id="sg-h">{E(d["h2"])}</h2></div>'
            f'<div class="sg-ans reveal"><small>Quick answer</small><p>{E(d["answer"])}</p></div>'
            f'<div class="sg-grid"><div class="sg-box reveal"><h3>How to use it</h3><ol class="sg-steps">{steps}</ol></div>'
            f'<div class="sg-box reveal">{right}</div></div>'
            f'<div class="sg-box sg-faq reveal"><h3>More questions people ask</h3>{faqs}</div>'
            f'<div class="sg-rel"><span>Related tools</span>{rel}</div>'
            f'</div></section>')


def _merge_schema(html, slug, d, url):
    """Append the new questions to the page's FAQPage, add a HowTo, bump dateModified."""
    blocks = list(re.finditer(r'<script type="application/ld\+json">(.*?)</script>', html, re.S))
    qs = [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in d["faqs"]]
    howto = {"@type": "HowTo", "@id": url + "#howto", "name": d["h2"].rstrip("?"), "description": d["answer"],
             "step": [{"@type": "HowToStep", "position": i + 1, "name": t, "text": x} for i, (t, x) in enumerate(d["steps"])]}
    done_faq = done_howto = False
    has_faq = any('"FAQPage"' in b.group(1) for b in blocks)
    for b in blocks:
        try:
            data = json.loads(b.group(1))
        except Exception:
            continue
        nodes = data["@graph"] if isinstance(data, dict) and "@graph" in data else [data] if isinstance(data, dict) else data
        changed = False
        for n in nodes:
            if not isinstance(n, dict):
                continue
            t = n.get("@type")
            if (t == "FAQPage" or (isinstance(t, list) and "FAQPage" in t)) and not done_faq:
                names = {x.get("name") for x in n.get("mainEntity", [])}
                n["mainEntity"] = n.get("mainEntity", []) + [x for x in qs if x["name"] not in names]
                done_faq = changed = True
            if t == "HowTo":
                done_howto = True
            if t == "WebPage" or (isinstance(t, list) and "WebPage" in t):
                n["dateModified"] = DATE
                changed = True
        if isinstance(data, dict) and "@graph" in data and not done_howto:
            data["@graph"].append(howto)
            done_howto = changed = True
        if not done_faq and not has_faq and isinstance(data, dict) and "@graph" in data:
            data["@graph"].append({"@type": "FAQPage", "mainEntity": qs})
            done_faq = changed = True
        if changed:
            html = html.replace(b.group(0), '<script type="application/ld+json">' + json.dumps(data, ensure_ascii=False) + "</script>", 1)
    extra = []
    if not done_faq:
        extra.append({"@type": "FAQPage", "mainEntity": qs})
    if not done_howto:
        extra.append(howto)
    if extra:
        html = html.replace("</head>", '<script type="application/ld+json">' + json.dumps({"@context": "https://schema.org", "@graph": extra}, ensure_ascii=False) + "</script>\n</head>", 1)
    return html


def _set_meta(html, d):
    if d.get("title"):
        t = E(d["title"])
        html = re.sub(r"<title>.*?</title>", f"<title>{t}</title>", html, count=1, flags=re.S)
        html = re.sub(r'(<meta property="og:title" content=")[^"]*(")', r"\g<1>" + t + r"\2", html, count=1)
        html = re.sub(r'(<meta name="twitter:title" content=")[^"]*(")', r"\g<1>" + t + r"\2", html, count=1)
    if d.get("desc"):
        ds = E(d["desc"])
        for pat in (r'(<meta name="description" content=")[^"]*(")', r'(<meta property="og:description" content=")[^"]*(")', r'(<meta name="twitter:description" content=")[^"]*(")'):
            html = re.sub(pat, r"\g<1>" + ds + r"\2", html, count=1)
    return html


def apply(html, name, site):
    slug = name[:-5] if name.endswith(".html") else name
    d = PAGES.get(slug)
    if not d or "</main>" not in html:
        return html
    if "data-sg=" in html:  # already applied this build: strip and reapply so edits flow through
        html = re.sub(r'<section class="bx-sec sg" id="guide".*?</section>', "", html, flags=re.S)
    html = html.replace("</main>", _section(slug, d) + "\n</main>", 1)
    html = html.replace('<section class="bx-sec sg" id="guide"', '<section class="bx-sec sg" id="guide" data-sg="1"', 1)
    html = _set_meta(html, d)
    html = _merge_schema(html, slug, d, site + "/" + slug)
    return html
