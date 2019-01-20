import webhoseio
import logging
import config

logger = logging.getLogger("uniLogger")

webhoseio.config(token=config.WEB_HOSE_TOKEN)
query_params = {
    "q": "title:\"big data\" -text:\"big data\" language:english",
    "sort": "crawled"
}
output = webhoseio.query("filterWebContent", query_params)
print(output['posts'][0]['text'])  # Print the text of the first post
# Print the text of the first post publication date
print(output['posts'][0]['published'])


# Get the next batch of posts

output = webhoseio.get_next()
if len(output['posts']) == 0:
    exit(0)

# Print the site of the first post
print(output['posts'][0]['thread']['site'])

# doesn't really get the kinds of articles I'm looking for.
def scrape_japanese_cuisine():
    query_params = {
        "q": "site_category:japanese_cuisine language:english site_type:blogs",
        "sort": "crawled"
    }


if __name__ == "__main__":
    scrape_japanese_cuisine()