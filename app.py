import streamlit as st
from api_call import note_generator
from PIL import Image
from api_call import audio_transcription
from api_call import quiz_generator


st.title("Note Summary and Quiz Generator")

st.markdown("Upload upto 3 images to generate a summary and quiz questions based on the content of the images.")
st.divider()

with st.sidebar:
    st.subheader("Upload Images")
    uploaded_files = st.file_uploader("Upload Image", 
                                      type=["png", "jpg", "jpeg"],
                                      accept_multiple_files=True)
    pil_images = [Image.open(file) for file in uploaded_files]
    if uploaded_files:
        if len(uploaded_files) > 3:
            st.error("Please upload a maximum of 3 images.")
        else:
            col=st.columns(len(uploaded_files))
            for i,image in enumerate(uploaded_files):
                with col[i]:
                    st.image(image)

    selected_option=st.selectbox("Select the difficulty level",
                                ("Easy", "Medium", "Hard"),
                                index=None)
    pressed=st.button("Generate Summary and Quiz", key="generate_button",type="primary")


if pressed :
    if not uploaded_files:
        st.error("Please upload at least one image.")
    if not selected_option:
        st.error("Please select a difficulty level.")
    if uploaded_files and selected_option:

        #Summary
        with st.container(border=True):
            st.subheader("Summary")
            with st.spinner("Generating summary..."):
                generated_notes=note_generator(pil_images)
                st.markdown(generated_notes)

        #Audio
        with st.container(border=True):
            st.subheader("Audio")
            with st.spinner("Generating Audio..."):
                #Claering Markdown formatting for audio transcription
                clean_text=generated_notes.replace("#","").replace("*","").replace("_","")
                audio_transcript=audio_transcription(clean_text)
                st.audio(audio_transcript, format="audio/mp3")

        #quiz
        with st.container(border=True):
            with st.spinner("Generating Quiz Questions..."):
                st.subheader(f"Quiz Questions({selected_option}) level")
                quiz_questions=quiz_generator(pil_images, selected_option)
                st.markdown(quiz_questions)