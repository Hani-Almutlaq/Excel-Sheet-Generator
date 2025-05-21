import io
import re
import pandas as pd
import openai
from django.http import HttpResponse

openai.api_key = ""

def generate(prompt, num_rows):
    estimated_tokens = min(1000, num_rows * 15)

    try:
        response = openai.ChatCompletion.create(
            model = "gpt-3.5-turbo",
            messages = [{"role": "user", "content": f"Generate random {num_rows} {prompt}, one per line, no problem with duplicate values"}],
            max_tokens = estimated_tokens,
            temperature = 0.7
        )
        items = response.choices[0].message.content.strip().split("\n")
        items = [re.sub(r"^\d+[\.\)-]\s*", "", item).strip() for item in items]

        if len(items) < num_rows:
            items.extend([f"MAX-TOKENS {i + 1}" for i in range(len(items), num_rows)])
        return items[:num_rows]

    except Exception as e:
        print(f"Error generating data: {e}")
        return ["Error"] * num_rows

def generate_columns(column_definitions, num_rows, file_name, file_type):
    data = {}
    for column in column_definitions:
        column_name = column[0]
        column_prompt = column[1]
        data[column_name] = generate(column_prompt, num_rows)

    df = pd.DataFrame(data)
    buffer = io.BytesIO()

    if file_type == "xlsx":
        df.to_excel(buffer, index=False)
        mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    elif file_type == "csv":
        csv_string = df.to_csv(index=False)
        buffer.write(csv_string.encode('utf-8'))
        mime_type = "text/csv"

    buffer.seek(0)

    sheet = HttpResponse(buffer.getvalue(), content_type=mime_type)
    sheet['Content-Disposition'] = f'attachment; filename="{file_name}.{file_type}"'

    return sheet
