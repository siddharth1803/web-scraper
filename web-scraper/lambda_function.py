import main


def lambda_handler(event, context):
    main.get_website_data()


lambda_handler(1, 1)
