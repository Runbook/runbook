from pkg_resources import resource_string

class Models:
    @staticmethod
    def model_template():
        return resource_string(__name__, 'templates/model.jinja')

    @staticmethod
    def view_template():
        return resource_string(__name__, 'templates/view.jinja')

    @staticmethod
    def controller_template():
        return resource_string(__name__, 'templates/controller.jinja')

