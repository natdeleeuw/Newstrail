# Newstrail
A model for generating articles based on multiple input articles about the same news. 

---

## Project Overview
The model processes a set of articles on a specific topic, identifies common themes and differing perspectives, and generates a impartial, well-structured article that highlights these findings.
It is a continious project, with as aim to use LLM's at it's fullest potential to create impartial news. With this project, we are not stating that LLM's (and technology in general) are neutral, we are simply experiencing how much they can help us
If you have any idea for improvements, please feel free to push suggestions (see end of readme) or to send us an email (contact@newstrail.info)

## Project next steps
- GPT 4o mini is used for the moment, the main raison is the length of the context window and the ease of use in the testing phase. Researched at Newstrail is done to see what other model (possibly open-source) we are going to use, with as main criterea context window, quality of summarises, neutrality. If you know some reseach about those criterea, feel free to send an email ;) contact@newstrail.info
- Combination of different LLM's models to reduce specific biases of models
- After processing check on the use of words on their neutrality and impartiality 
- Extend length of the articles 

## Requirements to run the model locally 

 The project requires a properly structured directory setup (see next paragraph) for smooth execution.
 following libraries/API/frameworks are needed : 
 1. **Python**: Ensure you have Python 3.8 or later installed. You can download it from [python.org](https://www.python.org/).
 2. **OpenAI API Key**: If you have no OpenAI API key, we can temporary provide you one for testing purposes.

---

## Project Directory Structure

Ensure the following directory structure is present for the project to run correctly:

```
project-root/
├── src/
│   ├── main.py           # Main script to run the process
├── tests/                # Unit tests for the project
├── data/
│   ├── articles/         # Folder to store input articles (required for the script to run)
│   └── .gitkeep          # Placeholder to keep the folder in the repository
├── output/               # Folder to store generated output articles
├── .env                  # Environment variables (e.g., API key)
├── .gitignore            # Files to exclude from version control
├── README.md             # Project overview and setup instructions
├── requirements.txt      # Python dependencies
└── LICENSE               # License for the repository
```
---


---

## Setup Instructions

### 1. Clone the Repository
Clone the repository to your local machine:
```bash
git clone https://github.com/natdeleeuw/newstrail.git
cd newstrail
```
### 2. Install Dependencies
Install the required Python packages using `pip`:
```
pip install -r requirements.txt
```


### 3. Create a `.env` File
Create a `.env` file in the root of the project to store environment variables. The `.env` file should include your OpenAI API key and any other configurations:
```
OPENAI_API_KEY=your_openai_api_key
```

### 4. Prepare the `data/articles` Folder
Ensure the `data/articles` folder exists and contains `.txt` files. Each file should represent an article on the same topic. Example:
```
data/articles/ 
├── article1.txt 
├── article2.txt 
├── article3.txt
```

If the folder does not exist, create it:
```
mkdir -p data/articles
```

---

## Running the Project

Run the main script to generate an article:
```
python src/main.py
```

The script will:
1. Read all `.txt` files in the `data/articles` folder.
2. Analyze the content for common themes and differing narratives.
3. Generate a neutral article based on the analysis.
4. Save the final article to the `output/` folder.

---

## Output
The generated article will be saved with a timestamped filename in the `output/` directory. Example:

```
output/ 
├── newstrail_article_20241123_123456.txt
```

## Testing
Unit tests are located in the `tests/` directory. To run the tests, use:
```
pytest tests/
```

---

## Troubleshooting

1. **Missing API Key**:
   Ensure the `.env` file exists and contains a valid `OPENAI_API_KEY`.

2. **No Articles Found**:
   Ensure the `data/articles/` folder exists and contains `.txt` files. If it's empty, add articles before running the script.

3. **Dependencies Not Installed**:
   If you encounter missing module errors, ensure you've installed all dependencies:

4. **Python Version Issues**:
Check your Python version:
Ensure it is Python 3.8 or later.

---

## Contribution Guidelines

1. Fork the repository and create a feature branch.
2. Create a branch with as format "[name-of-change]". Commit changes with clear, descriptive messages. (see : https://www.conventionalcommits.org/en/v1.0.0/)
3. Submit a pull request for review.

---

## License
This project is licensed under the GNU GENERAL PUBLIC license. See the `LICENSE` file for details.
