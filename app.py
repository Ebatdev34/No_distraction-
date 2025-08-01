import streamlit as st
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote
import random
import webbrowser

st.set_page_config(page_title="Curiosity Searcher", page_icon="🔍", layout="centered")

# ----- Session state to save search history -----
if "search_history" not in st.session_state:
    st.session_state.search_history = []

# ----- Curiosity prompt ideas -----
curiosity_prompts = [
    "What if we could feel sound?",
    "How do black holes affect time?",
    "What makes a memory permanent?",
    "Can AI feel emotions?",
    "Why do humans dream?",
    "Is reality a simulation?",
    "What if gravity disappeared for 5 seconds?",
    "How does music affect the brain?",
    "What is consciousness?",
    "What happens if the sun suddenly vanished?"
]

# ----- UI Layout -----
st.title("🔍 Curiosity Searcher")
st.caption("No trends. No distractions. Just wonder.")

col1, col2 = st.columns([3, 1])
with col1:
    query = st.text_input("What are you curious about today?", placeholder="e.g. 'how dreams work' or 'AI emotions'")
with col2:
    if st.button("🎲 Random Prompt"):
        query = random.choice(curiosity_prompts)

# ----- YouTube Search Logic -----
def search_youtube(query, max_results=10):
    search_url = f"https://www.youtube.com/results?search_query={quote(query)}"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(response.text, "lxml")

    videos = []
    for link in soup.find_all("a", href=True):
        href = link["href"]
        title = link.get("title")
        if href.startswith("/watch") and title:
            video_url = f"https://www.youtube.com{href}"
            videos.append({"title": title, "url": video_url})
        if len(videos) >= max_results:
            break
    return videos

# ----- Course Finder -----
def search_free_courses(topic):
    course_links = [
        f"https://www.coursera.org/search?query={quote(topic)}",
        f"https://www.edx.org/search?q={quote(topic)}",
        f"https://www.udemy.com/courses/search/?q={quote(topic)}&price=price-free",
        f"https://www.khanacademy.org/search?page_search_query={quote(topic)}"
    ]
    return course_links

# ----- Display Results -----
if query:
    st.session_state.search_history.append(query)
    with st.spinner("Looking into the universe..."):
        yt_results = search_youtube(query)
        course_links = search_free_courses(query)

    st.subheader("📺 YouTube Explorations")
    for i, video in enumerate(yt_results):
        col1, col2 = st.columns([6, 1])
        with col1:
            st.markdown(f"{i+1}. [{video['title']}]({video['url']})")
        with col2:
            if st.button("🔗 Open", key=f"yt_{i}"):
                webbrowser.open(video['url'])

    st.subheader("📚 Free Learning Resources")
    for i, link in enumerate(course_links):
        col1, col2 = st.columns([6, 1])
        with col1:
            st.markdown(f"{i+1}. [Explore Courses]({link})")
        with col2:
            if st.button("🔗 Open", key=f"course_{i}"):
                webbrowser.open(link)

# ----- Show Search History -----
if st.session_state.search_history:
    st.markdown("---")
    with st.expander("🧠 Your Curiosity Trail"):
        for i, q in enumerate(reversed(st.session_state.search_history[-10:]), 1):
            st.markdown(f"{i}. `{q}`")

# ----- Minimal Footer -----
st.markdown("""<hr style="margin-top:3em; opacity:0.2" />""", unsafe_allow_html=True)
st.caption("Made for the curious soul. No likes, no noise — just learning.")
