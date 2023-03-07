class BreadCrumb:
    def __init__(self, title, link, active=False):
        self.title = title
        self.link = link
        self.active = active

    def __str__(self):
        return self.title
