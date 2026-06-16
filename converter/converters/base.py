class BaseConverter:

    source_formats = []
    target_formats = []

    def convert(
        self,
        input_path,
        output_path
    ):
        raise NotImplementedError(
            "Subclasses must implement convert()"
        )