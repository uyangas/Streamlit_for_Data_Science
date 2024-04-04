import streamlit as st

st.header("**WIDGET-Н ТӨРЛҮҮД БА ЖИШЭЭ**")

# Текст утга авах
st.subheader("**1. ТЕКСТ УТГА АВАХ**")
text_input = st.text_input("Таны овог, нэр",
                           max_chars=30, placeholder="Овог, нэр")
st.write(f"Үр дүн: {text_input}")

# тоон утга авах
st.subheader("**2. ТООН УТГА АВАХ**")
number_input = st.number_input("Таны нас",
                               min_value=0, max_value=100, placeholder="25")
st.write(f"Үр дүн: {number_input}")

# утга сонгох
st.subheader("**3. ЖАГСААЛТААС НЭГ УТГА СОНГОХ**")
options = ["Бага","Дунд","Бүрэн дунд","Баклавр","Магистр","Доктор"]
selext_box = st.selectbox("Таны боловсрол",
                          options)
st.write(f"Үр дүн: {selext_box}")

# олон утга сонгох
st.subheader("**4. ЖАГСААЛТААС ОЛОН УТГА СОНГОХ**")
options = ["Машин сургалт", "Дата анализ","Дата зураглал",
            "Дата Сайнс","Компьютерийн хараа","Хэл шинжлэл",
            "Өгөгдлийн сангийн аркитект","Үүлэн технологи"]
multi_select = st.multiselect("Таны сонирхдог чиглэл",
                              options)
st.write(f"Үр дүн: {multi_select}")

# утга сонгох box 
st.subheader("**5. УТГА СОНГОХ BOX**")
# check_box = st.checkbox("pandas")
options = ["pandas","numpy","scikit-learn","pytorch","tensorflow","plotly"]
checkbox_values = {}
st.write("Таны түгээмэл ашигладаг Python сан")
for option in options:
    checkbox_values[option] = st.checkbox(option)

st.write(f"Үр дүн: {checkbox_values}")

# утга сонгох дугуй
st.subheader("**6. УТГА СОНГОХ ДУГУЙ**")
options = ["Ажлын шаардлагаар",
           "Өөрийн сонирхлоор",
           "Мэдлэгээ нэмэгдүүлэх зорилгоор",
           "Ажлаас гадуурх төсөлд оролцох",
           "Бусад"]

radio = st.radio("Энэ чиглэлд яагаад сонирхох болсон бэ?",
                 options)
st.write(f"Үр дүн: {radio}")

# slider үүсгэх
st.subheader("**7. SLIDER ҮҮСГЭХ**")
slider1 = st.slider("Хиймэл оюуны салбар хичнээн жил ажиллаж байгаа вэ?",
                   min_value=0, max_value=50
                   )
st.write(f"Үр дүн: {slider1}")

slider2 = st.slider("Хиймэл оюуны салбар хичнээн жил ажиллаж байгаа вэ?",
                   value=[1,50]
                   )
st.write(f"Үр дүн: {slider2}")

# товч үүсгэх
st.subheader("**8. ТОВЧ ҮҮСГЭХ**")
button = st.button("Мэдээллийг илгээх")
st.write(f"Үр дүн: {button}")

# файл авах
st.subheader("**9. ФАЙЛ АВАХ**")
file = st.file_uploader("Өөрийн resume-г хавсаргах")
st.write(f"Үр дүн: {file}")