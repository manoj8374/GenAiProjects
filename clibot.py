import os
from dotenv import load_dotenv
import time
load_dotenv()

from openai import (OpenAI)

providers = [
    {
        "client": OpenAI(api_key=os.environ["OPEN_API_KEY"]),
        "model": "gpt-4",
        "temperature": 2
    },
     {
            "client": OpenAI(api_key=os.environ["OPEN_API_KEY"]),
            "model": "gpt-4",
            "temperature": 0.2
        },
    {
        "client": OpenAI(api_key=os.environ["GOOGLE_API_KEY"], base_url="https://generativelanguage.googleapis.com/v1beta/openai/"),
        "model": "gemini-3.8-flash",
        "temperature": 0.4
    }
]
 

def solve():
    currMessages = [{
         "role": "system",
         "content": "You are a helpful assistant"

    }]


    while True:
         inputVal = input("Please enter your queries!!!  ")
         if inputVal == "Exit":
              return
         
         currMessages.append({"role": "user","content": inputVal})

         flag = False
         
         for i in providers:
            client = i["client"]
            model = i["model"]
            temp = i["temperature"]

            for j in range(0, 3):
                 try:
                    print(f"{model} is giving you the answer!!!!")
                    instance = client.chat.completions.create(
                        model=model,
                        messages=currMessages,
                        temperature=temp
                    )

                    currMess = instance.choices[0].message.content
                    print(currMess)
                    
                    currMessages.append({
                        "role": "assistant",
                        "content": currMess
                    })
                    flag = True
                    break

                 except Exception as error:
                      print(f"Please wait for this duration {pow(2, j + 1)}")
                      time.sleep(pow(2, j + 1))
                      print(error)
 
            if flag:
                 break         

         if flag == False:
            print("All our models did not give your answer... Sorry :(")
            break

solve()