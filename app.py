import streamlit as st
import pandas as pd

# वेब ऐप का टाइटल और लेआउट सेट करना
st.set_page_config(page_title="Admission Register Search", layout="wide")

st.title("🏫 छात्र खोज प्रणाली (Student Search System)")
st.subheader("प्रवेश-पंजी (Admission Register 2026-28)")

# एक्सेल फ़ाइल लोड करने का फंक्शन
@st.cache_data
def load_data():
    try:
        df = pd.read_excel("Admission_Register_2026_28.xlsx")
        df.columns = df.columns.str.strip() # कॉलम के फालतू स्पेस हटाना
        if 'Roll No' in df.columns:
            df['Roll No'] = df['Roll No'].astype(str).str.strip().str.zfill(2)
        return df
    except FileNotFoundError:
        st.error("❌ 'Admission_Register_2026_28.xlsx' फ़ाइल नहीं मिली! कृपया इसे इसी फोल्डर में रखें।")
        return None

df = load_data()

if df is not None:
    # साइडबार में सर्च का विकल्प देना
    st.sidebar.header("🔍 खोज का विकल्प चुनें")
    search_by = st.sidebar.radio("किस आधार पर खोजना चाहते हैं?", ["रोल नंबर (Roll No)", "नाम (Student Name)", "जाति/श्रेणी (Category)"])
    
    result = pd.DataFrame()
    
    # 1. रोल नंबर द्वारा खोज
    if search_by == "रोल नंबर (Roll No)":
        roll_input = st.sidebar.text_input("रोल नंबर दर्ज करें (उदा: 01, 05):").strip().zfill(2)
        if roll_input and roll_input != "00":
            result = df[df['Roll No'] == roll_input]
            
    # 2. नाम द्वारा खोज
    elif search_by == "नाम (Student Name)":
        name_input = st.sidebar.text_input("छात्र का नाम दर्ज करें:")
        if name_input:
            result = df[df['Student Name'].str.contains(name_input, case=False, na=False)]
            
    # 3. श्रेणी द्वारा खोज
    elif search_by == "जाति/श्रेणी (Category)":
        cat_input = st.sidebar.text_input("श्रेणी दर्ज करें (उदा: EBC, General, BC, ST):").strip()
        if cat_input:
            result = df[df['Category'].str.contains(cat_input, case=False, na=False)]

    # परिणाम प्रदर्शित करना
    if not result.empty:
        st.success(f"✅ कुल {len(result)} छात्र मिले:")
        
        # टेबल के रूप में डेटा दिखाना
        st.dataframe(result, use_container_width=True)
        
        # कार्ड के रूप में एक-एक छात्र का पूरा विवरण दिखाना
        st.write("---")
        st.subheader("📋 विस्तृत विवरण (Detailed View)")
        for index, row in result.iterrows():
            with st.expander(f"👤 {row.get('Student Name', 'Unknown')} (रोल नंबर: {row.get('Roll No', 'N/A')})"):
                # डेटा को दो कॉलम में बांटकर सुंदर दिखाना
                col1, col2 = st.columns(2)
                
                # उपलब्ध डेटा के हिसाब से कॉलम में जानकारी भरना
                all_cols = list(df.columns)
                half = len(all_cols) // 2
                
                with col1:
                    for c in all_cols[:half]:
                        st.write(f"**{c}:** {row[c]}")
                with col2:
                    for c in all_cols[half:]:
                        st.write(f"**{c}:** {row[c]}")
    else:
        if (search_by == "रोल नंबर (Roll No)" and roll_input and roll_input != "00") or \
           (search_by == "नाम (Student Name)" and name_input) or \
           (search_by == "जाति/श्रेणी (Category)" and cat_input):
            st.warning("❌ कोई रिकॉर्ड नहीं मिला! कृपया स्पेलिंग या रोल नंबर जांचें।")
        else:
            st.info("💡 खोजने के लिए बाईं (Left) तरफ दिए गए बॉक्स में विवरण दर्ज करें।")
