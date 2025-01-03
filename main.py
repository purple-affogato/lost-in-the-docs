import inquirer,re

import inquirer.errors
import wc2024.spiders.pandas_spider as pds

def main():
    questions = [inquirer.List(
        name='docs',message='What docs do you want to crawl?',
        choices=['pandas', 'python']
    ),
    inquirer.Text(
        name='keywords',message='Enter keywords separated by commas',
        validate=validate_keywords
        )]
    answers = inquirer.prompt(questions)
    keywords = answers['keywords'].casefold().strip().split(",")
    match answers['docs']:
        case 'pandas':
            crawl_pandas(keywords)
        case 'python':
            print("yet to be implemented")
        case _:
            print("oops")
    
def validate_keywords(answers:dict, current:str) -> bool:
    if len(current.strip().split(",")) > 5:
        raise inquirer.errors.ValidationError('', reason="Too many keywords.")
    return True


def crawl_pandas(keywords:list):
    pds.keywords = keywords.copy()
    pds.crawl_process()
    

main()
    

