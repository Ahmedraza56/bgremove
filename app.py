import streamlit as st
from rembg import remove
from PIL import Image
import io

def remove_bg(image_bytes):
    try:
        result_bytes = remove(image_bytes)
        return True, result_bytes
    except Exception as e:
        return False, str(e)

# Set up the Streamlit interface
st.title('Background Removal Tool')
st.write('Upload an image and the background will be removed.')

# File uploader allows user to add their own image
uploaded_file = st.file_uploader("Choose an image...", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    # Display the uploaded image
    st.image(uploaded_file, caption='Uploaded Image', use_column_width=True)
    
    # Remove the background of the image
    with st.spinner('Removing background...'):
        input_image = Image.open(uploaded_file)
        input_image_bytes = io.BytesIO()
        input_image.save(input_image_bytes, format=input_image.format)

        success, result_or_error = remove_bg(input_image_bytes.getvalue())

        if success:
            bytes_data = result_or_error
            result_image = Image.open(io.BytesIO(bytes_data))
            st.success('Here is your image with the background removed:')
            st.image(result_image, use_column_width=True)

            # Provide a button to download the result
            btn = st.download_button(
                 label="Download image",
                 data=bytes_data,
                 file_name="bg_removed.png",
                 mime="image/png"
             )
        else:
            st.error(f'An error occurred: {result_or_error}')