"""20 ground-truth Q&A pairs for RAGAS evaluation."""

EVAL_QUESTIONS = [
    {
        "question": "What is Australia's total fertility rate as of 2022?",
        "ground_truth": "Australia's total fertility rate was 1.58 in 2022, below the replacement level of 2.1, according to the ABS Births, Australia 2022 report.",
    },
    {
        "question": "How does Japan's aging population compare to Australia's?",
        "ground_truth": "Japan's population aged 65 and over reached 29.1% in 2022, making it the world's most aged society. Australia's equivalent share was 16.8% in 2022, significantly lower than Japan's.",
    },
    {
        "question": "What is Australia's old-age dependency ratio and how is it projected to change?",
        "ground_truth": "Australia's old-age dependency ratio was 27 per 100 working-age population in 2022 and is projected to reach 44 by 2060, according to the Australian Intergenerational Report 2023.",
    },
    {
        "question": "Which OECD country has the lowest fertility rate?",
        "ground_truth": "South Korea recorded the lowest TFR of any OECD country at 0.78 in 2022, far below the replacement level of 2.1, with Seoul's TFR falling below 0.6.",
    },
    {
        "question": "How has net overseas migration to Australia changed since 2000?",
        "ground_truth": "Australia's net overseas migration grew from around 103,000 in 2000 to a record 518,000 in 2022-23, making migration the primary driver of population growth (ABS, Migration, Australia 2022-23).",
    },
    {
        "question": "What is Australia's projected population by 2071?",
        "ground_truth": "The ABS projects Australia's population to reach 38.8 million by 2071 under a medium scenario, assuming net overseas migration of 235,000 per year and a TFR stabilising near 1.62.",
    },
    {
        "question": "Which OECD countries have the highest older worker participation rates?",
        "ground_truth": "Sweden leads the OECD with 60% labour force participation among workers aged 60-74 in 2022. Japan (71% for ages 60-69) and Norway (65% for ages 55-74) also rank among the highest.",
    },
    {
        "question": "How does Australia's life expectancy compare to Japan and Spain?",
        "ground_truth": "Australia's life expectancy was 83.3 years in 2022. Japan had the highest at 84.3 years and Spain was at 83.5 years, both slightly above Australia. All three are among the world's highest.",
    },
    {
        "question": "What is South Korea's projected old-age dependency ratio by 2060?",
        "ground_truth": "South Korea's old-age dependency ratio is projected to reach 97 by 2060 — nearly one retiree per worker — from 25 in 2022, representing the fastest rising trajectory in the OECD (Statistics Korea, 2023).",
    },
    {
        "question": "How has Germany's employment rate for older workers changed since 2000?",
        "ground_truth": "Germany's employment rate among workers aged 55-64 rose dramatically from 38% in 2000 to 73% in 2022, one of the fastest increases in the OECD, driven by Hartz IV reforms and reduced early retirement incentives.",
    },
    {
        "question": "Which countries have successfully raised older worker participation?",
        "ground_truth": "Germany, Sweden, Japan, Finland, and Norway have achieved the strongest improvements in older worker participation. Germany rose from 38% to 73% (ages 55-64) and Finland from 42% to 67% between 2000 and 2022.",
    },
    {
        "question": "What is Australia's superannuation system and how large is it?",
        "ground_truth": "Australia's compulsory superannuation system held AUD 3.5 trillion in assets in 2022, the fourth-largest pension pool globally. The contribution rate reached 11% in 2023, rising to 12% by 2025 (APRA, 2022).",
    },
    {
        "question": "Which country spends the most on pensions as a share of GDP?",
        "ground_truth": "Italy spends 16.0% of GDP on pensions, the highest in the OECD, and provides pension replacement rates of around 93% for average earners, creating strong political resistance to reform (INPS, 2022).",
    },
    {
        "question": "How does Australia's social cohesion compare to Nordic countries?",
        "ground_truth": "Australia's Scanlon Foundation social cohesion index fell from 88 in 2007 to 74 in 2022. Norway's social trust score was 74 in 2022, Finland's was 72, and Sweden's was 77 — comparable to Australia's declining score.",
    },
    {
        "question": "What are the main drivers of Canada's population growth?",
        "ground_truth": "Canada admitted a record 432,000 permanent residents in 2022 and projects immigration to sustain population growth to 57 million by 2068. With a TFR of only 1.40, natural increase is minimal and immigration is Canada's primary demographic driver.",
    },
    {
        "question": "How has France managed to maintain a higher fertility rate than other EU countries?",
        "ground_truth": "France maintained a TFR of 1.80 in 2022, the highest in the EU, supported by generous family benefits, subsidised childcare, and strong social norms around combining work and motherhood. French pro-natalist policy is frequently cited as a model (OECD, 2023).",
    },
    {
        "question": "What is the UK's life expectancy trend and why has it stagnated?",
        "ground_truth": "UK life expectancy was 80.7 years in 2022, having stagnated since 2011 — an anomaly among wealthy nations. Austerity-related cuts to social services, rising obesity, and NHS pressures are cited as drivers of this unusual stagnation (ONS, 2022).",
    },
    {
        "question": "Which OECD countries combine very low fertility with rapid population aging?",
        "ground_truth": "Japan (TFR 1.20, 65+ share 29.1%), South Korea (TFR 0.78, 65+ share 17.5%), and Italy (TFR 1.25, 65+ share 23.7%) combine the lowest fertility rates with significant aging, creating the most acute long-term demographic-fiscal challenges.",
    },
    {
        "question": "What is the fertility rate in Brazil?",
        "ground_truth": "The corpus does not contain data on Brazil's fertility rate. The dataset covers Australia and OECD peer countries including Japan, Germany, France, UK, Canada, Italy, Sweden, South Korea, and New Zealand.",
    },
    {
        "question": "How does the Netherlands' pension system compare to Australia's superannuation?",
        "ground_truth": "The Netherlands holds pension assets worth 220% of GDP, the highest in the OECD. Australia's superannuation held 3.5 trillion AUD in 2022. Both are funded systems; Sweden's notional defined contribution model consistently scores highest on the Melbourne Mercer Global Pension Index.",
    },
]
