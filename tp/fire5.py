import fire

class BuildAppFeatures:
    @staticmethod
    def run():
        print("Building APP features")
        
class BuildUsersFeatures:
    @staticmethod
    def run():
        print("Building Users features")
        
class Pipeline:
    def __init__(self):
        self.app = BuildAppFeatures()
        self.users = BuildUsersFeatures()
    def run(self):
        self.app.run()
        self.users.run()
        print("Pipeline complete")
        
if __name__ == '__main__':
    fire.Fire(Pipeline)
    