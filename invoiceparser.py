from pydantic import BaseModel, Field, ValidationError
import os
from dotenv import load_dotenv
from openai import OpenAI
from typing import Optional

load_dotenv()

class InvoiceItem(BaseModel):
    product_name: str = Field(description="Name of the product")
    quantity: int = Field(gt=0, default=1, description="Number of items purchased")
    unit_price: float = Field(gt=0, description="Price per individual item")

    @property
    def line_total(self) -> float:
        return self.quantity * self.unit_price

# a = InvoiceItem(product_name="asdfas", quantity=5, unit_price=5.5)

# print(a)
# jsonVal= a.model_dump_json()
# print(jsonVal)

class Invoice(BaseModel):
    name: str = Field(description="Name of the vendor")
    date: str = Field(description="Date when the items are purchased")
    items: list[InvoiceItem] = Field(description="All the items purchased")
    total: float = Field(gt=0, description="The total amount of the invoice")


class InvoiceResult(BaseModel):
    is_invoice: bool = Field(
        description="True only if the text describes a purchase/invoice with a vendor, items and amounts"
    )

    reason: str = Field(
        description="Short explanation. If not an invoice, say why."
    )

    invoice: Optional[Invoice] = Field(
        description="The extracted invoice, or null if is_invoice is false"
    )

     

#Constrained decoding is a technique where you restrict which tokens the model is allowed 
# to generate at each step, so the output is guaranteed to follow a format like a JSON schema 
# or grammar. You convert the schema into a grammar or state machine, and at every decoding step
#  you mask out the tokens that would violate it by setting their logits to negative infinity. 
# The model then samples only from valid tokens. So structure is enforced by the decoder, not by prompting.

def solve(maxTries, systemPrompt):
    inputVal = input("Please share your invoice here!!!   ")
    messages = [
        {
            "role": "system",
            "content": systemPrompt
        },
        {
            "role": "user",
            "content": inputVal
        }
    ]

    client = OpenAI(api_key=os.environ['OPEN_API_KEY'])

    for i in range(maxTries):
        try:
            response = client.chat.completions.parse(
                model="gpt-4.1",
                messages=messages,
                response_format=InvoiceResult
            )
            val = response.choices[0].message.parsed

            if not val.is_invoice or val.invoice is None:
                print("Not an invoice:", val.reason)
            else:
                print(val.invoice.model_dump_json(indent=2))
            return
        except (ValidationError) as e:
            print(f"Attempt failed to parse: {e}")
            messages.append({
                "role": "user",
                "content": f"Your last output could not be parsed: {e}. "
                           "Return a complete, valid result matching the schema.",
            })


system_prompt = (
    "Extract invoice details from the user's text. "
    "If the text is not about an invoice or purchase, set is_invoice to false, "
    "explain why in reason, and set invoice to null. Never invent values."
)

solve(3, system_prompt)