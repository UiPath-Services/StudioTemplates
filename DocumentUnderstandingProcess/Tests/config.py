class Config:
    def __init__(self, tdata):

        self.test_data = {
            'nuspec': '..TestDataGeneration/PythonTests/Nuspec_test_data.yaml',
            'user_guide': '..TestDataGeneration/PythonTests/UserGuide_test_data.yaml'
        }[tdata]
