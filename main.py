import re
from prettytable import PrettyTable

import connect
from models import Authors, Quotes
from decors import time_of, handle_empty_result, cache_decorator

table = PrettyTable()


# def case_insensitive_regex(value):
#     return re.compile(value, re.IGNORECASE)


@time_of
@cache_decorator
@handle_empty_result
def find_by_name(name: str):
    author = Authors.objects(full_name=name.strip()).first()
    if author:
        quotes = Quotes.objects(author=author)
        return quotes


@time_of
@cache_decorator
@handle_empty_result
def find_by_tag(tag: str):
    quote = Quotes.objects(tags__in=[tag.strip()]).all()
    if quote:
        return quote


@time_of
@cache_decorator
@handle_empty_result
def find_by_tags(tags: str):
    tag_list = tags.strip().split(',')
    quotes = Quotes.objects(tags__in=tag_list)
    if quotes:
        return quotes


@time_of
@cache_decorator
@handle_empty_result
def find_by_quote(part_of_quote: str):
    quotes = Quotes.objects(quote__contains=part_of_quote)
    if quotes:
        return quotes


@time_of
@cache_decorator
@handle_empty_result
def find_by_place(place: str):
    authors = Authors.objects(born_loc__contains=place)
    if authors:
        quotes = Quotes.objects(author__in=authors)
        return quotes


COMMANDS = {
    'name': find_by_name,
    'tag': find_by_tag,
    'tags': find_by_tags,
    'quote': find_by_quote,
    'born': find_by_place
}


def print_quotes(quotes):
    table.clear_rows()
    table.field_names = ['Author', 'Quote', 'Tags']
    for quote in quotes:
        table.add_row([quote.author.full_name, quote.quote, ', '.join(quote.tags)])
    table.align = "c"
    table.valign = "m"
    table.max_width['Quote'] = 50
    table.max_width['Tags'] = 30
    print(table)


def main():
    while True:
        user_input = input("Provide the command:\n>>> ")
        parts = user_input.split(":")
        if len(parts) != 2:
            print("Wrong search format. Example: <name:Steve Martin>")
            continue
        command, value = parts
        if command in COMMANDS.keys():
            quotes = COMMANDS[command](value)
            print_quotes(quotes)
        elif command == 'exit':
            print("Exiting the script...")
            break
        else:
            print("Unknown command.")


if __name__ == "__main__":
    main()
