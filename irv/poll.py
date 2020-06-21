import irv.db as db

class Poll:
    """
    Represents a poll.
    """

    def __init__(self):
        self._name = ""
        self._desc = ""
        self._opts = []
        self._open = True

    def get_name(self):
        return self._name

    def name(self, name: str):
        # TODO: Raise an error if a poll with that name already exists
        self._name = name
        return self

    def description(self, desc: str):
        self._desc = desc
        return self

    def option(self, option: str):
        self._opts.append(option)
        return self

    def create(self):
        db.register(self)
        return self

    def finalize(self):
        self._open = False

    def __repr__(self):
        return (
            f"Poll {{\n"
            f"\tname: {self._name}\n"
            f"\tdescription: {self._desc}\n"
            f"\toptions: {self._opts}\n"
            f"}}"
        )