import gradio as gr
import matplotlib.pyplot as plt
from theme_classifier import ThemeClassifier

def get_themes(theme_list_str, subtitles_path, save_path):
    theme_list = theme_list_str.split(',')
    theme_classifier = ThemeClassifier(theme_list)

    output_df = theme_classifier.get_themes(subtitles_path, save_path)
    theme_list = [theme for theme in theme_list if theme.strip().lower() != 'dialogue']

    output_df = output_df[theme_list]
    output_df = output_df.sum().reset_index()
    output_df.columns = ['Theme', 'Score']
    
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.barh(output_df['Theme'], output_df['Score'], color='skyblue')
    ax.set_xlabel("Score")
    ax.set_title("Series Themes")
    ax.invert_yaxis()
    plt.tight_layout()
    return fig

def main():
    with gr.Blocks() as iface:
        with gr.Row():
            with gr.Column():
                gr.HTML("<h1>Theme Classification (Zero Shot Classifiers)</h1>")
                with gr.Row():
                    with gr.Column():
                        plot = gr.Plot(label="Theme Plot")
                    with gr.Column():
                        theme_list = gr.Textbox(label="Themes (comma-separated)", placeholder="e.g. love, battle, hope")
                        subtitles_path = gr.Textbox(label="Subtitles Path", placeholder="Path to folder or file")
                        save_path = gr.Textbox(label="Save Path", placeholder="Output CSV path")
                        get_themes_button = gr.Button("Get Themes")
                        get_themes_button.click(
                            get_themes,
                            inputs=[theme_list, subtitles_path, save_path],
                            outputs=[plot]
                        )
    iface.launch(share=True)

if __name__ == '__main__':
    main()
