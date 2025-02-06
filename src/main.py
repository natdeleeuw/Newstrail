import openai
import os
import json
from dotenv import load_dotenv
import datetime

def get_timestamp():
    """Returns the current timestamp as a string in the format YYYYMMDD_HHMMSS."""
    return datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

def load_environment_variables():
    """Validates and loads required environment variables."""
    # Load environment variables from .env file
    load_dotenv()

    # Check if the OpenAI API key is set
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        raise ValueError("Error: OPENAI_API_KEY is not set in the environment variables or .env file.")
    
    # Set the OpenAI API key for the OpenAI library
    openai.api_key = openai_api_key

    # Set the path to the articles folder within the `data` directory
    articles_folder_path = "./data/articles"
    if not os.path.exists(articles_folder_path):
        raise FileNotFoundError(f"Error: ARTICLES_PATH folder '{articles_folder_path}' does not exist.")

    return articles_folder_path


def save_intermediate_output(content, filename_prefix):
    """
    Saves intermediate output to a file with a timestamp for uniqueness.
    """
    timestamp = get_timestamp()
    filename = f"{filename_prefix}_{timestamp}.txt"  # Add timestamp to filename
    file_path = os.path.join("data", filename)
    try:
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(content)
        print(f"Intermediate output saved to {file_path}")
    except Exception as e:
        print(f"Error saving intermediate output to {file_path}: {e}")



def read_articles_from_folder(folder_path):
    """Reads articles from .txt files in a folder, along with the journal name (filename)."""
    articles = []
    
    # Check if folder exists
    if not os.path.exists(folder_path):
        print(f"Folder {folder_path} not found.")
        return []
    
    # Iterate through each .txt file in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith('.txt'):
            file_path = os.path.join(folder_path, filename)
            try:    
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    journal_name = os.path.splitext(filename)[0]  # Remove the .txt extension
                    articles.append({
                        'journal': journal_name,
                        'content': content
                    })
            except Exception as e:
                print(f"Error reading file {file_path}: {e}")
    
    return articles, len(articles)

def create_articles_string(articles):
   
    journals = ""
    # Iterate through the articles and include the journal name in the prompt
    for article_data in articles:
        journal_name = article_data['journal']
        content = article_data['content']
        journals += f"(Journal: {journal_name}):\n{content}\n\n"
    
    
    return journals

def create_common_differ(articles, article_count):
    """Creates a prompt for the LLM model based on the input articles, including the journal source."""
    
    
    prompt = f"""You will be provided with {article_count} articles on the same subject.
Your task is to create two bullet-point lists based on the content of these articles:
Common Content: A list of points that are consistently mentioned in all {article_count} articles.
Unique Content: A list of points that are only mentioned in some of the articles.
Make sure the lists are concise and focus on the key ideas."""
    
    
    
    return [
        {"role": "system", "content": prompt},
        {"role": "user", "content": articles}
    ]


def create_newstrail_article(articles, common_differ, article_count):
    """Creates a prompt for the LLM model based on the input articles, including the journal source."""
    
    
    prompt = f"""Use the following step-by-step instructions to create a neutral article of 2000-2300 words based on {article_count} articles provided by the user. The article should highlight commonalities shared across these articles as well as present differing narratives in a balanced manner. The goal is to inform readers without persuading or advocating for a particular viewpoint.
    

    # Steps

**Read and Analyze**: Carefully read all {article_count} articles to identify both common themes and differing narratives.
  
**Identify Commonalities**: Extract the key themes, facts, or data that are consistently mentioned across the majority of the articles.

**Identify Differing Narratives**: Note any differing opinions, perspectives, or interpretations present in the articles.

**Outline the Article**: Create an article structure that includes an introduction, sections for common themes, sections for different narratives, and a concluding summary.
   
**Draft the Article**: Write the article, ensuring neutrality in presenting information without advocating for any particular perspective. Use neutral language and focus on clarity and balance.

**Review and Revise**: Edit the draft for coherence, tone, neutrality, and to ensure it meets the word count requirement.

# Output Format

A single continuous article of 2000-2300 words, structured with headings and subheadings as necessary, presenting both common themes and differing narratives from the source articles in a balanced and neutral manner.

# Notes

- Ensure that the article maintains a neutral tone and does not persuade or influence the reader towards any particular viewpoint.
- Be mindful of the coherence and flow, linking the common themes and differing perspectives seamlessly.
- It is critical that each part of the article directly relates to the content of the provided articles without introducing external arguments or data.

Here a first analysis of the articles, what is common and on what they differ, in the final article focus in the beginning of the articles on the common points, and at the end of article on the point they differ and state clearly that they differ and how : 
{common_differ}

The User will provide you the {article_count} articles """
    
    
    
    return [
        {"role": "system", "content": prompt},
        {"role": "user", "content": articles}
    ]

  

def call_LLM_api(prompt):
    """Calls the OpenAI API with the prompt."""
    try:
        
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=prompt,
            temperature=1,
        )
          
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error calling OpenAI API: {e}")
        return ""

def save_newstrail_article(content):
    """Saves the merged article to a file with a timestamp for uniqueness."""
    timestamp = get_timestamp()
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)  # Ensure the directory exists
    filename = os.path.join(output_dir, f"newstrail_article_{timestamp}.txt")  # Add timestamp to filename
    try:
        with open(filename, "w", encoding="utf-8") as file:
            file.write(content)
        print(f"Merged article saved to {filename}")
    except Exception as e:
        print(f"Error saving merged article to {filename}: {e}")

        
def main():
    """Main function to handle the merging process."""
    try:
        # Step 1: Set up variables and parameters
        # Load and validate environment variables (e.g., API key, folder path).
        # Read articles from the specified folder and format them into a single string for further processing.
        articles_folder_path = load_environment_variables()
        articles, article_count = read_articles_from_folder(articles_folder_path)
        
        if not articles:
            # Exit if no articles are found in the folder
            print("No articles were found in the specified folder.")
            return

        # Format articles into a single string suitable for LLM processing
        articles = create_articles_string(articles)
    except Exception as e:
        # Print an error message and exit if any setup step fails
        print(e)
        return

    # Step 2: Generate "common and differ" analysis
    # Prepares the LLM prompt and calls the API to extract commonalities and differences from the articles.
    common_differ = create_common_differ(articles, article_count)
    common_differ = call_LLM_api(common_differ)

    # Step 3: Save intermediate output for transparency and debugging
    # Saves the common and differing points into a separate file for review.
    save_intermediate_output(common_differ, "common_differ")

    # Step 4: Generate the NewsTrail article
    # Combines the article data and the common/differ analysis to construct a detailed instruction for the LLM.
    prompt = create_newstrail_article(articles, common_differ, article_count)
    newstrail_article = call_LLM_api(prompt)

    # Step 5: Output and save the generated article
    # If successful, save the final article to a file and notify the user.
    print(f"This is the article : {newstrail_article}")
    if newstrail_article:
        save_newstrail_article(newstrail_article)
    else:
        # Notify the user if the article generation failed
        print("Failed to generate the merged article.")

if __name__ == "__main__":
    main()
