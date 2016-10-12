
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
# from imageresize import imageresize


def resize_image(image, width):
    # Open image
    image_obj = Image.open(image)
    w, h = image_obj.size
    # If it hasn't been resized
    if w != width:
        # Proportional resize
        # Determine what percentage desired width is of original width
        wpercent = (width/float(image_obj.size[0]))
        # Multiply original height by that percentage to figure out proportional height
        hsize = int((float(image_obj.size[1])*float(wpercent)))
        # Resize image
        image_resized = image_obj.resize((width, hsize), Image.ANTIALIAS)

        # BytesIO magic to save it properly
        image_io  = BytesIO()
        image_resized.save(image_io, format='JPEG', quality=90)
        
        temp_name = image.name
        image.delete(save=False)  
        
        image.save(
            temp_name,
            content=ContentFile(image_io.getvalue()),
            save=False
        )

    
