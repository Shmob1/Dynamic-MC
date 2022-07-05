import os
import boto3
from botocore.vendored import requests

DEFAULT_REGION = "us-west-2"
DEFAULT_CLUSTER = "minecraft"
DEFAULT_SERVICE = "minecraft-server"

REGION = os.environ.get("REGION", DEFAULT_REGION)
CLUSTER = os.environ.get("CLUSTER", DEFAULT_CLUSTER)
SERVICE = os.environ.get("SERVICE", DEFAULT_SERVICE)
DISCORD_WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL", None)

if REGION is None or CLUSTER is None or SERVICE is None or DISCORD_WEBHOOK_URL is None:
    raise ValueError("Missing environment variables")


def lambda_handler(event, context):
    """Updates the desired count for a service."""

    ecs = boto3.client("ecs", region_name=REGION)
    response = ecs.describe_services(
        cluster=CLUSTER,
        services=[SERVICE],
    )

    desired = response["services"][0]["desiredCount"]

    if desired == 0:
        ecs.update_service(
            cluster=CLUSTER,
            service=SERVICE,
            desiredCount=1,
        )
        print("Updated desiredCount to 1")
    else:
        print("desiredCount already at 1")

    # Notify Discord
    response = requests.post(
        DISCORD_WEBHOOK_URL,
        json={"content": "Server has been requested"},
        headers={"Content-Type": "application/json"},
    )
    print(f"Discord response: {response.status_code}")
    if response.status_code != 200:
        print(f"Discord error response: {response.text}")
