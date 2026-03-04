from typing import Iterator, Any, Optional
import pymupdf
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
from langchain_opendataloader_pdf import OpenDataLoaderPDFLoader
from langchain_pymupdf4llm import PyMuPDF4LLMParser

# from langchain_text_splitters.base import 
#------------------- Documents Structure---------------
# documents = [
#     Document(
#         page_content="Dogs are great companions, known for their loyalty and friendliness.",
#         metadata={"source": "mammal-pets-doc"},
#     )
# ]

def pdfsloader(path: str, include_suffixes: list[str], exclude: list[str]) -> list[Document]:
    
    loader= GenericLoader(blob_loader= FileSystemBlobLoader(
                            path= path,
                            # glob= "*.pdf",
                            exclude=exclude,
                            suffixes= include_suffixes
                                ),
                            #blob_parser=PyMuPDF4LLMParser(),
                            blob_parser= PyPDFParser(mode= "single",
                                                pages_delimiter= "\n-----END-----\n",
                                                images_parser= TesseractBlobParser(),
                                                images_inner_format= "markdown-img",
                                                extraction_mode= "layout",
                                                ),
                        )
    '''
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
    '''    
    return loader.load()
'''
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
 '''

docs = pdfsloader("./static/pdfs/", include_suffixes=[".pdf"], exclude=["Motivation letter.pdf"])
print(docs[0].page_content)
print("--------------------------------")
print(docs[1].page_content)
print("--------------------------------")
