from assetManager import create_app
app = create_app()

if __name__ == "__main__":
    import logging
    app.logger.setLevel(logging.INFO)
    app.run()