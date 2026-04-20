import os
from PIL import Image
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def pdf_pie_all():
    # Define the folder where the pie chart images are stored
    folder_path = f"_0_out/_0_pie_charts"
    
    # List all PNG files in the folder
    image_files = [f for f in os.listdir(folder_path) if f.endswith('.png')]
    
    # Sort files to maintain order in the PDF
    image_files.sort()
    
    # Path for the resulting PDF
    pdf_path = '_0_out/_0_pie_charts/pdf/Pie_Charts_Compilation.pdf'
    
    # Create a PDF document with each image on a separate page
    c = canvas.Canvas(pdf_path, pagesize=letter)
    width, height = letter  # Width and height of the pages
    
    # Loop through image files and add each to a separate page
    for image_file in image_files:
        image_path = os.path.join(folder_path, image_file)
        img = Image.open(image_path)
        
        # Ensure the image is rendered as a square to maintain the pie chart's circle shape
        if img.width != img.height:
            max_side = max(img.width, img.height)
            square_img = Image.new("RGB", (max_side, max_side), (255, 255, 255))
            square_img.paste(img, ((max_side - img.width) // 2, (max_side - img.height) // 2))
            img = square_img
        
        # Fit image to page keeping aspect ratio
        aspect_ratio = img.width / img.height
        if aspect_ratio > 1:
            img_width = width
            img_height = img_width / aspect_ratio
        else:
            img_height = height
            img_width = img_height * aspect_ratio
        
        # Center the image
        x = (width - img_width) / 2 - 0.6 * 72 
        y = (height - img_height) / 2
    
        # Save image to canvas
        c.drawInlineImage(img, x, y, img_width, img_height)
        c.showPage()
    
    c.save()
    
    print(f"Compiled PDF saved as '{pdf_path}'. Open it to view the charts.")