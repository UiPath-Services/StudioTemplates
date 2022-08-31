class Config:
    def __init__(self, tdata):

        self.test_data = {
            'nuspec': '../PythonTests/Nuspec/test_data.json',
            'user_guide': '../PythonTests/UserGuide/test_data.json'
        }[tdata]
