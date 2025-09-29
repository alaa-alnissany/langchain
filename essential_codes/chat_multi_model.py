import base64
from io import BytesIO
from langchain_ollama.llms import OllamaLLM
from IPython.display import HTML, display
from PIL import Image

def convert_to_base64(pil_image):
    buffered = BytesIO()
    pil_image.save(buffered, format="JPEG")
    image_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
    return image_str

def plt_img_base64(image_base64):
    image_html = f'<img src="data:image/jpeg;base64,{image_base64}" />'
    display(HTML(image_html))

file_path = "static/images/tower.jpg"
pil_image= Image.open(file_path)
image_b64 = convert_to_base64(pil_image)
plt_img_base64(image_b64)

llm = OllamaLLM(model="gemma3")

llm_with_image_context = llm.bind(images=[image_b64])
print(llm_with_image_context.invoke(input="What is the main colors of this image:"))