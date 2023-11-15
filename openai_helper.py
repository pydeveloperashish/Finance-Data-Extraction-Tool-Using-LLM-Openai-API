import openai
import os
import json
import pandas as pd
from dotenv import load_dotenv,find_dotenv
load_dotenv(find_dotenv())

openai.api_key = os.environ.get("OPENAI_API_KEY")


def extract_financial_data(text):
    prompt = get_prompt_text() + text
    response = openai.ChatCompletion.create(
        model = 'gpt-3.5-turbo',
        messages = [{'role':'user', 'content': prompt}]
    )
    content = response.choices[0]['message']['content']
    
    try:
        data = json.loads(content)
        return pd.DataFrame(data.items(), columns=['Measure','Value'])
    
    except (json.JSONDecodeError, IndexError):
        pass


    return pd.DataFrame({
        "Measure": ['Company Name', 'Revenue', 'Net Income'],
        'Value': ['', '', '']
    })
    
    
def get_prompt_text():
    return ''' 
    retrieve company name, revenue, net income from this article and return response in json format
    '''
    
    


if __name__ == '__main__':
    text = '''
    Although Apple’s revenue in the latest quarter deceased 1% from last year to $89.5 billion, its profit rose 11% to $22.96 billion, or $1.46 per share. Both figures eclipsed analysts’ projections, according to FactSet Research.

“We continue to face an uncertain macroeconomic environment,” Apple CEO Tim Cook said during a conference call with analyst.

Apple’s stock price fell 3% in extended trading after the results came out. The shares have fallen by nearly 10% from their all-time highs reached in July, but are still up by more than 30% so far this year. The erosion during the past few months have been largely driven by worries about the sales slowdown and that China may prohibit purchases of iPhones by government workers amid rising tensions with the U.S., at the same time China’s Huawei rolls out new smartphones that pose tougher competition.

The Cupertino, California, company didn’t fare as well in China as analysts had hoped in the most recent quarter, with revenue in that region declining 2% from the same time last year.
'''

    df = extract_financial_data(text)
    print(df.to_string())