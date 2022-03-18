from status_code import StatusCode


def add_new_theme(theme_name):  # TODO
    print(theme_name)
    return StatusCode.OK, None
    # data = AllThemes.select().where(AllThemes.theme_name == theme_name).get()
    # breakpoint()
    # return StatusCode.OK
