class App:
    def run(self):
        """
        run the app
        """
        raise NotImplementedError

    def get_preview(self):
        """
        get a preview of the app to show in the selector
        """
        raise NotImplementedError

    def get_description(self) -> str:
        """
        get a description of the app to show in the selector
        """
        raise NotImplementedError
