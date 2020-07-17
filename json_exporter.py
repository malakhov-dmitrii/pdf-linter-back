import json
import os
import re

from miner_text_generator import extract_text_by_page


def get_doc_content_correct(page):
    # Проверка наличия страницы содержания
    res = re.match(r'\d{4}-\d{4}-\d{2}-[А-Я]{3}\d.\d.\d.\d-С', page)
    if res:
        return True
    return False


def get_doc_number(page):
    # Проверка наличия страницы содержания
    res = re.match(r'\d{4}-\d{4}-\d{2}-[А-Я]{3}\d.\d.\d.\d', page)
    if res:
        return res.group(0)
    return False


def parse_page(page):
    return page.strip()


def export_as_json(pdf_path):
    filename = os.path.splitext(os.path.basename(pdf_path))[0]
    data = {'filename': filename, 'number': None}
    data['pages'] = []
    doc_content_correct = False
    doc_number = None

    counter = 1
    for page in extract_text_by_page(pdf_path):
        parsed_page = parse_page(page)
        if get_doc_content_correct(parsed_page):
            doc_content_correct = True

        doc_number = get_doc_number(parsed_page)

        content = parsed_page

        if counter > 3:
            content = parsed_page.split('Взам. Инв. № 3434')
            # if content[1]:
            #     content = content[1]

        d = {
            'page': counter,
            'content': content,
        }

        data['pages'].append(d)
        counter += 1

    data['number'] = doc_number

    if doc_content_correct == False:
        # print("ОШИБКА - Нет или неправильная страница 'Содержание'")
        data['errors'] = ["ОШИБКА - Нет или неправильная страница 'Содержание'"]

    # with open(json_path, 'w', encoding="utf-8") as fh:
    #     json.dump(data, fh, ensure_ascii=False)
    return data


# if __name__ == '__main__':
#     pdf_path = 'pdf-to-lint-example.pdf'
#     json_path = 'w9.json'
#     export_as_json(pdf_path, json_path)
