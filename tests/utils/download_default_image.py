import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))



def download_default_image(output_path="./default_image.png"):
    """
    Downloads the default image for a Domo user and saves it to the specified path.

    Args:
        output_path (str): The file path where the image will be saved. Defaults to './default_image.png'.
    """
    import src.client.auth as dmda
    from src.classes.DomoUser import domo_default_img

    auth = dmda.DomoTokenAuth(
        domo_access_token=os.environ["DOMO_ACCESS_TOKEN"],
        domo_instance=os.environ["DOMO_INSTANCE"],
    )
    print(auth.who_am_i())

    # Ensure the directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Save the default image
    domo_default_img.save(output_path)
    print(f"Default image saved to {output_path}")


if __name__ == "__main__":
    download_default_image()
