import streamlit as st
import requests
import os
from dotenv import load_dotenv
from news_api import NewsAPI
from news_video import VideoGenerator

load_dotenv()

news_api_key = os.getenv('NEWS_API_KEY')
news_client = NewsAPI(api_key=news_api_key)
video_api_key = os.getenv("BEARER_TOKEN")
video_generator = VideoGenerator(video_api_key)

st.set_page_config(
    page_title="AI News Anchor",
    layout="wide"
)

st.title("AI News Anchor")
st.markdown('<style>h1{color: orange; text-align: center;}</style>', unsafe_allow_html=True)
st.subheader('Built with Midjourney, OpenAI, D-ID, Streamlit and ❤️')
st.markdown('<style>h3{color: pink;  text-align: center;}</style>', unsafe_allow_html=True)

image_url = st.text_input("Enter Image URL", "")
query = st.text_input("Enter Query Keywords", "")
num_news = st.slider("Number of News", min_value=1, max_value=5, value=3)

if st.button("Generate"):
    if image_url.strip() and query.strip() and num_news > 0:
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col1:
            st.info("Your AI News Anchor: Sophie")
            st.image(image_url, caption="Anchor Image", use_column_width=True)
        
        with col2:
            desc_list = news_client.get_news_descriptions(query, num_news=num_news)
            st.success("Your Fetched News")
            st.write(desc_list)
            numbered_paragraphs = "\n".join([f"{i + 1}. {paragraph}" for i, paragraph in enumerate(desc_list)])
            st.write(numbered_paragraphs)
        
        with col3:
            final_text = f"""
                Hello World, I'm Sophie, your AI News Anchor. Bringing you the latest updates for {query}.
                Here are the news for you: {numbered_paragraphs}
                That's all for today. Stay tuned for more news, Thank you!
            """
            try:
                video_url = video_generator.generate_video(final_text, image_url)
                st.warning("AI News Anchor Video")
                st.video(video_url)
            except Exception as e:
                st.error(f"An error occurred: {e}")
    else:
        st.write("Failed to fetch news data. Please check your query and API key.")
