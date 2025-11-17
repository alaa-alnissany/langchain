from typing import Iterator
import threading
from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader, FileSystemBlobLoader
from langchain_community.document_loaders.parsers import TesseractBlobParser, PyPDFParser
from langchain_community.document_loaders.base import BaseBlobParser
from langchain_community.document_loaders.generic import GenericLoader
from langchain_text_splitters.markdown import ExperimentalMarkdownSyntaxTextSplitter
from langchain_text_splitters.html import HTMLSemanticPreservingSplitter
from langchain_writer.pdf_parser import PDFParser
from langchain_community.document_loaders.blob_loaders import Blob

# from langchain_text_splitters.base import 
#------------------- Documents Structure---------------
# documents = [
#     Document(
#         page_content="Dogs are great companions, known for their loyalty and friendliness.",
#         metadata={"source": "mammal-pets-doc"},
#     )
# ]

class PyPDFmdParser(BaseBlobParser):
    _lock = threading.Lock()
    def __init__(self, mode, pages_delimiter, images_parser, images_inner_format, extraction_mode, extract_images: bool = False, format_is_markdown: bool = False):
        super().__init__(mode= mode,
                        pages_delimiter= pages_delimiter,
                        images_parser= images_parser,
                        images_inner_format= images_inner_format,
                        extraction_mode= extraction_mode,
                        )
        self.format_is_markdown = format_is_markdown
    
    def lazy_parse(self, blob: Blob) -> Iterator[Document]:
        try:
            import pymupdf
            import pymupdf4llm
        except ImportError: # 
            raise ImportError("pymupdf4llm package not found, please install it "
                "with `pip install pymupdf4llm`")
        with PyPDFmdParser._lock:
            with blob.as_bytes_io() as file_path:
                if blob.data is None:
                    doc = pymupdf.open(file_path)
                else:
                    doc = pymupdf.open(stream=file_path, filetype="pdf")
                full_content_md = []
            

        return super().lazy_parse(blob)

def pdfsloader(path: str) -> list[Document]:
    
    loader= GenericLoader(blob_loader= FileSystemBlobLoader(
                            path= path,
                            glob= "*.pdf"
                                ),
                          blob_parser= PyPDFParser(mode= "single",
                                                pages_delimiter= "\n-----END-----\n",
                                                images_parser= TesseractBlobParser(),
                                                images_inner_format= "markdown-img",
                                                extraction_mode= "layout",
                                                ),
                        )
    
    loader= GenericLoader(blob_loader= FileSystemBlobLoader(
                            path= path,
                            glob= "*.pdf"
                                ),
                          blob_parser= PDFParser(
                            format="markdown",
                            ),
                        )    
    return loader.load()

html_splitter = HTMLSemanticPreservingSplitter(
                                    headers_to_split_on=[("h1", "Header 1"), ("h2", "Header 2")],
                                    max_chunk_size= 1000,
                                    chunk_overlap= 100,
                                    preserve_images=True,
                                    preserve_audio=True,
                                    preserve_links= True,
                                    preserve_parent_metadata=True,
                                    preserve_videos=True,
                                    stopword_removal=True,
                                    stopword_lang="english",
                                    normalize_text=True)  
 

docs = pdfsloader("./static/pdfs/")
print(docs[0].page_content)
print("--------------------------------")
print(docs[1].page_content)
print("--------------------------------")