import os
import json
from dotenv import load_dotenv, find_dotenv
from langchain_core.messages import SystemMessage
from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from langchain_openai import ChatOpenAI

# Load environment variables
load_dotenv(find_dotenv())

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = os.getenv("LANGCHAIN_PROJECT")


model = ChatOpenAI(model_name="gpt-4", temperature=0)

# Define the prompt with clearer instructions and example format
prompt_msgs = [
    SystemMessage(
        content="You are an intelligent assistant specialized in converting extracted text from PDFs into a structured JSON format for various products in the kitchen and bath industry."
    ),
    HumanMessagePromptTemplate.from_template(
        """Use the given text to create all the different products by constructing and converting each unique product from the text and returning the results in a structured JSON format. 
        
        Please extract all the SKUs, Titles, Finishes, and Prices from the text in the following format: {example_format}

        Guidelines: {hint}
        
        If you are unsure of a product, please skip the whole product and move on to the next one.  
        
        It is extremely important not to return any additional text besides the array of products. Texts like ``` or "json" should never be included. 
        
        Text: 
        {text}"""
    ),
]


example_format = """
{
    products: [
        {
            "SKU": Product SKU,",
            "Title": "Product Title",
            "Finish": "Finish Code",
            "Price": "Price"
        },
        {
            "SKU": "Product SKU",
            "Title": "Product Title",
            "Finish": "Finish Code",
            "Price": "Price"
        }
    ]
}
"""

prompt = ChatPromptTemplate(
    messages=prompt_msgs,
    input_variables=["text", "hint"],
    partial_variables={
        "example_format": example_format,
    },
)

chain = prompt | model

results_dir = "../extract_data/results/"
hint = "All product SKUs are incomplete with 'xxx' and need to be completed using the finish code. Please create a new product for each SKU with a unique finish code. Also, if you can't find the price, it is the same as the product above it."

for filename in os.listdir(results_dir):
    if filename.endswith(".txt"):
        file_path = os.path.join(results_dir, filename)

        with open(file_path, "r") as file:
            text = file.read()

        output = chain.invoke({"text": text, "hint": hint})

        output_filename = f"output_{filename}"
        output_file_path = os.path.join(results_dir, output_filename)
        with open(output_file_path, "w") as output_file:
            output_file.write(json.dumps(output, indent=4))

        print(f"Processed {filename} and saved output to {output_filename}")

print("All files processed.")
