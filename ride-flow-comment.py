import os

current_directory = os.getcwd()



file_path = current_directory + '/nix/run-mobility-stack.nix'


lines_to_comment = [
    "allocation-service-exe.command = getExe \"allocation-service-exe\";",
    "driver-tracking-healthcheck-exe.command = getExe \"driver-tracking-healthcheck-exe\";",
    "image-api-helper-exe.command = getExe \"image-api-helper-exe\";",
    "mock-fcm-exe.command = getExe \"mock-fcm-exe\";",
    "mock-google-exe.command = getExe \"mock-google-exe\";",
    "mock-idfy-exe.command = getExe \"mock-idfy-exe\";",
    "mock-sms-exe.command = getExe \"mock-sms-exe\";",
    "provider-dashboard-exe.command = getExe \"provider-dashboard-exe\";",
    "public-transport-rider-platform-exe.command = getExe \"public-transport-rider-platform-exe\";",
    "public-transport-search-consumer-exe.command = getExe \"public-transport-search-consumer-exe\";",
    "rider-dashboard-exe.command = getExe \"rider-dashboard-exe\";",
    "scheduler-example-app-exe.command = getExe \"scheduler-example-app-exe\";",
    "scheduler-example-scheduler-exe.command = getExe \"scheduler-example-scheduler-exe\";",
    "search-result-aggregator-exe.command = getExe \"search-result-aggregator-exe\";",
    "static-offer-driver-app-exe.command = getExe \"static-offer-driver-app-exe\";",
    "transporter-scheduler-exe.command = getExe \"transporter-scheduler-exe\";",
    "special-zone-exe.command = self'.apps.special-zone-exe.program;",
    "mock-fcm-exe = { };",
    "mock-google-exe = { };",
    "mock-idfy-exe = { };",
    "mock-sms-exe = { };",
    "provider-dashboard-exe = { };",
    "public-transport-rider-platform-exe = { };",
    "public-transport-search-consumer-exe = { };",
    "driver-tracking-healthcheck-exe = { };",
    "image-api-helper-exe = { };",
    "rider-dashboard-exe = { };",
    "scheduler-example-app-exe = { };",
    "scheduler-example-scheduler-exe = { };",
    "search-result-aggregator-exe = { };",
    "special-zone-exe = { };"
]

commented_lines = []
previous_line = ""
with open(file_path, "r") as file:
    lines = file.readlines()
    for line in lines:
        if line.strip() in lines_to_comment:
            commented_lines.append("# " + line)
        else:
            commented_lines.append(line)
        previous_line = line.strip()

with open(file_path, "w") as file:
    file.writelines(commented_lines)

