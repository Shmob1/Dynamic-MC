import os
import json
from urllib.request import Request, urlopen
import boto3

DEFAULT_REGION = "us-west-2"
DEFAULT_CLUSTER = "minecraft"
DEFAULT_SERVICE = "minecraft-server"

REGION = os.environ.get("REGION", DEFAULT_REGION)
CLUSTER = os.environ.get("CLUSTER", DEFAULT_CLUSTER)
SERVICE = os.environ.get("SERVICE", DEFAULT_SERVICE)
DISCORD_WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL", None)

if REGION is None or CLUSTER is None or SERVICE is None:
    raise ValueError("Missing environment variables")

# Notify Discord
def discord_post():
    if DISCORD_WEBHOOK_URL is None:
        raise ValueError("Missing DISCORD_WEBHOOK_URL")
    req = Request(
        DISCORD_WEBHOOK_URL,
        json.dumps({"content": "Server requested"}).encode("utf-8"),
    )
    req.add_header("Content-Type", "application/json")
    req.add_header(
        "User-Agent", "Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11"
    )

    response = urlopen(req)
    print(response.read())


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

    discord_post()
