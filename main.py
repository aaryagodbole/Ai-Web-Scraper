import streamlit as st
from scrape import scrape_website, extract_body_content, clean_body_content, split_dom_content
from parse import parse_with_langchain

st.set_page_config(page_title="🕷️ AI Web Scraper", layout="centered")
st.title("🕷️ Smart Web Scraper (Selenium + LangChain + Ollama)")

# ✅ Take URL from user (NO DEFAULT!)
url = st.text_input("Enter website URL")

# ✅ Take parse instruction from user (keep default here if you want)
parse_description = st.text_area("What do you want to extract?", "")

# ✅ Only allow scraping if URL is filled
if st.button("Run Scraper"):
    if not url:
        st.warning("⚠️ Please enter a URL first.")
    else:
        with st.spinner(f"Scraping from {url}..."):
            raw_html = scrape_website(url)
            body = extract_body_content(raw_html)
            cleaned = clean_body_content(body)
            chunks = split_dom_content(cleaned)

            st.session_state["scraped_chunks"] = chunks
            st.session_state["url_used"] = url
            st.success(f"✅ Scraped and chunked into {len(chunks)} parts from {url}.")

# ✅ Parsing section
if st.button("Parse Content with AI"):
    if "scraped_chunks" not in st.session_state:
        st.warning("⚠️ Run the scraper first.")
    elif not parse_description.strip():
        st.warning("⚠️ Please enter what to extract.")
    else:
        chunks = st.session_state["scraped_chunks"]
        st.write(f"🧠 Parsing content from: `{st.session_state['url_used']}`")
        parsed = parse_with_langchain(chunks, parse_description, show_spinner=st.spinner)
        st.success("✅ Parsing done!")
        st.markdown(parsed)
