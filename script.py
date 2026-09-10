import csv
import os
import re
from PIL import Image, ImageDraw, ImageFont
# this file batch creates with a thank you template.png image with the guest list
# ==========================
# SETTINGS
# ==========================
# questions i need answered before process
'''
inputs:
what is csv file path?
what is the column called with the names?
Do you want to combine 2 columns? yes:1 or no:0
if so what is the second column called?
'''

TEMPLATE = "template.png"

# input need  depending on which CSV you are using
CSV_FILE = str(input("what is csv file path?"))
# CSV_FILE = "Couples.csv"
NAME_COLUMN = str(input("what is the column called with the names?"))
NEED_COLUMN2 = int(input("Do you want to combine 2 columns? yes:1 or no:0. "))
if NEED_COLUMN2 == 1:
    SECOND_COLUMN = str(input("if so, what is the second column called?"))

# Output folder
OUTPUT_DIR = "Output_file"

FONT_PATH = "/Library/Fonts/Times New Roman.ttf"

MAX_FONT_SIZE = 60
MIN_FONT_SIZE = 20

TEXT_COLOR = (244, 240, 225)

CENTER_Y = 120
MARGIN = 40

os.makedirs(OUTPUT_DIR, exist_ok=True)


# ==========================
# Find the biggest font that fits
# ==========================

def get_best_font(draw, text, image_width):

    max_width = image_width - (MARGIN * 2)

    for size in range(MAX_FONT_SIZE, MIN_FONT_SIZE - 1, -1):

        font = ImageFont.truetype(FONT_PATH, size)

        bbox = draw.textbbox(
            (0, 0),
            text,
            font=font
        )

        width = bbox[2] - bbox[0]

        if width <= max_width:
            return font

    return ImageFont.truetype(
        FONT_PATH,
        MIN_FONT_SIZE
    )


# ==========================
# Read CSV
# ==========================

with open(
    CSV_FILE,
    newline="",
    encoding="utf-8-sig"
) as f:

    reader = csv.DictReader(f)

    for row in reader:

        # ==========================
        
        # Has Prefix + Your name
        # ==========================

        if NEED_COLUMN2 == 1:

            prefix = str(
                row.get(SECOND_COLUMN, "") or ""
            ).strip()

            name_alone = str(
                row.get(NAME_COLUMN, "") or ""
            ).strip()

            name = f"{prefix} {name_alone}".strip()

        # ==========================
        # Couples
        # No Prefix/ no 2 columns needed
        # ==========================

        else:

            name = str(
                row.get(NAME_COLUMN, "") or ""
            ).strip()

        # ==========================
        # Skip empty names
        # ==========================

        if not name:
            continue

        # ==========================
        # Open template
        # ==========================

        img = Image.open(
            TEMPLATE
        ).convert("RGB")

        draw = ImageDraw.Draw(img)

        text = name

        # ==========================
        # Automatically resize font
        # ==========================

        font = get_best_font(
            draw,
            text,
            img.width
        )

        # ==========================
        # Calculate text size
        # ==========================

        bbox = draw.textbbox(
            (0, 0),
            text,
            font=font
        )

        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        # ==========================
        # Center horizontally
        # ==========================

        x = (img.width - text_width) / 2

        # ==========================
        # Draw text
        # ==========================

        draw.text(
            (x, CENTER_Y),
            text,
            fill=TEXT_COLOR,
            font=font
        )

        # ==========================
        # Create safe filename
        # ==========================

        filename = re.sub(
            r'[<>:"/\\|?*]',
            "",
            name
        ).strip()

        if not filename:
            filename = "unnamed"

        # ==========================
        # Save image
        # ==========================

        output_path = os.path.join(
            OUTPUT_DIR,
            filename + ".png"
        )

        img.save(output_path)

        print(f"Created: {output_path}")


print("Finished!")
