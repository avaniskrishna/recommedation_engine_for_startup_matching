import streamlit as st
import pandas as pd
from sentence_transformers import SentenceTransformer, util
import plotly.express as px

st.set_page_config(layout="wide")


@st.cache_resource
def load_model():
    return SentenceTransformer('all-MiniLM-L6-v2')

model = load_model()

@st.cache_data
def load_data():
    file_path = "C:/Users/avani/OneDrive/Desktop/STUDY PLAN/scaledux/TASK3/Cleaned_User_Matching_Dataset.csv"
    df = pd.read_csv(file_path)
    founders_df = df[df['user_id'].str.startswith('F')].copy()
    providers_df = df[df['user_id'].str.startswith('S')].copy()
    return founders_df, providers_df

founders_df, providers_df = load_data()

def calculate_semantic_score(text1, text2):
    embedding1 = model.encode(text1, convert_to_tensor=True)
    embedding2 = model.encode(text2, convert_to_tensor=True)
    cosine_score = util.pytorch_cos_sim(embedding1, embedding2)
    return int(cosine_score.item() * 100)

def calculate_industry_score(founder_industry, provider_preference):
    if founder_industry == provider_preference:
        return 100
    elif provider_preference == 'Any':
        return 70
    else:
        return 0

def calculate_timeline_score(project_deadline, provider_availability):
    deadline_mapping = {'Immediate': 3, 'Within 1 Month': 2, 'Flexible': 1}
    availability_mapping = {'Immediate': 3, 'Within 2 Weeks': 2, 'In 1-2 Months': 1, 'Unavailable': 0}
    founder_need = deadline_mapping.get(project_deadline, 0)
    provider_can_start = availability_mapping.get(provider_availability, 0)
    return 100 if provider_can_start >= founder_need else 0

def calculate_match_score(founder, provider):
    weights = {'skill_and_project': 0.50, 'industry': 0.30, 'timeline': 0.20}
    skill_score = calculate_semantic_score(founder['tech_requirement'], provider['core_skill'])
    project_type_score = calculate_semantic_score(founder['project_need'], provider['expertise_area'])
    avg_semantic_score = (skill_score + project_type_score) / 2
    industry_score = calculate_industry_score(founder['startup_industry'], provider['industry_preference'])
    timeline_score = calculate_timeline_score(founder['project_deadline'], provider['availability'])
    final_score = (avg_semantic_score * weights['skill_and_project']) + \
                  (industry_score * weights['industry']) + \
                  (timeline_score * weights['timeline'])
    return {'Final Score': round(final_score)}

@st.cache_data
def compute_all_matches(_founders_df, _providers_df):
    all_scores = []
    for _, founder in _founders_df.iterrows():
        for _, provider in _providers_df.iterrows():
            score_details = calculate_match_score(founder, provider)
            result = {'founder_id': founder['user_id'], 'provider_id': provider['user_id'], **score_details}
            all_scores.append(result)
    return pd.DataFrame(all_scores)

def get_top_matches(user_id, results_df, top_n=3):
    if user_id.startswith('F'):
        matches = results_df[results_df['founder_id'] == user_id]
        return matches.sort_values(by='Final Score', ascending=False).head(top_n)
    else:
        matches = results_df[results_df['provider_id'] == user_id]
        return matches.sort_values(by='Final Score', ascending=False).head(top_n)

@st.cache_data
def convert_df_to_csv(df):
    return df.to_csv(index=False).encode('utf-8')


match_results_df = compute_all_matches(founders_df, providers_df)
match_matrix = match_results_df.pivot_table(index='founder_id', columns='provider_id', values='Final Score')

# STREAMLIT USER INTERFACE 
st.title("Intelligent Matching Engine")
st.markdown("This dashboard simulates intelligent matchmaking between **Founders** and **Service Providers**. Select a user from the sidebar to view their top recommendations.")

# Sidebar Selections
st.sidebar.header("User Selection Panel")
view_as = st.sidebar.radio("View As:", ["Founder", "Service Provider"])
all_user_ids = ['-'] + (founders_df['user_id'].tolist() if view_as == "Founder" else providers_df['user_id'].tolist())
selected_user = st.sidebar.selectbox("Choose a User ID:", all_user_ids)

# User Info & Recommendations
if selected_user != '-':
    st.subheader(f"🧑‍💼 Profile Details for {selected_user}")
    user_df = founders_df if selected_user.startswith('F') else providers_df
    user_info = user_df[user_df['user_id'] == selected_user]
    st.json(user_info.to_dict(orient="records")[0])

    st.subheader(f"🔍 Top 3 Recommendations for {selected_user}")
    recommendations = get_top_matches(selected_user, match_results_df)
    if selected_user.startswith('F'):
        st.dataframe(recommendations[['provider_id', 'Final Score']])
    else:
        st.dataframe(recommendations[['founder_id', 'Final Score']])

#heatmap
st.subheader("📊 Overall Match Matrix")
fig = px.imshow(
    match_matrix,
    labels=dict(x="Provider ID", y="Founder ID", color="Match Score"),
    width=1200,
    height=700
)
st.plotly_chart(fig, use_container_width=True)

#export data 
st.subheader("📥 Export Match Data")
csv_data = convert_df_to_csv(match_results_df)
st.download_button(
    label="Download Full Match Scores as CSV",
    data=csv_data,
    file_name='match_scores.csv',
    mime='text/csv'
)
