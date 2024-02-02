import aiohttp
import json
import asyncio

async def server_get_answer(query):
    connection = "http://127.0.0.1:8080"
    data = {
        "inputs": query[:9000],
        "parameters": {"max_new_tokens": 128,
                       "temperature": 0.2}
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(f"{connection}/generate", json=data) as response:
            response_text = await response.text()
            text = json.loads(response_text)["generated_text"]
            print("got query length", len(query))
            print(data["inputs"])
            return text
        

# result = asyncio.run(server_get_answer("Wer ist Gallwitz?"))
# print(result)

