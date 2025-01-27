import requests
from bs4 import BeautifulSoup


class WebScraper:
    def __init__(self):
        self.github_issues = []

    def get_github_issues(self) -> list[str]:
        url = "https://github.com/MaltMover/MaltMadness/issues"
        try:
            response = requests.get(url)
        except requests.exceptions.ConnectionError:
            return self.github_issues
        soup = BeautifulSoup(response.text, "html.parser")
        issues = soup.find_all("h3")
        self.github_issues = [issue.text.strip() for issue in issues][:-1]
        return self.github_issues


if __name__ == '__main__':
    scraper = WebScraper()
    scraper.get_github_issues()
    print(scraper.github_issues)
