import os
import json
import re
from dotenv import load_dotenv, find_dotenv
from langchain_core.messages import SystemMessage
from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from langchain_openai import ChatOpenAI

load_dotenv(find_dotenv())

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = os.getenv("LANGCHAIN_PROJECT")


model = ChatOpenAI(model_name="gpt-4", temperature=0)

prompt_msgs = [
    SystemMessage(
        content="“You are a backend data processor that is part of our web sites programmatic workflow. The user prompt will provide data input and processing instructions. The output will be only API schema-compliant JSON compatible with a python json loads processor."
    ),
    HumanMessagePromptTemplate.from_template(
        """Use the given text to create all the different products by constructing and converting each unique product from the text and returning the results in a structured JSON format. 
        
        Please extract all the SKUs, Titles, Finishes, and Prices from the text with the following format and example values: {example_format}

        Guidelines: {hint}
        
        If you are unsure of a product, please skip the whole product and move on to the next one.  
        
        Do not include any explanation and don't return any code blocks.
        
        The extracted text consists of a lot of random characters, numbers, and lines that are not part of the products. Please clean the text from the jibberish and extract the products after.
        Text: 
        {text}"""
    ),
]


example_format = """
{
    products: [
        {
        "SKU": "5011.003.FD",
        "Title": "Knob w/ 5058 Rose Full Dummy",
        "Finish": "003",
        "Price": "$286"
        },
        {
        "SKU": "5011.003.IDM",
        "Title": "Knob w/ 5058 Rose Half Dummy",
        "Finish": "190",
        "Price": "$143"
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
hint = "All product SKUs are incomplete with 'xxx' and need to be completed using the finish code in the text. Please create a new product for each SKU with a unique finish code. Also, if you can't find the price, it is the same as the product above it."

index = 0
for filename in os.listdir(results_dir):
    if filename.endswith(".txt"):
        file_path = os.path.join(results_dir, filename)

        with open(file_path, "r") as file:
            text = file.read()

        output = chain.invoke({"text": text, "hint": hint})

        print(output)

        output_content = output.content

        output_content = re.sub(r"'''|\"\"\"|json", "", output_content)

        try:
            data = json.loads(output_content)
            products_data = data.get("products", [])
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON for file {filename}: {e}")
            products_data = []

        output_file_path = f"./outputs/output_{filename}"
        with open(output_file_path, "w") as output_file:
            output_file.write(json.dumps(products_data, indent=4))

        print(f"Processed {filename} and saved output to {output_file_path}")

print("All files processed.")
