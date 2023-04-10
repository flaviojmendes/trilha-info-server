from linkedin import linkedin

# API Key and Secret Key
api_key = "78sfodl6e3qzio"
secret_key = "8kdR14HI0HHllMNp"

# Create a LinkedIn application object
linkedinclient = linkedin.LinkedInApplication(api_key, secret_key)

# Authorize the application
linkedin.authorization_code = linkedinclient.authenticate_application()

# LinkedIn profile ID of the user
profile_id = "flaviojmendes"

# Get the verified assessments of the user
assessments = linkedin.get_member_network_updates(profile_id=profile_id, update_type=["APPS_YOU_MAY_LIKE"])

# Iterate through the assessments
for assessment in assessments:
    # Extract the relevant information from the assessment
    print(assessment.get("updateContent").get("companyStatusUpdate").get("share").get("comment"))