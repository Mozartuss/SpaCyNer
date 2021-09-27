import wikipedia
from tqdm import tqdm

wikipedia.set_lang("de")


class WikipediaType:
    """
    ENUM
    """
    Article = 1
    List = 2


def list_parser(title):
    """
    Filters all links from the Wikipedia article and parse their wikipedia page
    to get the summary there.
    If there is no Wikipedia page for this link
    or if it does not have a summary, only the title will be used.
    :param title: The title of the wikipedia page
    with wikipedia.search you can search for the title and the correct spelling
    :return: List of summaries with a blank line between them
    """
    item_list = []
    all_items = wikipedia.page(title).links
    item_progress = tqdm(all_items)
    for item in item_progress:
        item_progress.set_description(f"Processing {item}")
        try:
            item_list.append(wikipedia.page(item).summary.strip() + "\n")
        except:
            item_list.append(str(item).strip() + "\n")
    return item_list


def article_parser(title):
    """
    Return the complete Article form the given title
    :param title: The title of the wikipedia page
    with wikipedia.search you can search for the title and the correct spelling
    :return: (String) Plain text content of the wikipedia page
    """
    return wikipedia.page(title).content


def save_to_file(data, file_name):
    """
    Save data to file
    list -> line by line
    string -> original formatting
    :param data: list or string
    :param file_name: the file will be stored in the data folder
    with the given file_name and as txt
    :return: boolean if the write process is finished
    """
    with open(f"data/{file_name}.txt", "a", encoding="utf-8") as file:
        if isinstance(data, list):
            file.writelines(data)
        else:
            file.write(data)
    file.close()
    return file.closed


def main_parser(title, wikipedia_type, file_name):
    """
    This method parses Wikipedia articles from the text as plain text into text
    files, whereby a distinction can be made between lists
    and complete articles.
    For lists, the Wikipedia articles for all available links are summarized
    and stored as a list, whereby for complete articles the whole article is
    stored as plain text without images, tables and references.
    :param title: The title of the wikipedia page
    with wikipedia.search you can search for the title and the correct spelling
    :param wikipedia_type: WikipediaType.List or WikipediaType.Article
    :param file_name: The output filename without .txt
    :return:
    """
    if wikipedia_type == WikipediaType.List:
        data = list_parser(title)
    elif wikipedia_type == WikipediaType.Article:
        data = article_parser(title)
    else:
        data = None
    if data is not None:
        if save_to_file(data, file_name):
            print(f"Finish file {file_name}")
        else:
            print(f"Error in file {file_name}")


if __name__ == '__main__':
    list_of_wikipedia_entries = [
        ("Liste von Religionen und Weltanschauungen", WikipediaType.List,
         "Religionen_Liste"),
        # ("Liste von Religionen und Weltanschauungen", WikipediaType.Article,
        # "Religionen"),
        ("Liste von Theologen", WikipediaType.List, "Theologen_Liste"),
        ("Liste von Theologen", WikipediaType.Article, "Theologen"),
        ("Geschichte Deutschlands", WikipediaType.Article, "Geschichte")]
    for i in list_of_wikipedia_entries:
        main_parser(*i)
