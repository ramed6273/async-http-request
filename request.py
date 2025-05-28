import httpx
import asyncio
import time

urls = "./urls"

async def check_url(client, url):
    try:
        full_url = f'https://{url}'
        r = await client.get(full_url)
        return url, r.status_code
    except httpx.RequestError as e:
        return url, f"Error: {e}"
    except Exception as e:
        return url, f"Unexpected Error: {e}"

async def main():
    start_time = time.time()
    results = []

    try:
        with open(urls, "r") as file:
            urls_to_check = [line.strip() for line in file if line.strip()]

        async with httpx.AsyncClient(timeout=5, verify=False) as client:
            tasks = []
            for url in urls_to_check:
                tasks.append(check_url(client, url))
            results = await asyncio.gather(*tasks)

            print("\n--- All Results ---")
        for url, status in results:
            print(f"URL: {url}, Result: {status}")
        print(f"-------------------")
        print(f"Total time taken: {time.time() - start_time:.2f} seconds for {len(urls_to_check)} URLs")

    except FileNotFoundError:
        print(f"Error: The file '{urls}' was not found.")
    except Exception as e:
        print(f"An error occurred while opening or reading the file: {e}")

if __name__ == "__main__":
    asyncio.run(main())

