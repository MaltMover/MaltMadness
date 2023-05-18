import requests
from bs4 import BeautifulSoup


def get_github_issues() -> list[str]:
    url = "https://github.com/MaltMover/MaltMadness/issues"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    issues = soup.find_all("a", {"class": "Link--primary v-align-middle no-underline h4 js-navigation-open markdown-title"})
    return [issue.text.strip() for issue in issues]


if __name__ == '__main__':
    print(get_github_issues())
