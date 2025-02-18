import gradio as gr
from anything import Anything

# Create a global instance of Anything (this acts as our cached resource)
anything_instance = Anything()

def search_database(search_query, search_type):
    """Call semantic search on the Anything instance."""
    semantic_results = anything_instance.semantic_search(search_type, search_query)
    # Assuming the result is returned as a dict with key "Semantic search results"
    return {"Semantic search results": semantic_results}  
 
def search(search_query, search_type):
    """
    Perform the search and format the output based on the type.
    
    For text searches:
      - Returns an HTML string with expandable details for each result.
      
    For image searches:
      - Returns a list of (image_path, caption) tuples for display in a gallery.
    """
    results = search_database(search_query, search_type.lower())
    
    if search_type.lower() == "text":
        html = "<h2>Text Search Results</h2>"
        for result_type, result in results.items():
            for file_path, content, dist in result:
                html += (
                    f'<details style="margin-bottom: 10px;">'
                    f'<summary style="cursor: pointer;">'
                    f'Path: {file_path} | Similarity: {dist:.2f}'
                    f'</summary>'
                    f'<p>{content}</p>'
                    f'</details>'
                )
        # Return the HTML output and an empty list for the gallery.
        return html, []
    
    elif search_type.lower() == "image":
        gallery_data = []
        for result_type, result in results.items():
            for file_path, content, dist in result:
                caption = f"Path: {file_path} | Similarity: {dist:.2f}"
                gallery_data.append((file_path, caption))
        # Return an empty HTML string and the gallery data.
        return "", gallery_data

# Build the Gradio UI using Blocks
with gr.Blocks() as demo:
    gr.Markdown("# Anything")
    
    # Inputs: Search query and search type selection.
    with gr.Row():
        search_query = gr.Textbox(label="Type to search")
        search_type = gr.Radio(
            choices=["Text", "Image"], label="Choose an option", value="Text"
        )
    
    search_button = gr.Button("Search")
    
    # Outputs: One HTML component for text results and one Gallery for images.
    text_output = gr.HTML()
    gallery_output = gr.Gallery(label="Search Results", columns=3)
    
    # Connect the button to the search function.
    search_button.click(fn=search, inputs=[search_query, search_type], outputs=[text_output, gallery_output])

demo.launch()
