from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader, FileSystemBlobLoader
from langchain_community.document_loaders.parsers import TesseractBlobParser, PyPDFParser
from langchain_community.document_loaders.generic import GenericLoader

#------------------- Documents Structure---------------
# documents = [
#     Document(
#         page_content="Dogs are great companions, known for their loyalty and friendliness.",
#         metadata={"source": "mammal-pets-doc"},
#     )
# ]


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
    return loader.load()
   

docs = pdfsloader("./static/pdfs/")
print(docs[0].page_content)
