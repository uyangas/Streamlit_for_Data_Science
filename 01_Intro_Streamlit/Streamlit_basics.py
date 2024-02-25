import streamlit as st

st.title("Building Data Science App with Streamlit")
st.subheader("App by Uyanga Sumiya")
st.write("This app is sample app to show how Streamlit works")

st.sidebar.subheader("Please input the values")

name = st.sidebar.text_input("What is your name?")
age = st.sidebar.number_input(label="What is your age?",
                      min_value=0,
                      max_value=100)

if (len(name)>0) & (age>0):
    st.markdown(f'<span style="color: green;"> WELCOME TO MLUB {name.upper()}!</span>', unsafe_allow_html=True)
    video_file = open('../utils/Logo reveal.mp4', 'rb')
    video_bytes = video_file.read()
    st.video(video_bytes, start_time=0)
    
    st.markdown(f"### Your data journey is {age}% complete!")
    progress_bar = st.progress(0)

    # Update the progress bar incrementally
    for percent_complete in range(age):
        progress_bar.progress(percent_complete + 1)

    st.markdown("## YOU CAN DO IT!")
    