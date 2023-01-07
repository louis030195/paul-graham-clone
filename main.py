import streamlit as st
from gpt_index import GPTTreeIndex
import openai
import os
import streamlit.components.v1 as components

st.secrets.load_if_toml_exists()
openai.api_key = st.secrets["openai_api_key"]
openai.organization = st.secrets["openai_organization"]
assert openai.api_key is not None, "OpenAI API key not found"
os.environ["OPENAI_API_KEY"] = openai.api_key
os.environ["OPENAI_ORGANIZATION"] = openai.organization
st.title("Paul Graham's clone")

index_path = "index.json"
# check if index exists, if not, download from public repo
if not os.path.exists(index_path):
    import requests
    url = "https://raw.githubusercontent.com/jerryjliu/gpt_index/main/examples/paul_graham_essay/index.json"
    r = requests.get(url, allow_redirects=True)
    open(index_path, "wb").write(r.content)
index = GPTTreeIndex.load_from_disk(index_path)

# input box
user_input = st.text_input("You", "How can I build the most valuable product for humanity?")
# button
if st.button("Send"):
    # display user input
    st.write("You: " + user_input)
    # display clone response
    response = index.query(user_input)
    print("yo", dir(response))
    print(response)
    st.write("Paul: " + str(response))

components.html(
    """
<script>
const doc = window.parent.document;
buttons = Array.from(doc.querySelectorAll('button[kind=primary]'));
const send = buttons.find(el => el.innerText === 'Send');
doc.addEventListener('keydown', function(e) {
    switch (e.keyCode) {
        case 13:
            send.click();
            break;
    }
});
</script>
""",
    height=0,
    width=0,
)

# add a reference to the source code at https://github.com/louis030195/paul-graham-clone
st.markdown(
    """
    [Source code](https://github.com/louis030195/paul-graham-clone)
    """
)

# reference to gpt-index
st.markdown(
    """
    Built with ❤️ by [louis030195](https://louis030195.com) using the amazing [GPT-Index](https://https://github.com/jerryjliu/gpt_index) library
    """
)
