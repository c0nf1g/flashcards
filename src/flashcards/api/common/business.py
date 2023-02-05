from flask import url_for


def add_nav_links(pagination, api_path):
    nav_links = {}
    per_page = pagination.per_page
    this_page = pagination.page
    last_page = pagination.pages
    nav_links["self"] = url_for(api_path, page=this_page, per_page=per_page)
    nav_links["first"] = url_for(api_path, page=1, per_page=per_page)
    if pagination.has_prev:
        nav_links["prev"] = url_for(api_path, page=this_page - 1, per_page=per_page)
    if pagination.has_next:
        nav_links["next"] = url_for(api_path, page=this_page + 1, per_page=per_page)
    nav_links["last"] = url_for(api_path, page=last_page, per_page=per_page)
    return nav_links
