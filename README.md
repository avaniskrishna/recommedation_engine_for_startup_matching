# ✨ Startup Matchmaking Engine: Connecting Founders with Experts ✨

## 🚀 Project Overview

This project introduces a **Recommendation Engine** meticulously crafted to bridge the crucial gap between **Founders** in search of specialized support and **Service Providers/Mentors** offering their invaluable expertise.
The core mission is to answer pivotal questions for both sides of the entrepreneurial spectrum:

  * **For Founders:** "Who is the most suitable expert to assist me at my current startup stage and with my specific needs?"
  * **For Service Providers/Mentors:** "Which exciting startup projects align perfectly with my unique skills, extensive experience, and current availability?"

By leveraging a sophisticated **weighted scoring algorithm** combined with advanced **semantic analysis**, this engine precisely identifies optimal pairings, thereby fostering more efficient collaborations and accelerating the journey of startup growth.

## 🌟 Key Features

  * **Two-Sided Matching:** Provides intelligent, tailored recommendations for both Founders (identifying their top Service Providers/Mentors) and Service Providers/Mentors (pinpointing their most compatible Founder projects).
  * **Intelligent Scoring Algorithm:** At its heart lies a robust, weighted scoring system (normalized to a scale of 0-100) that meticulously evaluates compatibility across multiple critical criteria.
  * **Semantic Skill & Need Matching:** Goes beyond simple keyword matching\! Utilizes a powerful pre-trained **AI model (`all-MiniLM-L6-v2` from `SentenceTransformers`)** to deeply understand the underlying meaning and context of project needs and expertise areas.
  * **Multi-Factor Compatibility Analysis:** Considers a diverse array of crucial factors for a truly comprehensive match:
      * **🌐 Domain Relevance:** Seamlessly matches startup industry with the provider's preferred industry.
      * **🛠️ Skill Alignment:** Ensures a precise fit between technical requirements (e.g., Python) and core skills.
      * **🎯 Project Type Compatibility:** Aligns specific project needs (e.g., UI/UX Revamp) with relevant expertise areas (e.g., Design Expert).
      * **⏰ Timeline Fit:** Compares project deadlines with provider availability for realistic and efficient collaboration.
      * **📈 Startup Stage & Experience:** (Optional) Deeper consideration for nuanced compatibility based on growth phase.
  * **Structured Recommendations:** Generates clear, actionable lists of top matches, complete with user IDs, calculated match scores, and a concise explanation of the key reasons behind each recommendation.
  * **Interactive Streamlit Dashboard:** A user-friendly and intuitive web interface empowers users to effortlessly explore individual user profiles, view personalized top recommendations, and visualize the overall match landscape.
  * **Comprehensive Visualization:** Features an insightful **heatmap** that visually represents match scores across all Founder-Provider pairs, offering a high-level, at-a-glance overview of potential synergies.

## 🧠 How the Matching Logic Works

The core intelligence of this recommendation engine is powered by a robust, weighted scoring algorithm, thoroughly detailed in the `Logic behind the code.docx` document. In essence, it operates on three primary components:

1.  ### Semantic Skill & Need Matching (50% Weight)

      * Instead of basic keyword comparisons, a pre-trained `SentenceTransformer` model (`all-MiniLM-L6-v2`) transforms textual descriptions (such as a founder's `project_need` and a provider's `expertise_area` and `core_skill`) into rich numerical vectors, or embeddings.
      * **Cosine Similarity** is then computed between these vectors to ascertain their semantic closeness, yielding a score out of 100.

2.  ### Industry & Project Type Compatibility (30% Weight)

      * **Industry Match:** A direct comparison is made between `startup_industry` and `industry_preference`. A perfect alignment scores 100, while partial matches (e.g., related sectors) receive proportionally lower scores, and no match scores 0.
      * **Project Type Match:** This evaluates the alignment between `project_need` and `preferred_project_type`, with a scoring mechanism similar to the industry match.

3.  ### Timeline Fit (20% Weight)

      * This component compares the `project_deadline` with the provider's `availability`. Scores are assigned based on the degree of alignment, with perfect synchronization earning 100 points and increasing penalties applied for mismatches.

These individual component scores are then intelligently combined using their respective weights to produce a **Final Match Score** for every potential Founder-Service Provider pair.

## 📂 Repository Contents

  * `Cleaned_User_Matching_Dataset.csv`: The foundational dataset containing comprehensive user profiles for both Founders and Service Providers/Mentors. This data serves as the primary input for the recommendation engine.
  * `Code.ipynb`: A Jupyter Notebook encapsulating the core Python logic for data loading, preprocessing, the implementation of the sophisticated matching algorithm, score calculation, and the generation of comprehensive match results.
  * `dashboard.py`: The Python script that drives the interactive and intuitive Streamlit web application. This file defines the user interface and seamlessly integrates with the matching logic to present recommendations and visualizations.
  * `Logic behind the code.docx`: A detailed Microsoft Word document that provides an in-depth explanation of the conceptual framework, the intricate scoring system, and the step-by-step logic implemented within `Code.ipynb` and the dashboard.
  * `requirements.txt`: A comprehensive list of all necessary Python libraries and their specific versions required to successfully run both the core code and the Streamlit dashboard.
  * `README.md`: You are currently reading this file\! It provides a holistic overview of the project, detailed setup instructions, and deployment information.

## 📊 Dataset Structure

The `Cleaned_User_Matching_Dataset.csv` file comprises 100 meticulously curated user profiles, evenly divided into 50 Founders (identified by user IDs beginning with 'F') and 50 Service Providers/Mentors (identified by user IDs beginning with 'S'). Each user profile is enriched with relevant attributes, including:

**Founders (Demand Side):**

  * `user_id`
  * `startup_stage`
  * `startup_industry`
  * `project_need`
  * `tech_requirement`
  * `project_deadline`

**Service Providers / Mentors (Supply Side):**

  * `user_id`
  * `user_type` (e.g., "Service Provider" or "Mentor")
  * `expertise_area`
  * `industry_preference`
  * `preferred_project_type`
  * `core_skill`
  * `availability`


## 🖥️ Usage Guide (Streamlit Dashboard)

1.  **User Role Toggle:** In the sidebar on the left, effortlessly switch your perspective by selecting whether you want to "View As" a `Founder` or a `Service Provider`.
2.  **Select User ID:** From the convenient dropdown menu in the sidebar, choose a specific `user_id` you wish to explore.
3.  **View Profile Details:** The main content area will dynamically display the complete profile details for your selected user in a clear JSON format.
4.  **Explore Recommendations:** Directly below the profile, you'll find the "Top 3 Recommendations" specifically tailored for the selected user, complete with their calculated `Final Score`.
      * If you selected a Founder, the recommendations will showcase the most suitable Service Providers.
      * If you selected a Service Provider, the recommendations will highlight the most compatible Founders.
5.  **Overall Match Matrix:** A visually engaging heatmap provides a comprehensive overview, illustrating the match scores between all Founders and Service Providers. This allows for quick identification of strong potential connections.
6.  **Download Full Results:** A dedicated download button empowers you to export the complete set of match results (every Founder-Provider pair with their respective scores) as a convenient CSV file.

## 🌐 Live Demo

You can interact with the deployed Streamlit dashboard live on Streamlit Community Cloud:

[**🚀 Explore the Live Dashboard Here\! 🚀**](https://www.google.com/search?q=YOUR_STREAMLIT_APP_URL_HERE)

## 🛠️ Technologies Used

This project leverages a powerful stack of modern data science and web development tools:

  * **Python:** The core programming language underpinning the entire project's logic and application.
  * **Pandas:** Indispensable for efficient data manipulation, cleaning, and analysis of the user datasets.
  * **Sentence Transformers:** Utilized for generating sophisticated semantic embeddings from textual data and calculating cosine similarity, enabling intelligent text matching (`all-MiniLM-L6-v2` model).
  * **Streamlit:** The framework chosen for rapidly building and deploying the interactive, user-friendly web dashboard.
  * **Plotly Express:** Employed for creating rich, interactive visualizations, most notably the comprehensive match matrix heatmap.

## 📜 License

This project is open-source and distributed under the **MIT License**. See the `LICENSE` file for more details.

## 📧 Contact

For any inquiries, feedback, or potential collaborations, please don't hesitate to reach out:

  * **Your Name / GitHub Profile:** [Your GitHub Username](https://github.com/avaniskrishna)
  * **LinkedIn (Optional):** [Your LinkedIn Profile URL](https://linkedin.com/in/avani-s-krishna2004)

-----
