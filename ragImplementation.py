from ingestion_chroma import chromaWrap

import streamlit as st
instance = chromaWrap("testing")

st.title("Search about cricketers!!!")
st.write("Search about your favorite cricketer!!")

if "show_upload" not in st.session_state:
    st.session_state.show_upload = False

if st.button("Upload docs about your favorite cricketer"):
    st.session_state.show_upload = True

if st.session_state.show_upload:
    uploaded_files = st.file_uploader(
        "Upload documents about your favorite cricketer",
        type=["pdf", "txt", "docx"],
        accept_multiple_files=True
    )

    if st.button("Submit Documents"):
        if uploaded_files:
            with st.spinner("Ingesting documents... this may take a moment"):
                count = instance.process_ingest_docs(uploaded_files)

            st.success(f"{len(uploaded_files)} document(s) ingested).")

            for file in uploaded_files:
                st.write(f"{file.name}")
        else:
            st.warning("Please upload at least one document.")

query = st.text_input(
    "Enter your question",
    placeholder="What is ABD famous for?"
)

if st.button("Search"):
    if query.strip():
        with st.spinner("Searching..."):
            result = instance.query(query, 2)

        st.write("### Search Results")
        st.write(result)
    else:
        st.warning("Please enter a question.")