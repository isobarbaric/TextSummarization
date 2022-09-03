
import gradio as gr

from text_summarizer import TextSummarizer
from utility import Reader

a = TextSummarizer()
b = Reader()

def handle_input(text, num_sent):
    summarized_text = a.summarize(text, int(num_sent))
    b.save(summarized_text)
    return summarized_text

interface = gr.Interface(
    title = 'Text Summarizer',
    fn = handle_input,
    inputs = [
        gr.Textbox(lines = 10, placeholder = 'Paste your content here!', label = 'Textual Content'),
        gr.Slider(minimum = 3, maximum = 25, label = '# of Sentences in the Summary')
    ],
    outputs = [
        gr.Textbox(lines = 10, label = 'Summarized Text')
        # gr.Audio(source = "static/text-spoken.mp3", label = 'Narration via Google Text-to-Speech')
    ]
)

interface.launch()