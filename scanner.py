#!/usr/bin/python3

from argparse import ArgumentParser
import socket
from time import time
from threading import Thread

open_ports = []


def prepare_args():
    """
    Prepare arguments

    return:
        args(argparse.Namespace): Arguments
    """
    parser = ArgumentParser(description="Port scanner",
                            usage="scanner.py host [options]", epilog="Example - %(prog)s 10.0.0.12 -s 1 -e 4000 -t 500 -V")
    parser.add_argument(metavar="host", help="Host to scan", dest="host")
    parser.add_argument("-p", "--port", help="Port to scan",
                        type=int, default=0, dest="port", metavar='\b')
    parser.add_argument("-t", "--threads", help="Threads to use",
                        type=int, default=500, dest="threads", metavar='\b')
    parser.add_argument("-s", "--start", help="Start port",
                        type=int, default=0, dest="start", metavar='\b')
    parser.add_argument("-e", "--end", help="End port",
                        type=int, default=65535, dest="end", metavar='\b')
    parser.add_argument("-v", "--version", action="version",
                        version="Version : %(prog)s 1.0", help="Show program version")
    parser.add_argument("-V", "--verbose", action="store_true",
                        dest="verbose", help="Verbose mode")

    args = parser.parse_args()

    return args


def prepare_ports(start: int, end: int):
    """Generator Function to prepare ports

        Arguments:
            Start(int): Starting port
            End(int): Ending port
    """
    for port in range(start, end+1):
        yield port


def scan_port():
    """Scan port"""

    while True:
        try:
            s = socket.socket()
            s.settimeout(1)
            port = next(ports)
            try:
                s.connect((arguments.host, port))
                open_ports.append(port)
                if arguments.verbose:
                    print(f"\r{open_ports}", end="")
            except (ConnectionRefusedError, socket.timeout):
                continue
        except StopIteration:
            break
        except OSError as e:
            if e.errno == 49:
                continue
            raise


def prepare_threads(threads: int):
    """Prepare threads

        Arguments:
            threads(int): Number of threads
    """
    thread_list = []
    for _ in range(threads+1):
        thread_list.append(Thread(target=scan_port))

    for thread in thread_list:
        thread.start()

    for thread in thread_list:
        thread.join()


if __name__ == "__main__":
    arguments = prepare_args()
    ports = prepare_ports(arguments.start, arguments.end)
    start_time = time()
    prepare_threads(arguments.threads)
    end_time = time()

    if arguments.verbose:
        print("")

    print(f"\nOpen ports : {open_ports}")
    print(f"Time taken : {round(end_time - start_time, 2)}")
