import argparse


def main():
    parser = argparse.ArgumentParser(description="CLI program for CRUD operations with database")

    parser.add_argument("--action", "-a", choices=["create", "list", "update", "remove"], help="Action to perform", required=True)
    parser.add_argument("--model", "-m", choices=["Teacher", "Student", "Group", "Subject", "Rating"], help="Model to operate on", required=True)
    parser.add_argument("--id", type=int, help="ID of the record to operate on")
    parser.add_argument("--name", help="Name of the record to create or update")

    args = parser.parse_args()


# Когда нибудь я  это доделаю но не сегодня.