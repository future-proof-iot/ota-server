import os
import argparse
import json
import requests


def parse_args():
    parser = argparse.ArgumentParser(description="OTA publisher")
    parser.add_argument('--ota-host', type=str, default="localhost",
                        help="OTA server host.")
    parser.add_argument('--ota-port', type=int, default=8080,
                        help="OTA server port.")
    parser.add_argument('--publish-id', type=str,
                        help="published version identifier, should be unique")
    parser.add_argument('--manifest', type=str, default=None,
                        help="manifest file")
    parser.add_argument('--files', nargs='+', help="list of files to publish")
    parser.add_argument('--notify', nargs='+',
                        help="list of device urls to use to notify an update")
    return parser.parse_args()


def publish_files(args):
    files_dict = dict()
    for file in args.files:
        files_dict[file] = open(file, 'rb').read()
    response = requests.post(
        'http://{}:{}/publish'.format(args.ota_host, args.ota_port),
        files=files_dict, data=dict(publish_id=args.publish_id))
    print('{}: {}'.format(response.status_code, response.reason))


def publish_manifest(args):
    response = requests.post(
        'http://{}:{}/publish'.format(args.ota_host, args.ota_port),
        files=dict(manifest=open(args.manifest, 'rb').read()),
        data=dict(publish_id=args.publish_id))
    print('{}: {}'.format(response.status_code, response.reason))


def notify(args):
    response = requests.post(
        'http://{}:{}/notify'.format(args.ota_host, args.ota_port),
        data=dict(publish_id=args.publish_id,
                  urls=','.join(args.notify)))
    print('{}: {}'.format(response.status_code, response.reason))


def main(args):
    if args.files is not None and len(args.files) > 0:
        publish_files(args)
    if args.manifest is not None and os.path.isfile(args.manifest):
        publish_manifest(args)
    if args.notify is not None and len(args.notify) > 0:
        notify(args)


if __name__ == '__main__':
    try:
        main(parse_args())
    except Exception as exc:
        print("Error: {}".format(exc))