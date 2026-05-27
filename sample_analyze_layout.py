# coding: utf-8

# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""
FILE: sample_analyze_layout.py

DESCRIPTION:
    This sample demonstrates how to extract text, tables, figures, selection marks and document structure (e.g., sections) information 
    from a document given through a file.

    ------Install the Document Intelligence library------
    pip install azure-ai-documentintelligence

    ------Run this Python sample------
    Run:
        python sample_analyze_layout.py
"""

import os
from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeDocumentRequest


def analyze_layout_from_file():

    document_intelligence_client = DocumentIntelligenceClient(
        # Set local endpoint or cluster endpoint and fake key
        endpoint="http://localhost:5000", 
        credential=AzureKeyCredential("fake-key")
    )

    # Analyze a sample document layout from a local file
    script_dir = os.path.dirname(os.path.abspath(__file__))
    pdf_path = os.path.join(script_dir, "sample-layout.pdf")
    bytes_data = None
    with open(pdf_path, "rb") as f:
        bytes_data = f.read()
    print(f"Read {len(bytes_data)} bytes from {pdf_path}")
    poller = document_intelligence_client.begin_analyze_document(
        "prebuilt-layout", AnalyzeDocumentRequest(bytes_source=bytes_data )
    )
    result = poller.result()

    # Analyze styles (e.g., whether the document contains handwritten content)
    if result.styles:
        for idx, style in enumerate(result.styles):
            print(
                "Document contains {} content".format(
                    "handwritten" if style.is_handwritten else "no handwritten"
                )
            )

    # Analyze pages
    for page in result.pages:
        print(f"----Analyzing layout from page #{page.page_number}----")

        # Analyze lines
        if page.lines:
            for line_idx, line in enumerate(page.lines):
                print(
                    f"...Line #{line_idx} has text content '{line.content}'"
                )

        # Analyze selection marks
        if page.selection_marks:
            for selection_mark in page.selection_marks:
                print(
                    f"...Selection mark is '{selection_mark.state}' "
                    f"and has a confidence of {selection_mark.confidence}"
                )

    # Analyze tables
    if result.tables:
        for table_idx, table in enumerate(result.tables):
            print(
                f"Table #{table_idx} has {table.row_count} rows and {table.column_count} columns"
            )
            for cell in table.cells:
                print(
                    f"...Cell[{cell.row_index}][{cell.column_index}] has content '{cell.content}'"
                )

    print("----------------------------------------")


if __name__ == "__main__":
    from azure.core.exceptions import HttpResponseError
    from dotenv import find_dotenv, load_dotenv

    try:
        load_dotenv(find_dotenv())
        analyze_layout_from_file()
    except HttpResponseError as error:
        # Examples of how to check an HttpResponseError
        if error.error is not None:
            if error.error.code == "InvalidImage":
                print(f"Received an invalid image error: {error.error}")
            elif error.error.code == "InvalidRequest":
                print(f"Received an invalid request error: {error.error}")
            raise
        if "Invalid request".casefold() in error.message.casefold():
            print(f"Uh-oh! Seems there was an invalid request: {error}")
        raise

# Next steps:
# Learn more about Layout model: https://aka.ms/di-layout
# Find more sample code: https://aka.ms/doc-intelligence-samples
