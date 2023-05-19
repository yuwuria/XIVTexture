import streamlit as st
from PIL import Image
import os
import base64

overlayed_img = None


def overlay_images(user_image, existing_image):
    global overlayed_img  # Declare overlayed_img as a global variable

    # Open user image
    user_img = Image.open(user_image).convert("RGBA")

    # Open existing image
    existing_img = Image.open(existing_image).convert("RGBA")

    # Calculate the aspect ratios of both images
    user_aspect_ratio = user_img.width / user_img.height
    existing_aspect_ratio = existing_img.width / existing_img.height

    if user_aspect_ratio == existing_aspect_ratio:
        # If the aspect ratios are the same, downsize the larger image to match the size of the smaller image
        if user_img.width > existing_img.width:
            resized_user_img = user_img.resize((existing_img.width, existing_img.height))
            resized_existing_img = existing_img
        else:
            resized_user_img = user_img
            resized_existing_img = existing_img.resize((user_img.width, user_img.height))
    else:
        # If the aspect ratios are different, resize both images to have the same width or height, depending on the aspect ratio
        if user_aspect_ratio > existing_aspect_ratio:
            resized_user_img = user_img.resize((existing_img.width, int(existing_img.width / user_aspect_ratio)))
            resized_existing_img = existing_img
        else:
            resized_user_img = user_img
            resized_existing_img = existing_img.resize((int(user_img.height * existing_aspect_ratio), user_img.height))

    # Create a new image with the same size as the user image
    overlay_img = Image.new('RGBA', resized_user_img.size)

    # Calculate the position to overlay the existing image
    position = ((resized_user_img.width - resized_existing_img.width) // 2,
                (resized_user_img.height - resized_existing_img.height) // 2)

    # Overlay the existing image onto the new image
    overlay_img.paste(resized_existing_img, position, resized_existing_img)

    # Composite the images with alpha blending
    overlayed_img = Image.alpha_composite(resized_user_img, overlay_img)

    # Save the overlayed image as PNG
    overlayed_img.save('overlay.png')


def main():
    st.title("Image Overlay App")

    # Upload user image
    st.header("Upload your PNG image:")
    user_image = st.file_uploader("Choose a PNG file", type=["png"])

    # Check if the user has uploaded an image
    if user_image is not None:
        # Save the user image to a temporary location
        user_img_path = "user_img.png"
        with open(user_img_path, "wb") as file:
            file.write(user_image.getvalue())

        # Display the user image
        st.image(user_img_path, caption="Uploaded Image", use_column_width=True)

        # Load existing image from the "images" folder
        existing_image_path = "faceAura/f1whitehorn.png"
        existing_image = Image.open(existing_image_path)

        # Display the existing image
        st.image(existing_image, caption="Overlay", use_column_width=True)

        # Process images and overlay
        overlay_images(user_img_path, existing_image_path)

        # Check if overlayed_img is not None
        if overlayed_img is not None:
            # Display the overlayed image
            st.image(overlayed_img, caption="Overlayed Image", use_column_width=True)

            # Get the base64 representation of the overlayed image
            overlayed_img_base64 = base64.b64encode(open("overlay.png", "rb").read()).decode("utf-8")

            # Provide a download link to the overlayed image
            st.markdown("### Download Overlayed Image")
            href = f'<a href="data:image/png;base64,{overlayed_img_base64}" download="overlay.png">Click here to download the overlayed image</a>'
            st.markdown(href, unsafe_allow_html=True)

        # Remove temporary image file
        os.remove(user_img_path)
        os.remove("overlay.png")


if __name__ == "__main__":
    main()
