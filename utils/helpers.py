def format_docs(docs):
    """Formats a list of document objects into a single string.

    Args:
        docs (list): A list of document objects, each having a 'page_content' attribute.

    Returns:
        str: A single string containing the page content from each document, 
        separated by double newlines."""
    return "\n\n".join(doc.page_content for doc in docs)