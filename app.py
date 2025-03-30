import streamlit as st
from PIL import Image
import google.generativeai as genai
import os

# Set page config first (must be called before any other Streamlit command)
st.set_page_config(page_title="Image To Story", page_icon="✨")

# Secure API key handling
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
else:
    # Fallback to environment variable
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        # As a last resort, ask user (not recommended for production)
        api_key = st.sidebar.text_input("Enter Gemini API Key:", type="password")
        if not api_key:
            st.warning("Please provide a Gemini API key to continue.")
            st.info("For security, it's recommended to use Streamlit secrets or environment variables instead.")
            st.stop()

# Configure the Gemini API with the secure key
genai.configure(api_key=api_key)

# Function to get response from Gemini
def get_gemini_response(input, image):
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        if input != "":
            response = model.generate_content([
                input,
                image, 
                "The story should have a beautiful title related to the context of the story", 
                "A beautiful, insightful moral lesson should be mentioned at the end of the story"
            ])
        else:
            response = model.generate_content(image)

        return response.text
    except Exception as e:
        st.error(f"Error generating story: {str(e)}")
        return None

# Function to upload picture
def upload_picture():
    uploaded_file = st.file_uploader("Upload Picture", type=["jpg", "png", "jpeg"])
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption='Uploaded Picture', use_column_width=True)
        return image
    return None

# Function to display the sample picture options
def use_sample_picture():
    sample_option = st.selectbox('Select a sample picture:', ['Dog', 'Jungle'])
    sample_images = {
        'Dog': 'dog.jpeg',
        'Jungle': 'jungle.png'
    }
    if sample_option in sample_images:
        try:
            image = Image.open(sample_images[sample_option])
            st.image(image, caption=sample_option, use_column_width=True)
            return image
        except FileNotFoundError:
            st.error(f"Sample image file {sample_images[sample_option]} not found. Please make sure the file exists in the current directory.")
            return None
    return None

# Custom CSS styling
st.markdown("""
    <style>
        .header {
            font-size: 56px;
            color: #1E90FF;
            text-align: center;
            margin-bottom: 30px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        }
        .response {
            font-size: 36px;
            color: green;
            text-align: left;
            margin-bottom: 20px;
        }
        .output {
            font-size: 18px;
            color: #333333;
            line-height: 1.5;
            padding: 10px;
            border-radius: 5px;
            background-color: #f0f0f0;
            margin-top: 20px;
        }
        .creator {
            color: #888888;
            font-size: 14px;
            text-align: right;
            margin-top: 5px;
        }
    </style>
""", unsafe_allow_html=True)

# App header and creator info
st.markdown('<h1 class="header">Image To Story</h1>', unsafe_allow_html=True)
st.markdown("<p class='creator'>➡️created by 'Purushotham'</p>", unsafe_allow_html=True)

# App description
with st.expander("About the app..."):
    st.info("This is an AI-powered story generator app which will convert your images to interesting stories by assuming some characters and building a story around them. You will just upload the image and select what type of story you want.")

# Story genre selection
story_genre = st.radio("Select the story genre", horizontal=True, options=[
    "Adventure",
    "Romance",
    "Mystery",
    "Science Fiction",
    "Fantasy",
    "Thriller",
    "Historical Fiction",
    "Horror",
    "Drama",
    "Comedy",
    "Motivational"
])

# Create instructions based on genre
if story_genre:
    instructions = f"Craft an engaging {story_genre} story inspired by the provided image. The story should stick to the {story_genre} genre. Your story should seamlessly integrate with the visual elements, bringing them to life through vivid descriptions and imaginative storytelling. Aim for a minimum of 100 words to ensure depth and richness in your story. You should only use Islamic named characters in your story"

# Image source selection
choice = st.radio("Choose an option:", ("Upload Picture", "Use Sample Picture"))
image = None
if choice == "Upload Picture":
    image = upload_picture()
elif choice == "Use Sample Picture":
    image = use_sample_picture()

# Generate story button
submit = st.button("Generate Story..")
if submit and story_genre and image:
    with st.spinner("Writing Story..."):
        response = get_gemini_response(instructions, image)
        if response:
            st.markdown('<h2 class="response">Here is your Story...</h2>', unsafe_allow_html=True)
            st.markdown(f'<div class="output">{response}</div>', unsafe_allow_html=True)