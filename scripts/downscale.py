import logging
import os
from PIL import Image

# Configure standard Python logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def downscale_png_for_web(input_path: str, output_path: str, target_width: int) -> None:
    """
    Downscales a PNG image maintaining its aspect ratio and optimizes it for web.
    """
    if not os.path.exists(input_path):
        logger.error(f"Input file not found: {input_path}")
        return

    try:
        logger.info(f"Opening image: {input_path}")
        with Image.open(input_path) as img:
            
            # 1. Calculate dimensions
            original_width, original_height = img.size
            aspect_ratio = original_height / original_width
            target_height = int(target_width * aspect_ratio)

            logger.info(f"Original size: {original_width}x{original_height}")
            logger.info(f"Target size: {target_width}x{target_height}")

            # 2. Resize the image
            resized_img = img.resize((target_width, target_height), Image.Resampling.LANCZOS)

            # 3. Save and optimize
            logger.info(f"Saving optimized image to: {output_path}")
            resized_img.save(output_path, format="PNG", optimize=True)
            logger.info("Image downscaling complete.")

    except Exception as e:
        logger.error(f"Failed to process image: {e}")

if __name__ == "__main__":
    input_file = "frontcover.png"
    output_file = "cover.png"
    desired_width = 800
    
    downscale_png_for_web(input_file, output_file, desired_width)
